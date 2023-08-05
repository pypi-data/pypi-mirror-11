from difflib import get_close_matches
import os
from pathlib import Path
from thefuck.utils import sudo_support, memoize
from thefuck.shells import thefuck_alias, get_aliases


def _safe(fn, fallback):
    try:
        return fn()
    except OSError:
        return fallback


@memoize
def get_all_callables():
    tf_alias = thefuck_alias()
    return [exe.name
            for path in os.environ.get('PATH', '').split(':')
            for exe in _safe(lambda: list(Path(path).iterdir()), [])
            if not _safe(exe.is_dir, True)] + [
                alias for alias in get_aliases() if alias != tf_alias]


@sudo_support
def match(command, settings):
    return 'not found' in command.stderr and \
           bool(get_close_matches(command.script.split(' ')[0],
                                  get_all_callables()))


@sudo_support
def get_new_command(command, settings):
    old_command = command.script.split(' ')[0]
    new_command = get_close_matches(old_command,
                                    get_all_callables())[0]
    return ' '.join([new_command] + command.script.split(' ')[1:])


priority = 3000
