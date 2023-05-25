import random
from abc import ABC, abstractmethod


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


class FilledRectangle(Rectangle):
    def __init__(self, width, height, fill_char):
        super().__init__(width, height)
        self.fill_char = fill_char

    def __str__(self):
        return "\n".join([self.fill_char * self.width] * self.height)


# New: An abstract factory class defines the interface for creating rectangles
class AbstractRectangleFactory(ABC):
    @abstractmethod
    def create(self, width, height) -> Rectangle:
        pass


# New: Concrete factory for regular Rectangle objects
class RectangleFactory(AbstractRectangleFactory):
    def create(self, width, height) -> Rectangle:
        return Rectangle(width, height)


# New: Concrete factory for FilledRectangle objects
class FilledRectangleFactory(AbstractRectangleFactory):
    def __init__(self, fill_char):
        self.fill_char = fill_char
        # Note: fill_char must be set here, not in the create method, as the creation
        # parameters are fixed by the abstract factory interface

    def create(self, width, height) -> FilledRectangle:
        return FilledRectangle(width, height, self.fill_char)


# Note: In this example, the base class of FilledRectangleFactory could be the
# RectangleFactory, without needing an abstract factory.
# In the general case, the product classes would be derived from an abstract base too:
# class EmptyRectangle(AbstractRectangle)
# class FilledRectangle(AbstractRectangle)


class RectangleGenerator:
    def __init__(
        self,
        min_width=2,
        max_width=10,
        min_height=2,
        max_height=10,
        # New parameter
        rectangle_factory: AbstractRectangleFactory = RectangleFactory(),
    ) -> None:
        self.min_width = min_width
        self.max_width = max_width
        self.min_height = min_height
        self.max_height = max_height
        # New: We inject the creation logic through a factory object
        self.rectangle_factory = rectangle_factory

    # Removed: create_rectangle(self, width, height)
    # Now we use the factory object to create the rectangles
    # When new rectangles are defined, we only need create new subclasses of the
    # abstract factory.
    # This class does not depend on the concrete Rectangle types anymore.

    def generate_rectangles(self, count):
        rectangles = list[Rectangle]()
        for _ in range(count):
            width = random.randint(self.min_width, self.max_width)
            height = random.randint(self.min_height, self.max_height)
            # New: We call the create method of the stored factory
            rectangles.append(self.rectangle_factory.create(width, height))
        return rectangles

    def generate_squares(self, count):
        squares = list[Rectangle]()
        for _ in range(count):
            minsize = min(self.min_width, self.min_height)
            maxsize = min(self.max_width, self.max_height)
            size = random.randint(minsize, maxsize)
            # New: We call the create method of the stored factory
            squares.append(self.rectangle_factory.create(size, size))
        return squares


def print_rectangles(rectangles):
    for rectangle in rectangles:
        print(rectangle)
        print("Area:", rectangle.area())
        print()


if __name__ == "__main__":
    factory: AbstractRectangleFactory  # correct type annotation
    fill = input("Do you want to fill the rectangles? (y/n) ").lower() == "y"
    if fill:
        fill_char = input("Enter the fill character: ")[0]
        # New: We create a factory for filled rectangles
        factory = FilledRectangleFactory(fill_char)
    else:
        factory = RectangleFactory()
    gen = RectangleGenerator(rectangle_factory=factory)
    rectangles = gen.generate_rectangles(3) + gen.generate_squares(2)
    print_rectangles(rectangles)
