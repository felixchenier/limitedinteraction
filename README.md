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
```

![message_calculating](/doc/message_calculating.png)

```python
ltdi.message('')  # Close the message window.
```

### Asking for selection ###

```python
choice_index = ltdi.button_dialog(message='Please zoom on the figure and click Next.',
                                  choices=['Next', 'Cancel'],
                                  title='User interaction',
                                  icon='gear')
```

![button_dialog_user_interaction.png](/doc/button_dialog_user_interaction.png)


### Other functions ###
```python
filename = ltdi.get_filename()
folder = ltdi.get_folder()
```

## Known issues ##

If you are using *macOS Mojave* or *Anaconda python on Linux*, you may have these
problems:

- On macOS Mojave, tkinter is known to be seriously broken. If you use a Mac, please use
  any other OS version than Mojave.

- On Linux, tkinter fonts are ugly under anaconda python. It works, but it looks ancient.
