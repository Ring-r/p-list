import os

from src import core


def _main() -> None:
    while True:
        os.system('clear')
        core.print_ui()
        request: str = input('command: ')
        if request == 'quit':
            return

        try:
            core.process_command(request)
        except Exception as exc:
            core.set_ui_info(str(exc))


# app commands:
#  - help() -> None;
#  - help(msg) -> None;
#  - quit() -> None;
#
# see other in core.


@core.register_command()
def help(command_name: str | None = None) -> None:
    '''
    get help information (common or about command).
    '''
    if command_name is None:
        # TODO: return userfriendly description
        core.set_ui_info(f'available commands are {", ".join(core.commands.keys())}')
        return

    doc: str | None = core.commands[command_name].__doc__
    core.set_ui_info(doc if doc is not None else '')


@core.register_command()
def quit() -> None:
    '''
    quit.
    '''
    exit(0)


if __name__ == '__main__':
    try:
        _main()
    except KeyboardInterrupt:
        os.system('clear')
        print('bye')
