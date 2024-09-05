from GameEvents.event import GameEvent


class ViewSwitch(GameEvent):
    def __init__(self, id, type, hitbox, toUrl):
        super().__init__(id, type, hitbox, [])
        self.toUrl = toUrl
    def on_activate(self):
        from game import Game
        Game.get_instance().switch_view(self.toUrl)
    def update(self):

        from game import Game
        player = Game.get_instance().view.player
        if self.colliderect(player.hitbox):
            self.activate()
            return False
        return True

