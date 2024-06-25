import turtle as t

from constants import (
    PADDLE_WIDTH,
    PADDLE_WIDTH_FACTOR,
    SCREEN_WIDTH,
    STEP,
    TURTLE_HEIGHT,
)


class Paddle(t.Turtle):
    def __init__(self, starting_position):
        super().__init__()
        self.color("skyblue")
        self.shape("square")
        self.penup()
        self.setheading(180)
        self.goto(starting_position)
        self.shapesize(stretch_wid=1, stretch_len=PADDLE_WIDTH_FACTOR)

    def move_left(self):
        if self.distance(x=-SCREEN_WIDTH, y=self.ycor()) > PADDLE_WIDTH:
            self.forward(STEP)

    def move_right(self):
        if self.distance(x=SCREEN_WIDTH, y=self.ycor()) > PADDLE_WIDTH:
            self.back(STEP)

    def move_paddle(self):
        t.onkeypress(key="Left", fun=self.move_left)
        t.onkeypress(key="Right", fun=self.move_right)

    def hit_ball(self, ball):
        max_y_dist_for_hit = TURTLE_HEIGHT + ball.y_adj
        if (self.distance(ball) <= max_y_dist_for_hit) & (ball.y_adj < 0):
            return True
        # Custom check for hits made by corner of paddle
        max_x_dist_for_hit = (PADDLE_WIDTH / 2) + (TURTLE_HEIGHT / 2) + abs(ball.x_adj)
        if ((self.ycor() - ball.ycor()) <= max_y_dist_for_hit) & (
            abs(self.xcor() - ball.xcor()) <= max_x_dist_for_hit
        ):
            return True
        else:
            return False
