import time
import turtle as t

from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    TURTLE_HEIGHT,
)

from ball import Ball
from brick import BrickManager
from paddle import Paddle
from scoreboard import Scoreboard

screen = t.Screen()
screen.setup(width=SCREEN_WIDTH * 2, height=SCREEN_HEIGHT * 2)
screen.bgcolor("black")
screen.title("My Breakout Game")
screen.tracer(n=0)
paddle = Paddle((0, -SCREEN_HEIGHT + 20))
scoreboard = Scoreboard()
brick_manager = BrickManager()
ball = Ball()
screen.update()

screen.listen()
screen.onkeypress(key="Left", fun=paddle.move_left)
screen.onkeypress(key="Right", fun=paddle.move_right)

game_is_on = True

while game_is_on:
    time.sleep(0.1)
    screen.update()
    # Check if ball has to bounce off of walls or paddle
    if ball.ycor() + ball.y_adj > (SCREEN_HEIGHT - TURTLE_HEIGHT):
        ball.bounce_y()
    if abs(ball.xcor() + ball.x_adj) > (SCREEN_WIDTH - TURTLE_HEIGHT):
        ball.bounce_x()
    if paddle.hit_ball(ball):
        ball.bounce_y()
    # Check if player missed ball with paddle, lose a life
    if ball.ycor() < -SCREEN_HEIGHT:
        # lose a life
        ball.reset()
    # Check if hit a brick:
    for b in brick_manager.bricks:
        if b.check_hit(ball):
            scoreboard.update_score(b.points)
            brick_manager.remove_brick(b)
            # ball.bounce_x()
            ball.bounce_y()
    if len(brick_manager.bricks) == 0:
        brick_manager.reset_bricks()
    ball.move()

screen.exitonclick()
