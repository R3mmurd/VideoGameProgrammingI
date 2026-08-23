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
        settings.TIME_TO_SPAWN_LOGS = 2.0

    def update(self, dt: float) -> None:
        # Standard behavior, no dynamic scaling needed
        pass