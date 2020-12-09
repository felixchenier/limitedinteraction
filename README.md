# limitedinteraction

Provides simple, backend-independant GUI tools for simple user interaction.

This module provides simple GUI tools that run in their own process, so that it cannot
conflict with the current running event loop. It has no external dependency, and updates
the matplotlib event loop in background (if matplotlib is installed) while waiting for
user action.


## Statement of need ##

This module may interest people transitionning from Matlab to python, who miss Matlab's
simple ui functions such as msgbox, menu, etc. I could not find equivalent functions in
python that are blocking when needed, but still continue to refresh matplotlib
in an interactive IPython session, and that do not interfere with the current backend.

This module should be a no-brainer to use. It has no dependencies and runs its own
tkinter event loop in its own process, and is therefore compatible with any interactive
backend.


## Usage ##

### Importing ###

```python
import limitedinteraction as ltdi
```

### Creating a persistent message window ###

```python
ltdi.message('Please wait a few moments.',
              title='Calculating...',
              icon='clock')

# This is a non-blocking function. Any code after this call is executed immediately,
# while this message window stays in foreground.
```

![message_calculating](/doc/message_calculating.png)

```python
# Close the message window

ltdi.message('')
```

### Asking for user input ###

```python
choice_index = ltdi.button_dialog('Please zoom on the figure and click Next.',
                                  choices=['Next', 'Cancel'],
                                  title='User interaction',
                                  icon='gear')

# This is a blocking function. We wait for a choice before continuing. Meanwhile,
# Matplotlib's event loop is refreshed so that the user can interact with figures.
```

![button_dialog_user_interaction.png](/doc/button_dialog_user_interaction.png)


### Other functions ###
```python
# Get a file name using the operating system's standard file selection window.
filename = ltdi.get_filename()

# Get a folder name using the operating system's standard folder selection window.
folder = ltdi.get_folder()
```

## Known issues ##

If you are using *macOS Mojave* or *Anaconda python on Linux*, you may have these
problems:

- On macOS Mojave, tkinter is known to be seriously broken. If you use a Mac, please use
  any other OS version than Mojave.

- On Anaconda python on Linux, tkinter fonts are very ugly. It still works, but it looks
  ancient.
