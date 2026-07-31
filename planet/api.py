from typing import List, Optional
from .model import Planet
from .terrain import Tile, generate_terrain
from .resources import ResourceNode, spawn_resources
from . import storage


class PlanetEngine:
    def __init__(self) -> None:
        self.planets = {}

    def create_planet(self, name: str, seed: int, auto_generate: bool = True) -> Planet:
        planet = Planet(name=name, seed=seed)
        if auto_generate:
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

    def save_planet(self, name: str, dest: Optional[str] = None) -> None:
        """Serialize and persist a planet. If a world_store is available it will be used,
        otherwise a local file under .planets/ will be written. The optional `dest`
        argument can override the directory or store key used by the storage backend.
        """
        planet = self.planets.get(name)
        if planet is None:
            raise KeyError(f"Planet {name} not found")
        data = planet.to_dict()
        storage.save_planet(data, name, dest=dest)

    def load_planet(self, name: str, src: Optional[str] = None) -> Planet:
        """Load a planet from storage into memory and return it."""
        data = storage.load_planet(name, src=src)
        planet = Planet.from_dict(data)
        self.planets[name] = planet
        return planet
