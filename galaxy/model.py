"""Galaxy data models: stars, systems, planets."""

from dataclasses import dataclass, field
from typing import List, Optional, Set
from enum import Enum


class StarType(Enum):
    """Stellar classification (Hertzsprung-Russell)."""
    O = "O"  # Blue, massive, hot
    B = "B"  # Blue-white
    A = "A"  # White
    F = "F"  # Yellow-white
    G = "G"  # Yellow (Sun-like)
    K = "K"  # Orange
    M = "M"  # Red, small, cool
    
    def luminosity(self) -> float:
        """Base luminosity relative to Sun."""
        return {
            StarType.O: 1e5,
            StarType.B: 1e3,
            StarType.A: 10,
            StarType.F: 5,
            StarType.G: 1,
            StarType.K: 0.1,
            StarType.M: 0.001,
        }[self]
    
    def temperature(self) -> int:
        """Surface temperature in Kelvin."""
        return {
            StarType.O: 30000,
            StarType.B: 10000,
            StarType.A: 7500,
            StarType.F: 6000,
            StarType.G: 5778,
            StarType.K: 3700,
            StarType.M: 2800,
        }[self]
    
    def mass(self) -> float:
        """Mass relative to Sun."""
        return {
            StarType.O: 40,
            StarType.B: 7,
            StarType.A: 1.4,
            StarType.F: 1.04,
            StarType.G: 1.0,
            StarType.K: 0.7,
            StarType.M: 0.4,
        }[self]
    
    def habitable_zone_inner(self) -> float:
        """Inner habitable zone distance in AU."""
        l = self.luminosity()
        return (l / 1.1) ** 0.5
    
    def habitable_zone_outer(self) -> float:
        """Outer habitable zone distance in AU."""
        l = self.luminosity()
        return (l / 0.53) ** 0.5


class Atmosphere(Enum):
    """Planet atmosphere types."""
    NONE = "none"
    THIN_CO2 = "thin_co2"
    THIN_N2 = "thin_n2"
    EARTH_LIKE = "earth_like"
    VENUS_LIKE = "venus_like"
    TOXIC = "toxic"
    
    def breathable(self) -> bool:
        return self == Atmosphere.EARTH_LIKE


class Biome(Enum):
    """Planet biome types."""
    BARREN = "barren"
    DESERT = "desert"
    SAVANNA = "savanna"
    GRASSLAND = "grassland"
    FOREST = "forest"
    TUNDRA = "tundra"
    OCEAN = "ocean"
    SWAMP = "swamp"
    MOUNTAINS = "mountains"
    CANYON = "canyon"
    CAVE = "cave"
    LAVA = "lava"


@dataclass
class Planet:
    """Planetary body with physical properties."""
    id: str
    name: str
    body_type: str = "planet"  # planet, moon, asteroid, comet
    
    # Orbital properties
    orbital_distance: float = 1.0  # AU
    orbital_period: float = 365.0  # Earth days
    orbital_eccentricity: float = 0.0
    
    # Physical properties
    mass: float = 1.0  # Earth masses
    radius: float = 1.0  # Earth radii
    gravity: float = 1.0  # g
    rotation_period: float = 24.0  # Hours
    axial_tilt: float = 23.5  # Degrees
    
    # Atmospheric properties
    atmosphere: Atmosphere = Atmosphere.NONE
    atmospheric_density: float = 0.0  # Bar
    atmospheric_composition: dict = field(default_factory=dict)  # Gas -> percentage
    
    # Thermal properties
    temperature: float = 288.0  # Kelvin
    min_temperature: float = 250.0
    max_temperature: float = 320.0
    albedo: float = 0.3  # Reflectivity
    
    # Surface composition
    water_coverage: float = 0.0  # 0-1 (fraction of surface)
    biomes: List[Biome] = field(default_factory=list)
    
    # Resources
    resources: dict = field(default_factory=dict)  # Resource -> abundance (0-1)
    resource_richness: float = 0.5  # Overall richness multiplier
    
    # Life
    has_life: bool = False
    biodiversity: float = 0.0  # 0-1
    habitability: float = 0.0  # 0-1 (for players)
    
    def get_habitability_score(self) -> float:
        """Calculate habitability for human colonization."""
        score = 0.0
        
        # Atmosphere bonus
        if self.atmosphere == Atmosphere.EARTH_LIKE:
            score += 0.3
        elif self.atmosphere in (Atmosphere.THIN_N2, Atmosphere.THIN_CO2):
            score += 0.1
        
        # Temperature bonus (optimal: 273-313 K)
        if 273 <= self.temperature <= 313:
            score += 0.3
        elif 250 <= self.temperature <= 323:
            score += 0.15
        
        # Water bonus
        if 0.2 <= self.water_coverage <= 0.8:
            score += 0.2
        
        # Gravity bonus (optimal: 0.8-1.2 g)
        if 0.8 <= self.gravity <= 1.2:
            score += 0.1
        elif 0.5 <= self.gravity <= 1.5:
            score += 0.05
        
        # Life bonus
        if self.has_life:
            score += 0.1
        
        return min(score, 1.0)


@dataclass
class StarSystem:
    """A star and its orbiting bodies."""
    id: str
    name: str
    star_type: StarType
    
    # Planets and moons
    planets: List[Planet] = field(default_factory=list)
    
    # Faction control
    controlling_faction: Optional[str] = None
    contested: bool = False
    
    # Discovery
    discovered: bool = False
    discovered_by: Optional[str] = None
    
    # Economy
    market_goods: dict = field(default_factory=dict)  # Good -> price
    
    # Strategic value
    strategic_value: float = 0.0
    resource_value: float = 0.0
    
    def get_habitable_planets(self) -> List[Planet]:
        """Get planets in habitable zone."""
        hz_inner = self.star_type.habitable_zone_inner()
        hz_outer = self.star_type.habitable_zone_outer()
        return [
            p for p in self.planets
            if hz_inner <= p.orbital_distance <= hz_outer
        ]
    
    def calculate_strategic_value(self) -> float:
        """Calculate system value based on resources and position."""
        value = 0.0
        
        # Resource value
        for planet in self.planets:
            value += planet.resource_richness * 10
        
        # Habitability value
        habitable = self.get_habitable_planets()
        value += len(habitable) * 50
        
        return value


@dataclass
class Galaxy:
    """Collection of star systems."""
    seed: int
    systems: List[StarSystem] = field(default_factory=list)
    
    def get_system(self, system_id: str) -> Optional[StarSystem]:
        """Get system by ID."""
        for system in self.systems:
            if system.id == system_id:
                return system
        return None
    
    def get_systems_by_faction(self, faction: str) -> List[StarSystem]:
        """Get all systems controlled by a faction."""
        return [s for s in self.systems if s.controlling_faction == faction]
    
    def get_discovered_systems(self) -> List[StarSystem]:
        """Get all discovered systems."""
        return [s for s in self.systems if s.discovered]
    
    def calculate_distances(self) -> dict:
        """Calculate distances between systems (simplified: use system count)."""
        # In a real implementation, would use 3D positions
        return {}
