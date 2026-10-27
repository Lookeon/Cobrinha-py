import random
import tkinter as tk

BOARD_SIZE = 280
GRID_SIZE = 28
COLS = BOARD_SIZE // GRID_SIZE
ROWS = BOARD_SIZE // GRID_SIZE
INITIAL_SPEED = 170
BACKGROUND = "#0f172a"
SURFACE = "#172033"
BOARD_BACKGROUND = "#0b1220"
GRID_LIGHT = "#111b2e"
GRID_DARK = "#0e1829"
ACCENT = "#a3e635"


class Snake:
    def __init__(self, canvas):
        self.canvas = canvas
        center_x = COLS // 2
        center_y = ROWS // 2
        self.body = [
            (center_x, center_y),
            (center_x - 1, center_y),
            (center_x - 2, center_y),
        ]
        self.direction = (1, 0)
        self.next_direction = (1, 0)

    def set_direction(self, new_direction):
        if (
            self.direction[0] == -new_direction[0]
            and self.direction[1] == -new_direction[1]
        ):
            return
        self.next_direction = new_direction

    def update_direction(self):
        self.direction = self.next_direction

    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)

    def head(self):
        return self.body[0]

    def is_colliding_with_wall(self):
        head_x, head_y = self.head()
        return head_x < 0 or head_y < 0 or head_x >= COLS or head_y >= ROWS

    def is_colliding_with_itself(self):
        head = self.head()
        return any(segment == head for segment in self.body[1:])

    def draw(self):
        self.canvas.delete("snake")
        for index, (x, y) in enumerate(self.body):
            color = ACCENT if index == 0 else "#65a30d"
            x1 = x * GRID_SIZE
            y1 = y * GRID_SIZE
            self.canvas.create_rectangle(
                x1 + 3,
                y1 + 3,
                x1 + GRID_SIZE - 3,
                y1 + GRID_SIZE - 3,
                fill=color,
                outline=color,
                tags="snake",
            )


