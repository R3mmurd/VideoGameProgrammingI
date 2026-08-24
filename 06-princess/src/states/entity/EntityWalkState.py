"""
ISPPV1 2023
Study Case: The Legend of the Princess (ARPG)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class EntityWalkState.
"""

import random
from typing import TypeVar

import pygame

from src import commands
from src.states.entity.BaseEntityState import BaseEntityState
from src.states.entity.movement import move_and_bump

_DIRECTIONS = ["left", "right", "up", "down"]

# The same Command instances Player binds to InputHandler -- executed
# directly from process_ai instead of through a press/release event.
_MOVE_COMMANDS = {
    "left": commands.MOVE_LEFT,
    "right": commands.MOVE_RIGHT,
    "up": commands.MOVE_UP,
    "down": commands.MOVE_DOWN,
}
_STOP_COMMANDS = (
    commands.STOP_MOVE_LEFT,
    commands.STOP_MOVE_RIGHT,
    commands.STOP_MOVE_UP,
    commands.STOP_MOVE_DOWN,
)


class EntityWalkState(BaseEntityState):
    def enter(self) -> None:
        self.entity.change_animation("walk-down")

        # Used for AI control.
        self.move_duration = 0
        self.movement_timer = 0

        # Keeps track of whether we just hit a wall.
        self.bumped = False

    def update(self, dt: float) -> None:
        entity = self.entity
        held = entity.held

        if held["move_left"]:
            entity.direction = "left"
        elif held["move_right"]:
            entity.direction = "right"
        elif held["move_up"]:
            entity.direction = "up"
        elif held["move_down"]:
            entity.direction = "down"

        self.bumped = move_and_bump(entity, dt)

    def _pick_direction(self) -> None:
        # Only one direction is ever held at a time -- release the other
        # three before pressing the new one, the same way a player would.
        for stop in _STOP_COMMANDS:
            stop.execute(self.entity)

        direction = random.choice(_DIRECTIONS)
        _MOVE_COMMANDS[direction].execute(self.entity)
        self.entity.change_animation(f"walk-{direction}")

    def process_ai(self, room: TypeVar("Room"), dt: float) -> None:
        if self.move_duration == 0 or self.bumped:
            self.move_duration = random.randint(1, 5)
            self._pick_direction()
        elif self.movement_timer > self.move_duration:
            self.movement_timer = 0

            # Chance to go idle.
            if random.randint(1, 3) == 1:
                self.entity.change_state("idle")
                return

            self.move_duration = random.randint(1, 5)
            self._pick_direction()

        self.movement_timer += dt

    def render(self, surface: pygame.Surface) -> None:
        anim = self.entity.current_animation
        self.entity.render_sprite(surface, anim.texture_id, anim.get_current_frame())
