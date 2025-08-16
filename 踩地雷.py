import pygame
import sys
from random import randint as ri

# --- 遊戲參數 ---
CELL_SIZE = 30
FPS = 30
D = ((1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, -1), (-1, 1), (-1, 0))

# 數字顏色 (經典踩地雷風格)
NUM_COLORS = {
    1: (0, 0, 255),  # 藍
    2: (0, 128, 0),  # 綠
    3: (255, 0, 0),  # 紅
    4: (0, 0, 128),  # 深藍
    5: (128, 0, 0),  # 棕紅
    6: (0, 128, 128),  # 青色
    7: (0, 0, 0),  # 黑
    8: (128, 128, 128),  # 灰
}


# --- 函數 ---
def generate_map(W, H, N):
    mines_map = [[0 for _ in range(W)] for _ in range(H)]
    n = 0
    while n < N:
        x, y = ri(0, W - 1), ri(0, H - 1)
        if mines_map[y][x] != 9:
            mines_map[y][x] = 9
            n += 1
    for i in range(H):
        for j in range(W):
            if mines_map[i][j] == 0:
                for dy, dx in D:
                    ny, nx = i + dy, j + dx
                    if 0 <= ny < H and 0 <= nx < W and mines_map[ny][nx] == 9:
                        mines_map[i][j] += 1
    return mines_map


def stamp(x, y):
    if mask[y][x] == 1:
        return
    stack = [(x, y)]
    while stack:
        x, y = stack.pop()
        if mask[y][x] == 1:
            continue
        if mines_map[y][x] == 9:
            game_over("loss")
            return
        mask[y][x] = 1
        if mines_map[y][x] == 0:
            for dy, dx in D:
                ny, nx = y + dy, x + dx
                if 0 <= ny < H and 0 <= nx < W and mask[ny][nx] != 1:
                    stack.append((nx, ny))


def flag(x, y):
    if mask[y][x] == 0:
        mask[y][x] = 2
    elif mask[y][x] == 2:
        mask[y][x] = 0


def check_win1():
    for i in range(H):
        for j in range(W):
            if mask[i][j] != 1 and mines_map[i][j] != 9:
                return False
    return True


def check_win2():
    for i in range(H):
        for j in range(W):
            if mask[i][j] != 2 and mines_map[i][j] == 9:
                return False
    return True


def game_over(result):
    global running
    print(result)
    running = False


# --- 初始化 ---
W, H = 16, 16
N = 40
mines_map = generate_map(W, H, N)
mask = [[0 for _ in range(W)] for _ in range(H)]  # 0=隱藏 1=開啟 2=旗子

# 保證第一格是空白
while True:
    x, y = ri(0, W - 1), ri(0, H - 1)
    if mines_map[y][x] == 0:
        stamp(x, y)
        break

pygame.init()
screen = pygame.display.set_mode((W * CELL_SIZE, H * CELL_SIZE))
pygame.display.set_caption("踩地雷")
font = pygame.font.SysFont("consolas", 20, bold=True)
clock = pygame.time.Clock()

# --- 遊戲主迴圈 ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            gx, gy = mx // CELL_SIZE, my // CELL_SIZE
            if 0 <= gx < W and 0 <= gy < H:
                if event.button == 1:  # 左鍵
                    if mask[gy][gx] == 1 and mines_map[gy][gx] > 0:
                        # ✅ 已翻開的數字格，檢查是否可以展開
                        flags = 0
                        hidden = []
                        for dy, dx in D:
                            ny, nx = gy + dy, gx + dx
                            if 0 <= ny < H and 0 <= nx < W:
                                if mask[ny][nx] == 2:
                                    flags += 1
                                elif mask[ny][nx] == 0:
                                    hidden.append((nx, ny))
                        if flags == mines_map[gy][gx]:
                            for nx, ny in hidden:
                                stamp(nx, ny)
                    else:
                        # 一般左鍵挖格子
                        stamp(gx, gy)

                elif event.button == 3:  # 右鍵插旗
                    flag(gx, gy)

    # 繪製
    screen.fill((200, 200, 200))
    for y in range(H):
        for x in range(W):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            if mask[y][x] == 0:  # 未揭開
                pygame.draw.rect(screen, (180, 180, 180), rect)
                pygame.draw.line(screen, (255, 255, 255), rect.topleft, rect.topright, 2)
                pygame.draw.line(screen, (255, 255, 255), rect.topleft, rect.bottomleft, 2)
                pygame.draw.line(screen, (100, 100, 100), rect.bottomleft, rect.bottomright, 2)
                pygame.draw.line(screen, (100, 100, 100), rect.topright, rect.bottomright, 2)

            elif mask[y][x] == 2:  # 旗子
                pygame.draw.rect(screen, (180, 180, 180), rect)
                pole = (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + 5)
                base = (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE - 5)
                pygame.draw.line(screen, (0, 0, 0), pole, base, 2)
                flag_points = [
                    (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + 5),
                    (x * CELL_SIZE + CELL_SIZE // 2 + 12, y * CELL_SIZE + 10),
                    (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + 15),
                ]
                pygame.draw.polygon(screen, (255, 0, 0), flag_points)

            elif mask[y][x] == 1:  # 已揭開
                pygame.draw.rect(screen, (220, 220, 220), rect)
                if mines_map[y][x] == 9:  # 地雷
                    pygame.draw.circle(screen, (255, 0, 0), rect.center, CELL_SIZE // 4)
                elif mines_map[y][x] > 0:
                    color = NUM_COLORS.get(mines_map[y][x], (0, 0, 0))
                    num = font.render(str(mines_map[y][x]), True, color)
                    text_rect = num.get_rect(center=rect.center)
                    screen.blit(num, text_rect)

            pygame.draw.rect(screen, (0, 0, 0), rect, 1)

    if check_win1() or check_win2():
        game_over("win")

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
