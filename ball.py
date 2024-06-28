from turtle import Turtle
from random import choice
import math
import numpy as np

from constants import PADDLE_WIDTH


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.goto(0, 0)
        self.x_adj = choice([-10, 10])
        self.y_adj = -10
        self.move_speed = round(math.sqrt((self.x_adj) ** 2 + (self.y_adj) ** 2), 2)

    def move(self):
        print(f"BALL MOVING FROM ({self.xcor()}, {self.ycor()})")
        new_x = self.xcor() + self.x_adj
        new_y = self.ycor() + self.y_adj
        self.goto(new_x, new_y)
        print(f"BALL MOVING TO ({self.xcor()}, {self.ycor()})")

    def update_adj_coords_theta_approach(self, theta):
        x = math.cos(theta)
        y = math.sin(theta)
        theta_d = theta * 180 / math.pi
        print(
            f"For angle {theta:.2f} RAD ({theta_d:.2f}deg), new direction = ({x:.2f}, {y:.2f})"
        )
        self.x_adj = round(x * self.move_speed, 2)
        self.y_adj = round(y * self.move_speed, 2)
        print(f" NEW x_adj = {self.x_adj:.2f}, y_adj = {self.y_adj:.2f}")

    def reflect_v(self, normal_v):
        current_v = np.array([self.x_adj, self.y_adj])
        normal_v = np.array(normal_v)
        print(current_v @ normal_v)
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

        # ADD RANDOM VARIATION WHEN BALL BOUNCES BACK AND FORTH HORIZONTALLY

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
        print(f"Original speed = {self.move_speed:.2f}")
        print(f"Original deltas: x= {self.x_adj}, y={self.y_adj}")
        old_speed = self.move_speed
        self.move_speed *= 1.2
        self.x_adj *= self.move_speed / old_speed
        self.y_adj *= self.move_speed / old_speed
        print(f"Updated speed = {self.move_speed:.2f}")
        print(f"New deltas: x= {self.x_adj}, y={self.y_adj}")
