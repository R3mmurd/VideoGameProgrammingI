"""
ISPPV1 2023
Study Case: The Legend of the Princess (ARPG)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class Player.
"""

from typing import Any

from gale.command import CommandBindings
from gale.input_handler import InputData

from src.commands import (
    INTERACT,
    MOVE_DOWN,
    MOVE_LEFT,
    MOVE_RIGHT,
    MOVE_UP,
    STOP_MOVE_DOWN,
    STOP_MOVE_LEFT,
    STOP_MOVE_RIGHT,
    STOP_MOVE_UP,
    SWORD,
)
from src.Entity import Entity


class Player(Entity):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        # Edge-triggered intent: sword/take are one-shot actions resolved
        # (and cleared) by whichever player state's update() consumes them,
        # the same way jump_requested works in 05-super_martian.
        self.sword_requested = False
        self.interact_requested = False

        self.command_bindings = CommandBindings()
        self.command_bindings.bind("move_left", press=MOVE_LEFT, release=STOP_MOVE_LEFT)
        self.command_bindings.bind(
            "move_right", press=MOVE_RIGHT, release=STOP_MOVE_RIGHT
        )
        self.command_bindings.bind("move_up", press=MOVE_UP, release=STOP_MOVE_UP)
        self.command_bindings.bind("move_down", press=MOVE_DOWN, release=STOP_MOVE_DOWN)
        self.command_bindings.bind("sword", press=SWORD)
        self.command_bindings.bind("enter", press=INTERACT)

    def collides(self, target: Any) -> bool:
        """
        AABB with some slight shrinkage of the box on the top side, for
        perspective (so walking "into" the top edge of an obstacle from
        below doesn't collide until the player's feet actually reach it).
        """
        self_y = self.y + self.height / 2
        self_height = self.height - self.height / 2

        return not (
            self.x + self.width < target.x
            or self.x > target.x + target.width
            or self_y + self_height < target.y
            or self_y > target.y + target.height
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        self.command_bindings.dispatch(self, input_id, input_data)
