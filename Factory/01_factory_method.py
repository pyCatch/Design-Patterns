from enum import Enum
from math import sin, cos


class CoordinateSystem(Enum):
    CARTESIAN = 1
    POLAR = 2


class Point:
    def __init__(self, a, b, system=CoordinateSystem.CARTESIAN):
        if system == CoordinateSystem.CARTESIAN:
            self.y = b
            self.x = a
        elif system == CoordinateSystem.POLAR:
            self.x = a * sin(b)
            self.y = a * cos(b)

# Итак, это очень плохой код, который нарушает принцип OCP!
# Так же мы на самом деле не имеем представления о переменных a и b. Поэтому мы пойдем другим путем и создадим
# фабричные методы


class BestPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'x:{self.x}; y:{self.y}'

    def __repr__(self):
        return f'For f-string: x:{self.x}; y:{self.y}'

    @staticmethod
    def new_cartesian_point(x, y):
        return BestPoint(x, y)

    @staticmethod
    def new_polar_point(rho, theta):
        return BestPoint(rho * sin(theta), rho * cos(theta))


"""
    Заключение! Фабричный метод - любой метод, который создает объект. 
    В нашем примере new_cartesian_point() и new_polar_point().
    В итоге вы имеем хорошую альтернативу конструктору с множеством преимуществ! Например хороший найминг.
    Так же мы избавляемся от массивного конструктора  
"""

if __name__ == '__main__':
    point = BestPoint(2, 3)     # Будет работать!
    point_cartesian = BestPoint.new_cartesian_point(2, 3)
    point_polar = BestPoint.new_polar_point(1, 2)
    print(f'Old Point: {point}')
    print(f'New cartesian BestPoint: {point_cartesian=}')
    print(f'New polar BestPoint: {point_polar=}')
