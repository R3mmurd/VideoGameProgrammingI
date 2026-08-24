"""
ISPPV1 2023
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class FlyingCreature.
"""

from typing import Any, TypeVar

from src.GameEntity import GameEntity
from src.states.entities import creatures_states


class FlyingCreature(GameEntity):
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        game_level: TypeVar("GameLevel"),
        direction: str,
        **definition: Any,
    ) -> None:
        super().__init__(
            x,
            y,
            width,
            height,
            definition["texture_id"],
            game_level,
            states={
                "fly": lambda sm: creatures_states.FlyState(self, sm),
                "fall": lambda sm: creatures_states.FlyingFallState(self, sm),
            },
            animation_defs=definition["animation_defs"],
        )
        self.fly_speed = definition["fly_speed"]
        self.state_machine.change("fly", direction)
