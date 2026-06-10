import contextlib
import logging
from proxycraft.shared.utilities.http_compat import HTTPMethod
from pathlib import Path

import aiohttp
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Route, WebSocketRoute

from proxycraft.app.middleware_stack import configure_middlewares
from proxycraft.features.configuration.loader import get_file_config
from proxycraft.features.configuration.models import Config
from proxycraft.features.deployment.servers import run_server
from proxycraft.features.protocols.websocket_proxy import websocket_proxy
from proxycraft.features.routing.routing_selector import RoutingSelector
from proxycraft.features.virtual_upstream.resolver import handle_request
from proxycraft.shared.infrastructure.logging import get_logger, setup_structlog
from proxycraft.shared.networking.connection_pooling.tracing.default_trace_handler import (
    DefaultTraceHandlers,
    TraceHandlers,
)

logger = get_logger(__name__)


class ProxyCraft:
    def make_lifespan(self):
        @contextlib.asynccontextmanager
        async def lifespan(app):
            await self.startup_event()
            yield
            await self.shutdown_event()

        return lifespan

    def __init__(self, config_file: str | None = None, config: Config | None = None):
        async def handle_all_methods(request: Request):
            return await handle_request(
                self.routing_selector,
                self.config,
                self.app,
                request,
                None,
            )

        routes = [
            Route(
                "/{path:path}",
                handle_all_methods,
                methods=[
                    HTTPMethod.GET,
                    HTTPMethod.POST,
                    HTTPMethod.PUT,
                    HTTPMethod.DELETE,
                    HTTPMethod.PATCH,
                ],
            ),
            WebSocketRoute("/ws/{channel}", websocket_proxy),
        ]

        self.config = get_file_config(config_file) if config_file else config
        if not self.config:
            if config_file:
                logger.info(
                    "Configuration file not found, using defaults",
                    config_file=config_file,
                )
            self.config = Config(
                **{
                    "version": "1.0",
                    "name": "Default config",
                    "endpoints": [
                        {
                            "prefix": "/",
                            "match": "**/*",
                            "backends": {
                                "https": {
                                    "url": "https://jsonplaceholder.typicode.com/posts"
                                }
                            },
                            "upstream": {"proxy": {"enabled": True}},
                        }
                    ],
                }
            )
        self.routing_selector = RoutingSelector(self.config)

        self.app = Starlette(debug=True, routes=routes, lifespan=self.make_lifespan())
        configure_middlewares(self.app, self.config, self.routing_selector)

        self.proxy_baseurl = "http://127.0.0.1:8091"

    async def startup_event(self):
        connector = aiohttp.TCPConnector(
            limit=100, force_close=False, enable_cleanup_closed=False
        )

        trace_handlers = TraceHandlers(
            enable_logging=True, log_level=logging.INFO, logger_name="proxycraft"
        )

        handlers = DefaultTraceHandlers(trace_handlers)

        trace_config = aiohttp.TraceConfig()
        trace_config.on_request_start.append(handlers.on_request_start)
        trace_config.on_request_end.append(handlers.on_request_end)
        trace_config.on_request_exception.append(handlers.on_request_exception)
        trace_config.on_connection_create_start.append(
            handlers.on_connection_create_start
        )
        trace_config.on_connection_create_end.append(handlers.on_connection_create_end)
        trace_config.on_connection_reuseconn.append(handlers.on_connection_reuseconn)
        trace_config.on_dns_resolvehost_start.append(handlers.on_dns_resolvehost_start)
        trace_config.on_dns_resolvehost_end.append(handlers.on_dns_resolvehost_end)

        connector.trace_config = trace_config

        self.app.state.connector = connector
        self.app.state.trace_config = trace_config

    async def shutdown_event(self):
        if hasattr(self.app.state, "connector") and not self.app.state.connector.closed:
            await self.app.state.connector.close()

    def serve(self, host: str = "0.0.0.0", port: int | None = None):
        run_server(self.app, self.config, host=host, port=port)


def main() -> None:
    setup_structlog(json_logs=False)
    source_dir = Path(__file__).resolve().parent.parent
    config_path = source_dir / "features" / "configuration" / "default.json"
    if not config_path.exists():
        config_path = source_dir / "default.json"

    proxy = ProxyCraft(config_file=config_path.as_posix())
    proxy.serve()


if __name__ == "__main__":
    main()
