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


class FilledRectangle(Rectangle):
    def __init__(self, width, height, fill_char):
        super().__init__(width, height)
        self.fill_char = fill_char

    def __str__(self):
        return "\n".join([self.fill_char * self.width] * self.height)


class RectangleGenerator:
    def __init__(
        self,
        min_width=2,
        max_width=10,
        min_height=2,
        max_height=10,
        fill=False,
        fill_char="*",
    ) -> None:
        self.min_width = min_width
        self.max_width = max_width
        self.min_height = min_height
        self.max_height = max_height
        self.fill = fill
        self.fill_char = fill_char
        # Problem: This can get out of hand, if we add more types of rectangles
        # Problem: This class must be modified each time we add more types of rectangles

    def create_rectangle(self, width, height):
        # New: The logic for creating a rectangle is now in a separate factory method
        if self.fill:
            return FilledRectangle(width, height, self.fill_char)
        else:
            return Rectangle(width, height)

    def generate_rectangles(self, count):
        rectangles = list[Rectangle]()
        for _ in range(count):
            width = random.randint(self.min_width, self.max_width)
            height = random.randint(self.min_height, self.max_height)
            # New: We simply call the factory method
            rectangles.append(self.create_rectangle(width, height))
        return rectangles

    def generate_squares(self, count):
        squares = list[Rectangle]()
        for _ in range(count):
            minsize = min(self.min_width, self.min_height)
            maxsize = min(self.max_width, self.max_height)
            size = random.randint(minsize, maxsize)
            # New: We simply call the factory method
            squares.append(self.create_rectangle(size, size))
        return squares


def print_rectangles(rectangles):
    for rectangle in rectangles:
        print(rectangle)
        print("Area:", rectangle.area())
        print()


if __name__ == "__main__":
    fill = input("Do you want to fill the rectangles? (y/n) ").lower() == "y"
    fill_char = ""
    if fill:
        fill_char = input("Enter the fill character: ")[0]
    gen = RectangleGenerator(fill=fill, fill_char=fill_char)
    rectangles = gen.generate_rectangles(3) + gen.generate_squares(2)
    print_rectangles(rectangles)
