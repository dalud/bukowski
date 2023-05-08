import asyncio
import sys
from delayedPrint_IF import DelayedPrint

async def delay_print(s):
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        await asyncio.sleep(0.25)

#TODO: test async / threading with timed Arduino function
#asyncio.run(delay_print("hello world"))

printer = DelayedPrint(.25)
printer.print("Haista sinäkin kakka, senkin...")
