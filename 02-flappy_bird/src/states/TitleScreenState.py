"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class TitleScreenState.
"""

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

import settings
from src.DifficultyStrategy import EasyStrategy, HardStrategy
from src.World import World


class TitleScreenState(BaseState):
    def enter(self) -> None:
        self.world = World()
        self.strategies = [EasyStrategy(), HardStrategy()]
        self.selected_difficulty = 0

    def update(self, dt: float) -> None:
        self.world.update(dt, self.strategies[self.selected_difficulty])

    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)
        render_text(
            surface,
            "Flappy Bird",
            settings.FONTS["flappy"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 3,
            settings.COLOR_WHITE,
            center=True,
            shadowed=True,
        )
        render_text(
            surface,
            f"{'>' if self.selected_difficulty == 0 else ' '} Easy {'<' if self.selected_difficulty == 0 else ' '}",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH / 2,
            2 * settings.VIRTUAL_HEIGHT / 3,
            settings.COLOR_WHITE,
            center=True,
            shadowed=True,
        )
        render_text(
            surface,
            f"{'>' if self.selected_difficulty == 1 else ' '} Hard {'<' if self.selected_difficulty == 1 else ' '}",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH / 2,
            2 * settings.VIRTUAL_HEIGHT / 3 + 24,
            settings.COLOR_WHITE,
            center=True,
            shadowed=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "confirm" and input_data.pressed:
            self.state_machine.change(
                "count_down", strategy=self.strategies[self.selected_difficulty]
            )
        elif input_id in {"move_up", "move_left"} and input_data.pressed:
            self.selected_difficulty = (self.selected_difficulty - 1) % len(self.strategies)
        elif input_id in {"move_down", "move_right"} and input_data.pressed:
            self.selected_difficulty = (self.selected_difficulty + 1) % len(self.strategies)
