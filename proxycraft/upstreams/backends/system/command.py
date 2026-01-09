import asyncio
import logging
import platform
import pty
import struct
import os
import json
import fcntl
import termios
from http import HTTPStatus

from starlette.requests import Request
from starlette.responses import StreamingResponse, JSONResponse, Response

from proxycraft.config.models import Endpoint, Backends


class Command:
    """Command execution client for running system commands asynchronously."""

    def __init__(self, connection_pooling, endpoint: Endpoint, backend: Backends):
        self.connection_pooling = connection_pooling
        self.endpoint = endpoint
        self.backend = backend
        self.buffer_size = 4096
        self.timeout = 10

    async def handle_request(self, request: Request, headers: dict) -> Response:
        try:
            # -------------------------
            # Resolve command
            # -------------------------
            current_platform = platform.system().lower().replace(" ", "_")

            if hasattr(self.backend.command, current_platform):
                base_cmd = getattr(self.backend.command, current_platform)
            else:
                base_cmd = self.backend.command.default

            if isinstance(base_cmd, str):
                command = [base_cmd]
            else:
                command = list(base_cmd)

            body = (await request.body()).decode()
            if body:
                json_body = json.loads(body)
                if isinstance(json_body, dict) and "args" in json_body:
                    command.extend(map(str, json_body["args"]))

            logging.info("Executing command: %s", " ".join(command))

            env = os.environ.copy()
            env.update(
                {
                    "PYTHONUNBUFFERED": "1",
                    "TERM": "xterm-256color",
                }
            )

            # -------------------------
            # Streaming generator
            # -------------------------
            async def stream_output():
                master, slave = pty.openpty()

                # Terminal size
                term_size = struct.pack("HHHH", 24, 80, 0, 0)
                fcntl.ioctl(slave, termios.TIOCSWINSZ, term_size)

                process = await asyncio.create_subprocess_exec(
                    *command,
                    stdin=asyncio.subprocess.PIPE,
                    stdout=slave,
                    stderr=slave,
                    env=env,
                )

                os.close(slave)

                # Non-blocking master
                flags = fcntl.fcntl(master, fcntl.F_GETFL)
                fcntl.fcntl(master, fcntl.F_SETFL, flags | os.O_NONBLOCK)

                try:
                    while True:
                        try:
                            data = os.read(master, self.buffer_size)
                            if data:
                                yield data
                                continue
                        except BlockingIOError:
                            pass
                        except OSError:
                            break

                        if process.returncode is not None:
                            break

                        await asyncio.sleep(0.05)

                    # Drain remaining output
                    while True:
                        try:
                            data = os.read(master, self.buffer_size)
                            if not data:
                                break
                            yield data
                        except OSError:
                            break

                finally:
                    try:
                        os.close(master)
                    except OSError:
                        pass

                rc = await process.wait()
                yield f"\n[exit {rc}]\n".encode()

            return StreamingResponse(
                stream_output(),
                media_type="application/octet-stream",
            )

        except asyncio.TimeoutError:
            logging.error("Command execution timed out after %ss", self.timeout)
            return JSONResponse(
                content={"error": f"Command execution timed out after {self.timeout}s"},
                status_code=HTTPStatus.REQUEST_TIMEOUT.value,
            )

        except Exception as e:
            logging.exception("Unexpected error executing command")
            return JSONResponse(
                content={"error": str(e)},
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            )
