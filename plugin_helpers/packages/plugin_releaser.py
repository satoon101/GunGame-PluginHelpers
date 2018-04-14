# ../plugin_releaser.py

"""Creates a release for a plugin with its current version number."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from contextlib import suppress
from os import sep
from subprocess import PIPE, Popen
from zipfile import ZIP_DEFLATED
from zipfile import ZipFile

# Site-package
from configobj import ConfigObj
from git import Repo

# Package
from common.constants import RELEASE_DIR
from common.constants import START_DIR
from common.constants import plugin_list
from common.functions import clear_screen
from common.functions import get_plugin


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Store all allowed readable data file types
_readable_data = [
    'ini',
    'json',
    'vdf',
    'xml',
]

# Store plugin specific directories with their respective allowed file types
allowed_filetypes = {
    'addons/source-python/plugins/gungame/plugins/custom': (
        _readable_data + ['md', 'py']
    ),
    'addons/source-python/data/plugins/gungame': (
        _readable_data + ['md', 'txt']
    ),
    'resource/source-python/translations/gungame': ['ini'],
}

# Store non-plugin specific directories
#   with their respective allowed file types
other_filetypes = {
    'materials/': ['vmt', 'vtf'],
    'models/': ['mdl', 'phy', 'vtx', 'vvd'],
}

# Store directories with files that fit allowed_filetypes
#   with names that should not be included
exception_filetypes = {
    'resource/source-python/translations/gungame': [
        '_server.ini',
    ],
}

_info_path = 'addons/source-python/plugins/gungame/plugins/custom/'

_version_updates = {
    1: 'MAJOR',
    2: 'MINOR',
    3: 'PATCH',
    4: 'None',
}


# =============================================================================
# >> MAIN FUNCTION
# =============================================================================
def create_release(plugin_name=None):
    """Verify the plugin name and create the current release."""
    # Was no plugin name provided?
    if plugin_name not in plugin_list:
        print(
            'Invalid plugin name "{plugin_name}"'.format(
                plugin_name=plugin_name,
            )
        )
        return

    # Get the plugin's base path
    plugin_path = START_DIR / plugin_name

    plugin_path.chdir()
    output = Popen(
        'git ls-tree --full-tree -r HEAD'.split(),
        stdout=PIPE,
    ).communicate()[0]
    START_DIR.chdir()
    repo_files = [
        '{sep}{path}'.format(
            sep=sep,
            path=str(x).split('\\t')[1].replace('/', sep)[:~0],
        ) for x in output.splitlines()
    ]

    # Does the plugin not exist?
    if not plugin_path.isdir():
        print(
            'Plugin "{plugin_name}" not found.'.format(plugin_name=plugin_name)
        )
        return

    # Get the plugin's current version
    info_file = plugin_path.joinpath(
        'addons', 'source-python', 'plugins', 'gungame', 'plugins', 'custom',
        plugin_name, 'info.ini'
    )
    config_obj = ConfigObj(info_file)
    version = config_obj['version']

    # Was no version information found?
    if version is None:
        print('No version found.')
        return

    # Get the directory to save the release in
    save_path = RELEASE_DIR / plugin_name

    # Create the directory if it doesn't exist
    if not save_path.isdir():
        save_path.makedirs()

    # Get the zip file location
    zip_path = save_path / '{plugin_name} - v{version}.zip'.format(
        plugin_name=plugin_name,
        version=version,
    )

    # Does the release already exist?
    if zip_path.isfile():
        print('Release already exists for current version.')
        return

    # Create the zip file
    with ZipFile(zip_path, 'w', ZIP_DEFLATED) as zip_file:

        # Loop through all allowed directories
        for allowed_path in allowed_filetypes:

            # Get the full path to the directory
            check_path = plugin_path.joinpath(*allowed_path.split('/'))

            # Does the directory exist?
            if not check_path.isdir():
                continue

            # Loop through all files within the directory
            for full_file_path in _find_files(
                check_path.walkfiles(),
                allowed_path,
                allowed_filetypes,
            ):

                relative_file_path = full_file_path.replace(plugin_path, '')
                if relative_file_path in repo_files:

                    # Add the file to the zip
                    _add_file(
                        zip_file, full_file_path, relative_file_path,
                        plugin_path,
                    )

        # Loop through all other allowed directories
        for allowed_path in other_filetypes:

            # Get the full path to the directory
            check_path = plugin_path.joinpath(*allowed_path.split('/'))

            # Does the directory exist?
            if not check_path.isdir():
                continue

            # Loop through all files in the directory
            for full_file_path in _find_files(
                check_path.walkfiles(), allowed_path, other_filetypes
            ):

                relative_file_path = full_file_path.replace(plugin_path, '')
                if relative_file_path in repo_files:

                    # Add the file to the zip
                    _add_file(
                        zip_file, full_file_path, relative_file_path,
                        plugin_path,
                    )

    # Print a message that everything was successful
    print(
        'Successfully created {plugin_name} version {version} release:'.format(
            plugin_name=plugin_name,
            version=version,
        )
    )
    print('\t"{zip_path}"\n\n'.format(zip_path=zip_path))


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def _validate_diff(plugin_name):
    """Validate that the plugin does not have outstanding changes."""
    plugin_repo = START_DIR / plugin_name
    repo = Repo(plugin_repo)
    if str(repo.active_branch) != 'master':
        print(f'Not on "master" branch. On branch "{repo.active_branch}"')
        return False
    if bool(repo.index.diff(None)):
        print('There are uncommitted changes')
        return False
    return True


def _get_version_update_type(previous=None):
    """"""
    clear_screen()
    message = ''
    if previous is not None:
        message += f'Invalid value given "{previous}"\n\n'

    message += 'Which type of version update should this be?\n\n'
    for number, choice in sorted(_version_updates.items()):
        message += f'\t({number}) {choice}\n'

    value = input(message + '\n').strip()
    if not value.isdigit():
        return _get_version_update_type(value)

    value = int(value)
    if value not in _version_updates:
        return _get_version_update_type(value)

    return value


def _update_version(plugin_name):
    """"""
    plugin_repo = START_DIR / plugin_name
    info_file = plugin_repo / _info_path / plugin_name / 'info.ini'
    if not info_file.isfile():
        print('No info.ini file found')
        return False

    info = ConfigObj(info_file)
    version = info.get('version')
    if version is None:
        print('"version" not found in info.ini')
        return False

    try:
        version = [int(x) for x in version.split('.')]
    except ValueError:
        print(f'Invalid "version" in info.ini: "{version}"')
        return False

    if len(version) != 3:
        print(f'Invalid "version" in info.ini: "{version}"')
        return False

    update_type = _get_version_update_type()
    if update_type != 4:
        _commit_new_version(plugin_repo, info, version, update_type)

    return True


def _commit_new_version(plugin_repo, info, version, update_type):
    """"""
    repo = Repo(plugin_repo)
    version[update_type - 1] += 1
    version[update_type:] = [0] * (3 - update_type)

    version = info['version'] = '.'.join(map(str, version))
    info.write()
    repo.index.add([info.filename.replace(plugin_repo, '')[1:]])
    repo.index.commit(
        f'{_version_updates[update_type]} version update ({version})'
    )
    repo.remotes.origin.push()


def _find_files(generator, allowed_path, allowed_dictionary):
    """Yield files that should be added to the zip."""
    # Suppress FileNotFoundError in case the
    #    plugin specific directory does not exist.
    with suppress(FileNotFoundError):

        # Loop through the files from the given generator
        for file in generator:

            # Is the current file not allowed?
            if not file.ext[1:] in allowed_dictionary[allowed_path]:
                continue

            # Does the given directory have exceptions?
            if allowed_path in exception_filetypes:

                # Loop through the directory's exceptions
                for exception in exception_filetypes[allowed_path]:

                    # Is this file not allowed?
                    if exception in file.name:
                        break

                # Is the file not an exception?
                else:
                    yield file

            # Is the file allowed?
            else:
                yield file


def _add_file(zip_file, full_file_path, relative_file_path, plugin_path):
    """Add the given file and all parent directories to the zip."""
    # Write the file to the zip
    zip_file.write(full_file_path, relative_file_path)

    # Get the file's parent directory
    parent = full_file_path.parent

    # Get all parent directories to add to the zip
    while plugin_path != parent:

        # Is the current directory not yet included in the zip?
        current = parent.replace(plugin_path, '')[1:].replace('\\', '/') + '/'
        if current not in zip_file.namelist():

            # Add the parent directory to the zip
            zip_file.write(parent, current)

        # Get the parent's parent
        parent = parent.parent


# =============================================================================
# >> CALL MAIN FUNCTION
# =============================================================================
if __name__ == '__main__':

    # Get the plugin to check
    _plugin_name = get_plugin('release', False)

    # Was a valid plugin chosen?
    if _plugin_name is not None:

        # Validate that there are no outstanding changes
        if _validate_diff(_plugin_name):

            # Update the version
            if _update_version(_plugin_name):

                # Create a release for the chosen plugin
                create_release(_plugin_name)
