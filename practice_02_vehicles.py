from abc import ABC, abstractmethod


class Vehicle(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def describe(self):
        """Возвращает описание транспорта."""


class Car(Vehicle):
    def describe(self):
        return f"{self.name} — легковой автомобиль для поездок по дороге."


class Bicycle(Vehicle):
    def describe(self):
        return f"{self.name} — велосипед с педальным приводом."


class Boat(Vehicle):
    def describe(self):
        return f"{self.name} — лодка для передвижения по воде."


if __name__ == "__main__":
    for vehicle in (Car("Лада"), Bicycle("Стелс"), Boat("Волна")):
        print(vehicle.describe())
