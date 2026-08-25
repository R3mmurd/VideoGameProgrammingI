"""
ISPPV1 2023
Study Case: Breakout

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the base class PowerUp as an abstract class.
"""

from typing import TypeVar, Any

import pygame

import settings


class PowerUp:
    """
    The base power-up.
    """

    def __init__(self, x: int, y: int, frame: int) -> None:
        self.x = x
        self.y = y
        self.vy = settings.MAIN_SCROLL_SPEED
        self.active = True
        self.frame = frame

    def get_rect(self) -> pygame.Rect:
            return pygame.Rect(self.x, self.y, 30, 30)

    def collides(self, obj: Any) -> bool:
        return self.get_rect().colliderect(obj.get_rect())

    def update(self, dt: float) -> None:
        if self.y > settings.VIRTUAL_HEIGHT:
            self.active = False

        self.y += self.vy * dt
    
    def render(self, surface: pygame.Surface) -> None:
        surface.blit(settings.TEXTURES["powerup"], self.get_rect())

    def take(self, play_state: TypeVar("PlayState")) -> None:
        raise NotImplementedError
