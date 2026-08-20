"""
ISPPV1 2023
Study Case: Pong

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class PlayState.
"""

import random

import pygame

from gale.input_handler import InputData
from gale.state import BaseState

import settings
from src.rendering import render_table


class PlayState(BaseState):
    def enter(self, pong) -> None:
        self.pong = pong
        self.AI_ERROR = 0.0 # AI error factor, to make the game winnable

    def update(self, dt: float) -> None:
        pong = self.pong
        pong.player1.update(dt)
        pong.player2.update(dt)
        pong.ball.update(dt)

        # Move player2 if ball is moving towards it, otherwise stop it. (bot)
        if pong.ball.vx > 0 and pong.ball.x > settings.VIRTUAL_WIDTH / 2:
            if pong.ball.y < pong.player2.y - self.AI_ERROR * settings.PADDLE_HEIGHT:
                pong.player2.vy = -settings.PADDLE_SPEED
            elif pong.ball.y + pong.ball.height > pong.player2.y + settings.PADDLE_HEIGHT * (1 + self.AI_ERROR):
                pong.player2.vy = settings.PADDLE_SPEED
            else:
                pong.player2.vy = 0
        else:
            pong.player2.vy = 0
        
        ball_rect = pong.ball.get_rect()

        if ball_rect.left > settings.VIRTUAL_WIDTH:
            self._score(scorer=1)
            return

        if ball_rect.right < 0:
            self._score(scorer=2)
            return

        if ball_rect.top <= 0:
            settings.SOUNDS["wall_hit"].play()
            pong.ball.y = 0
            pong.ball.vy *= -1
        elif ball_rect.bottom >= settings.VIRTUAL_HEIGHT:
            settings.SOUNDS["wall_hit"].play()
            pong.ball.y = settings.VIRTUAL_HEIGHT - pong.ball.height
            pong.ball.vy *= -1

        # Refreshed since a wall bounce above may have changed ball.y.
        ball_rect = pong.ball.get_rect()
        player1_rect = pong.player1.get_rect()
        player2_rect = pong.player2.get_rect()

        if ball_rect.colliderect(player1_rect):
            settings.SOUNDS["paddle_hit"].play()
            pong.ball.x = player1_rect.right
            pong.ball.vx *= -1.03
            self._randomize_vy()
            self.AI_ERROR = random.uniform(0, 0.5)
        elif ball_rect.colliderect(player2_rect):
            settings.SOUNDS["paddle_hit"].play()
            pong.ball.x = player2_rect.left - pong.ball.width
            pong.ball.vx *= -1.03
            self._randomize_vy()

    def _randomize_vy(self) -> None:
        magnitude = random.randint(10, 149)
        self.pong.ball.vy = -magnitude if self.pong.ball.vy < 0 else magnitude

    def _score(self, scorer: int) -> None:
        pong = self.pong
        settings.SOUNDS["score"].play()

        # Neither ServeState, DoneState, nor TitleState handle p1_up/p1_down/
        # p2_up/p2_down, so if a paddle key is still held when a point is
        # scored, its eventual release event is dropped instead of zeroing
        # vy here — leaving the paddle drifting on its own once play resumes.
        pong.player1.vy = 0
        pong.player2.vy = 0

        if scorer == 1:
            pong.player1_score += 1
            pong.serving_player = 2
        else:
            pong.player2_score += 1
            pong.serving_player = 1

        if pong.player1_score == settings.MAX_POINTS or pong.player2_score == settings.MAX_POINTS:
            pong.winning_player = scorer
            self.state_machine.change("done", pong=pong)
            return

        pong.ball.reset(
            settings.VIRTUAL_WIDTH / 2 - settings.BALL_SIZE / 2,
            settings.VIRTUAL_HEIGHT / 2 - settings.BALL_SIZE / 2,
        )
        self.state_machine.change("serve", pong=pong)

    def render(self, surface: pygame.Surface) -> None:
        render_table(surface, self.pong)

    def on_input(self, input_id: str, input_data: InputData) -> None:
        pong = self.pong

        if input_id in ("p1_up", "p1_down"):
            if input_data.pressed:
                pong.player1.vy = (
                    -settings.PADDLE_SPEED if input_id == "p1_up" else settings.PADDLE_SPEED
                )
            elif input_data.released:
                sign = -1 if input_id == "p1_up" else 1
                if pong.player1.vy == sign * settings.PADDLE_SPEED:
                    pong.player1.vy = 0
        # elif input_id in ("p2_up", "p2_down"):
            # if input_data.pressed:
            #     pong.player2.vy = (
            #         -settings.PADDLE_SPEED if input_id == "p2_up" else settings.PADDLE_SPEED
            #     )
            # elif input_data.released:
            #     sign = -1 if input_id == "p2_up" else 1
            #     if pong.player2.vy == sign * settings.PADDLE_SPEED:
            #         pong.player2.vy = 0
