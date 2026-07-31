"""Planet engine skeleton for Project Infinite

Includes basic deterministic planet model, simple terrain and resource spawning,
and a small API wrapper for integration and tests.
"""
from .model import Planet, Biome
from .terrain import Tile, generate_terrain
from .resources import ResourceNode, spawn_resources

__all__ = ["Planet", "Biome", "Tile", "generate_terrain", "ResourceNode", "spawn_resources"]
