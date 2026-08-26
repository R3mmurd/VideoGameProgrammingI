"""
ISPPV1 2023
Study Case: Breakout

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the specialization of PowerUp to make the bird invincible for a short period.
"""

import random
from typing import TypeVar

from gale.factory import Factory

import settings
from src.Bird import Bird
from src.powerups.PowerUp import PowerUp


class GhostBird(PowerUp):
    """
    Power-up to make the bird invincible for a short period.
    """

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 8)

    def take(self, play_state: TypeVar("PlayState")) -> None:
        bird = play_state.bird

        self.active = False
        bird.invincible = True
        bird.invincible_timer = 5  # 5 seconds of invincibility
        bird.powerup_music_fading = False
        settings.MUSICS["marios_way"].stop()
        settings.MUSICS["powerup"].play()