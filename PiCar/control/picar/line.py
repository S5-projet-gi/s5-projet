import asyncio

import const
from SunFounder.line_follower import Line_Follower


class PiCarLine:
    line_follower: Line_Follower
    line = [0, 0, 0, 0, 0]

    def __init__(self) -> None:
        self.line_follower = Line_Follower(
            references=[const.line_follower["black_threshold"] for _ in range(5)]
        )
        asyncio.create_task(self.read_line_task())

    async def read_line_task(self):
        await asyncio.sleep(2)

        while True:
            analog = self.line_follower.read_analog()
            digital = self.line_follower.read_digital()

            refs = self.line_follower.references
            self.line = [0 if analog[i] >= refs[i] else 1 for i in range(5)]
            print(f"[LineSensor] analog={analog} digital={digital} line={self.line} refs={refs}")
            await asyncio.sleep(0.03)
