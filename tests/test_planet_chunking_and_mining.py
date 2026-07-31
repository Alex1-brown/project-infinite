"""Tests for chunking (LOD) and mining APIs."""
from planet.api import PlanetEngine
from planet.chunk import ChunkManager
from planet.mining import MiningAPI


def test_chunk_determinism():
    engine = PlanetEngine()
    engine.create_planet("LODTest", seed=424242)

    cm = ChunkManager(max_cache_size=4, chunk_size=8)
    c1 = cm.get_chunk(engine.planets["LODTest"].seed, 0, 0)
    c2 = cm.get_chunk(engine.planets["LODTest"].seed, 0, 0)
    assert c1 is c2  # from cache, same object
    # regenerate via a new manager to test determinism
    cm2 = ChunkManager(chunk_size=8)
    c1b = cm2.get_chunk(engine.planets["LODTest"].seed, 0, 0)
    assert [(t.x, t.y, round(t.elevation, 5), t.biome) for t in c1.tiles] == [(t.x, t.y, round(t.elevation, 5), t.biome) for t in c1b.tiles]


def test_chunk_different_coords():
    engine = PlanetEngine()
    engine.create_planet("LODTest2", seed=424243)

    cm = ChunkManager(chunk_size=4)
    a = cm.get_chunk(engine.planets["LODTest2"].seed, 0, 0)
    b = cm.get_chunk(engine.planets["LODTest2"].seed, 1, 0)
    # cursory check: tiles should differ across chunk coordinates
    assert any(t1.biome != t2.biome or round(t1.elevation, 5) != round(t2.elevation, 5) for t1, t2 in zip(a.tiles, b.tiles))


def test_mining_extracts_resources():
    engine = PlanetEngine()
    p = engine.create_planet("MineTest", seed=2026)
    miner = MiningAPI(engine)

    # Ensure there is at least some iron
    before = p.resources.get("iron", 0)
    extracted = miner.extract_by_type("MineTest", "iron", 50)
    assert extracted <= 50
    assert p.resources.get("iron", 0) == before - extracted
