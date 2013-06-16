#!/usr/bin/env python2
import session, command

sessions = session.df()
commands = command.df(sessions['filename'])

sessions[['filename','day']]
commands[['filename','datetime','is_comment','n_args','n_char']]

# Useful for testing
# reload(command); commands = command.df(sessions.head(10)['filename']); commands[range(2,len(commands.columns))].head(30)
