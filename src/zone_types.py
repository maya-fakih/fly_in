"""Defines zone types and traversal costs for pathfinding."""

from enum import Enum

from math import inf

class Zones(Enum):
    """Zone types and traversal costs.

    normal: 1 turn (default)
    restricted: 2 turns
    priority: 1 turn (but should be preferred in pathfinding algorithms)
    blocked: Inaccessible — cannot be entered
    """

    normal = 1
    restricted = 2
    priority = 1
    blocked = inf
