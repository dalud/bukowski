import asyncio
import sys

class DelayedPrint:
    def __init__(self, delay):
        self.delay = delay

    async def delay_print(self, message):
        for c in message:
            sys.stdout.write(c)
            sys.stdout.flush()
            await asyncio.sleep(self.delay)

    def print(self, message):
        asyncio.run(self.delay_print(message))
