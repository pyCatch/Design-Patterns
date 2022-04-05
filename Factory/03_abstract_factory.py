"""
    Идея. Если у вас есть иерархия типов, то у вас может быть и соответствующая иерархия фабрик. И поэтому у нас может
    быть абстрактная фабрика в качестве базового класса других фабрик.
"""

# Предположим, что мы хотим создать автомат по продаже чая или кофе.
from abc import ABC
from collections import namedtuple
from enum import Enum, auto


class HotDrink(ABC):
    def consume(self):
        """Клиент потребляет напиток"""
        pass


class Tea(HotDrink):
    def consume(self):
        print('This tea is delicious.')


class Coffee(HotDrink):
    def consume(self):
        print('This coffee is delicious.')


# Теперь у нас есть иерархия разных типов
# Предположим, что процесс создания напитков настолько сложны, что нам необходима для этого фабрика
class HotDrinkFactory(ABC):
    def prepare(self, amount):
        pass


class TeaFactory(HotDrinkFactory):
    def prepare(self, amount):
        print(f'Put in tea bag, boil water, pour {amount}ml, enjoy!')
        return Tea()


class CoffeeFactory(HotDrinkFactory):
    def prepare(self, amount):
        print(f'Grind some beans, boil water, pour {amount}ml, enjoy!')
        return Coffee()


def make_drink(drink_type: str):
    if drink_type == 'tea':
        return TeaFactory().prepare(200)
    elif drink_type == 'coffee':
        return CoffeeFactory().prepare(50)
    else:
        return None
# Единственное, что здесь не используется то это идея абстракции. У нас есть абстрактный класс HotDrinkFactory,
# но мы им не пользуемся. На данный момент единственна причина того, что у нас есть абстрактный класс -  это дать
# предписание конкретному api говорить, что всякий раз когда у нас есть наследник, этот наследник должен иметь
# метод prepare(), который принимает amount. Это единственный плюс


# Но мы можем организовать все лучше создав отдельный компонент HotDrinkMachine, который будет использовать разные
# фабрики и помещать их в какую то коллекцию
class HotDrinkMachine:
    """В этом примере мы нарушаем OCP, но ничего лучше тут не придумаешь. Идем на это осознано"""
    class AvailableDrinks(Enum):
        COFFEE = auto()
        TEA = auto()

    factories = []
    initialized = False

    def __init__(self):
        if not self.initialized:
            self.initialized = True
            for d in self.AvailableDrinks:
                name: str = d.name[0] + d.name[1:].lower()
                factory_name = name + 'Factory'
                factory_instance = eval(factory_name)()
                FactoryInfo = namedtuple('FactoryInfo', ['factory_name', 'factory_instance'])
                # self.factories.append((name, factory_instance))
                self.factories.append(FactoryInfo(name, factory_instance))

    def make_drink(self):
        print('Available Drinks: ')
        for f in self.factories:
            # print(f[0])
            print(f.factory_name)

        s = input(f'Please pick drink (0-{len(self.factories) - 1}): ')
        idx = int(s)
        s = input(f'Specify amount')
        amount = int(s)
        # return self.factories[idx][1].prepare(amount)
        return self.factories[idx].factory_instance.prepare(amount)


if __name__ == '__main__':
    # entry = input('What kind of drink would you like?')
    # drink = make_drink(entry)
    # drink.consume()

    # Вариант2
    hdm = HotDrinkMachine()
    hdm.make_drink().consume()
    """
        Примечание. На самом деле в этом примере нет необходимости в базовом классе, нам не нужен абстрактный класс 
        HotDrinkFactory. Это благодаря тому что есть утиная типизация. Но в ЯП с строгой типизацией и в лит-ре можно 
        встретить информацию, что абстрактный класс необходим для создания фабрики, но не явл-ся обязательным в python.
        Но иметь абстрактный класс хорошая идея, потому что мы явно видим какой api мы собираемся реализовывать  
    """
