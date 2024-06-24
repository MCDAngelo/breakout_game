import time
import turtle as t

from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)

from brick import BrickManager
from paddle import Paddle


screen = t.Screen()
screen.setup(width=SCREEN_WIDTH * 2, height=SCREEN_HEIGHT * 2)
screen.bgcolor("black")
screen.title("My Breakout Game")
screen.tracer(n=0)
paddle = Paddle((0, -SCREEN_HEIGHT + 20))
brick_manager = BrickManager()
screen.update()

screen.listen()
screen.onkeypress(key="Left", fun=paddle.move_left)
screen.onkeypress(key="Right", fun=paddle.move_right)

game_is_on = True

while game_is_on:
    time.sleep(0.1)
    screen.update()

screen.exitonclick()
