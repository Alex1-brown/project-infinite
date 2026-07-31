"""Deterministic random number generator using SHA256."""

import random
import hashlib
from typing import List, Sequence, TypeVar, Union


T = TypeVar('T')


class DeterministicRNG:
    """Seeded random number generator for reproducible procedural generation."""
    
    def __init__(self, seed: Union[int, str, float]):
        """Initialize RNG with a seed.
        
        Args:
            seed: Can be int, string, or float. Converted to hash for reproducibility.
        """
        # Convert seed to hash for uniform distribution
        hash_obj = hashlib.sha256(str(seed).encode())
        raw = int(hash_obj.hexdigest()[:16], 16)
        self.seed = raw
        self.r = random.Random(raw)
    
    def float(self, a: float = 0.0, b: float = 1.0) -> float:
        """Generate random float in [a, b]."""
        return self.r.uniform(a, b)
    
    def int(self, a: int, b: int) -> int:
        """Generate random integer in [a, b] inclusive."""
        return self.r.randint(a, b)
    
    def choice(self, seq: Sequence[T]) -> T:
        """Choose random element from sequence."""
        return self.r.choice(seq)
    
    def choices(self, seq: Sequence[T], k: int) -> List[T]:
        """Choose k elements from sequence."""
        return self.r.choices(seq, k=k)
    
    def shuffle(self, seq: List[T]) -> None:
        """Shuffle a list in place."""
        self.r.shuffle(seq)
    
    def sample(self, seq: Sequence[T], k: int) -> List[T]:
        """Sample k unique elements from sequence."""
        return self.r.sample(seq, k=k)
    
    def chance(self, p: float) -> bool:
        """Return True with probability p."""
        return self.r.random() < p
    
    def weighted_choice(self, options: dict) -> T:
        """Choose from weighted options.
        
        Args:
            options: Dict of {choice: weight}
        
        Returns:
            Selected choice
        """
        items = list(options.items())
        choices = [item[0] for item in items]
        weights = [item[1] for item in items]
        return self.r.choices(choices, weights=weights, k=1)[0]
    
    def normal(self, mu: float = 0.0, sigma: float = 1.0) -> float:
        """Generate normally distributed random number."""
        return self.r.gauss(mu, sigma)
