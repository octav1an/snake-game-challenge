from turtle import Screen

from arena import Arena
from food import FoodGenerator
from scoreboard import ScoreBoard
from snake import Snake

screen = Screen()
screen.setup(width=610, height=640)
screen.screensize(canvwidth=600, canvheight=600)
screen.bgcolor("black")
screen.title("Snake Game")

screen.listen()

SIZE = 290
arena = Arena(screen, SIZE)
arena.draw()

snake = Snake(screen)
snake.bind_keys()

food_generator = FoodGenerator(SIZE - 10)
food_generator.generate()

score_board = ScoreBoard()

while snake.alive:
    snake.start(food_generator)
    score_board.display(food_generator)

screen.exitonclick()
