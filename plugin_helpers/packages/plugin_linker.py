# ../plugin_linker.py

"""Links plugins to Source.Python's repository."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Package
from common.constants import GUNGAME_DIR, START_DIR, plugin_list
from common.functions import clear_screen, get_plugin, link_directory, link_file


# =============================================================================
# >> MAIN FUNCTION
# =============================================================================
def link_plugin(plugin_name):
    """Link the given plugin name to Source.Python's repository."""
    # Was an invalid plugin name given?
    if plugin_name not in plugin_list:
        print(
            f'Invalid plugin name "{plugin_name}"',
        )
        return

    # Get the plugin's path
    plugin_path = START_DIR / plugin_name

    # Link the main directory
    _link_directory(
        plugin_path, "addons", "source-python", "plugins",
        "gungame", "plugins", "custom", plugin_name,
    )

    # Link the data directory
    _link_directory(
        plugin_path, "addons", "source-python", "data",
        "plugins", "gungame", plugin_name,
    )

    # Link the data file
    _link_file(
        plugin_path, "addons", "source-python", "data",
        "plugins", "gungame", plugin_name + ".ini",
    )

    # Link the message translations file
    _link_file(
        plugin_path, "resource", "source-python", "translations",
        "gungame", "messages", "custom_plugins", plugin_name + ".ini",
    )

    # Link the commands translations file
    _link_file(
        plugin_path, "resource", "source-python", "translations",
        "gungame", "commands", "custom_plugins", plugin_name + ".ini",
    )

    # Link the config translations file
    _link_file(
        plugin_path, "resource", "source-python", "translations",
        "gungame", "config", "custom_plugins", plugin_name + ".ini",
    )

    # Link the rules translations file
    _link_file(
        plugin_path, "resource", "source-python", "translations",
        "gungame", "rules", "custom_plugins", plugin_name + ".ini",
    )

    # Link sounds
    sound_path = plugin_path / "sound" / "source-python" / "gungame" / "default"
    if not sound_path.isdir():
        return

    for sound_file in sound_path.files():
        _link_file(
            plugin_path, "sound", "source-python", "gungame", "default",
            sound_file.name,
        )


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def _link_directory(plugin_path, *args):
    """Link the directory using the given arguments."""
    # Get the path within the plugin
    src = plugin_path.joinpath(*args)

    # Does the path not exist?
    if not src.isdir():
        return

    # Get the path within the Source.Python repository
    dest = GUNGAME_DIR.joinpath(*args)

    # Does the destination not exist?
    if not dest.isdir():

        # Link the directory
        link_directory(src, dest)


def _link_file(plugin_path, *args):
    """Link the file using the given arguments."""
    # Get the path within the plugin
    src = plugin_path.joinpath(*args)

    # Does the path not exist?
    if not src.isfile():
        return

    # Get the path within the Source.Python repository
    dest = GUNGAME_DIR.joinpath(*args)

    # Does the destination not exist?
    if not dest.isfile():

        # Link the file
        link_file(src, dest)


# =============================================================================
# >> CALL MAIN FUNCTION
# =============================================================================
if __name__ == "__main__":

    # Get the plugin to link
    _plugin_name = get_plugin("link")

    # Was a valid plugin chosen?
    if _plugin_name is not None:

        # Clear the screen
        clear_screen()

        # Was ALL chosen?
        if _plugin_name == "ALL":

            # Loop through all plugins
            for _plugin_name in plugin_list:

                # Check the current plugin
                link_plugin(_plugin_name)

        # Was a valid plugin chosen?
        else:

            # Check the chosen plugin
            link_plugin(_plugin_name)
