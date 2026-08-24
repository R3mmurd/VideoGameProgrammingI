"""
ISPPV1 2023
Study Case: The Legend of the Princess (ARPG)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class PlayerWalkState.
"""

from typing import TypeVar

import pygame

from gale.state import StateMachine

import settings
from src.states.entity.BaseEntityState import BaseEntityState
from src.states.entity.movement import move_and_bump


class PlayerWalkState(BaseEntityState):
    def __init__(
        self,
        player: TypeVar("Player"),
        state_machine: StateMachine,
        dungeon: TypeVar("Dungeon"),
    ) -> None:
        super().__init__(player, state_machine)
        self.dungeon = dungeon

    def enter(self) -> None:
        # Render offset for spaced character sprite.
        self.entity.offset_y = 5
        self.entity.offset_x = 0

    def update(self, dt: float) -> None:
        player = self.entity

        if player.sword_requested:
            player.sword_requested = False
            player.change_state("swing-sword")
            return

        if player.interact_requested:
            player.interact_requested = False
            self.dungeon.current_room.take_adjacent_pot(player)

            if player.state_machine.current is not self:
                return

        held = player.held

        if held["move_left"]:
            player.direction = "left"
            player.change_animation("walk-left")
        elif held["move_right"]:
            player.direction = "right"
            player.change_animation("walk-right")
        elif held["move_up"]:
            player.direction = "up"
            player.change_animation("walk-up")
        elif held["move_down"]:
            player.direction = "down"
            player.change_animation("walk-down")
        else:
            player.change_state("idle")
            return

        # Perform base collision detection against walls.
        bumped = move_and_bump(player, dt)

        # If we bumped something when checking collision, check any doorway.
        if bumped:
            self._check_doorways(dt)

    def _check_doorways(self, dt: float) -> None:
        player = self.entity
        speed = player.walk_speed
        room = self.dungeon.current_room

        if player.direction == "left":
            player.x -= speed * dt

            for doorway in room.doorways:
                if doorway.open and player.collides(doorway):
                    # Shift entity to center of door to avoid phasing through wall.
                    player.y = doorway.y + 4
                    self.dungeon.begin_shifting(-settings.VIRTUAL_WIDTH, 0)

            player.x += speed * dt
        elif player.direction == "right":
            player.x += speed * dt

            for doorway in room.doorways:
                if doorway.open and player.collides(doorway):
                    player.y = doorway.y + 4
                    self.dungeon.begin_shifting(settings.VIRTUAL_WIDTH, 0)

            player.x -= speed * dt
        elif player.direction == "up":
            player.y -= speed * dt

            for doorway in room.doorways:
                if doorway.open and player.collides(doorway):
                    player.x = doorway.x + 8
                    self.dungeon.begin_shifting(0, -settings.VIRTUAL_HEIGHT)

            player.y += speed * dt
        else:
            player.y += speed * dt

            for doorway in room.doorways:
                if doorway.open and player.collides(doorway):
                    player.x = doorway.x + 8
                    self.dungeon.begin_shifting(0, settings.VIRTUAL_HEIGHT)

            player.y -= speed * dt

    def render(self, surface: pygame.Surface) -> None:
        anim = self.entity.current_animation
        self.entity.render_sprite(surface, anim.texture_id, anim.get_current_frame())
