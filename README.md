# Limited Interaction

```python
import limitedinteraction as li

li.button_dialog("Simple dialog windows for scripters and scientists.",
                 choices=['OK'],
                 title='Limited Interaction',
                 icon='light')
```

![message_calculating_macOS](https://raw.githubusercontent.com/felixchenier/limitedinteraction/main/doc/about.png)

This module provides simple, generic dialog windows specifically aimed to
scripters and scientists who need a concise, elegant way of interacting with
their script users.

This module does not require any GUI programming, it has no external
dependency, and it is completely independent of the graphical backend in use
(if any). In IPython-based environments, its blocking functions allow
interacting with Matplotlib figures while waiting for user action.

For those transitionning from Matlab, this module fulfils the same role as
Matlab's msgbox, inputdlg, menu and other simple GUI functions.

--------------------------------------------------------------------------------
[Home page](https://felixchenier.uqam.ca/limitedinteraction)
      [GitHub](https://github.com/felixchenier/limitedinteraction)
      [Issue tracker](https://github.com/felixchenier/limitedinteraction/issues)
      [API](https://felixchenier.uqam.ca/limitedinteraction/api.html)

--------------------------------------------------------------------------------


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
immediately, while this message window stays in foreground. To close the
message window:

```python
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
```

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


## Credits ##

This module is developed by Félix Chénier at the Mobility and Adaptive
Sports Research Lab (https://felixchenier.uqam.ca).

It includes artwork developed by these designers:

- Warning and gear icons: [Laura Reen](https://www.iconfinder.com/laurareen)
- Question mark icon: [Design Revision](https://www.iconfinder.com/DesignRevision)
- All other icons: [Recep Kütük](https://www.iconfinder.com/recepkutuk)
