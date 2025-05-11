from turtle import Screen, Turtle

from utils import animation_off


class Arena:
    def __init__(self, screen: Screen, size: int):
        self.screen = screen
        self.size = size

    def draw(self):
        with animation_off(self.screen):
            border_turtle = Turtle()
            border_turtle.penup()
            border_turtle.color("brown1")
            border_turtle.fillcolor("gray20")
            border_turtle.goto(-self.size, self.size)
            border_turtle.pendown()

            border_turtle.begin_fill()
            for _ in range(4):
                border_turtle.forward(self.size * 2)
                border_turtle.right(90)
            border_turtle.end_fill()

            border_turtle.hideturtle()
