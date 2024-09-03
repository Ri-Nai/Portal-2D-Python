import pygame.math

# 初始化 Pygame
pygame.init()

# 创建一个矩形
rect = pygame.Rect(0, 0, 100, 100)

# 创建一个 Vector2 对象
vector = pygame.math.Vector2(50, 50)

# 检查 Vector2 是否在矩形内
if rect.contains(vector):
    print("Vector is inside the rectangle.")
else:
    print("Vector is outside the rectangle.")
