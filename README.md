# Limited Interaction

Provides simple, backend-independant GUI tools for limited user interaction.

This module provides simple GUI tools that run in their own separate process,
which proves to be useful in interactive IPython sessions. It has no external
dependency and updates the matplotlib event loop in background (if matplotlib
is installed) while waiting for user action.


## Why another GUI module ##

This module may interest people transitionning from Matlab to python, who miss
Matlab's no-brainer ui functions such as msgbox, menu, etc. I could not find
equivalent functions in the vast python ecosystem that are:

- blocking when needed;
- but still continue to refresh matplotlib when launched in an interactive
  IPython session;
- independent of the currently running IPython event loop.

This module is designed to be a limited but extra-easy option to interact with
a user without even thinking about what is a GUI. It has no dependencies and
should work out of the box in any situation where the python interpreter is run
locally. It is based on tkinter, but since it starts its own processes, it can
be run conjointly with any other backend (Qt, wxWidgets, etc.).


## Installing ##

Using pip:
```
pip install limitedinteraction
```

Using conda:
```
conda install -c conda-forge limitedinteraction
```

## Usage ##

### Importing ###

```python
import limitedinteraction as li
```

### Creating a persistent message window ###

```python
li.message('Please wait a few moments.',
           title='Calculating...',
           icon='clock')
```

![message_calculating_macOS](https://raw.githubusercontent.com/felixchenier/limitedinteraction/main/doc/message_calculating.png)


This is a non-blocking function. Any code after this call is executed
immediately, while this message window stays in foreground.

```python
# Close the message window
li.message('')
```

### Asking for user input ###

```python
name = li.input_dialog('What is your name?', icon='question')
```

![input_dialog_name_macOS](https://raw.githubusercontent.com/felixchenier/limitedinteraction/main/doc/input_dialog_name.png)

This is a blocking function. We wait for user input before continuing.
Meanwhile, Matplotlib's event loop is refreshed so that the user can
interact with figures.

This same function can have several inputs and some inputs can be masked:

```python
credentials = li.input_dialog('Please enter your credentials',
                              labels=['Username:', 'Password:'],
                              initial_values=['username', 'password'],
                              masked=[False, True],
                              icon='lock')
```
![input_dialog_credentials_macOS](https://raw.githubusercontent.com/felixchenier/limitedinteraction/main/doc/input_dialog_credentials.png)


```python
choice_index = li.button_dialog('Please zoom on the figure and click Next.',
                                choices=['Next', 'Cancel'],
                                title='User interaction',
                                icon='gear')
```

![button_dialog_user_interaction_macOS](https://raw.githubusercontent.com/felixchenier/limitedinteraction/main/doc/button_dialog_user_interaction.png)

This is a blocking function. We wait for a choice before continuing. Meanwhile,
Matplotlib's event loop is refreshed so that the user can interact with
figures.


### Other functions ###

Get a file name using the operating system's standard file selection window:

```python
filename = li.get_filename()
````

Get a folder name using the operating system's standard folder selection
window:

```python
folder = li.get_folder()
```

## Known issues ##

If you are using *macOS Mojave* or *Anaconda python on Linux*, you may have these
problems:

- On macOS Mojave, tkinter is known to be seriously broken. If you use a Mac, please use
  any other OS version than Mojave.

- On Anaconda python on Linux, tkinter fonts are very ugly. It still works, but it looks
  ancient.
