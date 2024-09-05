class EventList:
    def __init__(self, events = None):
        if events:
            self.init(events)

    def init(self, events):
        self.events = {}
        for k, v in events.items():
            self.events[k] = create_event(k, v)

    def update(self, t):
        for event in self.events.values():
            event.update(t)

    def get_event(self, id):
        return self.events.get(id)

    def draw(self):
        for event in self.events.values():
            event.draw()

def create_event(id, event_data):
    # ButtonEvent
    if event_data['type'] == 1:
        from button import ButtonEvent
        e = ButtonEvent(
            id,
            event_data['type'],
            event_data['hitbox'],
            event_data['affect']
        )
        from game import Game
        Game.get_instance().map_manager.super_edges.append(e.block)
        return e
    # Wire
    if event_data['type'] == 2:
        from wire import Wire
        return Wire(
            id,
            event_data['type'],
            event_data['hitbox'],
            event_data['affect'],
            event_data['predir'],
            event_data['nxtdir'],
        )
    # ViewSwitch
    if event_data['type'] == 3:
        from view_switch import ViewSwitch
        return ViewSwitch(
            id,
            event_data['type'],
            event_data['hitbox'],
            event_data['toUrl']
        )
    # DoorEvent
    if event_data['type'] == 4:
        from door import DoorEvent
        e = DoorEvent(
            id,
            event_data['type'],
            event_data['hitbox'],
            event_data['affect']
        )
        from game import Game
        Game.get_instance().map_manager.super_edges.append(e.block)
        return e
    from event import GameEvent
    return GameEvent(
        id,
        event_data['type'],
        event_data['hitbox'],
        event_data['affect']
    )
