import time
import turtle as t

from ball import Ball
from brick import BrickManager
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, TURTLE_HEIGHT
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

    # Check if level has been completed
    if (len(brick_manager.bricks) == 0) and (scoreboard.display.level < 2):
        brick_manager.reset_bricks()

    else:
        # Check if player missed ball with paddle, lose a life
        if ball.ycor() <= -SCREEN_HEIGHT + ball.y_adj:
            # lose a life
            game_is_on = scoreboard.lose_life()
            ball.recenter()

        # Check if ball will bounce off of paddle or walls
        elif paddle.hit_ball(ball):
            print(
                f"BALL ({ball.xcor()}, {ball.ycor()}) - PADDLE ({paddle.xcor()}, {paddle.ycor()})"
            )
            print("__ HIT PADDLE ___")
            ball.bounce_paddle(paddle)
        elif ball.ycor() >= (SCREEN_HEIGHT - (TURTLE_HEIGHT / 2)):
            ball.bounce_horizontal_wall()
        elif abs(ball.xcor()) >= (SCREEN_WIDTH - (TURTLE_HEIGHT / 2)):
            ball.bounce_vertical_wall()

        # Check if hit a brick
        for b in brick_manager.bricks:
            if b.check_hit(ball):
                first_hit = scoreboard.update_score(b.points)
                brick_manager.remove_brick(b)
                # Update with method for bouncing off of brick depending on side hit
                ball.bounce_horizontal_wall()
                # ball.bounce_paddle(b)
                if (scoreboard.num_hits in [2, 3, 4, 12]) or first_hit:
                    ball.speed_up()

    ball.move()

screen.exitonclick()
