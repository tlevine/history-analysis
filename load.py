#!/usr/bin/env python2
import session, command

# sessions = session.df()
# commands = command.df(sessions['filename'].head(100))

import MySQLdb
con = MySQLdb.connect(
    host='history.cvjyprczkdry.us-west-2.rds.amazonaws.com',
    port=3306, user='tlevine', passwd='aoeuaoeu', db='history'
)

# sessions[['filename','day']]
pandas.io.sql.write_frame(sessions, 'sessions', con, flavor = 'mysql')

pandas.io.sql.write_frame(
    commands[['filename','datetime','is_comment','n_args','n_char']]
    'commands', con, flavor = 'mysql')

# Useful for testing
# reload(command); commands = command.df(sessions.head(10)['filename']); commands[range(2,len(commands.columns))].head(30)
