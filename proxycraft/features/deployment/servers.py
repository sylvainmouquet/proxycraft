import asyncio
import contextlib
from pathlib import Path

import gunicorn.app.base
from starlette.applications import Starlette

from proxycraft.features.configuration.models import Config
from proxycraft.shared.infrastructure.logging import get_logger
from proxycraft.shared.networking.connection_pooling.connectors.connector_sage_singleton import (
    safe_singleton,
)
from proxycraft.shared.networking.connection_pooling.connectors.event_loop_connector_manager import (
    event_loop_manager,
)
from proxycraft.shared.utilities.utils import check_path

logger = get_logger(__name__)

_PACKAGE_ROOT = Path(__file__).resolve().parents[2]


def run_server(
    app: Starlette,
    config: Config,
    *,
    host: str = "0.0.0.0",
    port: int | None = None,
) -> None:
    @contextlib.asynccontextmanager
    async def lifespan(_app):
        logger.info("Application starting")
        yield
        logger.info("Application shutting down")
        await event_loop_manager.cleanup_all()
        await safe_singleton.cleanup()

    app.router.lifespan_context = lifespan

    default_server = "gunicorn"
    nb_workers = 5

    server = default_server
    ssl = getattr(config, "ssl", False)
    if port is None:
        port = 8443 if ssl else 8080

    if check_path(config, "server.type"):
        server = config.server.type

    if check_path(config, "server.port") and config.server.port:
        port = config.server.port

    logger.debug("Server configuration", host=host, port=port)

    if server == "local":
        return

    if server == "granian":
        logger.info("Starting Granian server", host=host, port=port)

        from granian import Granian
        from granian.constants import Interfaces, Loops

        granian_app = Granian(
            target=app,
            address=host,
            port=port,
            interface=Interfaces.ASGI,
            workers=nb_workers,
            loop=Loops.uvloop,
            **(
                {"ssl_cert": Path("fullchain.pem"), "ssl_key": Path("privkey.pem")}
                if ssl
                else {}
            ),
        )
        granian_app.serve()

    elif server == "robyn":
        logger.info("Starting Robyn server", host=host, port=port)
        from robyn import Robyn

        robyn_app = Robyn(__file__)

        @robyn_app.get("/async/str/const", const=True)
        async def async_str_const_get():
            return "async str const get"

        robyn_app.start(host=host, port=port)

    elif server == "gunicorn":
        if check_path(config, "server.workers"):
            nb_workers = config.server.workers

        class StandaloneApplication(gunicorn.app.base.BaseApplication):
            def __init__(self, application, options=None):
                self.options = options or {}
                self.application = application
                super().__init__()

            def load_config(self):
                for key, value in self.options.items():
                    self.cfg.set(key.lower(), value)

            def load(self):
                return self.application

        options = {
            "bind": f"{host}:{port}",
            "workers": nb_workers,
            "worker_class": "uvicorn_worker.UvicornWorker",
            **(
                {
                    "keyfile": (_PACKAGE_ROOT / "privkey.pem").as_posix(),
                    "certfile": (_PACKAGE_ROOT / "fullchain.pem").as_posix(),
                    "ssl_version": 3,
                    "ciphers": "TLSv1.2:!aNULL:!eNULL:!EXPORT:!DES:!MD5:!PSK:!SRP:!CAMELLIA",
                }
                if ssl
                else {}
            ),
        }
        StandaloneApplication(app, options).run()

    elif server == "uvicorn":
        logger.info("Starting uvicorn server", host=host, port=port)

        import uvicorn

        uvicorn.run(
            app,
            host=host,
            port=port,
            **(
                {
                    "ssl_keyfile": (_PACKAGE_ROOT / "privkey.pem").as_posix(),
                    "ssl_certfile": (_PACKAGE_ROOT / "fullchain.pem").as_posix(),
                    "ssl_version": 3,
                    "ssl_ciphers": "TLSv1.2:!aNULL:!eNULL:!EXPORT:!DES:!MD5:!PSK:!SRP:!CAMELLIA",
                }
                if ssl
                else {}
            ),
        )
    else:
        logger.info("Starting hypercorn server", host=host, port=port)
        from hypercorn.asyncio import serve
        from hypercorn.config import Config as HypercornConfig

        hypercorn_config = HypercornConfig()
        hypercorn_config.bind = [f"{host}:{port}"]
        if ssl:
            hypercorn_config.certfile = (_PACKAGE_ROOT / "fullchain.pem").as_posix()
            hypercorn_config.keyfile = (_PACKAGE_ROOT / "privkey.pem").as_posix()
        hypercorn_config.alpn_protocols = ["h2", "http/1.1"]
        hypercorn_config.h2_max_concurrent_streams = 100
        hypercorn_config.h2_max_frame_size = 16384

        asyncio.run(serve(app, hypercorn_config))
