from starlette.websockets import WebSocket


async def websocket_proxy(websocket: WebSocket, channel: str):
    """WebSocket proxy with channel support."""
    await websocket.accept()

    try:
        pass
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()
