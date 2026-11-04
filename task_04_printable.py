from abc import ABC, abstractmethod

from task_03_book_methods import Book as BaseBook


class Printable(ABC):
    @abstractmethod
    def print_info(self):
        """Выводит информацию об объекте."""


class Book(BaseBook, Printable):
    def print_info(self):
        print(self.info())


if __name__ == "__main__":
    Book("Мастер и Маргарита", "Михаил Булгаков", 1967).print_info()
