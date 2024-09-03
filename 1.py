import pygame
import sys

# 初始化 Pygame
pygame.init()

# 设置屏幕大小
screen = pygame.display.set_mode((800, 600))

# 设置帧率
clock = pygame.time.Clock()

# 加载图像
image = pygame.image.load("D:\\Desktop\\Study\\Files\\2024-2025-1\\Python\\Portal-2D-Python\\RanaLogo.png")  # 替换为你的图像路径
# 定义绘制图像的函数
def draw_image(screen, image, position, size):
    # 截取图像的一部分（可选）
    image = image.subsurface(pygame.Rect((0, 0), size))
    # 绘制图像
    screen.blit(image, position)

# 游戏主循环
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 清屏
    screen.fill((0, 0, 0))

    # 定义绘制位置和大小
    positionX, positionY = 100, 100  # 起始位置
    sizeX, sizeY = 800, 800  # 图像大小

    # 绘制图像
    draw_image(screen, image, (positionX, positionY), (sizeX, sizeY))

    pygame.display.flip()

    # 控制帧率
    clock.tick(60)

# 退出 Pygame
pygame.quit()
