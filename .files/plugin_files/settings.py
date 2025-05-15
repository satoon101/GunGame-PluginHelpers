# ../gungame/plugins/custom/gg_{plugin_name}/settings.py

"""Player settings for gg_{plugin_name}."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.settings import gungame_player_settings


# =============================================================================
# >> SETTINGS
# =============================================================================
{plugin_name}_settings = gungame_player_settings.add_section(
    '{plugin_name}_settings'
)
