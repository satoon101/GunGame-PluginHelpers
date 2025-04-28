# ../common/functions.py

"""Provides commonly used functions."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from contextlib import suppress
from os import system

# Package
from common.constants import PLATFORM, plugin_list


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def clear_screen():
    """Clear the screen."""
    system("cls" if PLATFORM == "windows" else "clear")


def get_plugin(suffix, *, allow_all=True):
    """Return a plugin by name to do something with."""
    # Clear the screen
    clear_screen()

    # Are there any plugins?
    if not plugin_list:
        print(f"There are no plugins to {suffix}.")
        return None

    # Get the question to ask
    message = f"What plugin would you like to {suffix}?\n\n"

    # Loop through each plugin
    for number, plugin in enumerate(plugin_list, 1):

        # Add the current plugin
        message += f"\t({number}) {plugin}\n"

    # Add ALL to the list if it needs to be
    if allow_all:
        message += f"\t({len(plugin_list) + 1}) ALL\n"

    # Ask which plugin to do something with
    value = input(message + "\n").strip()

    # Was a plugin name given?
    if value in [*plugin_list, "ALL"]:

        # Return the value
        return value

    # Was an integer given?
    with suppress(ValueError):

        # Typecast the value
        value = int(value)

        # Was the value a valid plugin choice?
        if value <= len(plugin_list):

            # Return the plugin by index
            return plugin_list[value - 1]

        # Was ALL's choice given?
        if value == len(plugin_list) + 1 and allow_all:

            # Return ALL
            return "ALL"

    # If no valid choice was given, try again
    return get_plugin(suffix, allow_all)


def link_directory(src, dest):
    """Create a symbolic link for the given source at the given destination."""
    # Is this a Windows OS?
    if PLATFORM == "windows":

        # Link using Windows format
        system(
            f'mklink /d "{dest}" "{src}"',
        )

    # Is this a Linux OS?
    else:

        # Link using Linux format
        system(
            f'ln -s "{src}" "{dest}"',
        )


def link_file(src, dest):
    """Create a hard link for the given source at the given destination."""
    # Is this a Windows OS?
    if PLATFORM == "windows":

        # Link using Windows format
        system(
            f'mklink "{dest}" "{src}"',
        )

    # Is this a Linux OS?
    else:

        # Link using Linux format
        system(
            f'ln -s "{src}" "{dest}"',
        )
