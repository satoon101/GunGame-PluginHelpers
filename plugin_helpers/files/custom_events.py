# ../gungame/plugins/custom/gg_{plugin_name}/custom_events.py

"""Events used by gg_{plugin_name}."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from events.custom import CustomEvent
from events.variable import ShortVariable

# GunGame
from gungame.core.events.resource import GGResourceFile

# Plugin
from .info import info


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'GG_{plugin_class}',
)


# =============================================================================
# >> CLASSES
# =============================================================================
class {plugin_class}(CustomEvent):

    variable = ShortVariable('Description of the variable')


# =============================================================================
# >> RESOURCE FILE
# =============================================================================
GGResourceFile(info.name, GG_{plugin_class})
