from abc import ABC, abstractmethod
import settings
import random

class DifficultyStrategy(ABC):
    @abstractmethod
    def apply_settings(self) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        pass


class EasyStrategy(DifficultyStrategy):
    def apply_settings(self) -> None:
        settings.TIME_TO_SPAWN_LOGS = 1.5
        self.BIRD_HORIZONTAL_MOVEMENT = False

    def update(self, dt: float) -> None:
        # Standard behavior, no dynamic scaling needed
        pass

class HardStrategy(DifficultyStrategy):
    def apply_settings(self) -> None:
        settings.TIME_TO_SPAWN_LOGS = 1.5
        self.BIRD_HORIZONTAL_MOVEMENT = True

    def update(self, dt: float) -> None:
        settings.TIME_TO_SPAWN_LOGS = random.uniform(0.8, 3)