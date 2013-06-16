import datetime
import os
import warnings

HISTORY = os.path.join(os.environ['HOME'], '.history')

def open_history(filename):
    path = os.path.join(HISTORY, filename)
    return open(path, 'r')

def fts(commented_timestamp):
    try:
        timestamp = float(commented_timestamp[1:])
    except ValueError:
        # Like ~/.history/'sh-2013-02-26 20:16:04.229569561-05:00-3740cba5-bd2c-4465-9ad5-1cdc5c59f5b2'
        warnings.warn('''I could not decode the timestamp "%s"; it's probably part of a command with multiple lines.''' % commented_timestamp)
        return None
    else:
        return datetime.datetime.fromtimestamp(timestamp)
