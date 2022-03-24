from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, List, Type

SWIM_TRAINING = 'SWM'
WALK_TRAINING = 'WLK'
RUN_TRAINING = 'RUN'


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE: ClassVar[str] = ('Тип тренировки: {training_type}; '
                              'Длительность: {duration:.3f} ч.; '
                              'Дистанция: {distance:.3f} км; '
                              'Ср. скорость: {speed:.3f} км/ч; '
                              'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MINS_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CF_RUN_1: int = 18
    CF_RUN_2: int = 20

    def get_spent_calories(self) -> float:
        return ((self.CF_RUN_1 * self.get_mean_speed() - self.CF_RUN_2)
                * self.weight / self.M_IN_KM * self.duration
                * self.MINS_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CF_WALK_1: float = 0.035
    CF_WALK_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.CF_WALK_1 * self.weight
                 + (self.get_mean_speed()**2 // self.height)
                 * self.CF_WALK_2 * self.weight)
                * (self.duration * self.MINS_IN_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""

    CF_SW_1: float = 1.1
    CF_SW_2: int = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.CF_SW_1)
                * self.CF_SW_2 * self.weight)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_types: Dict[str, Type[Training]] = {
        RUN_TRAINING: Running,
        WALK_TRAINING: SportsWalking,
        SWIM_TRAINING: Swimming
    }
    if workout_type not in workout_types:
        raise ValueError(
            f'Укажите правильный вид тренировки: {workout_types.keys()}'
        )
    return workout_types[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        (SWIM_TRAINING, [720, 1, 80, 25, 40]),
        (RUN_TRAINING, [15000, 1, 75]),
        (WALK_TRAINING, [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
