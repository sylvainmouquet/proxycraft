import asyncio
from http import HTTPStatus

import httpx
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response

from proxycraft import __version__
from proxycraft.features.configuration.models import Config, Endpoint
from proxycraft.features.routing.routing_selector import RoutingSelector
from proxycraft.features.upstream_backends.factory import ProxyHandlerFactory
from proxycraft.shared.infrastructure.logging import get_logger

logger = get_logger(__name__)


async def _resolve_virtual_upstream(
    *,
    config: Config,
    app: Starlette,
    endpoint: Endpoint,
    request: Request,
    method: str,
) -> Response | None:
    upstream = endpoint.upstream
    if not (
        hasattr(upstream, "virtual")
        and upstream.virtual is not None
        and upstream.virtual.enabled is True
    ):
        return None

    sources = upstream.virtual.sources
    if upstream.virtual.strategy != "first-match":
        return None

    endpoints_by_identifier = {ep.identifier: ep for ep in config.endpoints}
    transport = httpx.ASGITransport(app=app)

    for source in sources:
        source_endpoint = endpoints_by_identifier[source]
        async with httpx.AsyncClient(
            transport=transport, base_url="http://testserver"
        ) as client:
            resource_path = request.url.path.removeprefix(endpoint.prefix)
            path = source_endpoint.prefix + resource_path

            if request.url.query:
                path = f"{request.url.path}?{request.url.query}"

            r = await client.request(url=path, method=method)
            if r.status_code != HTTPStatus.OK:
                continue
            return Response(
                status_code=r.status_code,
                media_type=r.headers["content-type"]
                if "content-type" in r.headers
                else "application/text",
                content=r.text,
            )
    return Response(
        status_code=HTTPStatus.NOT_FOUND,
        media_type="text/plain",
        content="Not Found",
    )


async def handle_request(
    routing_selector: RoutingSelector,
    config: Config,
    app: Starlette,
    request: Request,
    connection_pooling,
):
    method = request.method
    headers = dict(request.headers)
    headers.pop("host", None)
    headers.pop("content-length", None)
    headers.pop("accept-encoding", None)
    headers.pop("user-agent", None)

    headers["user-agent"] = f"python-proxycraft/{__version__}"

    try:
        endpoint: Endpoint = routing_selector.find_endpoint(
            request_url_path=request.url.path
        )

        upstream = endpoint.upstream

        if (
            hasattr(upstream, "proxy")
            and upstream.proxy is not None
            and upstream.proxy.enabled is True
        ):
            backend = (
                endpoint.backends[0]
                if isinstance(endpoint.backends, list)
                else endpoint.backends
            )
            logger.debug(f"{upstream=} - {backend=}")

            return await ProxyHandlerFactory.create_and_handle(
                backend, endpoint, request, headers, connection_pooling
            )

        virtual_response = await _resolve_virtual_upstream(
            config=config,
            app=app,
            endpoint=endpoint,
            request=request,
            method=method,
        )
        if virtual_response is not None:
            return virtual_response

        return Response(
            status_code=HTTPStatus.NOT_FOUND,
            media_type="text/plain",
            content="Not Found",
        )

    except Exception as e:
        logger.error(f"Error: {e}")
        logger.exception(e)
        if isinstance(e, asyncio.TimeoutError):
            return Response(
                content="Request timed out",
                status_code=HTTPStatus.REQUEST_TIMEOUT,
                headers={"Content-Type": "application/json"},
            )
        return Response(
            content=str(e),
            status_code=500,
            headers={"Content-Type": "application/json"},
        )
