from datetime import date

from task_01_book import Book as BaseBook


class Book(BaseBook):
    def __str__(self):
        return self.info()

    def __eq__(self, other):
        if not isinstance(other, Book):
            return NotImplemented
        return (self.title, self.author, self.year) == (
            other.title, other.author, other.year
        )

    @property
    def age(self):
        return date.today().year - self.year

    @classmethod
    def from_string(cls, text):
        """Создаёт книгу из строки «название | автор | год»."""
        title, author, year = (part.strip() for part in text.split("|"))
        return cls(title, author, int(year))


if __name__ == "__main__":
    book = Book.from_string("Мастер и Маргарита | Михаил Булгаков | 1967")
    print(book)
    print(f"Возраст книги в годах — {book.age}")
    print(book == Book("Мастер и Маргарита", "Михаил Булгаков", 1967))
