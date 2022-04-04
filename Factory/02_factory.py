"""
    Фабрика - это реализация принципа SRP. Идея в том, что когда в классе возникает слишком много фабричных методов,
    имеет смысл перенести их в отдельный класс.
"""
from math import sin, cos


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'x:{self.x}; y:{self.y}'

    def __repr__(self):
        return self.__str__()


class PointFactory:
    """
    Таким образом у нас появилась взаимосвязь между Point и PointFactory.
    Т.е. если что-то поменяется в Point нам придется исправить всю фабрику.
    """
    @staticmethod
    def new_cartesian_point(x, y):
        return Point(x, y)

    @staticmethod
    def new_polar_point(rho, theta):
        return Point(rho * sin(theta), rho * cos(theta))


# Попробуем избавиться от зависимостей
class NewPoint:
    class Point:
        def __init__(self, x=0, y=0):
            self.x = x
            self.y = y

    def __str__(self):
        return f'x:{self.x}; y:{self.y}'

    def __repr__(self):
        return self.__str__()


class NewPointFactory:
    """
    Нас не волнует как строится точка пока мы явно не изменим ее состояние
    """
    @staticmethod
    def new_cartesian_point(x, y):
        point = Point(x, y)
        point.x = x
        point.y = y
        return point

    @staticmethod
    def new_polar_point(rho, theta):
        return Point(rho * sin(theta), rho * cos(theta))


if __name__ == '__main__':
    point_cartesian = PointFactory.new_cartesian_point(2, 3)
    point_polar = PointFactory.new_polar_point(1, 2)
    print(f'New cartesian PointFactory: {point_cartesian}')
    print(f'New polar PointFactory: {point_polar}')
