from itertools import repeat, imap
import shlex

import pandas

from helpers import open_history, fts

def extract(filename):
    handle = open_history(filename)
    lines = handle.read().split('\n')
    handle.close()

    if lines == ['']:
        # sh-2013-05-30 07:19:43.899805117-07:00-21233
        return pandas.DataFrame()

    datetimes = map(fts, lines[0::2][:-1])
    commands = lines[1::2]

    return pandas.DataFrame(
        zip(repeat(filename), datetimes, commands),
        columns = ['filename', 'datetime', 'command']
    )

def eextract(filename):
    try:
        return extract(filename)
    except:
        print 'Error at ' + filename
        raise

def df(filenames_series):
    thin_df = reduce(lambda a,b: pandas.concat([a,b]), imap(eextract, (f for f in filenames_series)))
    return thin_df.merge(thin_df['command'].apply(features))

def _is_comment(command):
    stripped_command = command.lstrip()
    return len(stripped_command) > 0 and stripped_command[0] == '#'

def features(command):
    try:
        argv = shlex.split(command)
    except ValueError:
        # Not a full command
        return pandas.Series({
            'command': command,
            'is_comment': None,
            'n_char': len(command),
            'n_args': None,
            'argv0': None,
        })
    else:
        return pandas.Series({
            'command': command,
            'is_comment': _is_comment(command),
            'n_char': len(command),
            'n_args': len(argv),
            'argv0': argv[0] if len(argv) > 0 else None,
        })

