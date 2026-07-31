from dataclasses import dataclass
from typing import List
from .terrain import Tile, generate_terrain
from collections import OrderedDict


@dataclass
class Chunk:
    cx: int
    cy: int
    tiles: List[Tile]


class ChunkManager:
    """Simple in-memory chunk manager with deterministic chunk generation.

    - Each chunk is generated deterministically from the planet seed and chunk coords.
    - Uses a small LRU cache (OrderedDict) to bound memory.
    """

    def __init__(self, max_cache_size: int = 64, chunk_size: int = 16) -> None:
        self.max_cache_size = max_cache_size
        self.chunk_size = chunk_size
        self._cache = OrderedDict()  # key: (seed, cx, cy) -> Chunk

    @staticmethod
    def _combine_seed(seed: int, cx: int, cy: int) -> int:
        # Mix seed with chunk coords deterministically. Use simple integer mixing.
        return (seed & 0xFFFFFFFF) ^ ((cx * 73856093) ^ (cy * 19349663))

    def generate_chunk(self, seed: int, cx: int, cy: int) -> Chunk:
        combined = self._combine_seed(seed, cx, cy)
        tiles = generate_terrain(combined, width=self.chunk_size, height=self.chunk_size)
        return Chunk(cx=cx, cy=cy, tiles=tiles)

    def get_chunk(self, seed: int, cx: int, cy: int) -> Chunk:
        key = (seed, cx, cy)
        if key in self._cache:
            # move to end as most-recently used
            self._cache.move_to_end(key)
            return self._cache[key]
        chunk = self.generate_chunk(seed, cx, cy)
        self._cache[key] = chunk
        # enforce cache size
        while len(self._cache) > self.max_cache_size:
            self._cache.popitem(last=False)
        return chunk

    def clear(self) -> None:
        self._cache.clear()
