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

This file is not to be included as a module but instead called as a separate process by
limitedinteraction/__init__.py.
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


def center_window(root):
    """Center the root window on screen."""
    (width, height, left, top) = get_window_geometry(root)
    root.geometry('%dx%d+%d+%d' % (
                  width, height,
                  root.winfo_screenwidth()/2-width/2,
                  root.winfo_screenheight()/2-height/2))


def show_window(root):
    """Show the window (remove transparency)"""
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
    ichoice = 0
    for choice in kwargs['choices']:
        btn = ttk.Button(frame,
                        text=choice,
                        command=partial(return_choice, ichoice))
        btn.pack(fill=tk.X)
        ichoice = ichoice + 1

    center_window(root)
    show_window(root)
    root.mainloop()
    return selected_choice[0]


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
        if kwargs['picture'] == 'error':
            kwargs['picture'] = my_path + '/error.png'
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
        print(json.dumps(button_dialog(root, frame, **kwargs)))
    elif function == 'get_filename':
        print(json.dumps(get_filename(root, **kwargs)))
    elif function == 'get_folder':
        print(json.dumps(get_folder(root, **kwargs)))
        
