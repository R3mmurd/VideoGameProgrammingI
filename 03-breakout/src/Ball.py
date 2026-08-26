"""
ISPPV1 2023
Study Case: Breakout

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class Ball.
"""

import pygame

import settings
from src.BallBase import BallBase
from src.Paddle import Paddle


class Ball(BallBase):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)

    def push(self, paddle: Paddle) -> None:
        """
        Push the ball according to the position that it collides with the paddle and the paddle speed.
        """
        br = self.get_collision_rect()
        pr = paddle.get_collision_rect()
        d = pr.centerx - br.x

        if d > 0 and paddle.vx < 0 and pr.x > 0:
            self.vx = -50 - 8 * d
        elif d < 0 and paddle.vx > 0 and pr.right < settings.VIRTUAL_HEIGHT:
            self.vx = 50 - 8 * d
