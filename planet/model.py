from dataclasses import dataclass, field
from typing import List, Dict
import random


class Biome(str):
    """Simple biome identifiers."""
    PLAINS = "plains"
    MOUNTAINS = "mountains"
    DESERT = "desert"
    OCEAN = "ocean"
    TUNDRA = "tundra"


@dataclass
class Planet:
    name: str
    seed: int
    radius: float = 6371.0
    biomes: List[str] = field(default_factory=list)
    resources: Dict[str, int] = field(default_factory=dict)

    def generate(self, num_biomes: int = 5, resource_nodes: int = 10) -> None:
        """Populate planet with deterministic biomes and resources based on seed."""
        rng = random.Random(self.seed)

        possible_biomes = [Biome.PLAINS, Biome.MOUNTAINS, Biome.DESERT, Biome.OCEAN, Biome.TUNDRA]
        self.biomes = [rng.choice(possible_biomes) for _ in range(num_biomes)]

        # Simple deterministic resources map
        self.resources = {}
        for i in range(resource_nodes):
            resource_type = rng.choice(["iron", "copper", "water", "rare_earth"])
            amount = rng.randint(100, 10000)
            self.resources[resource_type] = self.resources.get(resource_type, 0) + amount

    def summary(self) -> dict:
        return {"name": self.name, "seed": self.seed, "biomes": self.biomes, "resources": self.resources}
