import asyncio

from SunFounder.line_follower import Line_Follower


class PiCarLine:
    linefolower: Line_Follower
    line = [0, 0, 0, 0, 0]

    def __init__(self) -> None:
        asyncio.create_task(self.read_line_task())

    async def read_line_task(self):
        await asyncio.sleep(2)

        while True:
            self.distance = self.linefolower.read_analog()
            await asyncio.sleep(0.03)
