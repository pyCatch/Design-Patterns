# LSP (принцип подстановки Лисков)
# Идея:
#   - если у вас есть API, который принимает какой то базовый класс,
#     вы должны иметь возможность передать туда любой производный класс и все должно работать

class Rectangle:
    def __init__(self, width, height):
        self._height = height
        self._width = width

    # Реализуем ширину и высоту как свойства, вместо того что бы предоставить их как атрибуты
    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def area(self):
        return self._width * self._height

    def __str__(self):
        return f'Width: {self.width}, height: {self.height}'


class Square(Rectangle):
    # Сам класс не нпдо создавать, его методы setter нарушают LSP
    def __init__(self, size):
        Rectangle.__init__(self, size, size)

    @Rectangle.width.setter
    def width(self, value):
        self._width = self._height = value

    @Rectangle.height.setter
    def height(self, value):
        self._width = self._height = value


def use_it(rc):
    # Принцип Лисков нарушен, так как функция может работать только с базовым классом
    w = rc.width
    rc.height = 10
    expected = int(w * 10)
    print(f'Expected an area of {expected}, got {rc.area}')


rc = Rectangle(2, 3)
use_it(rc)

sq = Square(5)
use_it(sq)