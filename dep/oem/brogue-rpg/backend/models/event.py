from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.models import Actor
    from backend.models.affix import Trigger

class EventDispatcher:
    triggers: list[Trigger]

    def __init__(self):
        self.triggers = []

    def add_trigger(self, trigger: 'Trigger') -> None:
        self.triggers.append(trigger)

    def broadcast(self, event: str, params):
        triggers = self.triggers.copy()
        for actor in current_world().actors.values():
            triggers.extend(actor.collect_triggers())
        
        context = {
            'target': None,
            'event': event,
            'params': params,
        }

        triggers = [t for t in triggers if t.event == event]
        triggers.sort(key=lambda t: -t.priority)

        for trigger in triggers:
            if trigger.check(context):
                if trigger(context):
                    break
    
    def send(self, actor: Actor, event: str, params):
        context = {
            'target': actor,
            'event': event,
            'params': params,
        }
        triggers = actor.collect_triggers()

        triggers = [t for t in triggers if t.event == event]
        triggers.sort(key=lambda t: -t.priority)
        
        for trigger in triggers:
            if trigger.check(context):
                if trigger(context):
                    break