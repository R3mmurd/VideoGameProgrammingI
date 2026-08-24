"""
ISPPV1 2023
Study Case: The Legend of the Princess (ARPG)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the Command classes shared by the player (driven by
InputHandler through CommandBindings) and by any AI-controlled entity
(driven directly from its own state's process_ai). Every Command only
records intent on the receiver -- held[direction], sword_requested,
interact_requested -- which every Entity (held) or Player
(sword_requested/interact_requested) already exposes, so the same
instance works for both a human-controlled entity and an AI-controlled
one. Turning that intent into an actual effect (resolving held into a
direction and moving, whether a sword swing or a pot pickup/throw is
currently allowed) is resolved every frame by the receiving entity's
own state, never by the Command itself.
"""

from gale.command import Command


class MoveLeftCommand(Command):
    def execute(self, receiver, dt: float = 0.0) -> None:
        receiver.held["move_left"] = True


class MoveRightCommand(Command):
    def execute(self, receiver, dt: float = 0.0) -> None:
        receiver.held["move_right"] = True


class MoveUpCommand(Command):
    def execute(self, receiver, dt: float = 0.0) -> None:
        receiver.held["move_up"] = True


class MoveDownCommand(Command):
    def execute(self, receiver, dt: float = 0.0) -> None:
        receiver.held["move_down"] = True


class StopMoveLeftCommand(Command):
    def execute(self, receiver, dt: float = 0.0) -> None:
        receiver.held["move_left"] = False


class StopMoveRightCommand(Command):
    def execute(self, receiver, dt: float = 0.0) -> None:
        receiver.held["move_right"] = False


class StopMoveUpCommand(Command):
    def execute(self, receiver, dt: float = 0.0) -> None:
        receiver.held["move_up"] = False


class StopMoveDownCommand(Command):
    def execute(self, receiver, dt: float = 0.0) -> None:
        receiver.held["move_down"] = False


class SwordCommand(Command):
    def execute(self, receiver, dt: float = 0.0) -> None:
        receiver.sword_requested = True


class InteractCommand(Command):
    def execute(self, receiver, dt: float = 0.0) -> None:
        receiver.interact_requested = True


MOVE_LEFT = MoveLeftCommand()
MOVE_RIGHT = MoveRightCommand()
MOVE_UP = MoveUpCommand()
MOVE_DOWN = MoveDownCommand()
STOP_MOVE_LEFT = StopMoveLeftCommand()
STOP_MOVE_RIGHT = StopMoveRightCommand()
STOP_MOVE_UP = StopMoveUpCommand()
STOP_MOVE_DOWN = StopMoveDownCommand()
SWORD = SwordCommand()
INTERACT = InteractCommand()
