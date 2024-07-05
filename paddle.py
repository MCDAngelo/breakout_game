import logging
import turtle as t

from constants import (PADDLE_WIDTH, PADDLE_WIDTH_FACTOR, SCREEN_WIDTH, STEP,
                       TURTLE_HEIGHT)

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("breakout_logger.log")
formatter = logging.Formatter("[%(asctime)s] - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


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
        if self.distance(x=-SCREEN_WIDTH, y=self.ycor()) > (PADDLE_WIDTH / 2):
            self.forward(STEP)

    def move_right(self):
        if self.distance(x=SCREEN_WIDTH, y=self.ycor()) > (PADDLE_WIDTH / 2):
            self.back(STEP)

    def move_paddle(self):
        t.onkeypress(key="Left", fun=self.move_left)
        t.onkeypress(key="Right", fun=self.move_right)

    def hit_ball(self, ball):
        max_y_dist_for_hit = TURTLE_HEIGHT
        max_x_dist_for_hit = (PADDLE_WIDTH / 2) + (TURTLE_HEIGHT / 2)
        logger.info(f"Checking paddle hit - ball ({ball.pos()}, paddle ({self.pos()}))")
        logger.debug(f"max x = {max_x_dist_for_hit}, max y = {max_y_dist_for_hit}")
        logger.debug(
            f"x boundaries: {self.xcor() - max_x_dist_for_hit} {self.xcor() + max_x_dist_for_hit}"
        )
        logger.debug(f"y boundaries: {self.ycor() } {self.ycor() + max_y_dist_for_hit}")
        if ball.y_adj < 0:  # To prevent bouncing up and down off of paddle
            if (
                (self.xcor() - max_x_dist_for_hit)
                <= ball.xcor()
                <= (self.xcor() + max_x_dist_for_hit)
            ) & ((self.ycor()) <= ball.ycor() <= (self.ycor() + max_y_dist_for_hit)):
                return True
