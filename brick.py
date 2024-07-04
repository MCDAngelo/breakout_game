import logging
import turtle as t

from constants import (
    BRICK_SCORING,
    BRICK_WIDTH,
    BRICK_WIDTH_FACTOR,
    NUM_BRICK_COLS,
    NUM_BRICK_ROWS,
    SCREEN_HEIGHT,
    TURTLE_HEIGHT,
)

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("breakout_logger.log")
formatter = logging.Formatter("[%(asctime)s] - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


class Brick(t.Turtle):
    def __init__(self, color, starting_pos, id):
        super().__init__()
        self.color(color)
        self.shape("square")
        self.get_points(color)
        self.penup()
        self.setheading(180)
        self.goto(starting_pos)
        self.shapesize(stretch_wid=1, stretch_len=BRICK_WIDTH_FACTOR)
        self.id = id

    def get_points(self, color):
        self.points = BRICK_SCORING.get(color)


class BrickManager:
    def __init__(self):
        self.brick_y_coords = [
            (SCREEN_HEIGHT - (i * (TURTLE_HEIGHT + 5)) - 110)
            for i in range(0, NUM_BRICK_ROWS)
        ]
        logger.info(
            f"Setting up {NUM_BRICK_ROWS} rows of bricks at: \n{self.brick_y_coords}"
        )
        self.brick_x_coords = [
            (i * (BRICK_WIDTH + 6) + 23)
            for i in range(-NUM_BRICK_COLS // 2, NUM_BRICK_COLS // 2)
        ]
        logger.info(
            f"Setting up {NUM_BRICK_COLS} columns of bricks at: \n{self.brick_x_coords}"
        )
        self.brick_colors = [i for i in BRICK_SCORING.keys() for _ in range(0, 2)]

        self.bricks = [
            Brick(color=c, starting_pos=(x, y), id=(x, y))
            for c, y in zip(reversed(self.brick_colors), reversed(self.brick_y_coords))
            for x in self.brick_x_coords
        ]
        self.used_bricks = []

    def reset_bricks(self):
        self.bricks = [b.reset() for b in self.used_bricks]
        self.used_bricks = []

    def remove_brick(self, b):
        self.used_bricks.append(b)
        self.bricks.remove(b)
        b.hideturtle()
