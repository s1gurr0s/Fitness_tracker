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
        'Дистанция: {:.3f} км; Ср. скорость: {:.3f} км/ч; '
        'Потрачено ккал: {:.3f}.'
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

    MEAN_SPEED_MULTIPLIER = 18
    MEAN_SPEED_SHIFT = 20

    def get_spent_calories(self) -> float:
        return (
            (
                self.MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                - self.MEAN_SPEED_SHIFT
            )
            * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_H
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    WEIGHT_MULTIPLIER_1 = 0.035
    WEIGHT_MULTIPLIER_2 = 0.029

    height: float

    def get_spent_calories(self) -> float:
        return (
            (
                self.WEIGHT_MULTIPLIER_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.WEIGHT_MULTIPLIER_2 * self.weight
            )
            * self.duration * self.MIN_IN_H
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    MEAN_SPEED_SHIFT = 1.1
    WEIGHT_MULTIPLIER = 2

    length_pool: float
    count_pool: int

    def get_mean_speed(self) -> float:
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.MEAN_SPEED_SHIFT)
            * self. WEIGHT_MULTIPLIER * self.weight
        )


SPORTS_TYPE_DATA = {
    'SWM': (Swimming, len(fields(Swimming))),
    'RUN': (Running, len(fields(Running))),
    'WLK': (SportsWalking, len(fields(SportsWalking)))
}

WRONG_WORKOUT_TYPE = 'Код тренировки {} не распознан'
WRONG_NUMBER_OF_PARAMETERS = (
    'Для расчета результатов тренировки '
    'класса {} передано неверное количество '
    'параметров: {}. Необходимо {}'
)


def read_package(workout_type: str, data: Sequence[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in SPORTS_TYPE_DATA:
        raise ValueError(WRONG_WORKOUT_TYPE.format(workout_type))
    else:
        SPORTS_TYPE_DATA.get(workout_type)
        if len(data) != SPORTS_TYPE_DATA.get(workout_type)[1]:
            raise ValueError(
                WRONG_NUMBER_OF_PARAMETERS.format(
                    workout_type, len(data),
                    SPORTS_TYPE_DATA[workout_type][1]
                )
            )
        else:
            return SPORTS_TYPE_DATA[workout_type][0](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40, 50]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
