import random
from abc import ABC, abstractmethod


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rotation_count = 0

    def area(self):
        return self.width * self.height

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

    # New method, gets called by copy.copy(rectangle)
    def __copy__(self):
        # Step 1: Create a new instance of the same class
        new_instance = Rectangle(self.width, self.height)
        # Better: this works for subclasses with the same constructor
        new_instance = self.__class__(self.width, self.height)
        # Step 2: Copy all attributes
        new_instance.__dict__.update(self.__dict__)
        # Step 3: Make custom changes
        new_instance.rotation_count = 0
        # Step 4: Return the new instance
        return new_instance

    # New method, gets called by copy.deepcopy(rectangle)
    def __deepcopy__(self, memo):
        # As this is a simple class, we can just call __copy__
        # If it had more complex attributes, we would need to call deepcopy on them
        return self.__copy__()


class FilledRectangle(Rectangle):
    def __init__(self, width, height, fill_char=""):
        super().__init__(width, height)
        self.fill_char = fill_char

    def __str__(self):
        return "\n".join([self.fill_char * self.width] * self.height)

    def __copy__(self):
        # We cannot reuse the inherited __copy__ method, as the constructor is different
        # If the fill_char param were optional in the ctor, we could use the inherited
        # __copy__ method
        new_instance = self.__class__(self.width, self.height, self.fill_char)
        new_instance.__dict__.update(self.__dict__)
        new_instance.rotation_count = 0
        return new_instance


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


# New class for storing and manipulating several rectangles
class RectangleContainer:
    def __init__(self, rectangles: list[Rectangle]) -> None:
        self.rectangles = rectangles

    def to_landscape(self):
        for rectangle in self.rectangles:
            if rectangle.height > rectangle.width:
                rectangle.rotate()

    def to_portrait(self):
        for rectangle in self.rectangles:
            if rectangle.width > rectangle.height:
                rectangle.rotate()

    # No need for custom deepcopy, as the default one calls deepcopy on every attribute


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


# Change from list[Rectangle] to RectangleContainer
def print_rectangles(container: RectangleContainer):
    for rectangle in container.rectangles:
        print(rectangle)
        print(f"Area: {rectangle.width}x{rectangle.height} = {rectangle.area()}")
        print(f"Rotations: {rectangle.rotation_count}")
        print()


def main():
    gen = RectangleGenerator()
    fgen = RectangleGenerator(rectangle_factory=FilledRectangleFactory("#"))
    rectangles = RectangleContainer(
        gen.generate_rectangles(1) + fgen.generate_rectangles(1)
    )
    print_rectangles(rectangles)
    from copy import copy, deepcopy

    shallow = copy(rectangles)
    assert shallow is not rectangles
    assert shallow.rectangles is rectangles.rectangles
    landscape = deepcopy(rectangles)
    assert landscape is not rectangles
    assert landscape.rectangles is not rectangles.rectangles
    landscape.to_landscape()
    print("Landscape:")
    print_rectangles(landscape)
    print("Original:")
    print_rectangles(rectangles)
    # Create a copy from the rotated list
    portrait = deepcopy(landscape)
    portrait.to_portrait()
    print("Portrait:")
    print_rectangles(portrait)


if __name__ == "__main__":
    main()
