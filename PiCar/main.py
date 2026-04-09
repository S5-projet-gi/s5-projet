from __future__ import annotations

import asyncio
import json
import os
import sys

from websockets.asyncio.server import ServerConnection, serve

from logic import Logic


async def main():
    if "pi" in sys.argv or os.getlogin() == "pi":
        # PiCar
        from control.picar import PiCarControl

        print("Starting PiCar control...")
        control = PiCarControl()
        logic = Logic(control)
        await asyncio.sleep(2)
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
        send_task = asyncio.create_task(self._send_commands(client, control))

        try:
            async for message in client:
                message = json.loads(message)
                if message["type"] == "sensor":
                    control.sensors = message["data"]
                    print(
                        f"[Server] Received sensor data: line_follower={message['data'].get('line_follower')}, distance={message['data'].get('distance')}"
                    )
        finally:
            logic_task.cancel()
            send_task.cancel()
            await client.close()
            print("Client connection closed")

    async def _send_commands(self, client: ServerConnection, control) -> None:
        """Send movement commands to GoDot every 50ms"""
        try:
            while True:
                await asyncio.sleep(0.05)
                command_data = json.dumps(
                    {
                        "type": "control",
                        "speed": control.last_speed,
                        "steer_dir": control.last_steer_dir,
                    }
                )
                await client.send(command_data)
                print(
                    f"[Server] Sent: speed={control.last_speed:.3f}, steer_dir={control.last_steer_dir:.3f}"
                )
        except asyncio.CancelledError:
            pass


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\nQuitting...")
