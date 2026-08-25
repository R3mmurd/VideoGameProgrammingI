"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class LogPair: a top log
(rendered flipped upside down) and a bottom log, LOGS_GAP pixels
apart, that scroll left together and score once the bird passes them.
"""

import pygame

import settings


class LogPair:
    def __init__(self, x: float, y: float, is_closing_log: bool = True) -> None:
        self.x: float = x
        self.y: float = y
        self.current_gap = settings.LOGS_GAP
        self.is_closing_log = is_closing_log
        self.closing = False
        self.scored: bool = False

    def get_top_rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y) - self.current_gap, settings.LOG_WIDTH, settings.LOG_HEIGHT)

    def get_bottom_rect(self) -> pygame.Rect:
        return pygame.Rect(
            round(self.x),
            round(self.y + settings.LOG_HEIGHT),
            settings.LOG_WIDTH,
            settings.LOG_HEIGHT,
        )

    def collides(self, rect: pygame.Rect) -> bool:
        return self.get_top_rect().colliderect(rect) or self.get_bottom_rect().colliderect(rect)

    def update(self, dt: float) -> None:
        self.x += -settings.MAIN_SCROLL_SPEED * dt
        if self.is_closing_log:
            if self.closing:
                self.current_gap = max(self.current_gap - 50 * dt, 0)
                if self.current_gap <= 0:
                    settings.SOUNDS["crush"].play()
                    self.closing = False
            else:
                self.current_gap = min(self.current_gap + 50 * dt, settings.LOGS_GAP)
                if self.current_gap >= settings.LOGS_GAP:
                    self.closing = True

    def is_out_of_game(self) -> bool:
        return self.x < -settings.LOG_WIDTH

    def update_scored(self, rect: pygame.Rect) -> bool:
        if self.scored:
            return False

        if rect.left > self.x + settings.LOG_WIDTH:
            self.scored = True
            return True

        return False

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(settings.TEXTURES["log_inverted"], self.get_top_rect())
        surface.blit(settings.TEXTURES["log"], self.get_bottom_rect())
