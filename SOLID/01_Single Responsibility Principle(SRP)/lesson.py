# SRP SOC
# Идея:
#   если у вас есть класс, у этого класса должна быть своя основная ответственность
#   и он не должен брать на себя другие ответсвенности.
# Пример:
class Journal:
    """Основная обязанность журнала это хранение и удаление записей."""
    def __init__(self):
        self.entries = []
        self.count = 0

    def add_entry(self, text):
        self.count += 1
        self.entries.append(f'{self.count}: {text}')

    def remove_entry(self, pos):
        del self.entries[pos]

    def __str__(self):
        return '\n'.join(self.entries)

    # Тепрь нарушим SRP возложив на журнал дополнительные ответственности
    # Далее мы добавляем вторичную ответственность сохранять себя в файл, а также загружать себя
    # Это плохая идея потому что:
    #   - в программе могут быть другие объекты у которых будут свои (или такие же) методы load, save и т.д.
    #   - в какой то момент придется централизованно изменять load, save... медоты
    #     ( напр.: добавить проверку, дано ли разрешение сохранять запись в определенный каталог )
    # Выделим ответсвенность сохранения в файл в отдельный класс
    # def save(self, filename):
    #     file = open(filename, 'w')
    #     file.write(str(self))
    #     file.close()
    #
    # def load(self, filename):
    #     pass
    #
    # def load_from_web(self, url):
    #     pass


# Мы, с помощью нового класса, реорганизуем код, что бы добиться разделения ответственности
class PersistenceManager:
    """Клас отвечает за сохранение определенного объекта в файл."""
    @staticmethod
    def save_to_file(journal, filename):
        file = open(filename, 'w')
        file.write(str(journal))
        file.close()

# ВЫВОД:
#   - НЕ перегружайте свои объекты большим колличеством обязанностей
# АНТИПАТТЕРН GodObject (собрать все что есть в один класс)


if __name__ == '__main__':
    j = Journal()
    j.add_entry('I worked today so much...')
    j.add_entry('I ate a bug')
    print(f'Journal entries: \n{j}')

    file = r'../data/journal.txt'
    PersistenceManager.save_to_file(j, file)

    with open(file) as fh:  # fh - file handle
        print(fh.read())
