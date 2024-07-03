import logging
import math
from random import choice, randint
from turtle import Turtle

import numpy as np

from constants import BRICK_WIDTH, PADDLE_WIDTH, TURTLE_HEIGHT

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("breakout_logger.log")
formatter = logging.Formatter("[%(asctime)s] - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.goto(0, 0)
        self.x_adj = choice([-13, 13])
        self.y_adj = -13
        self.move_speed = round(math.sqrt((self.x_adj) ** 2 + (self.y_adj) ** 2), 2)

    def move(self):
        new_x = self.xcor() + self.x_adj
        new_y = self.ycor() + self.y_adj
        self.goto(new_x, new_y)

    def update_adj_coords_theta_approach(self, theta):
        x = math.cos(theta)
        y = math.sin(theta)
        self.x_adj = round(x * self.move_speed, 2)
        self.y_adj = round(y * self.move_speed, 2)

    def reflect_v(self, normal_v):
        if abs(self.y_adj) < 5:
            rand_adj = randint(70, 100) / 100
            self.y_adj = (
                self.y_adj + rand_adj if self.y_adj > 0 else self.y_adj - rand_adj
            )
        current_v = np.array([self.x_adj, self.y_adj])
        normal_v = np.array(normal_v)
        reflected_v = current_v - 2 * (current_v @ normal_v) * normal_v
        self.x_adj = reflected_v[0]
        self.y_adj = reflected_v[1]

    def bounce_paddle(self, paddle):
        # For more realistic bouncing, vary the angle of the bounce depending on
        # where the ball hits the paddle
        # This article uses vector reflection for the bounces,
        # https://www.informit.com/articles/article.aspx?p=2180417&seqNum=2
        if self.xcor() < (paddle.xcor() - (PADDLE_WIDTH / 6)):
            norm_vector = [-0.196, 0.981]
        elif self.xcor() < (paddle.xcor() + (PADDLE_WIDTH / 6)):
            norm_vector = [0, 1]
        else:
            norm_vector = [0.196, 0.981]
        self.reflect_v(norm_vector)

        # Realistic bouncing where the angle varies from 45-90 degree bounce
        # depending on where the ball hits the paddle
        # d = paddle.xcor() - (PADDLE_WIDTH / 2) - self.xcor()
        # theta = ((d / PADDLE_WIDTH) - (1 / 2)) * (math.pi / 2)
        # print(f"Hit {d} distance from edge of paddle")
        # self.update_adj_coords_theta_approach(theta)

    def bounce_brick(self, brick):
        logger.debug(f"ball:({self.pos()}), brick: ({brick.pos()})")
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
            print("hello")
            logger.info("=== BOUNCED OFF OF BOTTOM ===")
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
            logger.info("=== BOUNCED OFF OF TOP ===")
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
            logger.info("=== BOUNCED OFF OF LEFT ===")
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
            logger.info("=== BOUNCED OFF OF RIGHT ===")
            self.bounce_vertical_wall()
            return True

    def bounce_vertical_wall(self):
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
        self.move_speed *= 1.2
        self.x_adj *= self.move_speed / old_speed
        self.y_adj *= self.move_speed / old_speed
