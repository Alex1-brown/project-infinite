"""Tests for galaxy generation."""

import pytest
from galaxy.generator import GalaxyGenerator
from galaxy.model import StarType, StarSystem, Planet


def test_galaxy_generation_deterministic():
    """Same seed produces identical galaxies."""
    gen1 = GalaxyGenerator(seed=42)
    gen2 = GalaxyGenerator(seed=42)
    
    galaxy1 = gen1.generate(num_systems=8)
    galaxy2 = gen2.generate(num_systems=8)
    
    assert len(galaxy1.systems) == len(galaxy2.systems)
    
    for s1, s2 in zip(galaxy1.systems, galaxy2.systems):
        assert s1.name == s2.name
        assert s1.star_type == s2.star_type
        assert len(s1.planets) == len(s2.planets)
        
        for p1, p2 in zip(s1.planets, s2.planets):
            assert p1.name == p2.name
            assert p1.mass == p2.mass
            assert p1.temperature == p2.temperature


def test_galaxy_generation_different_seeds():
    """Different seeds produce different galaxies."""
    gen1 = GalaxyGenerator(seed=42)
    gen2 = GalaxyGenerator(seed=43)
    
    galaxy1 = gen1.generate(num_systems=8)
    galaxy2 = gen2.generate(num_systems=8)
    
    # At least some systems should differ
    different = False
    for s1, s2 in zip(galaxy1.systems, galaxy2.systems):
        if s1.star_type != s2.star_type:
            different = True
            break
    
    assert different


def test_star_type_properties():
    """Star types have correct physical properties."""
    assert StarType.O.temperature() > StarType.M.temperature()
    assert StarType.O.luminosity() > StarType.M.luminosity()
    assert StarType.O.mass() > StarType.M.mass()
    
    # Habitable zones increase with luminosity
    assert StarType.O.habitable_zone_inner() > StarType.M.habitable_zone_inner()


def test_planet_habitability():
    """Planets calculate habitability correctly."""
    # Perfect planet
    perfect = Planet(
        id="test1",
        name="Perfect",
        atmosphere=Atmosphere.EARTH_LIKE,
        temperature=288,
        water_coverage=0.7,
        gravity=1.0,
        has_life=True,
    )
    
    assert perfect.get_habitability_score() > 0.8
    
    # Barren planet
    barren = Planet(
        id="test2",
        name="Barren",
        atmosphere=Atmosphere.NONE,
        temperature=700,
        water_coverage=0.0,
        gravity=2.0,
    )
    
    assert barren.get_habitability_score() < 0.2


def test_galaxy_system_count():
    """Galaxy has correct number of systems."""
    for num in [8, 16, 32, 64, 128]:
        gen = GalaxyGenerator(seed=1)
        galaxy = gen.generate(num_systems=num)
        assert len(galaxy.systems) == num


def test_system_has_planets():
    """All systems have at least one planet."""
    gen = GalaxyGenerator(seed=42)
    galaxy = gen.generate(num_systems=16)
    
    for system in galaxy.systems:
        assert len(system.planets) >= 1
        assert len(system.planets) <= 12


def test_planet_orbital_mechanics():
    """Planets follow Kepler's laws."""
    gen = GalaxyGenerator(seed=42)
    galaxy = gen.generate(num_systems=8)
    
    for system in galaxy.systems:
        for planet in system.planets:
            # Kepler's third law: P^2 = a^3 (in AU and Earth years)
            calculated_period = (planet.orbital_distance ** 1.5) * 365
            assert abs(planet.orbital_period - calculated_period) < 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


from galaxy.model import Atmosphere
