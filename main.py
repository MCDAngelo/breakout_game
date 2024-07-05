import logging
import time
import turtle as t

from ball import Ball
from brick import BrickManager
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, TURTLE_HEIGHT
from paddle import Paddle
from scoreboard import Scoreboard

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("breakout_logger.log")
formatter = logging.Formatter("[%(asctime)s] - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


screen = t.Screen()
screen.setup(width=SCREEN_WIDTH * 2, height=SCREEN_HEIGHT * 2)
screen.bgcolor("black")
screen.title("My Breakout Game")
screen.tracer(n=0)
logger.info("===Starting New Game===")
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
    time.sleep(0.01)
    screen.update()

    # Check if level has been completed
    if (len(brick_manager.bricks) == 0) and (scoreboard.display.level < 2):
        logger.info("Completed level 1")
        brick_manager.reset_bricks()

    else:
        logger.debug(
            f"ball position ({ball.xcor()}, {ball.ycor()}) - adj: ({ball.x_adj}, {ball.y_adj})"
        )
        # Check if player missed ball with paddle, lose a life
        if ball.ycor() <= -SCREEN_HEIGHT + ball.y_adj:
            game_is_on = scoreboard.lose_life()
            logger.info("- Lost a life")
            ball.recenter()

        # Check if ball will bounce off of paddle or walls
        elif paddle.hit_ball(ball):
            logger.info(f"Hit paddle - ball({ball.pos()}), paddle({paddle.pos()})")
            ball.bounce_paddle(paddle)
        elif ball.ycor() >= (SCREEN_HEIGHT - (TURTLE_HEIGHT / 2)):
            logger.info("Hit top wall")
            ball.bounce_horizontal_wall()
        elif (ball.xcor() <= (-SCREEN_WIDTH + (TURTLE_HEIGHT / 2))) & (ball.x_adj < 0):
            logger.info("Hit left wall")
            ball.bounce_vertical_wall()
        elif (ball.xcor() >= (SCREEN_WIDTH - (TURTLE_HEIGHT / 2))) & (ball.x_adj > 1):
            logger.info("Hit right wall ")
            ball.bounce_vertical_wall()

        # Check if hit a brick, order bricks by distance to ball
        brick_dists = {b: ball.distance(b) for b in brick_manager.bricks}
        ordered_bricks = sorted(brick_dists.items(), key=lambda x: x[1])
        for b, d in ordered_bricks:
            if d <= 37:
                logger.info(f"Checking {b.id} [{b.color()[0]}] - dist = {d:.2f}")
                if ball.bounce_brick(b):
                    logger.info(f"+ Hit brick {b.id} [{b.color()[0]}]")
                    first_hit = scoreboard.update_score(b.points)
                    brick_manager.remove_brick(b)
                    if (scoreboard.num_hits in [4, 12]) or first_hit:
                        ball.speed_up()
                    brick_dists = {}
                    ordered_bricks = []
                    break

    ball.move()

screen.exitonclick()
