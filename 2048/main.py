import pygame
import sys
import random

# 初始化Pygame
pygame.init()

# 游戏窗口大小
WIDTH, HEIGHT = 400, 400

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 游戏主循环速度
FPS = 60

# 初始化屏幕
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 Game")

# 初始化字体
font = pygame.font.Font(None, 36)

# 定义方块大小和间距
BLOCK_SIZE = 100
BLOCK_MARGIN = 10

# 初始化游戏板
board = [[0] * 4 for _ in range(4)]


def spawn_tile():
    # 在空白格子中随机生成2或4
    empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = random.choice([2, 4])


def draw_board():
    screen.fill(WHITE)
    for i in range(4):
        for j in range(4):
            pygame.draw.rect(screen, BLACK, (j * (BLOCK_SIZE + BLOCK_MARGIN),
                                            i * (BLOCK_SIZE + BLOCK_MARGIN),
                                            BLOCK_SIZE, BLOCK_SIZE))
            if board[i][j] != 0:
                text = font.render(str(board[i][j]), True, WHITE)
                screen.blit(text, (j * (BLOCK_SIZE + BLOCK_MARGIN) + BLOCK_SIZE / 2 - text.get_width() / 2,
                                   i * (BLOCK_SIZE + BLOCK_MARGIN) + BLOCK_SIZE / 2 - text.get_height() / 2))


def merge_tiles(row):
    # 合并相邻的相同数字，并移动其他数字
    merged = [False, False, False, False]
    for i in range(3, 0, -1):
        for j in range(i - 1, -1, -1):
            if board[row][i] != 0 and (board[row][i] == board[row][j] or board[row][j] == 0):
                if board[row][j] == 0:
                    board[row][j] = board[row][i]
                    board[row][i] = 0
                elif board[row][i] == board[row][j] and not merged[i] and not merged[j]:
                    board[row][j] *= 2
                    board[row][i] = 0
                    merged[j] = True
                    break


def move_left():
    for i in range(4):
        merge_tiles(i)


def move_right():
    for i in range(4):
        board[i].reverse()
        merge_tiles(i)
        board[i].reverse()


def move_up():
    for j in range(4):
        column = [board[i][j] for i in range(4)]
        merge_tiles(j)
        for i in range(4):
            board[i][j] = column[i]


def move_down():
    for j in range(4):
        column = [board[i][j] for i in range(3, -1, -1)]
        merge_tiles(j)
        for i in range(3, -1, -1):
            board[i][j] = column[3 - i]


def main():
    clock = pygame.time.Clock()

    # 初始化游戏板
    spawn_tile()
    spawn_tile()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_left()
                    spawn_tile()
                elif event.key == pygame.K_RIGHT:
                    move_right()
                    spawn_tile()
                elif event.key == pygame.K_UP:
                    move_up()
                    spawn_tile()
                elif event.key == pygame.K_DOWN:
                    move_down()
                    spawn_tile()

        draw_board()
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
