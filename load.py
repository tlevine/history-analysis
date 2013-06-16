#!/usr/bin/env python2
import os
import datetime
import re

import pandas

HISTORY = os.path.join(os.environ['HOME'], '.history')

def filename_to_session(filename):
    'unicode -> (unicode, unicode, datetime.date)'
    s = re.split(r'[- T]', filename.replace('r-log', 'rlog'))
    return filename, s[0], datetime.date(*map(int, s[1:4]))

def sessions_by_day():
    'IO () -> [session]'
    return [filename_to_session(filename) for filename in filter(lambda filename: '--' not in filename and '-' in filename, os.listdir(HISTORY))]

def fileinfo(filename):
    'unicode -> (int)'
    path = os.path.join(HISTORY, filename)

    handle = open(path)
    lines = handle.read().split('\n')
    handle.close()

    fts = datetime.datetime.fromtimestamp
    return pandas.Series({
        'filename': filename,
        'bytes': os.stat(path).st_size,
        'commands': len(lines)/2,
        'first_command_run': fts(float(lines[0][1:])),
        'last_command_run': fts(float(lines[-3][1:])) if len(lines) > 3 else None,
    })

# Extract stuff from the file information
df = pandas.DataFrame(sessions_by_day(), columns = ['filename', 'language', 'day'])
df.index = df['filename']

# Only shell
df = df[df['language'] == 'sh']

# Extract stuff from the file.
df = df.head(10)
df = df.merge(df['filename'].apply(fileinfo))
