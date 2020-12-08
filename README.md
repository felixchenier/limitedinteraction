# limitedinteraction

Provides simple, backend-independant GUI tools for simple user interaction.

This module provides simple GUI tools that run in their own process, so that it cannot
conflict with the current running event loop. It has no external dependency, and updates
the matplotlib event loop in background (if matplotlib is installed) while waiting for
user action.

## Statement of need ##

This module may interest people transitionning from Matlab to python, who miss Matlab's
simple ui functions such as msgbox, menu, etc. I could not find equivalent functions in
python that are both blocking when needed, but still continue to refresh matplotlib
in an interactive IPython session, and do not interfere with the current backend.

This module is a no-brainer. It has no dependencies and runs its own tkinter event loop
in its own process, and is therefore compatible with any interactive backend.

## Usage ##

At the moment, the following functions are implemented:

    import limitedinteraction as ltdi

	# button_dialog
	    
    choice = ltdi.button_dialog(message="Please select an option.",
                                choices=["Cancel", "OK"],
                                title="Window title",
                                picture=path/to/picture.png)
                                
    # get_folder
    
    folder_name = ltdi.get_folder(initial_folder='.')
    
    # get_filename
    
    file_name = ltdi.get_filename(initial_folder='.')
    

## Warning ##

This is still in early development. It will be great, but later.

## Known issues ##

If you are using *macOS Mojave** or *Anaconda python on Linux**, you may have these
problems:

- On macOS Mojave, tkinter is known to be seriously broken. If you use a Mac, please use
  any other OS version than Mojave.
  
- On Linux, tkinter fonts are ugly under anaconda python. It works, but it looks ancient.
