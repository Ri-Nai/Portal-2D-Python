class EventList:
    def __init__(self, events = None):
        if events:
            self.init(events)

    def init(self, events):
        self.events = {}
        for k, v in events.items():
            self.events[k] = create_event(k, v)
            # print(k, type(self.events[k]))

    def update(self):
        for event in self.events.values():
            if not event.update():
                break

    def get_event(self, id):
        # print(id, type(self.events.get(id)))
        return self.events.get(id)

    def draw(self):
        for event in self.events.values():
            event.draw()

def create_event(id, event_data):
    # ButtonEvent
    if event_data['type'] == 1:
        from GameEvents.button import ButtonEvent
        e = ButtonEvent(
            id,
            event_data['type'],
            event_data['hitbox'],
            event_data['affect']
        )
        from game import Game
        import copy
        Game.get_instance().map_manager.super_edges.append(e.block.hitbox)


        return e
    # Wire
    if event_data['type'] == 2:
        from GameEvents.wire import Wire
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
        from GameEvents.view_switch import ViewSwitch
        return ViewSwitch(
            id,
            event_data['type'],
            event_data['hitbox'],
            event_data['toUrl']
        )
    # DoorEvent
    if event_data['type'] == 4:
        from GameEvents.door import DoorEvent
        e = DoorEvent(
            id,
            event_data['type'],
            event_data['hitbox']
        )
        from game import Game
        Game.get_instance().map_manager.super_edges.append(e.block.hitbox)
        return e
    from GameEvents.event import GameEvent
    return GameEvent(
        id,
        event_data['type'],
        event_data['hitbox'],
        event_data['affect']
    )
