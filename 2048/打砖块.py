import pygame
import sys
import random

# 初始化Pygame
pygame.init()

# 游戏窗口设置
WIDTH, HEIGHT = 600, 400
FPS = 60
WHITE = (255, 255, 255)

# 球的属性
ball_radius = 15
ball_color = (255, 0, 0)
ball_speed = [3, 3]  # 减小速度

# 浮板的属性
paddle_width = 100
paddle_height = 10
paddle_color = (0, 255, 0)
paddle_speed = 8

# 砖块的属性
brick_width = 80
brick_height = 20
brick_color = (0, 0, 255)
brick_rows = 4
brick_columns = 8

# 初始化窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("打砖块游戏")

# 创建球、浮板和砖块
ball = pygame.Rect(WIDTH // 2 - ball_radius, HEIGHT // 2 - ball_radius, ball_radius * 2, ball_radius * 2)
paddle = pygame.Rect(WIDTH // 2 - paddle_width // 2, HEIGHT - 20, paddle_width, paddle_height)
bricks = []

for row in range(brick_rows):
    for col in range(brick_columns):
        brick = pygame.Rect(col * brick_width, row * brick_height, brick_width, brick_height)
        bricks.append(brick)

# 游戏循环
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 移动浮板
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += paddle_speed

    # 移动球
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # 碰撞检测
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed[0] = -ball_speed[0]
    if ball.top <= 0 or ball.colliderect(paddle):
        ball_speed[1] = -ball_speed[1]

    # 检测球与砖块的碰撞
    for brick in bricks:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_speed[1] = -ball_speed[1]

    # 清屏
    screen.fill(WHITE)

    # 绘制球、浮板和砖块
    pygame.draw.circle(screen, ball_color, ball.center, ball_radius)
    pygame.draw.rect(screen, paddle_color, paddle)
    for brick in bricks:
        pygame.draw.rect(screen, brick_color, brick)

    # 更新显示
    pygame.display.flip()

    # 控制帧率
    clock.tick(FPS)
