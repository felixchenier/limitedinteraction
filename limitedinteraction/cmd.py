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
Implements limitedinteraction functions.

This file is not to be included as a module but instead called as a separate
process by limitedinteraction/__init__.py.
"""

__author__ = "Félix Chénier"
__copyright__ = "Copyright (C) 2020 Félix Chénier"
__email__ = "chenier.felix@uqam.ca"
__license__ = "Apache 2.0"


# Imports
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
from functools import partial
import time
import os
import platform
import json
import sys


is_pc = True if platform.system() == 'Windows' else False
is_mac = True if platform.system() == 'Darwin' else False
is_linux = True if platform.system() == 'Linux' else False
my_path = os.path.dirname(os.path.abspath(__file__))


def get_window_geometry(root):
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


def place_window(root, **kwargs):
    """Place window in screen."""
    (width, height, left, top) = get_window_geometry(root)

    if width < kwargs['min_width']:
        width = kwargs['min_width']
    if width < kwargs['min_height']:
        height = kwargs['min_height']
    if 'left' in kwargs:
        left = kwargs['left']
    else:
        left = int(root.winfo_screenwidth() / 2 - width / 2)  # center
    if 'top' in kwargs:
        top = kwargs['top']
    else:
        top = int(root.winfo_screenheight() / 2 - height / 2)  # center

    root.geometry(f'{width}x{height}+{left}+{top}')


def show_window(root):
    """Show the window (remove transparency)."""
    # Unhide the window
    root.wm_attributes("-alpha", 1)
    root.attributes("-alpha", 1)


def button_dialog(root, frame, **kwargs):
    """Terminate composing the GUI and run it."""
    # We use a list of length 1 to pass selected_choice by reference.
    selected_choice = [-1]  # Default if we click close.

    def return_choice(ichoice):
        selected_choice[0] = ichoice
        root.quit()

    # Buttons
    buttons = []
    ichoice = 0
    for choice in kwargs['choices']:
        btn = ttk.Button(frame,
                         text=choice,
                         command=partial(return_choice, ichoice))
        btn.pack(fill=tk.X)
        buttons.append(btn)
        ichoice = ichoice + 1

    buttons[0].focus()

    place_window(root, **kwargs)
    show_window(root)
    root.mainloop()
    return selected_choice[0]


def input_dialog(root, frame, **kwargs):
    """Terminate composing the GUI and run it."""
    # Condition inputs
    if 'descriptions' in kwargs:
        descriptions = kwargs['descriptions']
    else:
        descriptions = []

    if 'initial_values' in kwargs:
        initial_values = kwargs['initial_values']
    else:
        initial_values = []

    if 'masked' in kwargs:
        masked = kwargs['masked']
    else:
        masked = []

    n_boxes = max(1,
                  len(descriptions),
                  len(initial_values),
                  len(masked))

    if len(descriptions) == 0:
        descriptions = [''] * n_boxes
    if len(initial_values) == 0:
        initial_values = [''] * n_boxes
    if len(masked) == 0:
        masked = [False] * n_boxes

    if (
            len(descriptions) != n_boxes or
            len(initial_values) != n_boxes or
            len(masked) != n_boxes):
        return ("!!!ERROR!!! Length mismatch between descriptions, "
                "initial_values and masked.")

    outputs = [[]]

    # OK callback
    def ok_pressed(*args):
        for entry in entries:
            outputs[0].append(entry.get())
        root.quit()

    # Add labels and entries
    labels = []
    entries = []
    for i, description in enumerate(descriptions):

        # Label
        if len(description) > 0:
            label = ttk.Label(frame, text=description)
            label.pack(fill=tk.X)
            label.configure(anchor="center")  # center justified
            labels.append(label)

        # Entry
        if masked[i]:
            entry = ttk.Entry(frame, show='*')
        else:
            entry = ttk.Entry(frame)

        entry.insert(0, initial_values[i])
        entry.bind('<Return>', ok_pressed)
        entry.pack(fill=tk.X)
        if i == 0:
            entry.focus()
        entries.append(entry)

    # Add OK button
    ok_btn = ttk.Button(frame, text='OK', command=ok_pressed,
                        default='active')
    ok_btn.bind('<Return>', ok_pressed)
    ok_btn.pack(fill=tk.X)

    place_window(root, **kwargs)
    show_window(root)
    root.mainloop()

    if outputs == [[]]:  # Closed the window
        return -1
    elif n_boxes == 1:  # Only one box, we return a str
        return outputs[0][0]
    else:  # Multiple boxes, we return the full list of str
        return outputs[0]


def message(root, frame, **kwargs):
    """Terminate composing the GUI and draw until flagfile is deleted."""
    place_window(root, **kwargs)
    show_window(root)

    def check_if_file_exists(file):
        try:
            fid = open(file, 'r')
        except FileNotFoundError:
            return False
        fid.close()
        return True

    while check_if_file_exists(kwargs['flagfile']):
        root.update()
        time.sleep(0.2)


def get_folder(root, **kwargs):
    root.withdraw()
    time.sleep(0.1)
    root.update()
    result = filedialog.askdirectory(
        title=kwargs['title'],
        initialdir=kwargs['initial_folder'])
    time.sleep(0.1)
    root.update()
    return result


def get_filename(root, **kwargs):
    root.withdraw()
    time.sleep(0.1)
    root.update()
    result = filedialog.askopenfilename(
        title=kwargs['title'],
        initialdir=kwargs['initial_folder'])
    time.sleep(0.1)
    root.update()
    return result


#--------------- ENTRY POINT ---------------#
if __name__ == '__main__':
    kwargs = json.loads(sys.argv[1])
    function = kwargs['function']
    kwargs.pop('function')

    #--- CREATE THE ROOT WINDOW ---#
    if 'title' not in kwargs:
        kwargs['title'] = ''
    if 'message' not in kwargs:
        kwargs['message'] = ''
    if 'min_width' not in kwargs:
        kwargs['min_width'] = 100
    if 'min_height' not in kwargs:
        kwargs['min_height'] = 100

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
    frame = ttk.Frame(root, padding=5)
    frame.pack(fill=tk.X)

    # Add the icon and set application icon
    if 'icon' in kwargs and kwargs['icon'] is not None:
        if kwargs['icon'] in ['alert', 'clock', 'cloud', 'error', 'find',
                              'gear', 'info', 'light', 'lock', 'question',
                              'warning']:
            small_icon = my_path + f"/images/{kwargs['icon']}_small.png"
            large_icon = my_path + f"/images/{kwargs['icon']}_large.png"

        else:
            if isinstance(kwargs['icon'], str):
                small_icon = kwargs['icon']
                large_icon = kwargs['icon']
            elif isinstance(kwargs['icon'], list):
                small_icon = kwargs['icon'][0]
                large_icon = kwargs['icon'][1]
            else:
                small_icon = None
                large_icon = None

        # Add the icon to the main frame
        try:
            icon_image = tk.PhotoImage(file=small_icon)
            icon = tk.Label(frame, image=icon_image)
            icon.pack(fill=tk.X)
        except:
            pass

        # Set the application icon
        root.iconphoto(False, tk.PhotoImage(file=large_icon))

    # Add the message label
    lbl = ttk.Label(frame, text=kwargs['message'], padding=(0, 5))
    lbl.configure(anchor="center")  # center justified
    lbl.pack(fill=tk.X)

    #--- PASS THE REST TO THE REQUESTED FUNCTION ---#

    if function == 'button_dialog':
        print(json.dumps(button_dialog(root, frame, **kwargs)))
    elif function == 'input_dialog':
        print(json.dumps(input_dialog(root, frame, **kwargs)))
    elif function == 'message':
        message(root, frame, **kwargs)
    elif function == 'get_filename':
        print(json.dumps(get_filename(root, **kwargs)))
    elif function == 'get_folder':
        print(json.dumps(get_folder(root, **kwargs)))

