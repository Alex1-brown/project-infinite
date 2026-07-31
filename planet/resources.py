"""Resource spawning helpers for planets.

Produces deterministic resource nodes using the planet seed.
"""
from dataclasses import dataclass
from typing import List
import random


@dataclass
class ResourceNode:
    resource_type: str
    x: int
    y: int
    quantity: int


def spawn_resources(seed: int, num_nodes: int = 20, area_width: int = 64, area_height: int = 64) -> List[ResourceNode]:
    rng = random.Random(seed + 0xC0FFEE)
    nodes: List[ResourceNode] = []
    types = ["iron", "copper", "water", "rare_earth"]
    for _ in range(num_nodes):
        rtype = rng.choice(types)
        x = rng.randrange(0, area_width)
        y = rng.randrange(0, area_height)
        qty = rng.randint(50, 5000)
        nodes.append(ResourceNode(resource_type=rtype, x=x, y=y, quantity=qty))
    return nodes
