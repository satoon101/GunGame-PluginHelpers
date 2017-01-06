# ../plugin_creater.py

"""Creates a plugin with its base directories and files."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from distutils.util import strtobool
# Package
from common.constants import AUTHOR
from common.constants import PREMADE_FILES_DIR
from common.constants import START_DIR
from common.constants import plugin_list
from common.functions import clear_screen


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_directory_or_file = {
    '1': 'file',
    '2': 'directory',
    '3': None,
}


# =============================================================================
# >> MAIN FUNCTION
# =============================================================================
def create_plugin(plugin_name, **options):
    """Verify the plugin name and create its base directories/files."""
    # Was no plugin name provided?
    if plugin_name is None:
        print('No plugin name provided.')
        return

    # Is the given plugin name valid?
    if not plugin_name.replace('_', '').isalnum():
        print('Invalid plugin name.')
        print(
            'Plugin name must only contain ' +
            'alpha-numeric values and underscores.')
        return

    # Get the path to create the plugin at
    plugin_base_path = START_DIR / plugin_name

    # Has the plugin already been created?
    if plugin_base_path.isdir():
        print('Plugin already exists.')
        return

    # Get the plugin's directory
    plugin_path = plugin_base_path.joinpath(
        'addons', 'source-python', 'plugins', 'gungame', 'plugins', 'custom',
        plugin_name,
    )

    # Create the plugin's directory
    plugin_path.makedirs()

    _copy_file(plugin_path / '__init__.py')

    _copy_file(plugin_path / 'info.py')

    _copy_file(plugin_path / plugin_name + '.py')

    if options.get('commands', False):
        _copy_file(plugin_path / 'commands.py')

        _create_file(
            plugin_base_path.joinpath(
                'resource', 'source-python', 'translations', 'gungame',
                'commands', 'custom_plugins', plugin_name + '.ini'
            )
        )

    if options.get('config', False):
        _copy_file(plugin_path / 'configuration.py')

        _create_file(
            plugin_base_path.joinpath(
                'resource', 'source-python', 'translations', 'gungame',
                'config', 'custom_plugins', plugin_name + '.ini'
            )
        )

    if options.get('events', False):
        _copy_file(plugin_path / 'custom_events.py')

    if options.get('rules', False):
        _copy_file(plugin_path / 'rules.py')

        _create_file(
            plugin_base_path.joinpath(
                'resource', 'source-python', 'translations', 'gungame',
                'rules', 'custom_plugins', plugin_name + '.ini'
            )
        )

    if options.get('settings', False):
        _copy_file(plugin_path / 'settings.py')

    if options.get('sounds', False):
        _copy_file(plugin_path / 'sounds.py')

    data = options.get('data', None)

    # Should a data file be created?
    if data == 'file':
        _create_file(
            plugin_base_path.joinpath(
                'addons', 'source-python', 'data', 'plugins', 'gungame',
                plugin_name + '.ini'
            )
        )

    # Should a data directory be created?
    elif data == 'directory':
        plugin_base_path.joinpath(
            'addons', 'source-python', 'data', 'plugins', 'gungame',
            plugin_name
        ).makedirs()

    translations = options.get('translations', False)

    # Should a translations file be created?
    if translations:
        _create_file(
            plugin_base_path.joinpath(
                'resource', 'source-python', 'translations', 'gungame',
                'messages', 'custom_plugins', plugin_name + '.ini'
            )
        )

    # Loop through all premade files
    for file in PREMADE_FILES_DIR.files():

        # Skip Python files
        if file.ext == '.py':
            continue

        # Copy the file to the plugin's base directory
        PREMADE_FILES_DIR.joinpath(file.namebase).copy(
            plugin_base_path / file.namebase
        )


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def _copy_file(filepath):
    """"""
    if PREMADE_FILES_DIR.joinpath(filepath.name).isfile():

        PREMADE_FILES_DIR.joinpath(filepath.name).copy(filepath)

    else:

        PREMADE_FILES_DIR.joinpath('plugin.py').copy(filepath)

    with filepath.open() as open_file:

        file_contents = open_file.read()

    plugin_name = filepath.parent.namebase.split('_', 1)[1]
    plugin_class = plugin_name.title()
    plugin_title = plugin_class.replace('_', ' ')
    plugin_command = plugin_title.replace(' ', '')

    file_contents = file_contents.format(
        plugin_name=plugin_name,
        plugin_class=plugin_class,
        plugin_title=plugin_title,
        plugin_command=plugin_command,
        author=AUTHOR,
    )

    with filepath.open('w') as open_file:

        open_file.write(file_contents)


def _create_file(filepath):
    if not filepath.parent.isdir():
        filepath.parent.makedirs()
    filepath.touch()


def _get_plugin_name():
    """Return a new plugin name."""
    # Clear the screen
    clear_screen()

    # Ask for a valid plugin name
    name = input(
        'What is the name of the plugin that should be created?\n\n'
    )
    if not name.startswith('gg_'):
        name = 'gg_' + name

    # Is the plugin name invalid?
    if not name.replace('_', '').isalnum():

        # Try to get a new plugin name
        return _ask_retry(
            'Invalid characters used in plugin name "{name}".\n'
            'Only alpha-numeric and underscores allowed.'.format(
                name=name,
            )
        )

    # Does the plugin already exist?
    if name in plugin_list:

        # Try to get a new plugin name
        return _ask_retry(
            'Plugin name "{name}" already exists.'.format(name=name)
        )

    # Return the plugin name
    return name


def _ask_retry(reason):
    """Ask if another plugin name should be given."""
    # Clear the screen
    clear_screen()

    # Get whether to retry or not
    value = input(
        reason + '\n\n' + 'Do you want to try again?\n\n' +
        '\t(1) Yes\n\t(2) No\n\n').lower()

    # Was the retry value invalid?
    try:
        value = bool(strtobool(value))

    # Try again
    except ValueError:
        return _ask_retry(reason)

    # Was Yes selected?
    if value:

        # Try to get another plugin name
        return _get_plugin_name()

    # Simply return None to not get a plugin name
    return None


def _get_file(name):
    """Return whether or not to create the given file."""
    clear_screen()

    value = input(
        'Do you want to include a {name} file?\n\n'
        '\t(1) Yes\n\t(2) No\n\n'.format(
            name=name,
        )
    ).lower()

    if value == '2':
        return False
    # Was the given value invalid?
    try:
        value = bool(strtobool(value))

    # Try again
    except ValueError:
        return _get_file(name)

    # Return the value
    return value


def _get_directory_or_file(name):
    """Return whether to create the given directory or file."""
    # Clear the screen
    clear_screen()

    # Get whether to add a directory, file, or neither
    value = input(
        'Do you want to include a {name} file, directory, or neither?\n\n'
        '\t(1) File\n\t(2) Directory\n\t(3) Neither\n\n'.format(
            name=name,
        )
    )

    # Was the given value invalid?
    if value not in _directory_or_file:

        # Try again
        _get_directory_or_file(name)

    # Return the value
    return _directory_or_file[value]


# =============================================================================
# >> CALL MAIN FUNCTION
# =============================================================================
if __name__ == '__main__':

    # Get the plugin name to use
    _plugin_name = _get_plugin_name()

    # Was a valid plugin name given?
    if _plugin_name is not None:

        _commands = _get_file('commands')
        _config = _get_file('configuration')
        _events = _get_file('custom events')
        _rules = _get_file('rules')
        _settings = _get_file('player settings')
        _sounds = _get_file('sounds')
        _data = _get_directory_or_file('data')
        _translations = _get_file('message translations')

        # Call create_plugin with the options
        create_plugin(
            _plugin_name, commands=_commands, config=_config, events=_events,
            rules=_rules, settings=_settings, sounds=_sounds, data=_data,
            translations=_translations,
        )
