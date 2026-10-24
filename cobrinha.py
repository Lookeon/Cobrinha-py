import random
import tkinter as tk

BOARD_SIZE = 280
GRID_SIZE = 28
COLS = BOARD_SIZE // GRID_SIZE
ROWS = BOARD_SIZE // GRID_SIZE
INITIAL_SPEED = 170


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
            color = "#a3e635" if index == 0 else "#65a30d"
            x1 = x * GRID_SIZE
            y1 = y * GRID_SIZE
            self.canvas.create_rectangle(
                x1 + 1,
                y1 + 1,
                x1 + GRID_SIZE - 1,
                y1 + GRID_SIZE - 1,
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
            x1 + 3,
            y1 + 3,
            x1 + GRID_SIZE - 3,
            y1 + GRID_SIZE - 3,
            fill="#ef4444",
            outline="#b91c1c",
            tags="food",
        )


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake OOP")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=BOARD_SIZE, height=BOARD_SIZE, bg="#0b1120", highlightthickness=0)
        self.canvas.pack()

        self.score_label = tk.Label(root, text="Pontuação: 0", font=("Arial", 16, "bold"), bg="#111827", fg="white")
        self.score_label.pack(pady=(8, 0))

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
        self.score_label.config(text=f"Pontuação: {self.score}")

    def draw_board(self):
        self.canvas.delete("all")
        for x in range(0, BOARD_SIZE, GRID_SIZE):
            for y in range(0, BOARD_SIZE, GRID_SIZE):
                self.canvas.create_rectangle(
                    x,
                    y,
                    x + GRID_SIZE,
                    y + GRID_SIZE,
                    outline="#94a3b8",
                    fill="#0b1120",
                    width=1,
                )

        self.snake.draw()
        self.food.draw()

    def end_game(self):
        self.running = False
        self.best_score = max(self.best_score, self.score)
        self.canvas.create_text(
            BOARD_SIZE / 2,
            BOARD_SIZE / 2 - 30,
            text="Fim de jogo",
            fill="white",
            font=("Arial", 22, "bold"),
            tags="game_over",
        )
        self.canvas.create_text(
            BOARD_SIZE / 2,
            BOARD_SIZE / 2,
            text=f"Pontuação: {self.score}",
            fill="white",
            font=("Arial", 16),
            tags="game_over",
        )

        if self.restart_button is None:
            self.restart_button = tk.Button(
                self.root,
                text="Jogar novamente",
                command=self.reset_game,
                bg="#a3e635",
                fg="#0b1120",
                font=("Arial", 12, "bold"),
                padx=18,
                pady=8,
            )
            self.restart_button.pack(pady=(8, 0))

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