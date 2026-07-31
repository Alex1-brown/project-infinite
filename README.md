# PROJECT INFINITE v2

A deterministic multiplayer space MMO foundation with procedurally generated galaxies, modular ship systems, dynamic economy, NPC AI, faction diplomacy, and large-scale multiplayer architecture.

## 🎮 Features

### ✅ Implemented
- Deterministic galaxy and planet generation
- Data models for stars, systems, and planets
- Modular ship systems (power, heat, damage)
- Dynamic market model
- NPC needs/goals/memory system
- Faction model (7 factions)
- Domain event engine
- Simulation clock
- Persistent world state
- Testable deterministic generation

### 🚧 In Development
- **Planet Engine** — Terrain, biomes, resources, climate simulation
- **Ship/Flight System** — Orbital mechanics, FTL travel, damage propagation
- **Mining & Production** — Resource extraction, refining, manufacturing
- **NPC AI** — Advanced goals, navigation, trading, combat
- **Factions/Diplomacy** — Wars, alliances, territory control
- **Stations & Colonies** — Building, management, upgrades
- **Research Tree** — Technology progression
- **Missions & Events** — Dynamic content generation
- **LOD Simulation** — Distance-based simulation scaling
- **Multiplayer** — Server architecture, interest management, replication

## 📦 Project Structure

```
project-infinite/
├── core/
│   ├── domain.py          # Event bus, entity system
│   ├── rng.py             # Deterministic RNG
│   └── simulation.py      # Simulation clock
├── galaxy/
│   ├── generator.py       # Galaxy generation
│   ├── model.py           # Star, system, planet models
│   └── resources.py       # Resource distribution
├── planet/
│   ├── engine.py          # Planet terrain & climate
│   ├── biomes.py          # Biome definitions
│   └── resources.py       # Resource placement
├── ship/
│   ├── model.py           # Ship structure
│   ├── systems.py         # Power, heat, damage
│   └── flight.py          # Orbital mechanics
├── economy/
│   ├── market.py          # Market dynamics
│   ├── production.py      # Manufacturing
│   └── logistics.py       # Trade routes
├── ai/
│   ├── npc.py             # NPC agent
│   ├── goals.py           # Goal system
│   └── navigation.py      # Pathfinding
├── factions/
│   ├── model.py           # Faction data
│   ├── diplomacy.py       # Relationships
│   └── warfare.py         # Combat & wars
├── world/
│   ├── state.py           # World state
│   ├── persistence.py     # Save/load
│   └── events.py          # Event system
├── tests/
│   ├── test_generation.py
│   ├── test_planet.py
│   ├── test_ship.py
│   └── test_ai.py
└── main.py                # Entry point
```

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/Alex1-brown/project-infinite.git
cd project-infinite

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Start the simulation
python main.py
```

## 📐 Architecture Principles

1. **Server Authoritative** — All persistent state validated on server
2. **Deterministic** — Same seed = same content (reproducible)
3. **Lazy Evaluation** — Generate content on-demand, don't persist
4. **LOD Simulation** — Far objects simulated less frequently
5. **Data-Driven** — Config-based gameplay parameters
6. **Event-Based** — Systems communicate via events, not direct calls
7. **Modular** — Each system independent and testable

## 🌍 Factions

- **Federation** — Law & order, bureaucracy
- **Empire** — Military dominance, expansion
- **Corporations** — Profit, monopolies, technology
- **Pirates** — Chaos, theft, opportunism
- **Scientists** — Knowledge, research, discovery
- **Colonists** — Settlement, sustainability, growth
- **Independents** — Freedom, self-reliance, trade

## 📊 Development Roadmap

### Phase 1: Foundation ✅
- [x] RNG and determinism
- [x] Entity system
- [x] Event bus
- [x] Data models

### Phase 2: Galaxy & Planet 🚧
- [ ] Planet Engine (terrain, biomes, resources)
- [ ] Climate simulation
- [ ] Resource distribution
- [ ] LOD streaming

### Phase 3: Ships & Flight 🚧
- [ ] Modular systems
- [ ] Orbital mechanics
- [ ] Flight model
- [ ] Damage system

### Phase 4: Economy 🚧
- [ ] Mining & extraction
- [ ] Production chains
- [ ] Markets & pricing
- [ ] Logistics

### Phase 5: AI & Factions 🚧
- [ ] NPC goals & needs
- [ ] Navigation & combat AI
- [ ] Faction strategies
- [ ] Diplomacy & wars

### Phase 6: Building 🚧
- [ ] Stations
- [ ] Colonies
- [ ] Research trees
- [ ] Missions

### Phase 7: Persistence & Multiplayer 🚧
- [ ] World state persistence
- [ ] Interest management
- [ ] Replication
- [ ] Zone handoff

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Database:** SQLite (expandable to PostgreSQL)
- **Networking:** WebSocket (planned)
- **Testing:** pytest
- **Typing:** Full type hints

## 📝 License

Copyright (c) 2026 Alex1-brown. All rights reserved.

## 👤 Authors

- **Alex1-brown** — Project creator & lead developer

---

**Status:** 🚀 Active Development

**Last Updated:** 2026-07-31
