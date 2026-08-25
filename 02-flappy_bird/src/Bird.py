"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class Bird.
"""

import pygame

import settings


class Bird:
    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        self.x: float = x
        self.y: float = y
        self.width: float = width
        self.height: float = height
        self.vy: float = 0.0
        self.vx: float = 0.0
        self.jumping: bool = False
        self.invincible: bool = False
        self.invincible_timer: float = 0.0

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y), self.width, self.height)

    def jump(self) -> None:
        self.jumping = True

    def update(self, dt: float, horizontal_movement: bool = False) -> None:
        if self.invincible:
            self.invincible_timer -= dt
            if self.invincible_timer <= 0:
                self.invincible = False

        self.vy += settings.GRAVITY * dt

        if self.jumping:
            settings.SOUNDS["jump"].play()
            self.vy = -settings.JUMP_TAKEOFF_SPEED
            self.jumping = False

        self.y += self.vy * dt
        if horizontal_movement:
            self.x += self.vx * dt

    def render(self, surface: pygame.Surface) -> None:
        if not self.invincible:
            surface.blit(settings.TEXTURES["bird"], self.get_rect())
        else:
            surface.blit(settings.TEXTURES["ghost"], self.get_rect())
