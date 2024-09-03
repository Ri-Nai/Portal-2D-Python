import pygame
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class MouseManager:
    def __init__(self, screen):
        self.screen = screen
        self.is_capture = False  # 添加一个属性来跟踪捕获状态
        self.x = self.screen.get_width() // 2
        self.y = self.screen.get_height() // 2
        self.left = False
        self.right = False

    def capture(self):
        self.is_capture = True
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

    def uncapture(self):
        self.is_capture = False
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)

    def update(self):
        # Update mouse position
        self.x, self.y = pygame.mouse.get_pos()
        self.x = max(0, min(self.x, self.screen.get_width()))
        self.y = max(0, min(self.y, self.screen.get_height()))

        # Check mouse buttons
        buttons = pygame.mouse.get_pressed()
        self.left = buttons[0]
        self.right = buttons[2]

    def draw(self):
        if self.is_capture:
            pygame.draw.rect(self.screen, (255, 255, 255), (self.x - 3, self.y - 3, 6, 6))
            pygame.draw.rect(self.screen, (0, 0, 0), (self.x - 2, self.y - 2, 4, 4))

    def get_position(self):
        return Vector(self.x, self.y)


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    mouse_manager = MouseManager(screen)
    paused = False  # 游戏初始状态为未暂停
    mouse_manager.capture()  # 初始捕获鼠标
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused  # 切换暂停状态
                    mouse_manager.uncapture() if paused else mouse_manager.capture()
            elif event.type == pygame.MOUSEBUTTONDOWN and not paused:
                mouse_manager.capture()

        mouse_manager.update()
        screen.fill((0, 0, 0))
        mouse_manager.draw()
        # draw_ui(screen, paused)  # 绘制UI界面
        if not paused:
            # 这里添加游戏的主逻辑
            pass
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
