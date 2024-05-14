import os
from operator import attrgetter
from typing import Callable

from src import storage

ui_info: str | None = None


def _get_ui_info() -> str | None:
    return ui_info


def set_ui_info(msg: str | None) -> None:
    global ui_info
    ui_info = msg


def print_ui() -> None:
    os.system('clear')

    items = storage.get_purchases()

    curr_items = [item for item in items if item.is_active]
    print(f'curr: {"-" * 44}',)
    curr_items.sort(key=attrgetter('name'))
    for curr_item in curr_items:
        print(f'{curr_item.name:35} [buy | cancel]')

    prev_items = [item for item in items if not item.is_active]
    print(f'prev: {"-" * 44}')
    prev_items.sort(key=attrgetter('name'))
    prev_items.sort(key=attrgetter('count'), reverse=True)
    for prev_item in prev_items:
        print(f'{prev_item.name:44} [add]')

    print('-' * 50)
    info = _get_ui_info()
    if info is not None:
        print(info)


commands: dict[str, Callable] = {}


def register_command(name: str | None = None):
    def actual_decorator(func: Callable):
        command_name = name if name is not None else func.__name__
        commands[command_name] = func

        def wrapper(*args) -> None:
            func(*args)

        return wrapper
    return actual_decorator


def process_command(request: str) -> None:
    set_ui_info(None)

    request_parts = request.split(maxsplit=1)

    if len(request_parts) == 0:
        set_ui_info('get empty message.')
        return

    request_command_name = request_parts[0]
    request_command_args: list[str] = request_parts[1:]
    set_ui_info(f'get command `{request_command_name}`.')

    command: Callable | None = commands.get(request_command_name)
    if command is None:
        set_ui_info(f'get command `{request_command_name}` which is not processed.')
        return

    command(*request_command_args)


# common (app, client) commands:
#  - set(data) -> None; seet data; set plist;
#
#  - add(id) -> None; add purchase to plist; add if it don't exist;
#  - buy(id) -> None; move purchase from plist to history (change counter)
#  - cancel(id) -> None; move purchase from plist to history (don't change counter)


@register_command()
def set(purchases_json: str) -> None:
    '''
    change all saved data; set list of purchases (include active and history).
    '''
    try:
        storage.set_purchase_json(purchases_json)
    except Exception as exc:
        set_ui_info(f'get data that is decoded with error ({str(exc)})')
        # TODO: disable all data functionality until fix this error


@register_command()
def add(purchase_name: str) -> None:
    '''
    add purchase to purchase list. create if it does not exist.

    params:
        purchase_name
    '''
    storage.add_purchase(purchase_name)


@register_command()
def buy(purchase_name: str) -> None:
    '''
    move purchase from purchase list to history. increment counter of buying.

    params:
        purchase_name
    '''
    storage.buy_purchase(purchase_name)


@register_command()
def cancel(purchase_name: str) -> None:
    '''
    move purchase from purchase list to history. not increment counter of buying.

    params:
        purchase_name
    '''
    storage.cancel_purchase(purchase_name)
