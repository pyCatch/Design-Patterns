# ISP - принцип разделения интерфейса
# Идея:
#     - не стоит добавлять слишком много программых членов (напр. методов в интерфейс)
# Допустим, что нам нужно разработать машину для сканирования, отправки факсов, печати и т.д.
# Мжет показаться хорошей идеей разработать один большой интерфейс,
# позволив клиентам реализовать его так как они захотят
from abc import abstractmethod

import abstract as abstract


class Machine:
    # Такой интерфейс может показаться хорошей идеей, если вы делаете многофункциональный принтер, тогда все впорядке
    def print(self, document):
        raise NotImplementedError

    def fax(self, document):
        raise NotImplementedError

    def scan(self, document):
        raise NotImplementedError


# Реализуем МФУ
class MultiFunctionPrinter(Machine):
    def print(self, document):
        pass

    def fax(self, document):
        pass

    def scan(self, document):
        pass


# Проблемы возникают когда мы заходим сделать следующий класса
class OldFashionedPrinter(Machine):
    # В отличие от МФУ он может только печатать
    def print(self, document):
        pass

    # Что делать с остальными методами?!
    # 1. Ничего не делать
    # 2. raise NotImplementedError
    def fax(self, document):
        pass

    def scan(self, document):
        """Not supported!"""
        raise NotImplementedError('Printer cannot scan!')


# Идея разделения интерфейса заключается в следующем:
#     - вместо того что бы иметь один большой интефейс, мы стремися к детализации (мы делим интерфейс на части,
#     которые можно реализовать по отдельности)
# Решим задачу по другому
class Printer:
    @abstractmethod
    def print(self, document):
        pass


class Scanner:
    @abstractmethod
    def scan(self, document):
        pass


class MyPrinter(Printer):
    def print(self, document):
        pass


class Photocopier(Printer, Scanner):
    def print(self, document):
        pass

    def scan(self, document):
        pass


class MultiFunctionDevice(Printer, Scanner):
    @abstractmethod
    def print(self, document):
        pass

    @abstractmethod
    def scan(self, document):
        pass


class MultiFunctionMachine(MultiFunctionDevice):
    def __init__(self, printer, scanner):
        self.printer = printer
        self.scanner = scanner

    def print(self, document):
        self.printer.print(document)

    def scan(self, document):
        self.scanner.scan(document)
