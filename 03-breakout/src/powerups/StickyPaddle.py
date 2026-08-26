"""
ISPPV1 2023
Study Case: Breakout

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the specialization of PowerUp to make the paddle sticky.
"""

from typing import Any

import settings
from src.powerups.PowerUp import PowerUp


class StickyPaddle(PowerUp):
    """
    Power-up to make the paddle sticky.
    """

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 6)

    def take(self, play_state: Any) -> None:
        paddle = play_state.paddle

        paddle.sticky = True
        paddle.sticky_time_remaining = settings.STICKY_PADDLE_DURATION

        self.active = False
