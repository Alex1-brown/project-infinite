from dataclasses import dataclass
from typing import Optional


@dataclass
class MineableSlot:
    resource_type: str
    x: int
    y: int
    quantity: int


class MiningAPI:
    """Very small mining interface for the initial implementation.

    At this stage mining is abstracted to operate on the planet.summary().resources map.
    In later iterations this will operate on spatial ResourceNode objects tied to chunks.
    """

    def __init__(self, engine):
        self.engine = engine

    def extract_by_type(self, planet_name: str, resource_type: str, amount: int) -> int:
        planet = self.engine.planets.get(planet_name)
        if planet is None:
            raise KeyError(f"Planet {planet_name} not found")
        available = planet.resources.get(resource_type, 0)
        to_extract = min(available, amount)
        if to_extract <= 0:
            return 0
        planet.resources[resource_type] = available - to_extract
        return to_extract
