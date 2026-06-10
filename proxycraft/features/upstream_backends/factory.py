from proxycraft.features.upstream_backends.file_system.file import File
from proxycraft.features.upstream_backends.http.echo import Echo
from proxycraft.features.upstream_backends.http.https import Https
from proxycraft.features.upstream_backends.http.mock import Mock
from proxycraft.features.upstream_backends.http.redirect import Redirect
from proxycraft.features.upstream_backends.system.command import Command
from proxycraft.features.upstream_backends.system.scheduler import Scheduler


class ProxyHandlerFactory:
    _handlers = {
        "command": Command,
        "echo": Echo,
        "redirect": Redirect,
        "mock": Mock,
        "https": Https,
        "file": File,
        "scheduler": Scheduler,
    }

    @classmethod
    async def create_and_handle(
        cls, backend, endpoint, request, headers, connection_pooling
    ):
        for attr_name, handler_class in cls._handlers.items():
            if hasattr(backend, attr_name) and getattr(backend, attr_name):
                handler = handler_class(
                    connection_pooling=connection_pooling,
                    endpoint=endpoint,
                    backend=backend,
                )
                return await handler.handle_request(request=request, headers=headers)

        raise ValueError("No valid handler found for backend")
