import random
from abc import ABC, abstractmethod


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # New attribute: count the number of rotations applied
        self.rotation_count = 0

    def area(self):
        return self.width * self.height

    # New method
    def rotate(self):
        self.width, self.height = self.height, self.width
        self.rotation_count += 1

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


class FilledRectangle(Rectangle):
    def __init__(self, width, height, fill_char):
        super().__init__(width, height)
        self.fill_char = fill_char

    def __str__(self):
        return "\n".join([self.fill_char * self.width] * self.height)


class AbstractRectangleFactory(ABC):
    @abstractmethod
    def create(self, width, height) -> Rectangle:
        pass


class RectangleFactory(AbstractRectangleFactory):
    def create(self, width, height):
        return Rectangle(width, height)


class FilledRectangleFactory(AbstractRectangleFactory):
    def __init__(self, fill_char):
        self.fill_char = fill_char

    def create(self, width, height):
        return FilledRectangle(width, height, self.fill_char)


class RectangleGenerator:
    def __init__(
        self,
        min_width=2,
        max_width=6,
        min_height=2,
        max_height=6,
        rectangle_factory=RectangleFactory(),
    ) -> None:
        self.min_width = min_width
        self.max_width = max_width
        self.min_height = min_height
        self.max_height = max_height
        self.rectangle_factory = rectangle_factory

    def generate_rectangles(self, count):
        rectangles = list[Rectangle]()
        for _ in range(count):
            width = random.randint(self.min_width, self.max_width)
            height = random.randint(self.min_height, self.max_height)
            rectangles.append(self.rectangle_factory.create(width, height))
        return rectangles


def print_rectangles(rectangles: list[Rectangle]):
    for rectangle in rectangles:
        print(rectangle)
        print(f"Area: {rectangle.width}x{rectangle.height} = {rectangle.area()}")
        print(f"Rotations: {rectangle.rotation_count}")
        print()


def main1():
    gen = RectangleGenerator()
    fgen = RectangleGenerator(rectangle_factory=FilledRectangleFactory("#"))
    rectangles = gen.generate_rectangles(1) + fgen.generate_rectangles(1)
    print_rectangles(rectangles)
    rotated = rectangles  # Bug: rotated and rectangles are the same list
    for rectangle in rotated:
        rectangle.rotate()
    print("Rotated:")
    print_rectangles(rotated)
    print("Original:")
    print_rectangles(rectangles)


def main2():
    gen = RectangleGenerator()
    fgen = RectangleGenerator(rectangle_factory=FilledRectangleFactory("#"))
    rectangles = gen.generate_rectangles(1) + fgen.generate_rectangles(1)
    print_rectangles(rectangles)
    rotated = rectangles.copy()  # Bug: this is a shallow copy
    assert rotated is not rectangles
    # 2 lists but both contain references to the same Rectangle objects
    # same as writing any of these:
    # rotated = list(rectangles)
    # rotated = rectangles[:]
    # rotated = [r for r in rectangles]
    # import copy
    # rotated = copy.copy(rectangles)
    for rectangle in rotated:
        rectangle.rotate()
    print("Rotated:")
    print_rectangles(rotated)
    print("Original:")
    print_rectangles(rectangles)


def main3():
    gen = RectangleGenerator()
    fgen = RectangleGenerator(rectangle_factory=FilledRectangleFactory("#"))
    rectangles = gen.generate_rectangles(1) + fgen.generate_rectangles(1)
    print_rectangles(rectangles)
    rotated = list[Rectangle]()
    for rectangle in rectangles:
        if isinstance(rectangle, FilledRectangle):
            rotated.append(
                FilledRectangle(rectangle.width, rectangle.height, rectangle.fill_char)
            )
        else:
            rotated.append(Rectangle(rectangle.width, rectangle.height))
        # Problems:
        # - cumbersome if there are many subclasses
        # - if a new subclass is added, this code needs to be updated
        # - initialization != copying, rotation_count is not copied
    for rectangle in rotated:
        rectangle.rotate()
    print("Rotated:")
    print_rectangles(rotated)
    print("Original:")
    print_rectangles(rectangles)


def main4():
    gen = RectangleGenerator()
    fgen = RectangleGenerator(rectangle_factory=FilledRectangleFactory("#"))
    rectangles = gen.generate_rectangles(1) + fgen.generate_rectangles(1)
    print_rectangles(rectangles)
    from copy import deepcopy
    # copy.copy() creates a shallow copy
    # attributes of the clone will reference the same objects
    rotated = [r for r in rectangles]
    # copy.deepcopy() recursively copies contents of the object
    rotated = deepcopy(rectangles)
    for rectangle in rotated:
        rectangle.rotate()
    print("Rotated:")
    print_rectangles(rotated)
    print("Original:")
    print_rectangles(rectangles)
    # Create a copy from the rotated list
    rotated2 = deepcopy(rotated)
    print("Rotated copy:")
    print_rectangles(rotated2)
    # What if we want the rotation_count to be 0 in the copies?


if __name__ == "__main__":
    main4()
