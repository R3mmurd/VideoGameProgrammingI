import random
from typing import Optional
import pygame

from gale.factory import AbstractFactory
from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

import settings
from src.Bird import Bird
from src.World import World
from src.DifficultyStrategy import DifficultyStrategy, HardStrategy
import src.powerups


class PlayingState(BaseState):
    def enter(self,
              world: Optional[World] = None,
              bird: Optional[Bird] = None,
              score: int = 0,
              strategy: Optional[DifficultyStrategy] = None,
              powerups: Optional[list] = None
    ) -> None:
        self.strategy = strategy if strategy is not None else HardStrategy()

        self.powerups = powerups if powerups is not None else []
        self.powerups_abstract_factory = AbstractFactory("src.powerups")

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
        self.bird.update(dt, self.strategy.BIRD_HORIZONTAL_MOVEMENT)
        if self.strategy.BIRD_HORIZONTAL_MOVEMENT:
            if self.bird.x < 0:
                self.bird.x = 0
            elif self.bird.x + settings.BIRD_WIDTH > settings.VIRTUAL_WIDTH:
                self.bird.x = settings.VIRTUAL_WIDTH - settings.BIRD_WIDTH
        self.world.update(dt, self.strategy)

        

        if not self.bird.invincible:
            if self.world.collides(self.bird.get_rect()):
                settings.SOUNDS["explosion"].play()
                settings.SOUNDS["hurt"].play()
                self.state_machine.change("count_down")
                return

        if self.world.update_scored(self.bird.get_rect()):
            self.score += 1
            settings.SOUNDS["score"].play()

            if random.random() < 0.1 and self.strategy.POWERUP_SPAWN and not self.bird.invincible:
                self.powerups.append(
                    self.powerups_abstract_factory.get_factory("GhostBird").create(
                        self.bird.x, 0
                    )
                )

        # Update powerups
        for powerup in self.powerups:
            powerup.update(dt)

            if powerup.collides(self.bird):
                powerup.take(self)

        # Remove powerups that are not in play
        self.powerups = [p for p in self.powerups if p.active]

    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)
        self.bird.render(surface)
        for powerup in self.powerups:
            powerup.render(surface)
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
        elif input_id == "move_left" and self.strategy.BIRD_HORIZONTAL_MOVEMENT:
            if input_data.pressed:
                self.bird.vx = -settings.BIRD_VELOCITY_X
            elif input_data.released and self.bird.vx < 0:
                self.bird.vx = 0
        elif input_id == "move_right" and self.strategy.BIRD_HORIZONTAL_MOVEMENT:
            if input_data.pressed:
                self.bird.vx = settings.BIRD_VELOCITY_X
            elif input_data.released and self.bird.vx > 0:
                self.bird.vx = 0
        elif input_id == "pause" and input_data.pressed:
            self.state_machine.change("pause", self.world, self.bird, self.score, strategy=self.strategy)