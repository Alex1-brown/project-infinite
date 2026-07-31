"""Basic tests for the Planet Engine skeleton."""
import pytest
from planet.api import PlanetEngine


def test_create_planet_and_generate():
    engine = PlanetEngine()
    p = engine.create_planet("Test", seed=12345)
    assert p.name == "Test"
    assert isinstance(p.seed, int)
    assert len(p.biomes) > 0
    assert len(p.resources) > 0


def test_deterministic_generation():
    engine = PlanetEngine()
    p1 = engine.create_planet("A", seed=54321)
    p2 = engine.create_planet("B", seed=54321)
    # Two planets with same seed should have same summaries
    assert p1.summary()["biomes"] == p2.summary()["biomes"]
    assert p1.summary()["resources"] == p2.summary()["resources"]
