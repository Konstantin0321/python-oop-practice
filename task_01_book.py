class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def info(self):
        return f"«{self.title}», {self.author}, {self.year} г."


if __name__ == "__main__":
    print(Book("Мастер и Маргарита", "Михаил Булгаков", 1967).info())
