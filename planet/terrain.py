"""Simple terrain generation utilities.

This is intentionally lightweight for the initial skeleton: it produces a deterministic grid
of Tile objects using the planet seed.
"""
from dataclasses import dataclass
from typing import List, Tuple
import random


@dataclass
class Tile:
    x: int
    y: int
    elevation: float
    biome: str


def generate_terrain(seed: int, width: int = 16, height: int = 16) -> List[Tile]:
    rng = random.Random(seed)
    tiles: List[Tile] = []
    for y in range(height):
        for x in range(width):
            elevation = rng.random() * 1.0  # 0.0 .. 1.0
            # Simple biome selection based on elevation for demo
            if elevation < 0.2:
                biome = "ocean"
            elif elevation < 0.4:
                biome = "plains"
            elif elevation < 0.7:
                biome = "mountains"
            else:
                biome = "tundra"
            tiles.append(Tile(x=x, y=y, elevation=elevation, biome=biome))
    return tiles
