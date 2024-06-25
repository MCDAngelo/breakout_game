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
        if self.distance(x=-SCREEN_WIDTH, y=self.ycor()) > PADDLE_WIDTH / 2:
            self.forward(STEP)

    def move_right(self):
        if self.distance(x=SCREEN_WIDTH, y=self.ycor()) > PADDLE_WIDTH / 2:
            self.back(STEP)

    def move_paddle(self):
        t.onkeypress(key="Left", fun=self.move_left)
        t.onkeypress(key="Right", fun=self.move_right)

    def hit_ball(self, ball):
        max_y_dist_for_hit = TURTLE_HEIGHT + (abs(ball.y_adj) / 2)
        max_x_dist_for_hit = (PADDLE_WIDTH / 2) + (TURTLE_HEIGHT / 2)
        if ball.y_adj < 0:
            if self.distance(ball) <= max_y_dist_for_hit:
                return True
            # Custom check for hits made by corner of paddle
            if ((ball.ycor() - self.ycor()) < max_y_dist_for_hit) & (
                abs(self.xcor() - ball.xcor()) < max_x_dist_for_hit
            ):
                return True
