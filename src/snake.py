import time
from collections import deque
from enum import IntEnum
from turtle import Screen, Turtle

from food import FoodGenerator
from utils import Queue, animation_off


class Direction(IntEnum):
    UP = 90
    DOWN = 270
    LEFT = 180
    RIGHT = 0


class SquareTurtle(Turtle):
    body_size = 20
    stroke_color = "white"

    def __init__(
        self,
        index: int,
        x: int = 0,
        y: int = 0,
    ):
        super().__init__()
        self.index = index
        self.shape("square")
        self.penup()
        self.hideturtle()
        self.color(*self.get_color_set(index))
        self.teleport(x=x, y=y)
        self.showturtle()

    def get_color_set(self, index: int) -> tuple[str, str]:
        """Sets the fill and stroke color for the turtle, the head turtle will have a different color"""
        fill_color, stroke_color = "DarkOliveGreen3", SquareTurtle.stroke_color
        if index == 0:
            fill_color = "DarkOliveGreen2"

        return stroke_color, fill_color


class Snake:
    def __init__(self, screen: Screen):
        self.screen = screen
        self.head: SquareTurtle = None
        self.headings = deque([Direction.RIGHT])  # start with the snake moving to right
        self.positions = Queue()
        self.turtles = self.create_start_snake_dict(5)
        self.alive = True

    def bind_keys(self):
        self.screen.onkeypress(lambda: self.set_heading(Direction.UP), "w")
        self.screen.onkeypress(lambda: self.set_heading(Direction.DOWN), "s")
        self.screen.onkeypress(lambda: self.set_heading(Direction.LEFT), "a")
        self.screen.onkeypress(lambda: self.set_heading(Direction.RIGHT), "d")

    def create_start_snake_dict(self, length: int) -> list[SquareTurtle]:
        turtles = []
        with animation_off(self.screen):
            for i in range(0, length):
                t = SquareTurtle(index=i, x=-SquareTurtle.body_size * i)
                turtles.append(t)
                if i != 0:
                    # The creating order is inverted, the head is created first, don't include the head
                    self.positions.append_right(str(t.position()))
            self.head = turtles[0]
        return turtles

    def start(self, food_generator: FoodGenerator):
        time.sleep(0.1)
        self.move_forward()

        if self.head.distance(food_generator.food_position) < 5:
            last = self.turtles[-1]
            new_segment = SquareTurtle(
                index=len(self.turtles), x=last.xcor(), y=last.ycor()
            )
            self.turtles.append(new_segment)
            self.positions.append_right(str(new_segment.position()))

            print("Food is eaten. Spawn new food")
            food_generator.generate()

    def move_forward(self):
        with animation_off(self.screen):
            if self.headings:
                self.move(self.headings.popleft())
            else:
                self.move(self.head.heading())

    def set_heading(self, direction: Direction):
        self.headings.append(direction)

    def move(self, direction: int):
        if not self.alive:
            return

        if not self.is_within_arena(direction):
            self.die()
            return

        if self.is_opposite(direction):
            direction = self.head.heading()

        for i in range(len(self.turtles) - 1, 0, -1):
            prev_pos = self.turtles[i - 1].position()
            self.turtles[i].setposition(prev_pos)
        self.head.setheading(direction)
        self.head.forward(SquareTurtle.body_size)

        if self.is_biting_itself():
            # TODO: fix the moving, might get tricky
            self.die()
            return

        # Update position queue
        self.positions.append(str(self.head.position()))
        self.positions.pop()

        # self.debug_mode()

    def is_opposite(self, direction: Direction) -> bool:
        groups = [{0, 180}, {90, 270}]
        curr_heading = self.head.heading()
        return any(direction in g and curr_heading in g for g in groups)

    def is_within_arena(self, direction: int) -> bool:
        x, y = int(self.head.xcor()), int(self.head.ycor())
        # Adjust for the current move before it will take place
        # so we catch if the snake is dead with bounds
        match abs(direction):
            case 0:
                x += 20
            case 180:
                x -= 20
            case 90:
                y += 20
            case 270:
                y -= 20
            case _:
                raise ValueError(
                    f"Should not get this current heading value: {direction}"
                )

        size = 280  # TODO: fix this hardcoded size
        if abs(x) > size or abs(y) > size:
            return False
        return True

    def is_biting_itself(self) -> bool:
        return str(self.head.position()) in self.positions

    def die(self):
        """Color the snake red when it dies"""
        self.alive = False
        for t in self.turtles:
            t.color(SquareTurtle.stroke_color, "red")

    def debug_mode(self):
        self.head.clear()
        self.head.write(f"x={round(self.head.xcor())};y={round(self.head.ycor())}")
