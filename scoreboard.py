import logging
from turtle import Turtle

from constants import (
    DISPLAY_ALIGNMENT,
    DISPLAY_FONT,
    GAME_OVER_FONT,
    SCORE_DISPLAY_FONT,
    SCREEN_HEIGHT,
)

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("breakout_logger.log")
formatter = logging.Formatter("[%(asctime)s] - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


class ScoreDisplay(Turtle):
    def __init__(self, position):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.position = position
        self.score = 0
        self.lives = 3
        self.level = 1
        self.write_score()

    def write_score(self):
        scoreboard_format = f"{self.score}"
        lives_format = f"{"♥︎ "*self.lives + "  "*(3-self.lives)}"
        self.goto(self.position)
        self.write(scoreboard_format, align=DISPLAY_ALIGNMENT, font=SCORE_DISPLAY_FONT)
        self.forward(200)
        self.write(lives_format, align=DISPLAY_ALIGNMENT, font=DISPLAY_FONT)
        self.backward(400)
        self.write(f"Level: {self.level}", align=DISPLAY_ALIGNMENT, font=DISPLAY_FONT)


class Scoreboard:
    def __init__(self):
        self.display = ScoreDisplay((0, SCREEN_HEIGHT - 90))
        self.num_hits = 0
        self.has_hit_orange = False
        self.has_hit_red = False

    def update_score(self, points):
        self.display.score += points
        self.num_hits += 1
        self.display.clear()
        self.display.write_score()
        return self.check_first_hits(points)

    def check_first_hits(self, points):
        if (not self.has_hit_orange) and (points == 5):
            logger.info("hit first orange")
            self.has_hit_orange = True
            return True
        if (not self.has_hit_red) and (points == 7):
            logger.info("hit first red")
            self.has_hit_red = True
            return True

    def lose_life(self):
        self.display.lives -= 1
        self.display.clear()
        self.display.write_score()
        if self.display.lives > 0:
            return True
        else:
            self.game_over()
            return False

    def game_over(self):
        self.tim = Turtle()
        self.tim.color("white")
        self.tim.penup()
        self.tim.hideturtle()
        self.tim.teleport(0, 0)
        self.tim.write("GAME OVER", align=DISPLAY_ALIGNMENT, font=GAME_OVER_FONT)
