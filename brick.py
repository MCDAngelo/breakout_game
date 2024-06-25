import turtle as t

from constants import (
    BRICK_SCORING,
    NUM_BRICK_COLS,
    NUM_BRICK_ROWS,
    SCREEN_HEIGHT,
    TURTLE_HEIGHT,
    BRICK_WIDTH,
    BRICK_WIDTH_FACTOR,
)


class Brick(t.Turtle):
    def __init__(self, color, starting_pos):
        super().__init__()
        self.color(color)
        self.shape("square")
        self.get_points(color)
        self.penup()
        self.setheading(180)
        self.goto(starting_pos)
        self.shapesize(stretch_wid=1, stretch_len=BRICK_WIDTH_FACTOR)

    def get_points(self, color):
        self.points = BRICK_SCORING.get(color)


class BrickManager:
    def __init__(self):
        self.brick_y_coords = [
            (SCREEN_HEIGHT - (i * (TURTLE_HEIGHT + 5)) - 110)
            for i in range(0, NUM_BRICK_ROWS)
        ]
        self.brick_x_coords = [
            (i * (BRICK_WIDTH + 5) + 25)
            for i in range(-NUM_BRICK_COLS // 2, NUM_BRICK_COLS // 2)
        ]
        self.brick_colors = [i for i in BRICK_SCORING.keys() for _ in range(0, 2)]

        self.bricks = [
            Brick(c, (x, y))
            for c, y in zip(self.brick_colors, self.brick_y_coords)
            for x in self.brick_x_coords
        ]
