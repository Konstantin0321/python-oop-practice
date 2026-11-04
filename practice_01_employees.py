from dataclasses import dataclass


@dataclass
class Employee:
    name: str
    base_salary: int

    def calculate_salary(self):
        return self.base_salary


@dataclass
class Manager(Employee):
    team_size: int
    bonus_per_member: int

    def calculate_salary(self):
        return super().calculate_salary() + self.team_size * self.bonus_per_member


@dataclass
class Developer(Employee):
    overtime_hours: int
    overtime_rate: int

    def calculate_salary(self):
        return super().calculate_salary() + self.overtime_hours * self.overtime_rate


if __name__ == "__main__":
    employees = [
        Employee("Анна", 50_000),
        Manager("Иван", 80_000, 5, 2_000),
        Developer("Ольга", 95_000, 6, 1_500),
    ]
    for employee in employees:
        print(f"{employee.name} — {employee.calculate_salary()} руб.")
