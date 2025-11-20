import heapq

# --- Манхэттенская эвристика ---
def manhattan(board):
    dist = 0
    for i, val in enumerate(board):
        if val == 0:
            continue
        correct_row = (val - 1) // 4
        correct_col = (val - 1) % 4
        curr_row = i // 4
        curr_col = i % 4
        dist += abs(correct_row - curr_row) + abs(correct_col - curr_col)
    return dist

# --- Проверка на достижимость (чётность перестановки + строка пустой клетки) ---
def is_solvable(board):
    inv = 0
    arr = [x for x in board if x != 0]
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] > arr[j]:
                inv += 1
    blank_row = board.index(0) // 4  # 0 сверху
    return (inv + blank_row) % 2 == 0

# --- Проверка цели ---
def is_goal(board):
    return board == list(range(1, 16)) + [0]

# --- Получение соседей (движения пустой клетки) ---
def get_neighbors(board):
    neighbors = []
    zero = board.index(0)
    zr, zc = zero // 4, zero % 4

    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in moves:
        nr, nc = zr + dr, zc + dc
        if 0 <= nr < 4 and 0 <= nc < 4:
            new_board = board[:]
            new_index = nr * 4 + nc
            new_board[zero], new_board[new_index] = new_board[new_index], new_board[zero]
            neighbors.append(new_board)
    return neighbors

# --- A* ---
def a_star(start):
    if not is_solvable(start):
        return -1

    open_heap = []
    heapq.heappush(open_heap, (manhattan(start), 0, start))
    closed = set()

    while open_heap:
        f, g, board = heapq.heappop(open_heap)

        if is_goal(board):
            return g

        board_tuple = tuple(board)
        if board_tuple in closed:
            continue
        closed.add(board_tuple)

        for nb in get_neighbors(board):
            if tuple(nb) not in closed:
                new_g = g + 1
                new_f = new_g + manhattan(nb)
                heapq.heappush(open_heap, (new_f, new_g, nb))

    return -1

# --- Ввод ---
print("Введите 16 чисел (0 — пустая клетка):")
nums = list(map(int, input().split()))
if len(nums) != 16:
    print("Ошибка: нужно 16 чисел.")
else:
    res = a_star(nums)
    print("Минимальное число ходов:", res)