# OCP = open for extension, closed for modification.
from enum import Enum


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class Size(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


class Product:
    def __init__(self, name, color, size):
        self.size = size
        self.color = color
        self.name = name


# Допустим наше приложение должно иметь фильтрацию продукта по цвету
class ProductFilter:
    def filter_by_color(self, products, color):
        for p in products:
            if p.color == color:
                yield p
# После этого появилось требование добавить в приложение фильтрацию по размеру
# Логичным вариантом будет добавить новы метод классу ProductFilter
    def filter_by_sizes(self, products, size):
        for p in products:
            if p.size == size:
                yield p
# Добавив этот метод мы нарушили принцип открытости-закрытости.
# Согласно этому принципу, при добавлении новой функциональности
# мы должны добавлять его через раширение, а не через модификацию!
# Это означает, что после создания и тестирования конкретного класса, то не следует изменять его
# для добавления нового функционала. Вместо этого мы должны его расширить.
# Допустим нам необходимо добавить еще один фильтр по цвету и размеру. Мы добавим следующий метод...
    def filter_by_sizes_and_color(self, products, size, color):
        for p in products:
            if p.color == color and p.size == size:
                yield p
# Этот подход не маштабируемый. Его нельзя придерживаться вечно, помимо того что он нарушает OCP,
# он также приводит к взрывному росту сложности.
#  Если будут добавлены дополные критерии, то кол-во методов будет раснти с неимоверной скоростью.
# 2 критерия --> 3 метода(мин)
# 3 --> 7
# Как видно такое решение очень плохо масштабируется.
# Мы перепишем пример, для начала, не нарушая принципа OCP.
# Мы применим корпоративный шаблон проектирования "Специаикация"


# Specification
class Specification:
    """Класс лпределяет, удовлетворяет ли конкретный элемент определенному критерию."""
    def is_satisfied(self, item):
        """Это будет базовый класс, не умеющий своего функционала."""
        pass

    def __and__(self, other):
        return AndSpecification(self, other)


class Filter:
    """Базовый класс"""
    def filter(self, items, spec):
        pass


# Идея в том, что бы расширять функционал, а не модифицировать его!
# Мы наследуем классы и реализуем его функциональность.
class ColorSpecification(Specification):
    def __init__(self, color):
        self.color = color

    def is_satisfied(self, item):
        return item.color == self.color


class SizeSpecification(Specification):
    def __init__(self, size):
        self.size = size

    def is_satisfied(self, item):
        return item.size == self.size


class AndSpecification(Specification):
    """Класс комбинатор"""
    def __init__(self, *args):
        self.args = args

    def is_satisfied(self, item):
        return all(
            map(lambda spec: spec.is_satisfied(item), self.args)
        )


class BetterFilter(Filter):
    def filter(self, items, spec):
        for item in items:
            if spec.is_satisfied(item):
                yield item


# Вывод:
#   - идея принципа OCP состоит в том, что нужно избегать ситуаций, когда нужно менять код,
#   который уже был написан, протестирован и запущен в продакшен.
# Возможно код используется другими людьми и не всегда его хочется менять.
# Намного лучше определить разные базовые классы. А затем, когда нам понадобятся новые критерии для фильтрации,
# мы просто определим новые специаикации.
# Итак, мы получили болшую гибкость и более устойчивую экосистему.

if __name__ == '__main__':
    apple = Product('Apple', Color.GREEN, Size.SMALL)
    tree = Product('Tree', Color.GREEN, Size.LARGE)
    house = Product('House', Color.BLUE, Size.LARGE)

    products = [apple, tree, house]

    # Old version
    pf = ProductFilter()
    print('Green products (old):')
    for p in pf.filter_by_color(products, Color.GREEN):
        print(f' - {p.name} is green')

    # New version
    bf = BetterFilter()
    print('Green products (new):')
    green = ColorSpecification(Color.GREEN)
    for p in bf.filter(products, green):
        print(f' - {p.name} is green')

    print('Large products:')
    large = SizeSpecification(Size.LARGE)
    for p in bf.filter(products, large):
        print(f' - {p.name} is large')

    print('Large blue products:')
    large_blue = AndSpecification(large, ColorSpecification(Color.BLUE))
    large_blue_with_and = large & ColorSpecification(Color.BLUE)
    for p in bf.filter(products, large_blue):
        print(f' - {p.name} is large and blue')

    print('Large blue products (with &):')
    large_blue_with_and = large & ColorSpecification(Color.BLUE)
    for p in bf.filter(products, large_blue_with_and):
        print(f' - {p.name} is large and blue')