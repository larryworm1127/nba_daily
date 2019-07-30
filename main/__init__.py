"""Main package.

@date: 06/02/2019
@author: Larry Shi
"""
from datetime import datetime

from jinja2 import Template

__author__ = "Larry Shi"

# ==============================================================================
# Constants
# ==============================================================================
PLAYER_PHOTO_LINK = Template(
    "https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{{ player_id }}.png"
)


def get_closest_game_date(curr_date: datetime.date) -> datetime.date:
    """Return the closest date with games.

    === Attributes ===
    curr_date:
        the current date to search from.
    """

