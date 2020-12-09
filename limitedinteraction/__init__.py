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

This module provides simple GUI tools that run in their own process, so that
it cannot conflict with the current running event loop. It has no external
dependency, and updates the matplotlib event loop in background (if
matplotlib is installed) while waiting for user action.
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
from threading import Thread
import subprocess
import warnings
from typing import Sequence, Union, Any, List, Dict, Optional


# Try setting polling pause() to plt.pause() if matplotlib is installed
try:
    import matplotlib.pyplot as plt

    def polling_pause():
        """Pause while refreshing Matplotlib while waiting for user."""
        plt.pause(0.2)

except ImportError:

    def polling_pause():
        """Pause while waiting for user."""
        time.sleep(0.2)


# Set some constants
is_pc = True if platform.system() == 'Windows' else False
is_mac = True if platform.system() == 'Darwin' else False
is_linux = True if platform.system() == 'Linux' else False
my_path = os.path.dirname(os.path.abspath(__file__))
cmd_file = my_path + '/cmd.py'

# Temporary folder
try:
    if is_pc and 'TEMP' in os.environ:
        _base_temp_folder = os.environ['TEMP']
        _temp_folder = _base_temp_folder + '/limitedinteraction'
    elif is_mac and 'TMPDIR' in os.environ:
        _base_temp_folder = os.environ['TMPDIR']
        _temp_folder = _base_temp_folder + '/limitedinteraction'
    else:
        _temp_folder = os.environ['HOME'] + '/.limitedinteraction'

    try:
        os.mkdir(_temp_folder)
    except FileExistsError:
        pass

except Exception:
    warnings.warn('Could not set temporary folder.')
    _temp_folder = '.'

# Set some state variables
_message_window_int = [0]


def _print_command_call(command_call):
    """Print command call (for debugging)."""
    print(f'command call: {command_call}')
    expanded = ''
    for _ in command_call:
        expanded = expanded + f"'{_}' "
    print(f'expanded command call: {expanded}')


def button_dialog(message="Please select an option",
                  choices=["Cancel", "OK"],
                  title="",
                  icon=None,
                  **kwargs):
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
    icon (optional)
        Path to an icon (png image) to include in the dialog window.

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
         'icon': icon,
         **kwargs})]

    def threaded_function():
        button[0] = int(subprocess.check_output(command_call,
                        stderr=subprocess.DEVNULL))

    thread = Thread(target=threaded_function)
    thread.start()

    while button[0] is None:
        polling_pause()  # Update matplotlib so that is responds to user input

    return button[0]


def message(message, **kwargs) -> None:
    """
    Show a message window.

    Parameters
    ----------
    message
        The message to show. Use '' to close the previous message windows.

    """
    # Begins by deleting the current message
    for file in os.listdir(_temp_folder):
        if 'limitedinteraction_message_flag' in file:
            os.remove(_temp_folder + '/' + file)

    if message is None or message == '':
        return

    print(message)

    _message_window_int[0] += 1
    flagfile = (f"{_temp_folder}/"
                f"limitedinteraction_message_flag{_message_window_int}")

    fid = open(flagfile, 'w')
    fid.write("DELETE THIS FILE TO CLOSE THE LIMITEDINTERACTION MESSAGE "
              "WINDOW.")
    fid.close()

    command_call = [sys.executable, cmd_file, json.dumps(
        {'function': 'message',
         'message': message,
         'flagfile': flagfile,
         **kwargs})]

    def threaded_function():
        subprocess.call(command_call,
                        stderr=subprocess.DEVNULL)

    thread = Thread(target=threaded_function)
    thread.start()


def input_dialog(
        message: str = '',
        descriptions: Sequence[str] = [],
        initial_values: Sequence[str] = [],
        masked: Sequence[bool] = [],
        **kwargs) -> List[str]:
    """
    Prompt the user with an input dialog.

    Parameters
    ----------
    message
        Message to show to the user

    inputs
        Inputs description and configuration. This is a list of either:
            - str, in which case the provided str is the description of the
              corresponding input.
            - dict with the following key:
                - 'description' (str): Description of the corresponding input.
                - 'initial' (optional, str): Initial value.
                - 'mask' (optiona, bool): True to mask the input with ****.

    Returns
    -------
    List[str]
        A list of the returnes inputs.

    """
    # Run the input dialog in a separate thread to allow updating matplotlib
    output = [None]
    command_call = [sys.executable, cmd_file, json.dumps(
        {'function': 'input_dialog',
         'message': message,
         'descriptions': descriptions,
         'initial_values': initial_values,
         'masked': masked,
         **kwargs})]

    if 'debug' in kwargs and kwargs['debug']:
        _print_command_call(command_call)

    def threaded_function():
        p_output = json.loads(subprocess.check_output(command_call).decode())
        if isinstance(p_output, str) and p_output.startswith('!!!ERROR!!!'):
            print(p_output)
            output[0] = []
        else:
            output[0] = p_output

    thread = Thread(target=threaded_function)
    thread.start()

    while output[0] is None:
        polling_pause()  # Update matplotlib so that is responds to user input

    return output[0]


def get_folder(initial_folder: str = '.', **kwargs) -> str:
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
            'initial_folder': initial_folder,
            **kwargs})],
        stderr=subprocess.DEVNULL)

    return json.loads(temp.decode(sys.getdefaultencoding()))


def get_filename(initial_folder: str = '.', **kwargs) -> str:
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
            'initial_folder': initial_folder,
            **kwargs})],
        stderr=subprocess.DEVNULL)

    return json.loads(temp.decode(sys.getdefaultencoding()))


if __name__ == '__main__':
    # Running this script launches the interactive test/demo."
    choice = button_dialog(
        "Now we will run Limited Interaction's tests.",
        ["OK, let's go", "Quit"],
        icon='gear')

    if choice == 0:

        message('Pick a folder that is not the current folder.')
        foldername = get_folder(icon='gear')

        message('Check that you are in the same folder that you selected and '
                'pick a random file.')
        filename = get_filename(initial_folder=foldername, icon='gear')
        message('')

        choice = button_dialog(f'Did you select this file:\n{filename}?',
                               ['Yes', 'No'], icon='question')
        assert choice == 0

        something = input_dialog('Please enter something.')
        inputs = input_dialog(
            'Enter ok in 1st position if what you entered is in second '
            'position and if last position is masked.',
            ['1st position', '2nd position', '3rd position'],
            [1, something[0], 'you should see it'],
            [False, False, True])

        assert inputs[0].lower() == 'ok'
