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
Limited Interaction
===================
Provides simple, backend-independant GUI tools for limited user interaction.

This module provides simple GUI tools that run in their own process, so that
it cannot conflict with the current running event loop. If Matplotlib is
imported, it updates its event loop in background while waiting for user
action.

Additional parameters
---------------------
All functions except `get_folder` and `get_filename` accept these
parameters in addition to their own parameters:

title
    Title of the dialog window.
icon
    Can be either None, a str from ['alert', 'clock', 'cloud', 'error',
    'find', 'gear', 'info','light', 'lock', 'question', 'warning'] or a
    or a tuple of png files: (path_to_image_in_dialog.png,
    path_to_dock_icon.png)
left
    Distance between the monitor's left edge and the window's left edge in
    pixels. Parameters 'left' and 'right' cannot be used together.
right
    Distance between the monitor's right edge and the window's right edge in
    pixels. Parameters 'left' and 'right' cannot be used together.
top
    Distance between the monitor's top edge and the window's top edge in
    pixels. Parameters 'top' and 'bottom' cannot be used together.
bottom
    Distance between the monitor's bottom edge and the window's bottom edge in
    pixels. Parameters 'top' and 'bottom' cannot be used together.
min_width
    Minimal width of the dialog window in pixels.
min_height
    Minimal width of the dialog window in pixels.

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
from typing import Sequence, Union, List


# Set some constants
is_pc = True if platform.system() == 'Windows' else False
is_mac = True if platform.system() == 'Darwin' else False
is_linux = True if platform.system() == 'Linux' else False
my_path = os.path.dirname(os.path.abspath(__file__))

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


def _define_polling_pause():
    """
    Return the polling pause function.

    The returned function is a wrapper to either matplotlib.pyplot.pause (in
    the case where matplotlib is among the imported modules), or time.sleep
    (if matplotlib is not imported).
    """
    if 'matplotlib' in sys.modules:
        import matplotlib.pyplot as plt
        def polling_pause():
            """Pause while refreshing Matplotlib while waiting for user."""
            plt.pause(0.2)

    else:
        def polling_pause():
            """Pause while waiting for user."""
            time.sleep(0.2)

    return polling_pause


def _launch_subprocess(blocking=True, debug=False, **kwargs):
    """Launch a function and update event loop while waiting (if blocking)."""
    output = [None]
    command_call = [
        sys.executable,  # python3
        my_path + '/cmd.py',  # cmd.py
        json.dumps(kwargs)]

    if debug:
        print('-------')
        print(f'command call: {command_call}')
        expanded = ''
        for _ in command_call:
            expanded = expanded + f"'{_}' "
        print('-------')
        print(f'expanded command call: {expanded}')

    def threaded_function():
        """Start cmd.py in its own process and wait for its completion."""
        if blocking:
            output[0] = subprocess.check_output(command_call,
                                                stderr=subprocess.DEVNULL)
        else:
            subprocess.call(command_call,
                            stderr=subprocess.DEVNULL)

    # Start the new process in a thread - probably too much but it works and
    # it's easy.
    thread = Thread(target=threaded_function)
    thread.start()

    if blocking:
        polling_pause = _define_polling_pause()
        while output[0] is None:
            polling_pause()  # Update event loop or just wait.

    if output[0] is None:
        return None
    else:
        to_return = json.loads(output[0].decode())

        # Check if we should raise an error
        if to_return[0] != '':
            if to_return[0] == 'ModuleNotFoundError':
                raise ModuleNotFoundError(to_return[1])
            elif to_return[0] == 'ValueError':
                raise ValueError(to_return[1])
            else:
                raise Exception(to_return[0] + ': ' + to_return[1])

        return to_return[1]


def message(
        message: str,
        **kwargs) -> None:
    """
    Show or close a non-blocking message window.

    Parameters
    ----------
    message
        The message to show. Use '' to close the previous message windows.
    kwargs
        Consult the module's help for additional parameters.

    Returns
    -------
    None

    """
    # Begins by deleting the current message
    for file in os.listdir(_temp_folder):
        if 'limitedinteraction_message_flag' in file:
            os.remove(_temp_folder + '/' + file)

    if message is None or message == '':
        return

    _message_window_int[0] += 1
    flagfile = (f"{_temp_folder}/"
                f"limitedinteraction_message_flag{_message_window_int}")

    fid = open(flagfile, 'w')
    fid.write("DELETE THIS FILE TO CLOSE THE LIMITEDINTERACTION MESSAGE "
              "WINDOW.")
    fid.close()

    _launch_subprocess(
        blocking=False,
        function='message',
        message=message,
        flagfile=flagfile,
        **kwargs)


