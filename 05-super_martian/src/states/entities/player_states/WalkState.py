"""
ISPPV1 2023
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class WalkState for player.
"""

import settings
from src.states.entities.BaseEntityState import BaseEntityState


class WalkState(BaseEntityState):
    def enter(self) -> None:
        self.entity.flipped = self.entity.move_direction < 0
        self.entity.vx = settings.PLAYER_SPEED * self.entity.move_direction
        self.entity.change_animation("walk")

    def update(self, dt: float) -> None:
        if self.entity.jump_requested:
            self.entity.jump_requested = False
            self.entity.change_state("jump")
            return

        if not self.entity.on_ground:
            self.entity.change_state("fall")
            return

        if self.entity.move_direction == 0:
            self.entity.change_state("idle")
            return

        self.entity.flipped = self.entity.move_direction < 0
        self.entity.vx = settings.PLAYER_SPEED * self.entity.move_direction
