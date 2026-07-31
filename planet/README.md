# Planet Engine

This directory contains the initial skeleton for the Planet Engine: a deterministic
planet model, simple terrain generation and resource spawning utilities, and a
small API wrapper used by the rest of Project Infinite.

Files:
- model.py — Planet dataclass and deterministic generator
- terrain.py — simple grid-based terrain tiles
- resources.py — deterministic resource node spawning
- api.py — PlanetEngine facade
- tests/test_planet_engine.py — basic pytest tests

Next steps (planned):
- Integrate LOD tile streaming and chunking
- Add richer biome maps and climate simulation
- Connect mining/harvesting interfaces
- Add serialization to world_store and save/load support
