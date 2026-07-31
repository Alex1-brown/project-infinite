"""High-level Planet Engine API for integration with the rest of the project.

This module provides a small wrapper around the underlying model/terrain/resources modules.
It is intentionally simple in this first iteration and will be extended in future commits.
"""
from typing import List
from .model import Planet
from .terrain import Tile, generate_terrain
from .resources import ResourceNode, spawn_resources


class PlanetEngine:
    def __init__(self) -> None:
        self.planets = {}

    def create_planet(self, name: str, seed: int) -> Planet:
        planet = Planet(name=name, seed=seed)
        planet.generate()
        self.planets[name] = planet
        return planet

    def get_terrain(self, name: str, width: int = 16, height: int = 16) -> List[Tile]:
        planet = self.planets.get(name)
        if planet is None:
            raise KeyError(f"Planet {name} not found")
        return generate_terrain(planet.seed, width=width, height=height)

    def get_resources(self, name: str, num_nodes: int = 20):
        planet = self.planets.get(name)
        if planet is None:
            raise KeyError(f"Planet {name} not found")
        return spawn_resources(planet.seed, num_nodes=num_nodes)
