import io
from pathlib import Path

from starlette.responses import Response, StreamingResponse

from proxycraft.shared.utilities.path_compat import is_regular_file


async def download_text_file(path: Path):
    if not path.exists() or not is_regular_file(path):
        return Response(status_code=404, media_type="text/plain", content="Not Found")

    def text_file_streamer():
        with io.open(path, "r", encoding="utf-8", buffering=8192) as file:
            while chunk := file.read(8192):
                if chunk:
                    yield chunk.encode("utf-8")

    return StreamingResponse(
        text_file_streamer(),
        media_type="text/plain; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{path.name}"'},
    )
