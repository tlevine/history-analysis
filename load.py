#!/usr/bin/env python2
import session, command

sessions = session.df()
commands = command.df(sessions.head(10)['filename'])
