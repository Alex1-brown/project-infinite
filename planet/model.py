from dataclasses import dataclass, field
from typing import List, Dict, Any, ClassVar
import random


class Biome(str):
    """Simple biome identifiers."""
    PLAINS = "plains"
    MOUNTAINS = "mountains"
    DESERT = "desert"
    OCEAN = "ocean"
    TUNDRA = "tundra"
    VOLCANIC = "volcanic"


@dataclass
class Planet:
    name: str
    seed: int
    radius: float = 6371.0
    layers: Dict[str, Any] = field(default_factory=dict)
    biomes: List[str] = field(default_factory=list)
    resources: Dict[str, int] = field(default_factory=dict)
    generated: bool = False

    DEFAULT_LAYERS: ClassVar[List[str]] = ["core", "mantle", "crust", "surface", "atmosphere"]

    def generate(self, num_biomes: int = 8, resource_nodes: int = 16, rng_hint: int = 0) -> None:
        """Populate planet with deterministic layers, biomes and resources based on seed.

        This generator is intentionally lightweight but deterministic: identical seed
        and parameters produce the same result.
        """
        rng = random.Random((self.seed << 32) ^ rng_hint)

        # Simple layer generation: composition percentages
        self.layers = {}
        for layer in self.DEFAULT_LAYERS:
            # keep core/mantle heavier, atmosphere light
            base = 0.0
            if layer == "core":
                base = rng.uniform(0.2, 0.35)
            elif layer == "mantle":
                base = rng.uniform(0.3, 0.45)
            elif layer == "crust":
                base = rng.uniform(0.05, 0.15)
            elif layer == "surface":
                base = rng.uniform(0.01, 0.03)
            else:
                base = rng.uniform(0.001, 0.01)
            self.layers[layer] = round(base, 5)

        # Biome generation: uses a seeded RNG to choose a sequence of biomes
        possible_biomes = [Biome.PLAINS, Biome.MOUNTAINS, Biome.DESERT, Biome.OCEAN, Biome.TUNDRA, Biome.VOLCANIC]
        self.biomes = [rng.choice(possible_biomes) for _ in range(num_biomes)]

        # Resource distribution
        self.resources = {}
        for i in range(resource_nodes):
            resource_type = rng.choice(["iron", "copper", "water", "rare_earth", "silicon"])
            amount = rng.randint(100, 10000)
            self.resources[resource_type] = self.resources.get(resource_type, 0) + amount

        self.generated = True

    def summary(self) -> dict:
        return {
            "name": self.name,
            "seed": self.seed,
            "radius": self.radius,
            "layers": self.layers,
            "biomes": self.biomes,
            "resources": self.resources,
            "generated": self.generated,
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "seed": self.seed,
            "radius": self.radius,
            "layers": self.layers,
            "biomes": self.biomes,
            "resources": self.resources,
            "generated": self.generated,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Planet":
        p = cls(name=data["name"], seed=int(data["seed"]), radius=float(data.get("radius", 6371.0)))
        p.layers = data.get("layers", {})
        p.biomes = data.get("biomes", [])
        p.resources = data.get("resources", {})
        p.generated = bool(data.get("generated", False))
        return p
