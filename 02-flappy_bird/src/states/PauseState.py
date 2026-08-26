"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class TitleScreenState.
"""

from typing import Optional

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

import settings
from src.Bird import Bird
from src.World import World
from src.powerups.PowerUp import PowerUp

from src.DifficultyStrategy import DifficultyStrategy, EasyStrategy


class PauseState(BaseState):
    def enter(
        self,
        world: Optional[World] = None,
        bird: Optional[Bird] = None,
        score: int = 0,
        strategy: Optional[DifficultyStrategy] = None,
        powerups: Optional[list[PowerUp]] = None,
    ) -> None:
        self.strategy = strategy if strategy is not None else EasyStrategy()
        self.world = world if world is not None else World()
        self.powerups = powerups if powerups is not None else []
        self.bird = bird if bird is not None else Bird(
            settings.VIRTUAL_WIDTH / 2 - settings.BIRD_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 2 - settings.BIRD_HEIGHT / 2,
            settings.BIRD_WIDTH,
            settings.BIRD_HEIGHT,
        )
        self.invincible_timer = self.bird.invincible_timer
        self.score = score
        settings.MUSICS["powerup"].stop()
        settings.MUSICS["marios_way"].play(-1)

    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)
        self.bird.render(surface)
        for powerup in self.powerups:
            powerup.render(surface)
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
            "Press P to resume",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH / 2,
            2 * settings.VIRTUAL_HEIGHT / 3,
            settings.COLOR_WHITE,
            center=True,
            shadowed=True,
        )
        render_text(
                    surface,
                    f"Score: {self.score}",
                    settings.FONTS["flappy"],
                    20,
                    10,
                    settings.COLOR_WHITE,
                    shadowed=True,
                )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "pause" and input_data.pressed:
            self.bird.invincible_timer = self.invincible_timer
            settings.MUSICS["marios_way"].stop()
            if self.bird.invincible:
                settings.MUSICS["powerup"].play()
            else:
                settings.MUSICS["marios_way"].play(-1)
            self.state_machine.change(
                "playing",
                self.world,
                self.bird,
                self.score,
                self.strategy,
                self.powerups,
            )
            