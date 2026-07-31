"""Deterministic galaxy generation."""

from typing import List
from core.rng import DeterministicRNG
from .model import (
    StarType, StarSystem, Planet, Galaxy,
    Atmosphere, Biome, Atmosphere as AtmosphereEnum
)


class GalaxyGenerator:
    """Generates deterministic galaxies from seeds."""
    
    # Resource types and their distribution
    RESOURCES = {
        "water": 0.3,
        "metal": 0.5,
        "rare_earth": 0.2,
        "radioactive": 0.1,
        "crystal": 0.15,
        "gas": 0.4,
        "hydrocarbons": 0.25,
    }
    
    # Atmosphere types by probability
    ATMOSPHERES = [
        AtmosphereEnum.NONE,
        AtmosphereEnum.THIN_CO2,
        AtmosphereEnum.THIN_N2,
        AtmosphereEnum.EARTH_LIKE,
        AtmosphereEnum.VENUS_LIKE,
        AtmosphereEnum.TOXIC,
    ]
    
    def __init__(self, seed: int = 1):
        self.seed = seed
        self.rng = DeterministicRNG(seed)
    
    def generate(self, num_systems: int = 64) -> Galaxy:
        """Generate a galaxy with specified number of systems.
        
        Args:
            num_systems: Number of star systems to generate
        
        Returns:
            Generated Galaxy object
        """
        galaxy = Galaxy(seed=self.seed)
        
        for i in range(num_systems):
            system = self._generate_system(i, num_systems)
            galaxy.systems.append(system)
        
        return galaxy
    
    def _generate_system(self, index: int, total: int) -> StarSystem:
        """Generate a single star system."""
        # Deterministic RNG for this system
        system_rng = DeterministicRNG(f"{self.seed}:system:{index}")
        
        # Generate star
        star_types = list(StarType)
        star_type = system_rng.choice(star_types)
        
        system_id = f"S{index}"
        system_name = f"Kepler-{index}"
        
        system = StarSystem(
            id=system_id,
            name=system_name,
            star_type=star_type,
        )
        
        # Generate planets
        num_planets = system_rng.int(1, 12)
        for j in range(num_planets):
            planet = self._generate_planet(index, j, star_type, system_rng)
            system.planets.append(planet)
        
        # Calculate strategic value
        system.strategic_value = system.calculate_strategic_value()
        
        return system
    
    def _generate_planet(self, system_idx: int, planet_idx: int, star_type: StarType, rng: DeterministicRNG) -> Planet:
        """Generate a single planet."""
        planet_rng = DeterministicRNG(f"{self.seed}:system:{system_idx}:planet:{planet_idx}")
        
        # Orbital properties
        orbital_distance = planet_rng.float(0.1, 50.0)
        orbital_period = (orbital_distance ** 1.5) * 365  # Kepler's third law
        
        # Physical properties
        mass = planet_rng.float(0.05, 8.0)
        radius = planet_rng.float(0.2, 3.5)
        gravity = (mass / (radius ** 2))  # Simplified gravity calculation
        rotation_period = planet_rng.float(6, 48)
        axial_tilt = planet_rng.float(0, 90)
        
        # Thermal properties (simplified)
        base_temp = 278 - (5 * (orbital_distance - 1))  # Decrease with distance
        temperature = planet_rng.float(base_temp - 20, base_temp + 20)
        min_temp = temperature - planet_rng.float(20, 50)
        max_temp = temperature + planet_rng.float(20, 50)
        
        # Atmosphere
        if planet_rng.chance(0.7):  # 70% chance of atmosphere
            atmosphere = planet_rng.choice(self.ATMOSPHERES)
            atmospheric_density = planet_rng.float(0.1, 2.0) if atmosphere != AtmosphereEnum.NONE else 0.0
        else:
            atmosphere = AtmosphereEnum.NONE
            atmospheric_density = 0.0
        
        # Water coverage
        water_coverage = planet_rng.float(0, 1.0) if atmosphere != AtmosphereEnum.NONE else 0.0
        
        # Biomes
        biomes = []
        if atmosphere != AtmosphereEnum.NONE:
            num_biomes = planet_rng.int(1, 6)
            biome_types = list(Biome)
            biomes = planet_rng.sample(biome_types, min(num_biomes, len(biome_types)))
        
        # Resources
        resources = {}
        resource_richness = planet_rng.float(0.05, 1.0)
        for resource_type, base_abundance in self.RESOURCES.items():
            if planet_rng.chance(base_abundance):
                resources[resource_type] = planet_rng.float(0.1, 1.0) * resource_richness
        
        # Life (very rare, needs good conditions)
        hz_inner = star_type.habitable_zone_inner()
        hz_outer = star_type.habitable_zone_outer()
        in_habitable_zone = hz_inner <= orbital_distance <= hz_outer
        has_life = in_habitable_zone and atmosphere == AtmosphereEnum.EARTH_LIKE and planet_rng.chance(0.1)
        
        planet = Planet(
            id=f"S{system_idx}P{planet_idx}",
            name=f"Kepler-{system_idx}b" if planet_idx == 0 else f"Kepler-{system_idx}{chr(98 + planet_idx)}",
            body_type="planet",
            orbital_distance=orbital_distance,
            orbital_period=orbital_period,
            orbital_eccentricity=planet_rng.float(0, 0.3),
            mass=mass,
            radius=radius,
            gravity=gravity,
            rotation_period=rotation_period,
            axial_tilt=axial_tilt,
            atmosphere=atmosphere,
            atmospheric_density=atmospheric_density,
            temperature=temperature,
            min_temperature=min_temp,
            max_temperature=max_temp,
            albedo=planet_rng.float(0.1, 0.6),
            water_coverage=water_coverage,
            biomes=biomes,
            resources=resources,
            resource_richness=resource_richness,
            has_life=has_life,
            biodiversity=planet_rng.float(0, 1) if has_life else 0.0,
        )
        
        planet.habitability = planet.get_habitability_score()
        
        return planet
