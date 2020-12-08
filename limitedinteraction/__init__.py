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


import sys
import json
import tkinter as tk
import tkinter.ttk as ttk
import platform
import time
from functools import partial
from threading import Thread
import subprocess


is_pc = True if platform.system() == 'Windows' else False
is_mac = True if platform.system() == 'Darwin' else False
is_linux = True if platform.system() == 'Linux' else False


def _get_window_geometry(root):
    """Return the root geometry as the tuple (width, height, left, top)."""
    root.update()
    geometry = root.geometry()

    size = geometry[:geometry.find('+')]
    position = geometry[geometry.find('+')+1:]

    width = int(size[:size.find('x')])
    height = int(size[geometry.find('x')+1:])

    left = int(position[:position.find('+')])
    top = int(position[position.find('+')+1:])

    return (width, height, left, top)


def _show_window(root):
    """Show the window (remove transparency)"""
    
    # Move the root window to the top left of the screen, with a slight offset to
    # compensate for macOS menu bar and to avoid hiding maximized window bar and
    # controls.
    (width, height, left, top) = _get_window_geometry(root)
    root.geometry(f'{width}x{height}+40+40')

    # Unhide the window
    root.wm_attributes("-alpha", 1)
    root.attributes("-alpha", 1)


def button_dialog(message="Please select an option.",
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
    command_call = [sys.executable, __file__, json.dumps(
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


def _button_dialog(root, frame, **kwargs):
    """Implement button_dialog."""
    # We use a list of length 1 to pass selected_choice by reference.
    selected_choice = [-1]  # Default if we click close.

    def return_choice(ichoice):
        selected_choice[0] = ichoice
        root.quit()

    # Buttons
    ichoice = 0
    for choice in kwargs['choices']:
        btn = ttk.Button(frame,
                        text=choice,
                        command=partial(return_choice, ichoice))
        btn.pack(fill=tk.X)
        ichoice = ichoice + 1

    _show_window(root)
    root.mainloop()
    return selected_choice[0]


#--------------- ENTRY POINT ---------------#
if __name__ == '__main__':
    kwargs = json.loads(sys.argv[1])
    function = kwargs['function']
    kwargs.pop('function')
    

    #--- CREATE THE ROOT WINDOW ---#
    if 'title' not in kwargs:
        kwargs['title'] = ''

    root = tk.Tk()

    # Make it transparent while we modify it.
    root.wm_attributes("-alpha", 0)
    root.attributes('-alpha', 0)

    # Ensure the window is not created as a tab on macOS
    root.resizable(width=False, height=False)
    root.title(kwargs['title'])

    # Set topmost
    root.attributes('-topmost', True)

    # Disable resize button on windows
    if is_pc:
        root.attributes('-toolwindow', True)    
        
    # Add the main frame
    frame = ttk.Frame(root, padding=5 if is_mac else 0)
    frame.pack(fill=tk.X)

    # Add the picture
    if 'picture' in kwargs and kwargs['picture'] is not None:
        try:
            picture_image = tk.PhotoImage(file=kwargs['picture'])
            picture = tk.Label(frame, image=picture_image)
            picture.pack(fill=tk.X)
        except:
            pass

    # Add the message label
    lbl = ttk.Label(frame, text=kwargs['message'])
    lbl.pack(fill=tk.X)
    
    #--- PASS THE REST TO THE REQUESTED FUNCTION ---#

    if function == 'button_dialog':
        print(json.dumps(_button_dialog(root, frame, **kwargs)))


#--------------- WHEN IMPORTED AS A MODULE ---------------#
else:
    # Set the pause function to update matplotlib if installed.
    try:
        import matplotlib.pyplot as plt    
        def polling_pause():
            plt.pause(0.2)
    except ImportError:
        def polling_pause():
            time.sleep(0.2)
