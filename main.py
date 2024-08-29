from game import Game
import pygame
import sys

def main():
    pygame.init()
    pygame.key.stop_text_input()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Pygame Example")

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
        pygame.time.Clock().tick(75)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
