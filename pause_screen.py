import pygame

class PauseScreen:
    def __init__(self):
        self.pause_screen = pygame.Surface((1280, 720), pygame.SRCALPHA)
        self.pause_screen.fill((0, 0, 0, 128))

    def draw(self):
        from game import Game
        if (Game.get_instance().is_paused):
            self.build()
            Game.get_instance().screen.blit(self.pause_screen, (0, 0))

    def build(self):
        box_height = 540
        box_width = 240
        pos = pygame.Rect((1280 - box_width) // 2, (720 - box_height) // 2 ,box_width, box_height)
        from game import Game
        self.button_list([
            { "text": "Resume", "callback": lambda: Game.get_instance().resume() },
            { "text": "Quit", "callback": lambda: pygame.event.post(pygame.event.Event(pygame.QUIT)) }
        ], pos)

    def button(self, text, position: pygame.Rect, callback):
        font = pygame.font.Font(None, 32)
        text = font.render(text, True, (0, 0, 0))
        pygame.draw.rect(self.pause_screen, (255, 255, 255), position)

        text_position = position.move(16, 8)

        self.pause_screen.blit(text, text_position)
        self.on_click(position, callback)

    def button_list(self, buttons, position: pygame.Rect):
        GAP = 10
        PADDING = 20
        X = position.x + PADDING
        Y = position.y + PADDING
        width = position.width - 2 * PADDING
        for button in buttons:
            pos = pygame.Rect(X, Y, width, 40)
            self.button(button["text"], pos, button["callback"])
            Y += 40 + GAP

    def on_click(self, position: pygame.Rect, callback):
        from game import Game
        if (
            position.collidepoint(pygame.mouse.get_pos()) and
            pygame.mouse.get_pressed()[0]
        ):
            callback()
