# Copyright (c) 2012 John Reese
# Licensed under the MIT License

from __future__ import absolute_import, division

import os
from os import path

# Default dotfile path
installpath = path.dirname(path.realpath(__file__))

# Check the user's .pyranha and create it if needed
userpath = path.expanduser('~/.pyranha')
if path.exists(userpath):
    if not path.isdir(userpath):
        raise IOError('pyranha dotfile path {0} exists but is not a directory'.format(userpath))
else:
    os.mkdir(userpath)


engine = None
ui = None

def async_engine_command(command, network=None, params=None):
    """Send a command to the current backend engine."""
    return engine.async_command(command, network, params)

def async_ui_message(message_type, network=None, content=None):
    """Send a message to the current frontend user interface."""
    return ui.async_message(message_type, network, content)

def start(frontend='gtk'):
    """Initialize both the backend and frontend, and wait for them to mutually exit."""
    global engine
    global ui

    import pyranha.logging

    frontend = frontend.lower()

    if frontend == 'stdout':
        from pyranha.ui.stdout import StdoutUI
        ui = StdoutUI()

    elif frontend == 'gtk':
        from pyranha.ui.gtk import GtkUI
        ui = GtkUI()

    else:
        raise Exception('unsupported frontend type "{0}"'.format(frontend))

    from pyranha.engine.engine import Engine
    engine = Engine()

    engine.start()
    ui.start()

    while engine.is_alive():
        engine.join()

    while ui.is_alive():
        ui.join()
