import logging
import math
from random import choice
from turtle import Turtle

import numpy as np

from constants import BRICK_WIDTH, PADDLE_WIDTH, TURTLE_HEIGHT

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("breakout_logger.log")
formatter = logging.Formatter("[%(asctime)s] - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.goto(0, 0)
        self.x_adj = choice([-2.0, 2.0])
        self.y_adj = -2.0
        self.move_speed = round(math.sqrt((self.x_adj) ** 2 + (self.y_adj) ** 2), 2)

    def move(self):
        new_x = self.xcor() + self.x_adj
        new_y = self.ycor() + self.y_adj
        logger.debug(f"Ball moving from ({self.pos()}) to ({new_x:.2f}, {new_y:.2f})")
        logger.debug(f"Adjustments of x: {self.x_adj:.2f}, y {self.y_adj:.2f}")
        self.goto(new_x, new_y)

    def get_normal_vector(self, theta):
        theta = math.radians(theta)
        x = round(math.cos(theta), 2)
        y = round(math.sin(theta), 2)
        return [x, y]

    def reflect_v(self, normal_v):
        current_v = np.array([self.x_adj, self.y_adj])
        normal_v = np.array(normal_v)
        reflected_v = current_v - 2 * (current_v @ normal_v) * normal_v
        self.x_adj = reflected_v[0]
        self.y_adj = reflected_v[1]

    def bounce_paddle(self, paddle):
        # For more realistic bouncing, vary the angle of the bounce depending on
        # where the ball hits the paddle
        # The angle is interpolated based on where the ball hit the paddle,
        # the left-most side uses a normal vector at (-0.196, 0.981) for the reflection
        # the right-most side uses a normal vector at (0.196, 0.981), and the middle uses
        # a normal vector (0,1), based on the normal vectors referenced in the article below
        # https://www.informit.com/articles/article.aspx?p=2180417&seqNum=2
        if self.xcor() < (paddle.xcor() - (PADDLE_WIDTH / 2)):
            d = -PADDLE_WIDTH
        elif self.xcor() > (paddle.xcor() + (PADDLE_WIDTH / 2)):
            d = 0
        else:
            d = self.xcor() - paddle.xcor() + (PADDLE_WIDTH / 2)
        LEFT_MOST = round(math.degrees(math.acos(-0.196 / 1)), 1)
        RIGHT_MOST = round(math.degrees(math.acos(0.196 / 1)), 1)
        theta = ((d / PADDLE_WIDTH) * (LEFT_MOST - RIGHT_MOST)) + RIGHT_MOST
        norm_vector = self.get_normal_vector(theta)
        logger.info(f"Ball = ({self.pos()}), paddle = ({paddle.pos()})")
        logger.info(
            f"Hit {d:.2f} distance from edge of paddle - angle = {theta:.2f}, N = {norm_vector}"
        )
        self.reflect_v(norm_vector)

    def bounce_brick(self, brick):
        logger.info(f"ball:({self.pos()}), brick: ({brick.pos()})")
        BUFFER = 5
        yspan_for_brick = TURTLE_HEIGHT + BUFFER
        xspan_for_brick = (BRICK_WIDTH / 2) + (TURTLE_HEIGHT / 2) + BUFFER
        if (
            (brick.ycor() >= self.ycor() >= (brick.ycor() - yspan_for_brick))
            & (
                (brick.xcor() - xspan_for_brick)
                <= self.xcor()
                <= (brick.xcor() + xspan_for_brick)
            )
            & (self.y_adj > 0)
        ):
            logger.info("Bounced off of bottom of brick")
            self.bounce_horizontal_wall()
            return True
        elif (
            (brick.ycor() <= self.ycor() <= (brick.ycor() - yspan_for_brick))
            & (
                (brick.xcor() - xspan_for_brick)
                <= self.xcor()
                <= (brick.xcor() + xspan_for_brick)
            )
            & (self.y_adj < 0)
        ):
            logger.info("Bounced off of top of brick")
            self.bounce_horizontal_wall()
            return True
        elif (
            (brick.xcor() >= self.xcor() >= (brick.xcor() - xspan_for_brick))
            & (
                (brick.ycor() - yspan_for_brick)
                <= self.ycor()
                <= (brick.ycor() + yspan_for_brick)
            )
            & (self.x_adj < 0)
        ):
            logger.info("Bounced off of left side of brick")
            self.bounce_vertical_wall()
            return True
        elif (
            (brick.xcor() <= self.xcor() <= (brick.xcor() + xspan_for_brick))
            & (
                (brick.ycor() - yspan_for_brick)
                <= self.ycor()
                <= (brick.ycor() + yspan_for_brick)
            )
            & (self.x_adj > 0)
        ):
            logger.info("Bounced off of right side of brick")
            self.bounce_vertical_wall()
            return True

    def bounce_vertical_wall(self):
        if self.y_adj == 0:
            self.reflect_v(self.get_normal_vector(92))
        else:
            self.reflect_v([1, 0])

    def bounce_horizontal_wall(self):
        self.reflect_v([0, -1])

    def recenter(self):
        if self.y_adj > 0:
            self.y_adj *= -1
        self.goto(0, 0)
        self.x_adj *= -1

    def speed_up(self):
        old_speed = self.move_speed
        self.move_speed = round(old_speed * 1.2, 2)
        logger.info(f"Ball sped up from {old_speed:.2f} to {self.move_speed:.2f}")
        self.x_adj *= self.move_speed / old_speed
        self.y_adj *= self.move_speed / old_speed
        logger.info(
            f"Ball adjustments now set to x: {self.x_adj:.2f}, y: {self.y_adj:.2f}"
        )
