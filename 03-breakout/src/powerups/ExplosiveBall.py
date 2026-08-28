"""
ISPPV1 2026
Study Case: Breakout

Power-up that turns the active balls into explosive projectiles.
"""

from typing import Any

import settings
from src.powerups.PowerUp import PowerUp


class ExplosiveBall(PowerUp):
    """Power-up that makes active balls destroy nearby bricks on impact."""

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 7)

    def take(self, play_state: Any) -> None:
        for ball in play_state.balls:
            ball.is_explosive = True
            ball.explosive_time_remaining = settings.EXPLOSIVE_BALL_DURATION

        self.active = False