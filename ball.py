from turtle import Turtle
from random import choice


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.x_adj = choice([-10, 10])
        self.y_adj = -10
        self.move_speed = 0.1

    def move(self):
        new_x = self.xcor() + self.x_adj
        new_y = self.ycor() + self.y_adj
        self.goto(new_x, new_y)

    def bounce_x(self):
        self.x_adj *= -1

    def bounce_y(self):
        self.y_adj *= -1

    def recenter(self):
        if self.y_adj > 0:
            self.y_adj *= -1
        self.goto(0, 0)
        self.bounce_x()
