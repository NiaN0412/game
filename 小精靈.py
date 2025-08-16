from random import randint
from os import system

D = ((1, 0), (0, 1), (-1, 0), (0, -1))


def generate_maze(W: int, H: int) -> list[list[int]]:
    maze: list[list[int]] = [[1 if i % 2 == 1 and j % 2 == 1 else 0 for i in range(W)] for j in range(H)]
    already: set[tuple[int, int]] = set(((1, 1),))
    ready: list[tuple[int, int, int, int]] = [(1, 3, 1, 2), (3, 1, 2, 1)]
    while len(ready) > 0:
        a = ready.pop(randint(0, len(ready) - 1))
        if (a[0], a[1]) in already:
            continue
        already.add((a[0], a[1]))
        maze[a[3]][a[2]] = 1
        for d in D:
            x, y = a[0] + d[0] * 2, a[1] + d[1] * 2
            if x < 0 or y < 0 or x >= W or y >= H or (x, y) in already:
                continue
            ready.append((x, y, a[0] + d[0], a[1] + d[1]))
    return maze


def show_maze(maze: list[list[int]], W: int, H: int) -> None:
    system("cls")
    for i in range(H):
        for j in range(W):
            if [j, i] == player:
                print("桃", end="")
            elif maze[i][j] == 0:
                print("牆", end="")
            elif maze[i][j] == 1:
                print("  ", end="")

        print()


def move(player: list[int], maze: list[list[int]], d: tuple[int, int], W: int, H: int) -> None:
    nx, ny = player[0] + d[0], player[1] + d[1]
    if nx < 0 or ny < 0 or nx > W or ny > H:
        return
    if maze[ny][nx] == 0:
        return
    player[0], player[1] = nx, ny


def generate_enemy(W: int, H: int, enemy_site: list[list[int]]) -> None:
    enemy_site.append([1, H - 2])
    enemy_site.append([W - 2, 1])


def enemy_move(maze: list[list[int]], enemy_site: list[list[int]]) -> None:
    


W = int(input("請輸入地圖長: "))
H = int(input("請輸入地圖寬: "))
maze = generate_maze(W, H)
player = [1, 1]
enemy_site: list[list[int]] = []
generate_enemy(W, H, enemy_site)
while True:
    show_maze(maze, W, H)
    di = input("輸入WASD來移動: ")

    if di == "W" or di == "w":
        move(player, maze, (0, -1), W, H)
    elif di == "A" or di == "a":
        move(player, maze, (-1, 0), W, H)
    elif di == "S" or di == "s":
        move(player, maze, (0, 1), W, H)
    elif di == "D" or di == "d":
        move(player, maze, (1, 0), W, H)

    enemy_move(maze, enemy_site)
