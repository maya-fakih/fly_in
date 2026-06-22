"""Hub file for hub representation."""
from dataclasses import dataclass, field
from typing import List

from hub_type import HubType

from zone_types import Zones


@dataclass
class Hub:
    """Dataclass to represent a hub."""

    name: str
    x: int
    y: int
    zone: Zones
    color: str
    max_drones: int
    hub_type: HubType
    # connections to other hubs (names or identifiers)
    connections: List = field(default_factory=list)
