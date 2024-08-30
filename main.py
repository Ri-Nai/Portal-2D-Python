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


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                print("Key pressed")
        # 运行游戏循环
        game.loop()

        pygame.display.flip()
        pygame.time.Clock().tick(90)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
