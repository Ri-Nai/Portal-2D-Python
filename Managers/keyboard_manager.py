import pygame
import sys


class KeyboardManager:
    def __init__(self):
        pygame.key.stop_text_input()
        # pygame.key.set_repeat(1, 1)  # 设置按键持续事件间隔和按键持续时间
        self.keymap = {
            "Esc": pygame.K_ESCAPE,
            "Space": pygame.K_SPACE,
            "Left": pygame.K_LEFT,
            "Right": pygame.K_RIGHT,
            "A": pygame.K_a,
            "D": pygame.K_d,
            "E": pygame.K_e,
        }
        self.status = {key: False for key in self.keymap}
        self.is_held = {key: False for key in self.keymap}

    def update(self):
        keys_pressed = pygame.key.get_pressed()
        for key in self.keymap:
            self.status[key] = keys_pressed[self.keymap[key]]

    def isKeyDown(self, key):
        return self.status[key]

    def isKeysDown(self, keys):
        return any(self.isKeyDown(key) for key in keys)

    def firstDown(self, key, operate=None):
        if self.isKeyDown(key):
            if not self.is_held[key]:
                if operate is not None:
                    operate()
                self.is_held[key] = True
        else:
            self.is_held[key] = False
        return self.is_held[key]

    def show(self):
        for key, value in self.status.items():
            if value:
                print(f"{key}: {value}")


# Example usage
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    keyboard_manager = KeyboardManager()

    running = True
    while running:
        keyboard_manager.update()
        keyboard_manager.show()  # 显示按键状态
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