def button_dialog(
        message: str = 'Please select an option',
        choices: Sequence[str] = ['OK', 'Cancel'],
        **kwargs) -> int:
    """
    Show a blocking dialog window with a selection of buttons.

    Parameters
    ----------
    message
        Optional. Instruction to show to the user.
    choices
        Optional. List of str, each entry corresponding to a button caption.
    kwargs
        Consult the module's help for additional parameters.

    Returns
    -------
    int
        The selected button index (0 = First button, 1 = Second button, etc.).
        If the user closes the window instead of clicking a button, a value
        of -1 is returned.
    """
    return _launch_subprocess(
        function='button_dialog',
        message=message,
        choices=choices,
        **kwargs)


def input_dialog(
        message: str = '',
        labels: Sequence[str] = [],
        initial_values: Sequence[str] = [],
        masked: Sequence[bool] = [],
        **kwargs) -> Union[str, List[str]]:
    """
    Prompt the user with an input dialog.

    Parameters
    ----------
    message
        Optional. Instruction to show to the user.
    labels
        Optional. List of str: abels for each input.
    initial_values
        Optional. List of str: initial values for each input.
    masked
        Optional. List of bool: True to mask an input using stars.
    kwargs
        Consult the module's help for additional parameters.

    Returns
    -------
    str or List[str]
        If there was only one input, a str corresponding to this input is
        returned. If there was multiple inputs, a list of str is returned.

    """
    # Run the input dialog in a separate thread to allow updating matplotlib
    return _launch_subprocess(
        function='input_dialog',
        message=message,
        labels=labels,
        initial_values=initial_values,
        masked=masked,
        **kwargs)


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
    return _launch_subprocess(
        function='get_folder',
        initial_folder=initial_folder,
        **kwargs)


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
    return _launch_subprocess(
        function='get_filename',
        initial_folder=initial_folder,
        **kwargs)


def __dir__():
    return ['message', 'input_dialog', 'button_dialog', 'get_folder', 'get_filename']


#--- Check that the cmd module will respond well when asked.
_launch_subprocess(function='import')


if __name__ == '__main__':
    # Running this script launches the interactive test/demo."
    choice = button_dialog(
        "Now we will run Limited Interaction's tests.",
        ["OK, let's go", "Quit"],
        icon='gear')

    if choice == 0:

        #---- Non-interactive tests
        try:
            something = input_dialog('Test with bad arguments',
                                     labels=['one', 'two', 'three'],
                                     initial_values=['one', 'two'])
            raise ValueError('You should not see this error.')
        except ValueError:
            pass  # all is ok


        try:
            something = button_dialog(left=0, right=0)
            raise ValueError('You should not see this error.')
        except ValueError:
            pass  # all is ok

        try:
            something = button_dialog(top=0, bottom=0)
            raise ValueError('You should not see this error.')
        except ValueError:
            pass  # all is ok

        #---- Interactive tests

        choice = button_dialog(
            'Check that "Hello" is written in menu bar,\n'
            'then close the window.',
            ['Click here only if this window is not in the right-bottom corner'],
            title='Hello', right=0, bottom=0)
        assert choice == -1

        something = input_dialog('Close the window again.')
        assert something == -1

        something = input_dialog('Please enter "test".')
        assert something == 'test'

        inputs = input_dialog(
            'Click ok if:\n'
            '- first entry is 1\n'
            '- second entry is "test"\n'
            '- last entry is masked\n'
            '- you see labels titles.\n'
            'Close the window otherwise.',
            ['Label 1', 'Label 2', 'Label 3'],
            [1, 'test', 'you should not see it'],
            [False, False, True])

        assert inputs[0] == '1'
        assert inputs[1] == 'test'
        assert inputs[2] == 'you should not see it'

        message('Pick a folder that is not the current folder.')
        foldername = get_folder(icon='gear')

        message('Check that you are in the same folder that '
                'you just selected,\n'
                'then pick any file.')
        filename = get_filename(initial_folder=foldername, icon='gear')
        message('')

        choice = button_dialog(f'Did you select this file:\n{filename}?',
                               ['Yes', 'No'], icon='question')
        assert choice == 0

        button_dialog('Test completed.', ['OK'])
