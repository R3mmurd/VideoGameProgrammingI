"""
ISPPV1 2026
Study Case: Breakout

Author: Sebastian Ramirez

Base class for moving balls and projectiles.
"""

import random
from typing import Any, Optional, Tuple

import pygame

import settings


class BallBase:
    is_cannon_ball = False

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.width = 8
        self.height = 8

        self.vx = 0
        self.vy = 0

        self.texture = settings.TEXTURES["spritesheet"]
        self.frame = random.randint(0, 6)
        self.active = True
        self.stuck = False
        self.stuck_offset_x = 0.0

    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def solve_world_boundaries(self) -> None:
        r = self.get_collision_rect()

        if r.left < 0:
            settings.SOUNDS["wall_hit"].stop()
            settings.SOUNDS["wall_hit"].play()
            self.x = 0
            self.vx *= -1
        elif r.right > settings.VIRTUAL_WIDTH:
            settings.SOUNDS["wall_hit"].stop()
            settings.SOUNDS["wall_hit"].play()
            self.x = settings.VIRTUAL_WIDTH - self.width
            self.vx *= -1
        elif r.top < 0:
            settings.SOUNDS["wall_hit"].stop()
            settings.SOUNDS["wall_hit"].play()
            self.y = 0
            self.vy *= -1
        elif r.top > settings.VIRTUAL_HEIGHT:
            settings.SOUNDS["hurt"].play()
            self.active = False

    def collides(self, another: Any) -> bool:
        return self.get_collision_rect().colliderect(another.get_collision_rect())

    def update(self, dt: float) -> None:
        self.x += self.vx * dt
        self.y += self.vy * dt

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(
            self.texture, (self.x, self.y), settings.FRAMES["balls"][self.frame]
        )

    @staticmethod
    def get_intersection(
        r1: pygame.Rect, r2: pygame.Rect
    ) -> Optional[Tuple[int, int]]:
        if r1.x > r2.right or r1.right < r2.x or r1.bottom < r2.y or r1.y > r2.bottom:
            return None

        if r1.centerx < r2.centerx:
            x_shift = r2.x - r1.right
        else:
            x_shift = r2.right - r1.x

        if r1.centery < r2.centery:
            y_shift = r2.y - r1.bottom
        else:
            y_shift = r2.bottom - r1.y

        return (x_shift, y_shift)

    def rebound(self, another: Any) -> None:
        ball_rect = self.get_collision_rect()
        other_rect = another.get_collision_rect()
        intersection = self.get_intersection(ball_rect, other_rect)

        if intersection is None:
            return

        shift_x, shift_y = intersection
        min_shift = min(abs(shift_x), abs(shift_y))

        if min_shift == abs(shift_x):
            self.x += shift_x
            self.vx *= -1
        else:
            self.y += shift_y
            self.vy *= -1
