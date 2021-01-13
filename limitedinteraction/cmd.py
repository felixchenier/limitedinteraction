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

Functions that return something print a json string with [returnval, contents] where
returnval is '' for success or a string that represent an exception to raise (e.g.,
'ModuleNotFoundError') by the module on error.
"""

__author__ = "Félix Chénier"
__copyright__ = "Copyright (C) 2020 Félix Chénier"
__email__ = "chenier.felix@uqam.ca"
__license__ = "Apache 2.0"



#---- Main imports
import json
import sys


#---- Exception management
def exit_and_raise(exception_type: str, exception_text: str):
    """Print [exception_type, exception_text] as a json string and exit."""
    print(json.dumps([exception_type, exception_text]))
    sys.exit(0)


#---- Other imports

# Try to import tkinter and gracefully fail if not available
try:
    import tkinter as tk
    import tkinter.ttk as ttk
    import tkinter.filedialog as filedialog
except ModuleNotFoundError:
    exit_and_raise(
        'ModuleNotFoundError', (
            "Failed to import tkinter. \n"
            "If you are seeing this message and are using your operating system's \n"
            "supplied python, you may try to install the tk GUI toolkit, or best, \n"
            "install a proper version of python (e.g., python.org, anaconda.org, \n"
            "etc.) which normally includes tkinter and links correctly to the tk \n"
            "GUI toolkit."))


from functools import partial
import time
import os
import platform
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
    if 'left' in kwargs and 'right' in kwargs:
        exit_and_raise('ValueError',
                       "'left' and 'right' cannot be both specified.")
    if 'top' in kwargs and 'bottom' in kwargs:
        exit_and_raise('ValueError',
                       "'top' and 'bottom' cannot be both specified.")

    # Get current dimensions
    (contents_width, contents_height,
     contents_left, contents_top) = get_window_geometry(root)

    # Calculate frame width and titlebar height
    # From https://exceptionshub.com/
    #     how-to-center-a-window-on-the-screen-in-tkinter.html
    frm_width = root.winfo_rootx() - root.winfo_x()
    win_width = contents_width + 2 * frm_width
    titlebar_height = root.winfo_rooty() - root.winfo_y()
    win_height = contents_height + titlebar_height + frm_width

    # Ensure to meet given minimal values for width and height
    if win_width < kwargs['min_width']:
        win_width = kwargs['min_width']

    if 'min_height' in kwargs and win_height < kwargs['min_height']:
        win_height = kwargs['min_height']

    if 'left' in kwargs:
        win_left = kwargs['left']
    elif 'right' in kwargs:
        win_left = root.winfo_screenwidth() - win_width - kwargs['right']
    else:
        win_left = int(root.winfo_screenwidth() / 2 - win_width / 2)  # center

    if 'top' in kwargs:
        win_top = kwargs['top']
    elif 'bottom' in kwargs:
        win_top = root.winfo_screenheight() - win_height - kwargs['bottom']
    else:
        win_top = int(root.winfo_screenheight() / 2 - win_height / 2)  # center

    # Window parameters to contents paramaters
    contents_width = win_width - 2 * frm_width
    contents_height = win_height - titlebar_height - frm_width

    root.geometry(f'{contents_width}x{contents_height}+{win_left}+{win_top}')


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
    if 'labels' in kwargs:
        labels = kwargs['labels']
    else:
        labels = []

    if 'initial_values' in kwargs:
        initial_values = kwargs['initial_values']
    else:
        initial_values = []

    if 'masked' in kwargs:
        masked = kwargs['masked']
    else:
        masked = []

    n_boxes = max(1,
                  len(labels),
                  len(initial_values),
                  len(masked))

    if len(labels) == 0:
        labels = [''] * n_boxes
    if len(initial_values) == 0:
        initial_values = [''] * n_boxes
    if len(masked) == 0:
        masked = [False] * n_boxes

    if (
            len(labels) != n_boxes or
            len(initial_values) != n_boxes or
            len(masked) != n_boxes):
        exit_and_raise('ValueError', ("Length mismatch between labels, "
                                      "initial_values and masked."))

    outputs = [[]]

    # OK callback
    def ok_pressed(*args):
        for tk_entry in tk_entries:
            outputs[0].append(tk_entry.get())
        root.quit()

    # Add labels and entries
    tk_labels = []
    tk_entries = []
    for i, label in enumerate(labels):

        # Label
        if len(label) > 0:
            tk_label = ttk.Label(frame, text=label)
            tk_label.pack(fill=tk.X)
            tk_label.configure(anchor="center")  # center justified
            tk_labels.append(tk_label)

        # Entry
        if masked[i]:
            tk_entry = ttk.Entry(frame, show='*')
        else:
            tk_entry = ttk.Entry(frame)

        tk_entry.insert(0, initial_values[i])
        tk_entry.bind('<Return>', ok_pressed)
        tk_entry.pack(fill=tk.X)
        if i == 0:
            tk_entry.focus()
        tk_entries.append(tk_entry)

    # Add OK button
    tk_ok_btn = ttk.Button(frame, text='OK', command=ok_pressed,
                           default='active')
    tk_ok_btn.bind('<Return>', ok_pressed)
    tk_ok_btn.pack(fill=tk.X)

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

    #---- Pass the rest to the requested function and return

    if function == 'import':
        print(json.dumps(['', '']))
    elif function == 'button_dialog':
        print(json.dumps(['', button_dialog(root, frame, **kwargs)]))
    elif function == 'input_dialog':
        print(json.dumps(['', input_dialog(root, frame, **kwargs)]))
    elif function == 'message':
        message(root, frame, **kwargs)
    elif function == 'get_filename':
        print(json.dumps(['', get_filename(root, **kwargs)]))
    elif function == 'get_folder':
        print(json.dumps(['', get_folder(root, **kwargs)]))

