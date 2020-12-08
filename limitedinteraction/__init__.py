#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Félix Chénier

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Provides simple, backend-independant GUI tools for simple user interaction.

This module provides simple GUI tools that run in their own process, so that it cannot
conflict with the current running event loop. It has no external dependency, and updates
the matplotlib event loop in background (if matplotlib is installed) while waiting for
user action.
"""

__author__ = "Félix Chénier"
__copyright__ = "Copyright (C) 2020 Félix Chénier"
__email__ = "chenier.felix@uqam.ca"
__license__ = "Apache 2.0"


import os
import sys
import json
import platform
import time
from functools import partial
from threading import Thread
import subprocess


# Try setting polling pause() to plt.pause() if matplotlib is installed
try:
    import matplotlib.pyplot as plt
    def polling_pause():
        plt.pause(0.2)
except ImportError:
    def polling_pause():
        time.sleep(0.2)


# Set some constants
is_pc = True if platform.system() == 'Windows' else False
is_mac = True if platform.system() == 'Darwin' else False
is_linux = True if platform.system() == 'Linux' else False
my_path = os.path.dirname(os.path.abspath(__file__))
cmd_file = my_path + '/cmd.py'


def button_dialog(message="Please select an option",
                  choices=["Cancel", "OK"],
                  title="",
                  picture=None):
    """
    Create a blocking dialog window with a selection of buttons.

    Parameters
    ----------
    message
        Message that is presented to the user.
    choices
        List of button text.
    title (optional)
        Title of the dialog window.
    picture (optional)
        Path to a picture to include in the dialog window.

    Returns
    -------
    int
        The button number (0 = First button, 1 = Second button, etc.) If the
        user closes the window instead of clicking a button, a value of -1 is
        returned.
    """
    # Run the button dialog in a separate thread to allow updating matplotlib
    button = [None]
    command_call = [sys.executable, cmd_file, json.dumps(
        {'function': 'button_dialog',
         'message': message,
         'choices': choices,
         'title': title,
         'picture': picture})]

    def threaded_function():
        button[0] = int(subprocess.check_output(command_call,
                        stderr=subprocess.DEVNULL))

    thread = Thread(target=threaded_function)
    thread.start()

    while button[0] is None:
        polling_pause()  # Update matplotlib so that is responds to user input

    return button[0]


def get_folder(initial_folder: str = '.') -> str:
    """
    Get folder interactively using a file dialog window.

    Parameters
    ----------
    initial_folder
        Optional. The initial folder of the file dialog.

    Returns
    -------
    str
        The full path of the selected folder. An empty string is returned if
        the user cancelled.

    """
    temp = subprocess.check_output(
        [sys.executable, cmd_file, json.dumps({
            'function': 'get_folder',
            'initial_folder': initial_folder})],
        stderr=subprocess.DEVNULL)

    return json.loads(temp.decode(sys.getdefaultencoding()))


def get_filename(initial_folder: str = '.') -> str:
    """
    Get file name interactively using a file dialog window.

    Parameters
    ----------
    initial_folder
        Optional. The initial folder of the file dialog.

    Returns
    -------
    str
        The full path of the selected file. An empty string is returned if the
        user cancelled.
    """
    temp = subprocess.check_output(
        [sys.executable, cmd_file, json.dumps({
            'function': 'get_filename',
            'initial_folder': initial_folder})],
        stderr=subprocess.DEVNULL)

    return json.loads(temp.decode(sys.getdefaultencoding()))
