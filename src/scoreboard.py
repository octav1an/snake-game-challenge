from turtle import Turtle

from food import FoodGenerator

FONT = ("Arial", "11", "normal")
FONT_COLOR = "white"
ALIGNMENT = "center"


class ScoreBoard(Turtle):
    def __init__(self):
        super().__init__()
        self.color(FONT_COLOR)
        self.teleport(x=0, y=300)
        self.shapesize(stretch_len=2, stretch_wid=2)
        self.hideturtle()
        self.speed("fastest")

    def display(self, food_generator: FoodGenerator):
        self.clear()
        self.write(
            f"Score: {food_generator.count}",
            align=ALIGNMENT,
            font=FONT,
        )
