# ../gungame/plugins/custom/gg_{plugin_name}/rules.py

"""Creates the gg_{plugin_name} rules."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.rules.instance import GunGameRules
from gungame.core.rules.strings import rules_translations

# Plugin
from .info import info


# =============================================================================
# >> RULES
# =============================================================================
{plugin_name}_rules = GunGameRules(info.name)
