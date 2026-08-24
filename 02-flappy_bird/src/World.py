"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class World: the scrolling
background/ground, and the log pairs the bird must fly through.
"""

import random
from typing import List, Optional

import pygame

from gale.factory import Factory

import settings
from src.LogPair import LogPair

from src.DifficultyStrategy import DifficultyStrategy


class World:
    def __init__(self, generate_logs: bool = False) -> None:
        self.generate_logs: bool = generate_logs
        self.background_x: float = 0.0
        self.ground_x: float = 0.0
        self.logs: List[LogPair] = []
        self.logs_spawn_timer: float = 0.0
        self.last_log_y: float = -settings.LOG_HEIGHT + random.randint(0, 80) + 20 + settings.LOGS_GAP
        self.log_pair_factory: Factory = Factory(LogPair)

    def reset(self, generate_logs: bool) -> None:
        self.generate_logs = generate_logs

    def collides(self, rect: pygame.Rect) -> bool:
        if rect.bottom >= settings.VIRTUAL_HEIGHT:
            return True

        return any(log_pair.collides(rect) for log_pair in self.logs)

    def update_scored(self, rect: pygame.Rect) -> bool:
        return any(log_pair.update_scored(rect) for log_pair in self.logs)

    def update(self, dt: float, strategy: Optional[DifficultyStrategy] = None) -> None:
        if self.generate_logs:
            self.logs_spawn_timer += dt

            if self.logs_spawn_timer >= settings.TIME_TO_SPAWN_LOGS:
                self.logs_spawn_timer = 0.0
                distance = settings.MAIN_SCROLL_SPEED * settings.TIME_TO_SPAWN_LOGS
                max_delta_y = int(distance * 0.25)
                delta_y = random.randint(-max_delta_y, max_delta_y)
                y = max(
                    -settings.LOG_HEIGHT + 10 + settings.LOGS_GAP,
                    min(
                        self.last_log_y + delta_y,
                        settings.VIRTUAL_HEIGHT + 90 - settings.LOG_HEIGHT,
                    ),
                )
                self.last_log_y = y

                if strategy is not None and strategy.CLOSING_LOGS:
                    r = random.random()
                    if r < 0.2:
                        is_closing_log = True
                    else:
                        is_closing_log = False
                else:
                    is_closing_log = False
                self.logs.append(self.log_pair_factory.create(settings.VIRTUAL_WIDTH, y, { "is_closing_log": is_closing_log }))

        self.background_x += -settings.BACK_SCROLL_SPEED * dt

        if self.background_x <= -settings.BACKGROUND_LOOPING_POINT:
            self.background_x = 0

        self.ground_x += -settings.MAIN_SCROLL_SPEED * dt

        if self.ground_x <= -settings.VIRTUAL_WIDTH:
            self.ground_x = 0

        for log_pair in self.logs:
            log_pair.update(dt)

        self.logs = [log_pair for log_pair in self.logs if not log_pair.is_out_of_game()]

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(settings.TEXTURES["background"], (round(self.background_x), 0))

        for log_pair in self.logs:
            log_pair.render(surface)

        surface.blit(
            settings.TEXTURES["ground"],
            (round(self.ground_x), settings.VIRTUAL_HEIGHT - settings.GROUND_HEIGHT),
        )
