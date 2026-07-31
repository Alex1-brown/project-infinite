"""Domain model: entities, components, and event system."""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Type
import time
import uuid
from enum import Enum


EntityId = str


def new_id() -> EntityId:
    """Generate a unique entity ID."""
    return uuid.uuid4().hex


class EventType(Enum):
    """Game event types."""
    # Galaxy events
    SYSTEM_DISCOVERED = "system.discovered"
    PLANET_DISCOVERED = "planet.discovered"
    
    # Ship events
    SHIP_SPAWNED = "ship.spawned"
    SHIP_DAMAGED = "ship.damaged"
    SHIP_DESTROYED = "ship.destroyed"
    SHIP_DOCKED = "ship.docked"
    
    # Economy events
    RESOURCE_MINED = "resource.mined"
    RESOURCE_PRODUCED = "resource.produced"
    TRADE_COMPLETED = "trade.completed"
    PRICE_CHANGED = "price.changed"
    
    # Faction events
    FACTION_WAR_STARTED = "faction.war_started"
    FACTION_WAR_ENDED = "faction.war_ended"
    FACTION_RELATION_CHANGED = "faction.relation_changed"
    
    # NPC events
    NPC_SPAWNED = "npc.spawned"
    NPC_GOAL_CHANGED = "npc.goal_changed"
    NPC_MEMORY_UPDATED = "npc.memory_updated"
    
    # World events
    SIMULATION_TICK = "simulation.tick"
    WORLD_SAVED = "world.saved"
    WORLD_LOADED = "world.loaded"


@dataclass
class Event:
    """Base event class."""
    type: EventType
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    source_id: Optional[EntityId] = None
    
    def __repr__(self) -> str:
        return f"Event({self.type.value}, {self.payload})"


class EventBus:
    """Central event dispatcher for decoupled system communication."""
    
    def __init__(self):
        self._handlers: Dict[EventType, List[Callable]] = {}
        self.history: List[Event] = []
        self._max_history = 10000
    
    def subscribe(self, event_type: EventType, handler: Callable[[Event], None]) -> None:
        """Register a handler for an event type."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
    
    def unsubscribe(self, event_type: EventType, handler: Callable[[Event], None]) -> None:
        """Unregister a handler."""
        if event_type in self._handlers:
            self._handlers[event_type].remove(handler)
    
    def publish(self, event: Event) -> None:
        """Publish an event to all subscribed handlers."""
        self.history.append(event)
        if len(self.history) > self._max_history:
            self.history.pop(0)
        
        for handler in self._handlers.get(event.type, []):
            try:
                handler(event)
            except Exception as e:
                print(f"Error in event handler for {event.type}: {e}")
    
    def get_history(self, event_type: Optional[EventType] = None) -> List[Event]:
        """Get event history, optionally filtered by type."""
        if event_type is None:
            return self.history[:]
        return [e for e in self.history if e.type == event_type]


@dataclass
class Component:
    """Base class for entity components."""
    pass


@dataclass
class Entity:
    """Entity with component-based architecture."""
    id: EntityId = field(default_factory=new_id)
    name: str = ""
    components: Dict[str, Component] = field(default_factory=dict)
    
    def add_component(self, component: Component) -> 'Entity':
        """Add a component to this entity."""
        self.components[type(component).__name__] = component
        return self
    
    def get_component(self, component_type: Type[Component]) -> Optional[Component]:
        """Get a component by type."""
        return self.components.get(component_type.__name__)
    
    def has_component(self, component_type: Type[Component]) -> bool:
        """Check if entity has a component."""
        return component_type.__name__ in self.components
    
    def remove_component(self, component_type: Type[Component]) -> bool:
        """Remove a component."""
        if component_type.__name__ in self.components:
            del self.components[component_type.__name__]
            return True
        return False
