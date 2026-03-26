import asyncio

from SunFounder.line_follower import Line_Follower


class PiCarLine:
    line_follower: Line_Follower
    line = [0, 0, 0, 0, 0]

    def __init__(self) -> None:
        self.line_follower = Line_Follower()
        asyncio.create_task(self.read_line_task())

    async def read_line_task(self):
        await asyncio.sleep(2)

        while True:
            self.distance = self.line_follower.read_analog()
            await asyncio.sleep(0.03)
