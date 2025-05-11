import random
from turtle import Turtle


class Food(Turtle):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.shape("circle")
        self.color("white", "gold")
        self.teleport(x, y)


class FoodGenerator:
    def __init__(self, size: int):
        self.size = size
        self.count = -1
        self.food = None

    @property
    def food_position(self) -> tuple[int, int]:
        return self.food.position()

    def generate(self):
        # clean old food
        if self.food:
            self.food.hideturtle()
            self.food = None

        x, y = (
            random.randrange(-self.size, self.size, 20),
            random.randrange(-self.size, self.size, 20),
        )
        self.count += 1
        self.food = Food(x, y)
        print(f"food: {self.food.position()}")
