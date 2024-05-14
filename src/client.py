import asyncio
import os
import sys

import websockets

from src import core


async def _main() -> None:
    websocket_url: str | None = sys.argv[1] if len(sys.argv) == 2 else None
    if websocket_url is None:
        websocket_url = input('enter websocket url: ')

    async with websockets.connect(websocket_url) as connection:
        await connection.send('get')

        while True:
            request = await connection.recv()
            if isinstance(request, str):
                core.process_command(request)
            else:
                core.set_ui_info('get unknown type of data (expected string).')
            core.print_ui()


# client commands:
#  - info(msg) -> None;
#
# see other in core.


@core.register_command()
def info(msg: str) -> None:
    core.set_ui_info(msg)


if __name__ == '__main__':
    try:
        asyncio.run(_main())
    except KeyboardInterrupt:
        os.system('clear')
        print('bye')
