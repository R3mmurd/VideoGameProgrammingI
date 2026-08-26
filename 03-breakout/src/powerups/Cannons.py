"""
ISPPV1 2026
Study Case: Breakout

Author: Sebastian Ramirez

This file contains the specialization of PowerUp to add two cannons to the paddle.
"""

from typing import Any

import pygame

import settings
from src.BallBase import BallBase
from src.powerups.PowerUp import PowerUp


class CannonBullet(BallBase):
    is_cannon_ball = True

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.vy = -240

    def solve_world_boundaries(self) -> None:
        if self.y + self.height < 0:
            self.active = False


class Cannons(PowerUp):
    """
    Power-up to add two cannons to the paddle.
    """

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 1)
        self.mounted = False
        self.paddle = None

    def take(self, play_state: Any) -> None:
        self.mounted = True
        self.paddle = play_state.paddle
        play_state.cannon_powerup = self

    def update(self, dt: float) -> None:
        if not self.mounted:
            super().update(dt)

    def fire(self, play_state: Any) -> None:
        if not self.mounted:
            return

        paddle = play_state.paddle
        for x in (paddle.x, paddle.x + paddle.width - 8):
            play_state.balls.append(CannonBullet(x, paddle.y - 8))

        settings.SOUNDS["paddle_hit"].stop()
        settings.SOUNDS["paddle_hit"].play()
        self.mounted = False
        self.active = False
        play_state.cannon_powerup = None

    def render(self, surface: pygame.Surface) -> None:
        if not self.mounted or self.paddle is None:
            super().render(surface)
            return

        cannon = settings.TEXTURES["cannon"]
        for x in (self.paddle.x, self.paddle.x + self.paddle.width - cannon.get_width()):
            surface.blit(cannon, (x, self.paddle.y - cannon.get_height()))
