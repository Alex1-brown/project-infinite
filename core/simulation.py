"""Simulation clock and tick system."""

from dataclasses import dataclass
from typing import Callable, List


@dataclass
class SimulationClock:
    """Manages game time and simulation ticks."""
    current_time: float = 0.0
    delta_time: float = 0.016  # Default 60 FPS
    tick_count: int = 0
    
    def tick(self, delta: float = None) -> None:
        """Advance simulation time.
        
        Args:
            delta: Time delta in seconds. Uses default if not provided.
        """
        if delta is not None:
            self.delta_time = delta
        self.current_time += self.delta_time
        self.tick_count += 1
    
    def set_time_scale(self, scale: float) -> None:
        """Set time scale multiplier (1.0 = normal speed)."""
        self.delta_time *= scale
    
    def reset(self) -> None:
        """Reset clock to zero."""
        self.current_time = 0.0
        self.tick_count = 0
    
    def elapsed(self) -> float:
        """Get total elapsed time."""
        return self.current_time
    
    def ticks(self) -> int:
        """Get total tick count."""
        return self.tick_count
