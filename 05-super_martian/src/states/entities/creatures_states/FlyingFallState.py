"""
ISPPV1 2023
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class FlyingFallState for flying creatures.
"""

from src.states.entities.BaseEntityState import BaseEntityState


class FlyingFallState(BaseEntityState):
    def enter(self) -> None:
        self.entity.change_animation("fall")
        self.entity.vx = 0

    def update(self, dt: float) -> None:
        # Dies either by falling past the bottom of the level, or by
        # landing on solid ground/a platform mid-fall -- both read as
        # "it fell out of the sky and is gone" rather than leaving a
        # bird standing wherever it happened to hit something.
        if self.entity.on_ground or self.entity.y > self.entity.tilemap.pixel_height:
            self.entity.is_dead = True
