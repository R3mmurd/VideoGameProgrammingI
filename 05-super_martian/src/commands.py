"""
ISPPV1 2023
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the Command classes shared by the player (driven by
InputHandler through CommandBindings) and by any autonomous entity
(driven directly from its own state's decision logic). Every Command
only records intent on the receiver -- move_direction, jump_requested
-- which every GameEntity already exposes, so the same instance works
for both a human-controlled entity and an AI-controlled one. Turning
that intent into an actual effect (how fast it translates into vx,
whether a jump is currently allowed, which way the sprite should be
flipped for its own artwork) is resolved every frame by the receiving
entity's own state, never by the Command itself.
"""

from gale.command import Command


class MoveLeftCommand(Command):
    def execute(self, receiver, dt: float = 0.0) -> None:
        receiver.move_direction = -1


class MoveRightCommand(Command):
    def execute(self, receiver, dt: float = 0.0) -> None:
        receiver.move_direction = 1


class StopMoveLeftCommand(Command):
    def execute(self, receiver, dt: float = 0.0) -> None:
        if receiver.move_direction < 0:
            receiver.move_direction = 0


class StopMoveRightCommand(Command):
    def execute(self, receiver, dt: float = 0.0) -> None:
        if receiver.move_direction > 0:
            receiver.move_direction = 0


class JumpCommand(Command):
    def execute(self, receiver, dt: float = 0.0) -> None:
        receiver.jump_requested = True


MOVE_LEFT = MoveLeftCommand()
MOVE_RIGHT = MoveRightCommand()
STOP_MOVE_LEFT = StopMoveLeftCommand()
STOP_MOVE_RIGHT = StopMoveRightCommand()
JUMP = JumpCommand()
