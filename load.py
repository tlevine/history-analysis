#!/usr/bin/env python2
import os
import datetime
import re

import pandas

HISTORY = os.path.join(os.environ['HOME'], '.history')

def filename_to_session(filename):
    'unicode -> (unicode, datetime.date)'
    s = re.split(r'[- T]', filename.replace('r-log', 'rlog'))
    return s[0], datetime.date(*map(int, s[1:4]))

def sessions_by_day():
    'IO () -> [session]'
    return [filename_to_session(filename) for filename in filter(lambda filename: '--' not in filename and '-' in filename, os.listdir(HISTORY))]

df = pandas.DataFrame(sessions_by_day(), columns = ['language', 'day'])

days = df[df['language'] == 'sh'].groupby('day')['day'].count()
