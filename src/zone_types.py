from enum import Enum

class Zones(Enum):
    """
    • normal: 1 turn (default)
    • restricted: 2 turns
    • priority: 1 turn (but should be preferred in pathfinding algorithms)
    • blocked: Inaccessible — cannot be entered
    """
    normal = 1
    restricted = 2
    priority = 1
    blocked = 0
