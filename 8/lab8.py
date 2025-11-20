import heapq

GOAL = (1, 2, 3, 4,
        5, 6, 7, 8,
        9, 10, 11, 12,
        13, 14, 15, 0)

# Предрасчитанные координаты правильных позиций
goal_pos = {val: (i // 4, i % 4) for i, val in enumerate(GOAL)}

# Манхэттен
def manhattan(board):
    dist = 0
    for idx, val in enumerate(board):
        if val == 0:
            continue
        r, c = idx // 4, idx % 4
        gr, gc = goal_pos[val]
        dist += abs(r - gr) + abs(c - gc)
    return dist

# Достижимость
def is_solvable(board):
    inv = 0
    arr = [x for x in board if x != 0]

    # считаем инверсии
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] > arr[j]:
                inv += 1

    # позиция пустой клетки: строка снизу
    blank_row_from_bottom = 4 - (board.index(0) // 4)

    # условие решаемости для 4×4
    return (inv + blank_row_from_bottom) % 2 == 1


# Генерация соседей
def neighbors(board):
    zero = board.index(0)
    r, c = zero // 4, zero % 4
    moves = []

    # смещения
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r+dr, c+dc
        if 0 <= nr < 4 and 0 <= nc < 4:
            new_i = nr*4 + nc
            lst = list(board)
            lst[zero], lst[new_i] = lst[new_i], lst[zero]
            moves.append(tuple(lst))
    return moves

# A*
def a_star(start):
    if not is_solvable(start):
        return -1

    pq = []
    g = {start: 0}
    h0 = manhattan(start)
    heapq.heappush(pq, (h0, 0, start))

    visited = set()

    while pq:
        f, cost, state = heapq.heappop(pq)

        if state == GOAL:
            return cost

        if state in visited:
            continue
        visited.add(state)

        for nb in neighbors(state):
            if nb in visited:
                continue
            ng = cost + 1
            if ng < g.get(nb, 99999999):
                g[nb] = ng
                heapq.heappush(pq, (ng + manhattan(nb), ng, nb))

    return -1


# ----- Ввод -----

print("Введите состояние (16 чисел, 0 — пусто):")
arr = list(map(int, input().split()))
if len(arr) != 16:
    print("Ошибка: нужно 16 чисел")
else:
    start = tuple(arr)
    res = a_star(start)
    print("Ответ:", res)

# Ввод: 1 2 3 4 5 6 7 8 9 10 11 12 13 0 14 15
# Вывод: 2
