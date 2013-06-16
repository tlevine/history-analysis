#!/usr/bin/env python2
import os
import datetime
import re

import pandas

HISTORY = os.path.join(os.environ['HOME'], '.history')

def fts(commented_timestamp):
    return datetime.datetime.fromtimestamp(float(commented_timestamp[1:]))

def filename_to_session(filename):
    'unicode -> (unicode, unicode, datetime.date)'
    s = re.split(r'[- T]', filename.replace('r-log', 'rlog'))
    return filename, s[0], datetime.date(*map(int, s[1:4]))

def sessions_by_day():
    'IO () -> [session]'
    return [filename_to_session(filename) for filename in filter(lambda filename: '--' not in filename and '-' in filename, os.listdir(HISTORY))]

def open_history(filename):
    path = os.path.join(HISTORY, filename)
    return open(path, 'r')

def file_info(filename):
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

def file_features():
    # Extract stuff from the file information
    df = pandas.DataFrame(sessions_by_day(), columns = ['filename', 'language', 'day'])
    df.index = df['filename']

    # Only shell
    df = df[df['language'] == 'sh']

    # Extract stuff from the file.
    # df = df.head(10)
    # df = df.merge(df['filename'].apply(file_info))

    return df

def command_info(filename):
    handle = open_history(filename)
    lines = handle.read().split('\n')
    handle.close()

    timestamps = map(fts, lines[0::2][:-1])
    commands = lines[1::2]
    return zip(timestamps, commands)

def command_features(filenames_series):
    filenames_series.apply()

file_df    = file_features()
# command_df = command_features(filenames['filenames'])
