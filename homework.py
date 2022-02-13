from dataclasses import dataclass, fields
from typing import Sequence


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    TRAINING_INFO = (
        'Тип тренировки: {}; Длительность: {:.3f} ч.; '
        + 'Дистанция: {:.3f} км; Ср. скорость: {:.3f} км/ч; '
        + 'Потрачено ккал: {:.3f}.'
    )

    def get_message(self) -> str:
        return self.TRAINING_INFO.format(
            self.training_type, self.duration,
            self.distance, self.speed, self.calories
        )


@dataclass
class Training:
    """Базовый класс тренировки."""

    M_IN_KM = 1000
    MIN_IN_H = 60
    LEN_STEP = 0.65

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""

    MSP_MULTIPL = 18
    MSP_SUBTR = 20

    def get_spent_calories(self) -> float:
        return (
            (self.MSP_MULTIPL * self.get_mean_speed() - self.MSP_SUBTR)
            * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_H
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    WEIGHT_MULTIPL = 0.035
    COEFF_FOR_SPENT_CAL = 0.029

    height: float

    def get_spent_calories(self) -> float:
        return (
            (self.WEIGHT_MULTIPL * self.weight + (self.get_mean_speed() ** 2
             // self.height) * self.COEFF_FOR_SPENT_CAL * self.weight)
            * self.duration * self.MIN_IN_H
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    MSP_ADD = 1.1
    COEFF_FOR_SPENT_CAL = 2

    length_pool: float
    count_pool: int

    def get_mean_speed(self) -> float:
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.MSP_ADD)
            * self. COEFF_FOR_SPENT_CAL * self.weight
        )


SPORT_TYPE = {
    'SWM': (Swimming, len(fields(Swimming))),
    'RUN': (Running, len(fields(Running))),
    'WLK': (SportsWalking, len(fields(SportsWalking)))
}

EXCEPT_1 = (
    'Для расчета результатов тренировки '
    + 'класса {} передано неверное количество '
    + 'параметров: {}. Необходимо {}'
)
EXCEPT_2 = 'Код тренировки {} не распознан'


def read_package(workout_type: str, data: Sequence[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type in SPORT_TYPE:
        if len(data) == SPORT_TYPE[workout_type][1]:
            return SPORT_TYPE[workout_type][0](*data)
        else:
            raise ValueError(
                EXCEPT_1.format(workout_type, len(data),
                                SPORT_TYPE[workout_type][1])
            )
    else:
        raise ValueError(EXCEPT_2.format(workout_type))


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
