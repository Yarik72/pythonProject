from math import pi, sqrt


class Figure:
    sides_count = 0

    def __init__(self, color, *sides):
        self.__sides = sides
        self.__color = color
        self.filed = False
        if len(sides) == self.sides_count:
            self.__sides = list(sides)
        else:
            self.__sides = list(sides * self.sides_count)

    def get_color(self):
        return self.__color

    def __is_valid_color(self, r, g, b):
        return \
            (isinstance(r, int)
             and isinstance(g, int)
             and isinstance(b, int)
             and 0 <= r <= 255
             and 0 <= g <= 255
             and 0 <= b <= 255)

    def set_color(self, r, g, b):
        if self.__is_valid_color(r, g, b):
            self.__color = [r, g, b]

    def __is_valid_sides(self, *sides):
        # Проверка количества сторон
        if len(sides) != self.sides_count:
            return False

        # Проверка каждого значения стороны
        for side in sides:
            # Проверка типа данных (должно быть целым числом)
            if not isinstance(side, int):
                return False

            # Проверка значения (должно быть больше 0)
            if side <= 0:
                return False

        # Если все проверки пройдены, то стороны валидны
        return True

    def get_sides(self):
        return self.__sides

    def __len__(self):
        return sum(self.__sides)

    def set_sides(self, *new_sides):
        if self.__is_valid_sides(*new_sides):
            self.__sides = list(new_sides)


class Circle(Figure):
    sides_count = 1

    def __init__(self, color, *sides):
        super().__init__(color, *sides)
        self.__radius = self.get_sides()[0] / (2 * pi)

    def get_square(self):
        return pi * (self.__radius ** 2)


class Triangle(Figure):
    sides_count = 3

    def __init__(self, color, *sides):
        super().__init__(color, *sides)
        self.__height = self.__calculate_height()

    def __calculate_height(self):
        a, b, c = self.get_sides()
        s = (a + b + c) / 2
        return (2 / a) * sqrt(s * ((s - a) * (s - b) * (s - c)))

    def get_square(self):
        a, b, c = self.get_sides()
        return 0.5 * a * self.__height


class Cube(Figure):
    sides_count = 12

    def __init__(self, color, *sides):
        super().__init__(color, *sides)

    def get_volume(self):
        side = self.get_sides()[0]
        return side ** 3


circle1 = Circle((200, 200, 100), 10)  # (Цвет, стороны)
cube1 = Cube((222, 35, 130), 6)
triangle1 = Triangle((100, 100, 100), 5)

# Проверка на изменение цветов:
circle1.set_color(55, 66, 77)  # Изменится
print(circle1.get_color())
cube1.set_color(300, 70, 15)  # Не изменится
print(cube1.get_color())

# Проверка на изменение сторон:
cube1.set_sides(5, 3, 12, 4, 5)  # Не изменится
print(cube1.get_sides())
circle1.set_sides(15)  # Изменится
print(circle1.get_sides())

# Проверка периметра (круга), это и есть длина:
print(len(circle1))

# Проверка объёма (куба):
print(cube1.get_volume())

# Выходные данные (консоль):
# [55, 66, 77]
# [222, 35, 130]
# [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]
# [15]
# 15
# 216
