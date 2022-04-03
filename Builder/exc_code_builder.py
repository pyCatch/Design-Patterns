# Необходимо реализовать паттерн Builder для формирования кусочков кода.
# Пример API которое необходимо поддержать:
#   cb = CodeBuilder('Person').add_field('name','""').add_field('age','0').add_field('')
#   print(cb)
# Ожидаемый вывод:
# class Person:
#     def __init__(self):
#         self.name = ""
#         self.age = 0
# Необходимо учесть пробелы и отступы
# Пример с пустым классом:
# cb = CodeBuilder('Foo')
# class Foo:
#     pass
from typing import List


class Code:
    indent_size = 4

    def __init__(self, name):
        self.name: str = name
        self.attributes: List[tuple] = []

    def create_init_body(self):
        indent = ' ' * self.indent_size * 2
        result = f'{" " * self.indent_size}def __init__(self):\n'
        for elem in self.attributes:
            result += f'{indent}self.{elem[0]} = {elem[1]}\n'
        return result

    def __str(self):
        header = f'class {self.name}:\n'
        init_body = self.create_init_body() if len(self.attributes) != 0 else f'{" " * self.indent_size}pass'
        return header + init_body

    def __str__(self):
        return self.__str()


class CodeBuilder:
    def __init__(self, root_name):
        self.root_name: str = root_name
        self.__root = Code(name=root_name)

    def add_field(self, type, name):
        self.__root.attributes.append((type, name))
        return self

    def __str__(self):
        return str(self.__root)


cb = CodeBuilder('Person').add_field('name', '""').add_field('age', '0')
print(cb)
print('EMPTY::')
empty_cd = CodeBuilder('Foo')
print(empty_cd)
