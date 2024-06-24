import turtle as t
from constants import (
    SCREEN_HEIGHT,
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
        self.shapesize(stretch_wid=1, stretch_len=5)

    def move_left(self):
        if self.distance(x=-SCREEN_WIDTH, y=self.ycor()) > TURTLE_HEIGHT:
            self.forward(STEP)

    def move_right(self):
        if self.distance(x=SCREEN_WIDTH, y=self.ycor()) > TURTLE_HEIGHT:
            self.back(STEP)

    def move_paddle(self):
        t.onkeypress(key="Left", fun=self.move_left)
        t.onkeypress(key="Right", fun=self.move_right)

    def hit_ball(self, ball):
        if (
            (self.distance(ball) <= 45)
            & (ball.y_adj < 0)
            & (abs(ball.ycor()) < (SCREEN_HEIGHT - TURTLE_HEIGHT))
        ):
            return True
