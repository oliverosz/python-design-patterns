import random


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def __str__(self):
        lines = []
        for i in range(self.height):
            if i == 0 or i == self.height - 1:
                lines.append(
                    "+" + "-" * max(0, self.width - 2) + ("+" if self.width > 1 else "")
                )
            else:
                lines.append(
                    "|" + " " * max(0, self.width - 2) + ("|" if self.width > 1 else "")
                )
        return "\n".join(lines)


class RectangleGenerator:
    def __init__(self, min_width=2, max_width=10, min_height=2, max_height=10) -> None:
        self.min_width = min_width
        self.max_width = max_width
        self.min_height = min_height
        self.max_height = max_height

    def generate_rectangles(self, count):
        rectangles = list[Rectangle]()
        for _ in range(count):
            width = random.randint(self.min_width, self.max_width)
            height = random.randint(self.min_height, self.max_height)
            rectangles.append(Rectangle(width, height))
        return rectangles

    def generate_squares(self, count):
        squares = list[Rectangle]()
        for _ in range(count):
            minsize = min(self.min_width, self.min_height)
            maxsize = min(self.max_width, self.max_height)
            size = random.randint(minsize, maxsize)
            squares.append(Rectangle(size, size))
        return squares


def print_rectangles(rectangles: list[Rectangle]):
    for rectangle in rectangles:
        print(rectangle)
        print("Area:", rectangle.area())
        print()


if __name__ == "__main__":
    gen = RectangleGenerator()
    rectangles = gen.generate_rectangles(3) + gen.generate_squares(2)
    print_rectangles(rectangles)


"""Feature request:
A new type of rectangle, which gets completely filled with a user-given character.
E.g.:
****
****
****
"""
