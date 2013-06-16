#!/usr/bin/env python2
import os
import datetime
import re
import warnings

import pandas

from helpers import HISTORY, open_history, fts

def from_filename(filename):
    'unicode -> (unicode, unicode, datetime.date)'
    s = re.split(r'[- T]', filename.replace('r-log', 'rlog'))
    return filename, s[0], datetime.date(*map(int, s[1:4]))

def features(filename):
    'unicode -> (int)'
    handle = open_history(filename)
    lines = handle.read().split('\n')
    handle.close()

    with warnings.catch_warnings():
        first_command_run = fts(lines[0])
        last_command_run = fts(lines[-3]) if len(lines) >= 3 else None

    return pandas.Series({
        'filename': filename,
        'bytes': os.stat(os.path.join(HISTORY, filename)).st_size,
        'commands': len(lines)/2,
        'first_command_run': first_command_run,
        'last_command_run': last_command_run,
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

