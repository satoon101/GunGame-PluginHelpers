# ../gungame/plugins/custom/gg_{{ plugin_name }}/commands.py

"""Command registration for gg_{{ plugin_name }}."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.commands.registration import register_command_callback


# =============================================================================
# >> FUNCTIONS
# =============================================================================
@register_command_callback("{{ plugin_name }}", "{{ plugin_name.title().replace('_', '') }}:Command")
def _{{ plugin_name }}_callback(index):
    pass
