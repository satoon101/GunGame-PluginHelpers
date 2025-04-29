# ../common/constants.py

"""Provides commonly used constants."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from platform import system

# Site-Package
from configobj import ConfigObj
from path import Path

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Store the platform
PLATFORM = system().lower()

# Store the main directory
START_DIR = Path(__file__).parent.parent.parent.parent

# Store the premade files location
PREMADE_FILES_DIR = START_DIR / "plugin_helpers" / "files"

# Get the configuration
config_obj = ConfigObj(START_DIR / "config.ini")

# Store the author value
AUTHOR = config_obj["AUTHOR"]

# Store the GunGame repository directory
GUNGAME_DIR = Path(config_obj["GUNGAME_DIRECTORY"])

# Get Source.Python's addons directory
GUNGAME_ADDONS_DIR = GUNGAME_DIR.joinpath(
    "addons", "source-python", "gungame", "plugins", "custom",
)

# Store the Release directory
RELEASE_DIR = Path(config_obj["RELEASE_DIRECTORY"])

# Store the Python executable path
PYTHON_EXE = config_obj["PYTHON_EXECUTABLE"]

SEMANTIC_VERSIONING_COUNT = 3

# Get a list of all plugins
plugin_list = [
    x.stem for x in START_DIR.dirs()
    if not x.stem.startswith((".", "_")) and x.stem != "plugin_helpers"
]
