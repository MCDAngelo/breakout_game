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

    def check_hit(self, ball):
        if self.distance(ball) <= 2 * TURTLE_HEIGHT:
            return True
        # Check for hits made to corners of the brick, as .distance method
        # compares from center of turtle
        # Note that the ball roughly has diameter of TURTLE_HEIGHT
        max_x_dist_for_hit = (BRICK_WIDTH / 2) + (TURTLE_HEIGHT / 2) + abs(ball.x_adj)
        max_y_dist_for_hit = TURTLE_HEIGHT / 2 + ball.y_adj
        if (abs(self.xcor() - ball.xcor()) <= max_x_dist_for_hit) & (
            abs(self.ycor() - ball.ycor()) <= max_y_dist_for_hit
        ):
            return True
        else:
            return False


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
        self.used_bricks = []

    def reset_bricks(self):
        self.bricks = [b.reset() for b in self.used_bricks]
        self.used_bricks = []

    def remove_brick(self, b):
        self.used_bricks.append(b)
        self.bricks.remove(b)
        b.hideturtle()
