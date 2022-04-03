# Строитель - представляет лаконичный API для поэтапного конструирования сложного объекта
# Пример: будем строить html-элементы

# Рассмотрим простой пример - создание абзаца
text = 'hello'
parts = ['<p>', text, '</p>']
print(''.join(parts))

# Рассмотрим более сложный сценарий - даны слова и будем создавать из них список
words = ['hello', 'world']
parts = ['<ul>']
for w in words:
    parts.append(f'  <li>{w}</li>')
parts.append('</ul>')
print('\n'.join(parts))


# Builder
class HtmlElement:
    indent_size = 2

    def __init__(self, name='', text=''):
        self.text = text
        self.name = name
        self.elements = []

    # Каждый html-элемент может иметь любое кол-во вложенных элементов.
    # Ключевым элементом HtmlElement явл-ся возможность печатать самого себя.
    # Распечатка включает также распечатку всех вложенных элементов.
    def __str(self, indent):
        lines = []
        i = ' ' * (indent * self.indent_size)
        lines.append(f'{i}<{self.name}>')

        if self.text:
            i1 = ' ' * ((indent + 1) * self.indent_size)
            lines.append(f'{i1}{self.text}')

        for e in self.elements:
            lines.append(e.__str(indent + 1))
        lines.append(f'{i}</{self.name}>')
        return '\n'.join(lines)

    def __str__(self):
        return self.__str(0)

    # На последнем этапе(после создания строителя) мы можем создать статический метод, который упростит работу с API.
    # Это нужно для того, что бы клиент мог разобраться как работать с конструктором. "Как с этим работать и с чего
    # начать?!". Поэтому мы предоставим строителя напрямую из класса через статический метод. Да это нарушает OCP
    # принцип, в каком то смысле, но мы должны понимать что между объектом и его строителем есть связь!
    # Если они не разделены на отдельные интерфейсы или части системы мы можем это реализовать!
    # Это даст альтернативный вариант работы со строителем.
    @staticmethod
    def create(name):
        return HtmlBuilder(name)


# Идея состоит в том, что если у вас есть ООС, которая является рекурсивной, и которая может хранить в себе вложенные
# элементы, Вы можете создать строителя. Это конструкция, которая может принять элемент и сконструировать его! Строитель
# будет помогать в построении элемента с помощью определенного API
class HtmlBuilder:
    def __init__(self, root_name):
        self.root_name = root_name  # Элемент верхнего уровня
        self.__root = HtmlElement(name=root_name)  # Экземпляр элемента, который мы создаем
        # Мы определили, что именно мы создаем __root, без прямого доступа к нему.
        # Но в какой-то момент доступ будет необходим.

    # Предоставим объект, который мы создаем
    def __str__(self):
        return str(self.__root)

    # Следующий этап - создание API с которым мы работаем
    def add_child(self, child_name, child_text):
        """Метод, который добавляет вложенный элемент к текущему __root, с определенным именем."""
        self.__root.elements.append(
            HtmlElement(child_name, child_text)
        )

    # В примере выше HtmlBuilder, который является специальным компонентом для создания различных html-элементов.
    # Это можно улучшить что бы сделать текучий интерфейс. Это необходимо для построения цепочки вызовов.
    # Добавим следующий класс в API
    def add_child_fluent(self, child_name, child_text):
        """Метод, который добавляет вложенный элемент к текущему __root, с определенным именем и возвращает объект"""
        self.__root.elements.append(
            HtmlElement(child_name, child_text)
        )
        return self     # Именно это позволяет строить цепочки вызовов

builder = HtmlBuilder('ul')
builder.add_child('li', 'hello')
builder.add_child('li', 'world')
print('Ordinary builder:')
print(builder)
builder_ext = HtmlBuilder('ul')
builder_ext.add_child_fluent('li', 'chain')\
    .add_child_fluent('li', 'creation')\
    .add_child_fluent('li', 'test')
print('Extended builder:')
print(builder_ext)
builder_alt = HtmlElement.create('ul')
builder_alt.add_child_fluent('li', 'Creating') \
    .add_child_fluent('li', 'from') \
    .add_child_fluent('li', 'HtmlElement')
print('builder from HtmlElement:')
print(builder_alt)


