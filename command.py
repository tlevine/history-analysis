from itertools import repeat, imap

import pandas

from helpers import open_history, fts

def features(filename):
    handle = open_history(filename)
    lines = handle.read().split('\n')
    handle.close()

    datetimes = map(fts, lines[0::2][:-1])
    commands = lines[1::2]

    return pandas.DataFrame(
        zip(repeat(filename), datetimes, commands),
        columns = ['filename', 'datetime', 'command']
    )

def df(filenames_series):
    return reduce(lambda a,b: pandas.concat([a,b]), imap(features, (f for f in filenames_series)))
