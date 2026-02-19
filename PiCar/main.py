import asyncio

from websockets.asyncio.server import ServerConnection, serve
from websockets.exceptions import ConnectionClosedError


async def handler(websocket: ServerConnection):
    host, port = websocket.remote_address[:2]
    print(f"New client connected from {host}:{port}")
    try:
        async for message in websocket:
            await websocket.send(message)
    except ConnectionClosedError:
        pass
    finally:
        await websocket.close()
        print("Client connection closed")


async def main():
    print("Starting server...")
    async with serve(handler, None, 8765) as server:
        host, port = server.sockets[0].getsockname()[:2]
        print(f"Server listening at {host} on port {port}")
        await server.serve_forever()


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\nQuitting...")
