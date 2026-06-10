from starlette.applications import Starlette

from proxycraft.features.configuration.models import Config
from proxycraft.features.performance.caching.in_file import InFileCacheMiddleware
from proxycraft.features.performance.caching.in_memory import InMemoryCacheMiddleware
from proxycraft.features.performance.compression import CompressionMiddleware
from proxycraft.features.performance.content_length import ContentLengthMiddleware
from proxycraft.features.performance.resource_filter import ResourceFilterMiddleware
from proxycraft.features.routing.routing_selector import RoutingSelector
from proxycraft.features.security_filtering.bot_filter import BotFilterMiddleware
from proxycraft.features.security_filtering.ip_filter import IpFilterMiddleware
from proxycraft.features.transformation.response_transform import (
    ResponseTransformerMiddleware,
)
from proxycraft.shared.utilities.utils import check_path


def configure_middlewares(
    app: Starlette,
    config: Config,
    routing_selector: RoutingSelector,
) -> None:
    app.add_middleware(ContentLengthMiddleware)  # type: ignore

    if (
        check_path(config, "middlewares.performance.cache.memory.enabled")
        and config.middlewares.performance.cache.memory.enabled is True
    ):
        app.add_middleware(InMemoryCacheMiddleware, config=config)  # type: ignore

    if (
        check_path(config, "middlewares.performance.cache.file.enabled")
        and config.middlewares.performance.cache.file.enabled is True
    ):
        app.add_middleware(InFileCacheMiddleware, config=config)  # type: ignore

    if (
        check_path(config, "middlewares.security.bot_filter.enabled")
        and config.middlewares.security.bot_filter.enabled is True
    ):
        app.add_middleware(BotFilterMiddleware, config=config)  # type: ignore

    if (
        check_path(config, "middlewares.security.ip_filter.enabled")
        and config.middlewares.security.ip_filter.enabled is True
    ):
        app.add_middleware(IpFilterMiddleware, config=config)  # type: ignore

    if (
        check_path(config, "middlewares.performance.resource_filter.enabled")
        and config.middlewares.performance.resource_filter.enabled is True
    ):
        app.add_middleware(ResourceFilterMiddleware, config=config)  # type: ignore

    app.add_middleware(
        CompressionMiddleware,
        config=config,  # type: ignore
        routing_selector=routing_selector,
    )  # type: ignore

    app.add_middleware(ResponseTransformerMiddleware, routing_selector=routing_selector)  # type: ignore

    app.user_middleware.reverse()
