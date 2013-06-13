#!/usr/bin/env python2
import os
import collections
import datetime
import re

HISTORY = os.path.join(os.environ['HOME'], '.history')

def filename_to_session(filename):
    s = re.split(r'[- T]', filename.replace('r-log', 'rlog'))
    return s[0], datetime.date(*map(int, s[1:4]))

def sessions_by_day():
    'IO () -> [(language, datetime.date, int)]'
    for filename in filter(lambda filename: '--' not in filename and '-' in filename, os.listdir(HISTORY)):
        print filename
        print filename_to_session(filename)
