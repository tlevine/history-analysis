#!/usr/bin/env python2
import sqlite3

import session, command

sessions = session.df()
commands = command.df(sessions['filename'])

con = sqlite3.connect('/tmp/history.db')

# Write the sessions
pandas.io.sql.write_frame(sessions[['filename','day']], 'sessions', con)

# Write the commands
safe_command_columns = ['filename','datetime','is_comment','n_args','n_char']
pandas.io.sql.write_frame(commands[safe_command_columns], 'commands', con)

# Useful for testing
# reload(command); commands = command.df(sessions.head(10)['filename']); commands[range(2,len(commands.columns))].head(30)
