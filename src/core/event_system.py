from enum import Enum
from typing import List, Dict, Callable


class EventType(Enum):
    OBJECT_ADDED = 'object_added'
    OBJECT_REMOVED = 'object_removed'

class EventSystem:
    def __init__(self):
        self._listeners: Dict[EventType, List[Callable]] = {
            et: [] for et in EventType
        }

    def subscribe(self, event_type: EventType, callback: Callable):
        self._listeners[event_type].append(callback)

    def unsubscribe(self, event_type: EventType, callback: Callable):
        if callback in self._listeners[event_type]:
            self._listeners[event_type].remove(callback)

    def notify(self, event_type: EventType, data: dict = None):
        for callback in self._listeners[event_type]:
            callback(data or {})