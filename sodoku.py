import tkinter as tk
import time

# --- Sudoku puzzle (0 = empty) ---
board = [
    [5,3,0,0,7,0,0,0,0],
    [6,0,0,1,9,5,0,0,0],
    [0,9,8,0,0,0,0,6,0],
    [8,0,0,0,6,0,0,0,3],
    [4,0,0,8,0,3,0,0,1],
    [7,0,0,0,2,0,0,0,6],
    [0,6,0,0,0,0,2,8,0],
    [0,0,0,4,1,9,0,0,5],
    [0,0,0,0,8,0,0,7,9]
]

# --- Tkinter setup ---
root = tk.Tk()
root.title("🌈 Sudoku Solver Visualization")

canvas = tk.Canvas(root, width=450, height=450, bg="#f9f9f9")
canvas.pack(pady=10)

cell_size = 50
cells = {}
rects = {}

# --- Draw grid and cells ---
for i in range(9):
    for j in range(9):
        x1 = j * cell_size
        y1 = i * cell_size
        x2 = x1 + cell_size
        y2 = y1 + cell_size

        rect_color = "#ffffff" if board[i][j] == 0 else "#d1ffd1"  # light green for fixed
        rect = canvas.create_rectangle(x1, y1, x2, y2, fill=rect_color, outline="black", width=1)
        txt = canvas.create_text(
            x1 + 25, y1 + 25,
            text=str(board[i][j]) if board[i][j] != 0 else "",
            font=("Helvetica", 18, "bold"),
            fill="black"
        )
        cells[(i, j)] = txt
        rects[(i, j)] = rect

# --- Thicker lines for 3×3 boxes ---
for i in range(10):
    width = 3 if i % 3 == 0 else 1
    canvas.create_line(0, i * cell_size, 450, i * cell_size, width=width)
    canvas.create_line(i * cell_size, 0, i * cell_size, 450, width=width)

# --- Helper functions ---
def update_board(color_cell=None, color="#b3e6ff"):
    """Updates the GUI with optional cell color highlight"""
    if color_cell:
        i, j = color_cell
        canvas.itemconfig(rects[(i, j)], fill=color)
    for i in range(9):
        for j in range(9):
            canvas.itemconfig(
                cells[(i, j)],
                text=str(board[i][j]) if board[i][j] != 0 else "",
                fill="black"
            )
    root.update()
    time.sleep(0.0001)

def reset_color(i, j):
    """Resets a cell color after highlight"""
    base_color = "#ffffff" if board[i][j] == 0 else "#d1ffd1"
    canvas.itemconfig(rects[(i, j)], fill=base_color)
    root.update()

# --- Sudoku Logic ---
def find_empty():
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def valid(num, pos):
    r, c = pos
    # Row
    if num in board[r]:
        return False
    # Column
    if num in [board[i][c] for i in range(9)]:
        return False
    # Box
    box_r, box_c = r // 3, c // 3
    for i in range(box_r * 3, box_r * 3 + 3):
        for j in range(box_c * 3, box_c * 3 + 3):
            if board[i][j] == num:
                return False
    return True

def solve():
    find = find_empty()
    if not find:
        return True
    r, c = find

    for num in range(1, 10):
        if valid(num, (r, c)):
            board[r][c] = num
            update_board((r, c), color="#c1f2b0")  # 🟢 filling color

            if solve():
                return True

            # 🔴 Backtrack
            board[r][c] = 0
            update_board((r, c), color="#ffb3b3")
            reset_color(r, c)

    return False

# --- Buttons ---
def start_solving():
    solve()
    canvas.create_text(225, 470, text="✅ Sudoku Solved!", font=("Helvetica", 16, "bold"), fill="green")

start_button = tk.Button(
    root,
    text="▶ Start Solving",
    font=("Helvetica", 14, "bold"),
    bg="#4CAF50",
    fg="white",
    command=start_solving
)
start_button.pack(pady=10)

root.mainloop()
