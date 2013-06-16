#!/usr/bin/env python2
import os
import datetime
import re
from helpers import HISTORY

import pandas

def from_filename(filename):
    'unicode -> (unicode, unicode, datetime.date)'
    s = re.split(r'[- T]', filename.replace('r-log', 'rlog'))
    return filename, s[0], datetime.date(*map(int, s[1:4]))

def features(filename):
    'unicode -> (int)'
    handle = open_history(filename)
    lines = handle.read().split('\n')
    handle.close()

    return pandas.Series({
        'filename': filename,
        'bytes': os.stat(path).st_size,
        'commands': len(lines)/2,
        'first_command_run': fts(lines[0]),
        'last_command_run': fts(lines[-3]) if len(lines) >= 3 else None,
    })

def df():
    'IO () -> DataFrame'
    sessions = [from_filename(filename) for filename in filter(lambda filename: '--' not in filename and '-' in filename, os.listdir(HISTORY))]

    # Extract stuff from the file information
    df = pandas.DataFrame(sessions, columns = ['filename', 'language', 'day'])
    df.index = df['filename']

    # Only shell
    df = df[df['language'] == 'sh']

    # Extract stuff from the file.
    df = df.merge(df['filename'].apply(features))

    return df

