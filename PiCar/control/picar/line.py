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
            try:
                new_line = self.line_follower.read_analog()
                print(f"[LineSensor] raw={new_line}")

                if (
                    isinstance(new_line, list)
                    and len(new_line) == 5
                    and all(value in (0, 300) for value in new_line)
                ):
                    self.line = [
                        0
                        if x > const.line_follower["black_threshold"]
                        else 1
                        if x > const.line_follower["gray_threshold"]
                        else 2
                        for x in new_line
                    ]
                    print(f"[LineSensor] digital={self.line}")
                else:
                    print(
                        f"[LineSensor] invalid read ignored: {new_line}, keeping last={self.line}"
                    )
            except OSError as e:
                print(
                    f"[LineSensor] I2C read error ignored: {e}, keeping last={self.line}"
                )
            except Exception as e:
                print(
                    f"[LineSensor] unexpected read error ignored: {e}, keeping last={self.line}"
                )
            await asyncio.sleep(0.03)
