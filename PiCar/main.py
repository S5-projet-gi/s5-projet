import asyncio
import json
import os
import sys

from websockets.asyncio.server import ServerConnection, serve

from logic import Logic


async def main():
    if (len(sys.argv) > 1 and sys.argv[1] == "pi") or os.getlogin() == "pi":
        # PiCar
        from control.picar import PiCarControl

        print("Starting PiCar control...")
        control = PiCarControl()
        logic = Logic(control)
        await logic.run()
        return

    # GoDot
    server = WebsocketServer()
    await server.start()


class WebsocketServer:
    client: ServerConnection | None = None

    async def start(self):
        print("Starting websocket server...")
        async with serve(self.handler, None, 8765) as server:
            host, port = server.sockets[0].getsockname()[:2]
            print(f"Server listening at {host} on port {port}")
            await server.serve_forever()

    async def handler(self, client: ServerConnection):
        if self.client is not None:
            await self.client.close()
        self.client = client

        host, port = client.remote_address[:2]
        print(f"New client connected from {host}:{port}")

        from control.godot import GoDotControl

        print("Starting GoDot control...")
        control = GoDotControl(client)
        logic = Logic(control)
        logic_task = asyncio.create_task(logic.run())

        try:
            async for message in client:
                message = json.loads(message)
                if message["type"] == "sensor":
                    control.sensors = message["data"]
        finally:
            logic_task.cancel()
            await client.close()
            print("Client connection closed")


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\nQuitting...")
