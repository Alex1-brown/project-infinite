"""Storage helpers for persisting planets.

This module attempts to use a repository-level `world_store` module if available (so the
engine can integrate with the existing persistence layer). If not available, it falls back
to a simple local file store in `.planets/` relative to the repository root.

The storage API here is intentionally small and synchronous for clarity. In later
iterations we'll add async hooks and integrate with real databases.
"""
import json
import os
from typing import Dict, Any, Optional


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _fallback_path_for(name: str, base_dir: Optional[str] = None) -> str:
    base = base_dir if base_dir is not None else ".planets"
    _ensure_dir(base)
    return os.path.join(base, f"{name}.json")


def save_planet(data: Dict[str, Any], name: str, dest: Optional[str] = None) -> None:
    """Save planet data. `dest` optionally overrides storage key/directory behavior.

    Try to call into an optional repository-level `world_store` module with a
    `save_planet(name, data)` function. If not present, write to `.planets/{name}.json`.
    """
    try:
        import world_store  # type: ignore
        if hasattr(world_store, "save_planet"):
            if dest:
                # the world_store may accept an explicit key/path
                world_store.save_planet(name, data, dest=dest)
            else:
                world_store.save_planet(name, data)
            return
    except Exception:
        # world_store not available or failed — fall back to file
        pass

    path = _fallback_path_for(name, base_dir=dest)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_planet(name: str, src: Optional[str] = None) -> Dict[str, Any]:
    """Load planet data by name. Tries world_store.load_planet(name) then fallback file.

    Returns deserialized dict.
    """
    try:
        import world_store  # type: ignore
        if hasattr(world_store, "load_planet"):
            if src:
                return world_store.load_planet(name, src=src)
            return world_store.load_planet(name)
    except Exception:
        pass

    path = _fallback_path_for(name, base_dir=src)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Planet data not found at {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
