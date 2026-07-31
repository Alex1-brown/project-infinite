# Planet Engine

This directory contains the initial skeleton for the Planet Engine: a deterministic
planet model, simple terrain generation and resource spawning utilities, and a
small API wrapper used by the rest of Project Infinite.

Files:
- model.py — Planet dataclass and deterministic generate()
- terrain.py — simple grid-based terrain tiles
- resources.py — deterministic resource node spawning
- api.py — PlanetEngine facade
- storage.py — simple persistence bridge (world_store fallback)
- chunk.py — LOD chunk manager and deterministic chunk generation
- mining.py — early mining API (operates on planet resources map)
- tests/test_planet_engine.py — basic pytest tests
- tests/test_planet_storage.py — tests for save/load
- tests/test_planet_chunking_and_mining.py — tests for chunking and mining

Next steps (planned):
- Improve biome maps and climate simulation
- Spatial ResourceNode persistence tied to chunks
- Asynchronous storage and streaming for large worlds
- Server-side LOD simulation for multiplayer
