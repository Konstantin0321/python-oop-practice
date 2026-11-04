from dataclasses import dataclass
from random import Random


@dataclass
class SpaceShip:
    fuel: int
    hull: int = 100
    speed: int = 0

    def accelerate(self, fuel_used):
        if not 0 < fuel_used <= self.fuel:
            raise ValueError("Недостаточно топлива для разгона.")
        self.fuel -= fuel_used
        self.speed += 10 * fuel_used

    def take_damage(self, damage):
        self.hull = max(0, self.hull - damage)


@dataclass
class CrewMember:
    name: str
    role: str
    skills: dict[str, int]
    health: int = 100

    def injure(self, damage):
        self.health = max(0, self.health - damage)


class Mission:
    def __init__(self, goal, target_distance, supplies, rng=None):
        self.goal = goal
        self.target_distance = target_distance
        self.supplies = supplies.copy()
        self.distance = 0
        self.rng = rng if rng is not None else Random()
        self.events = (self.asteroid, self.engine_failure, self.quiet_turn)

    def asteroid(self, ship, crew):
        evasion = max(
            (member.skills.get("пилотирование", 0)
             for member in crew if member.role == "пилот" and member.health > 0),
            default=0,
        )
        damage = max(0, 30 - evasion)
        ship.take_damage(damage)
        for member in crew:
            member.injure(damage // 2)
        return f"Астероид. Повреждение корпуса — {damage}."

    def engine_failure(self, ship, crew):
        engineer = any(
            member.role == "инженер" and member.health > 0
            and member.skills.get("ремонт", 0) >= 20
            for member in crew
        )
        if engineer and self.supplies.get("запчасти", 0) > 0:
            self.supplies["запчасти"] -= 1
            return "Инженер восстановил двигатель."
        ship.speed //= 2
        ship.take_damage(15)
        return "Авария двигателя. Скорость упала, корпус повреждён."

    def quiet_turn(self, ship, crew):
        return "Спокойный участок маршрута."

    def run(self, ship, crew):
        print(self.goal)
        while ship.hull > 0 and any(member.health > 0 for member in crew):
            if ship.fuel:
                ship.accelerate(min(2, ship.fuel))

            print(self.rng.choice(self.events)(ship, crew))
            if ship.hull == 0 or not any(member.health > 0 for member in crew):
                break

            self.distance += ship.speed
            print(f"Путь — {self.distance}/{self.target_distance}, "
                  f"топливо — {ship.fuel}, корпус — {ship.hull}, "
                  f"скорость — {ship.speed}")
            if self.distance >= self.target_distance:
                return True
            if ship.speed == 0 and ship.fuel == 0:
                break
        return False


if __name__ == "__main__":
    ship = SpaceShip(fuel=12)
    crew = [
        CrewMember("Анна", "пилот", {"пилотирование": 22}),
        CrewMember("Иван", "инженер", {"ремонт": 25}),
    ]
    mission = Mission("Долететь до орбитальной станции", 160, {"запчасти": 2}, Random(7))
    print("Миссия выполнена." if mission.run(ship, crew) else "Миссия прервана.")
