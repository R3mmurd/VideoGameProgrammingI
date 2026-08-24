"""
ISPPV1 2023
Study Case: The Legend of the Princess (ARPG)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class PlayerPotLiftState.
"""

from typing import Any, TypeVar

import pygame

from gale.state import StateMachine
from gale.timer import Timer

from src.states.entity.BaseEntityState import BaseEntityState


class PlayerPotLiftState(BaseEntityState):
    def __init__(
        self,
        player: TypeVar("Player"),
        state_machine: StateMachine,
        dungeon: TypeVar("Dungeon"),
    ) -> None:
        super().__init__(player, state_machine)
        self.dungeon = dungeon
        self.entity.change_animation(f"pot-lift-{self.entity.direction}")

    def enter(self, pot: Any) -> None:
        self.pot = pot
        self.pot.taken = True
        self.entity.current_animation.reset()
        Timer.tween(
            0.3,
            [
                (
                    self.pot,
                    {
                        "x": self.entity.x,
                        "y": self.entity.y - self.pot.height / 2,
                    },
                )
            ],
        )

    def update(self, dt: float) -> None:
        self.entity.sword_requested = False
        self.entity.interact_requested = False

        if self.entity.current_animation.times_played > 0:
            self.entity.current_animation.times_played = 0
            self.entity.change_state("pot-idle", pot=self.pot)

    def render(self, surface: pygame.Surface) -> None:
        anim = self.entity.current_animation
        self.entity.render_sprite(surface, anim.texture_id, anim.get_current_frame())
        self.pot.render(surface)
