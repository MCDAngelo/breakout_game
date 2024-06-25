from turtle import Turtle

from constants import SCREEN_HEIGHT


class ScoreDisplay(Turtle):
    def __init__(self, position):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(position)
        self.score = 0
        self.write_score()

    def write_score(self):
        self.write(self.score, align="center", font=("Courier", 80, "normal"))


class Scoreboard:
    def __init__(self):
        self.display = ScoreDisplay((0, SCREEN_HEIGHT - 90))

    def update_score(self, points):
        self.display.score += points
        self.display.clear()
        self.display.write_score()
