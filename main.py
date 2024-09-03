from game import Game
import pygame
import sys
import os

def main():
    pygame.init()
    pygame.key.stop_text_input()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Portal-2D")
    icon_image = pygame.image.load(os.path.join(os.path.dirname(__file__), "./assets/ico/RanaLogo.png"))
    pygame.display.set_icon(icon_image)
    # 创建 Game 实例
    game = Game.get_instance(screen)
    clock = pygame.time.Clock()

    paused = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # print("Key pressed")
                if event.key == pygame.K_ESCAPE:
                    paused = not paused  # 切换暂停状态
                    game.mouse_manager.uncapture() if paused else game.mouse_manager.capture()
            elif event.type == pygame.MOUSEBUTTONDOWN and not paused:
                game.mouse_manager.capture()

        # 运行游戏循环
        game.loop()
        # print(clock.get_fps())
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
