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
        warnings.warn('Could not decode the timestamp "%s"' % commented_timestamp)
        return None
    else:
        return datetime.datetime.fromtimestamp(timestamp)
