from random import randint as ri
from os import system


def display() -> None:
    system("cls")
    for i in range(W + 1):
        if i == 0:
            print("/", end="")
        else:
            print((i - 1) % 10, end="")
    print()
    for i in range(H):
        for j in range(W + 1):
            if j == 0:
                print(i % 10, end="")
            elif mask[i][j - 1] == 1:
                if mines_map[i][j - 1] == 0:
                    print(" ", end="")
                elif mines_map[i][j - 1] == 9:
                    print("x", end="")
                else:
                    print(mines_map[i][j - 1], end="")
            elif mask[i][j - 1] == 2:
                print("◤", end="")
            else:
                print("▓", end="")
        print()


def loss() -> None:
    print("loss")
    exit()


def check_win1() -> None:
    for i in range(H):
        for j in range(W):
            if mask[i][j] != 1 and mines_map[i][j] != 9:
                return
    print("win")
    exit()


def check_win2() -> None:
    for i in range(H):
        for j in range(W):
            if mask[i][j] != 2 and mines_map[i][j] == 9:
                return
    print("win")
    exit()


def stamp(x: int, y: int) -> None:
    if mask[y][x] == 1:
        return
    stack.append((x, y))
    while len(stack) > 0:
        x, y = stack.pop()
        if mines_map[y][x] == 9:
            loss()
        elif mines_map[y][x] == 0:
            mask[y][x] = 1
            for dy, dx in D:
                ny, nx = y + dy, x + dx
                if 0 <= ny < H and 0 <= nx < W and mask[ny][nx] != 1:
                    stack.append((nx, ny))
        else:
            mask[y][x] = 1


def flag(x: int, y: int) -> None:
    if mask[y][x] == 0:
        mask[y][x] = 2
    elif mask[y][x] == 2:
        mask[y][x] = 0


def mine_num(W: int, H: int):
    try:
        n = int(input("請輸入難度等級(1最小，5最大): "))
    except ValueError:
        print("輸入非數字")
        exit()
    if n < 1 or n > 5:
        print("錯誤:請輸入1~5的數字")
    mine_count = (12 + n * 3) * W * H // 100
    print(f"你選擇了難度 {n}，會有 {mine_count} 顆地雷。")
    return mine_count


try:
    W = int(input("請輸入寬: "))
    H = int(input("請輸入高: "))
    N = mine_num(W, H)
except ValueError:
    print("輸入非數字")
    exit()
if N >= W * H or N <= 0:
    print("錯誤:地雷數量錯誤")
    exit()
stack: list[tuple[int, int]] = []
mines_map = [[0 for _ in range(W)] for _ in range(H)]
mask = [[0 for _ in range(W)] for _ in range(H)]
n = 0
while n < N:
    x, y = ri(0, W - 1), ri(0, H - 1)
    if mines_map[y][x] != 9:
        mines_map[y][x] = 9
        n += 1
D = ((1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, -1), (-1, 1), (-1, 0))
for i in range(H):
    for j in range(W):
        if mines_map[i][j] == 0:
            for dy, dx in D:
                if 0 <= i + dy < H and 0 <= j + dx < W and mines_map[i + dy][j + dx] == 9:
                    mines_map[i][j] += 1
while True:
    x, y = ri(0, W - 1), ri(0, H - 1)
    if mines_map[y][x] == 0:
        stamp(x, y)
        break

display()
while True:
    try:
        x, y, o = map(
            int, input("請輸入三個用空白隔開的正整數x, y和o\n用x, y來指定一要操作的座標\n用o來指定操作(1是挖開，2是插旗): ").split()
        )
        if not (0 <= y < H and 0 <= x < W):
            print("座標超出範圍")
            continue
        if o <= 0 or o > 2:
            print("操作符錯誤")
            continue
    except ValueError:
        print("請輸入兩個用空白隔開的正整數")
        continue
    if o == 1:
        stamp(x, y)
    else:
        flag(x, y)
    display()
    check_win1()
    check_win2()