class Food:
    def __init__(self, canvas, snake):
        self.canvas = canvas
        self.snake = snake
        self.position = (0, 0)
        self.spawn()

    def spawn(self):
        while True:
            x = random.randint(0, COLS - 1)
            y = random.randint(0, ROWS - 1)
            if (x, y) not in self.snake.body:
                self.position = (x, y)
                break

    def draw(self):
        self.canvas.delete("food")
        x, y = self.position
        x1 = x * GRID_SIZE
        y1 = y * GRID_SIZE
        self.canvas.create_rectangle(
            x1 + 5,
            y1 + 5,
            x1 + GRID_SIZE - 5,
            y1 + GRID_SIZE - 5,
            fill="#ef4444",
            outline="#ef4444",
            tags="food",
        )


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Cobrinha")
        self.root.resizable(False, False)
        self.root.configure(bg=BACKGROUND)

        self.content = tk.Frame(root, bg=BACKGROUND)
        self.content.pack(padx=24, pady=22)

        tk.Label(
            self.content,
            text="COBRINHA",
            font=("Segoe UI", 20, "bold"),
            bg=BACKGROUND,
            fg="#f8fafc",
        ).pack(anchor="w")
        tk.Label(
            self.content,
            text="Coma, cresça e não bata.",
            font=("Segoe UI", 10),
            bg=BACKGROUND,
            fg="#94a3b8",
        ).pack(anchor="w", pady=(2, 16))

        score_panel = tk.Frame(self.content, bg=SURFACE)
        score_panel.pack(fill="x", pady=(0, 12))

        score_current = tk.Frame(score_panel, bg=SURFACE)
        score_current.pack(side="left", padx=14, pady=10)
        tk.Label(
            score_current,
            text="PONTUAÇÃO",
            font=("Segoe UI", 8, "bold"),
            bg=SURFACE,
            fg="#94a3b8",
        ).pack(anchor="w")
        self.score_label = tk.Label(
            score_current,
            text="0",
            font=("Segoe UI", 16, "bold"),
            bg=SURFACE,
            fg=ACCENT,
        )
        self.score_label.pack(anchor="w")

        best_score_panel = tk.Frame(score_panel, bg=SURFACE)
        best_score_panel.pack(side="right", padx=14, pady=10)
        tk.Label(
            best_score_panel,
            text="RECORDE",
            font=("Segoe UI", 8, "bold"),
            bg=SURFACE,
            fg="#94a3b8",
        ).pack(anchor="e")
        self.best_score_label = tk.Label(
            best_score_panel,
            text="0",
            font=("Segoe UI", 16, "bold"),
            bg=SURFACE,
            fg="#f8fafc",
        )
        self.best_score_label.pack(anchor="e")

        board_frame = tk.Frame(self.content, bg="#263449", padx=5, pady=5)
        board_frame.pack()
        self.canvas = tk.Canvas(
            board_frame,
            width=BOARD_SIZE,
            height=BOARD_SIZE,
            bg=BOARD_BACKGROUND,
            highlightthickness=0,
        )
        self.canvas.pack()

        tk.Label(
            self.content,
            text="SETAS ou W A S D   ·   ESPAÇO para jogar novamente",
            font=("Segoe UI", 8, "bold"),
            bg=BACKGROUND,
            fg="#64748b",
        ).pack(pady=(14, 0))

        self.score = 0
        self.best_score = 0
        self.running = False
        self.after_id = None
        self.last_time = 0
        self.move_accumulator = 0
        self.restart_button = None

        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)

        self.reset_game()

    def reset_game(self):
        self.score = 0
        self.move_accumulator = 0
        self.last_time = 0
        self.running = True
        self.canvas.delete("game_over")

        if self.restart_button is not None:
            self.restart_button.destroy()
            self.restart_button = None

        self.snake = Snake(self.canvas)
        self.food = Food(self.canvas, self.snake)
        self.update_score()
        self.draw_board()

        if self.after_id is not None:
            self.root.after_cancel(self.after_id)

        self.after_id = self.root.after(INITIAL_SPEED, self.game_loop)

    def update_score(self):
        self.score_label.config(text=str(self.score))
        self.best_score_label.config(text=str(max(self.best_score, self.score)))

    def draw_board(self):
        self.canvas.delete("all")
        for row, y in enumerate(range(0, BOARD_SIZE, GRID_SIZE)):
            for column, x in enumerate(range(0, BOARD_SIZE, GRID_SIZE)):
                self.canvas.create_rectangle(
                    x,
                    y,
                    x + GRID_SIZE,
                    y + GRID_SIZE,
                    outline="",
                    fill=GRID_LIGHT if (row + column) % 2 == 0 else GRID_DARK,
                )

        self.snake.draw()
        self.food.draw()

    def end_game(self):
        self.running = False
        self.best_score = max(self.best_score, self.score)
        self.update_score()
        self.canvas.create_text(
            BOARD_SIZE / 2,
            BOARD_SIZE / 2 - 30,
            text="Fim de jogo",
            fill="#f8fafc",
            font=("Segoe UI", 22, "bold"),
            tags="game_over",
        )
        self.canvas.create_text(
            BOARD_SIZE / 2,
            BOARD_SIZE / 2,
            text=f"Pontuação: {self.score}",
            fill="#cbd5e1",
            font=("Segoe UI", 12),
            tags="game_over",
        )

        if self.restart_button is None:
            self.restart_button = tk.Button(
                self.content,
                text="JOGAR NOVAMENTE",
                command=self.reset_game,
                bg=ACCENT,
                fg="#1a2e05",
                activebackground="#bef264",
                activeforeground="#1a2e05",
                font=("Segoe UI", 10, "bold"),
                padx=16,
                pady=9,
                relief="flat",
                borderwidth=0,
                cursor="hand2",
            )
            self.restart_button.pack(pady=(12, 0), fill="x")

    def check_food(self):
        if self.snake.head() == self.food.position:
            self.score += 10
            self.update_score()
            self.snake.grow()
            self.food.spawn()
            self.draw_board()

    def game_loop(self):
        if not self.running:
            return

        self.snake.update_direction()
        next_head = (
            self.snake.head()[0] + self.snake.direction[0],
            self.snake.head()[1] + self.snake.direction[1],
        )

        if (
            next_head[0] < 0
            or next_head[1] < 0
            or next_head[0] >= COLS
            or next_head[1] >= ROWS
            or next_head in self.snake.body[:-1]
        ):
            self.end_game()
            return

        self.snake.grow()
        if next_head == self.food.position:
            self.score += 10
            self.update_score()
            self.food.spawn()
        else:
            self.snake.body.pop()

        self.draw_board()
        self.after_id = self.root.after(INITIAL_SPEED, self.game_loop)

    def on_key_press(self, event):
        key = event.keysym.lower()

        if key == "space" and not self.running:
            self.reset_game()
            return

        if key == "up" or key == "w":
            self.snake.set_direction((0, -1))
        elif key == "down" or key == "s":
            self.snake.set_direction((0, 1))
        elif key == "left" or key == "a":
            self.snake.set_direction((-1, 0))
        elif key == "right" or key == "d":
            self.snake.set_direction((1, 0))

    def on_key_release(self, event):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()