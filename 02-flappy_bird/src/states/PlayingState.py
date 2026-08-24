from typing import Optional
import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

import settings
from src.Bird import Bird
from src.World import World
from src.DifficultyStrategy import DifficultyStrategy, HardStrategy


class PlayingState(BaseState):
    def enter(self, world: Optional[World] = None, bird: Optional[Bird] = None, score: int = 0, strategy: Optional[DifficultyStrategy] = None,
    ) -> None:
        self.strategy = strategy if strategy is not None else HardStrategy()

        self.world = world if world is not None else World()
        self.world.reset(True)
        self.bird = bird if bird is not None else Bird(
            settings.VIRTUAL_WIDTH / 2 - settings.BIRD_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 2 - settings.BIRD_HEIGHT / 2,
            settings.BIRD_WIDTH,
            settings.BIRD_HEIGHT,
        )
        self.score = score

    def update(self, dt: float) -> None:
        self.strategy.update(dt)
        self.bird.update(dt)
        self.world.update(dt)

        if self.world.collides(self.bird.get_rect()):
            settings.SOUNDS["explosion"].play()
            settings.SOUNDS["hurt"].play()
            self.state_machine.change("count_down")
            return

        if self.world.update_scored(self.bird.get_rect()):
            self.score += 1
            settings.SOUNDS["score"].play()

    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)
        self.bird.render(surface)
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
        if input_id == "jump" and input_data.pressed:
            self.bird.jump()
        elif input_id == "pause" and input_data.pressed:
            self.state_machine.change("pause", self.world, self.bird, self.score, strategy=self.strategy)