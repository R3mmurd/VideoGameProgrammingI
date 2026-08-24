"""
ISPPV1 2023
Study Case: The Legend of the Princess (ARPG)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class Entity.
"""

from typing import Any, Dict, Optional

import pygame

from gale.animation import Animation
from gale.state import StateMachine
from gale.stencil import Stencil

import settings


class Entity:
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        walk_speed: float,
        health: int,
        animation_defs: Dict[str, Dict[str, Any]],
        states: Dict[str, Any],
    ) -> None:
        # In top-down games, there are four directions instead of two.
        self.direction = "down"

        # Movement intent, updated by MOVE_*/STOP_MOVE_* Commands -- from
        # InputHandler for the player, from process_ai for AI-controlled
        # entities -- and resolved into self.direction/movement by each
        # entity's own walk state, every frame.
        self.held = {
            "move_left": False,
            "move_right": False,
            "move_up": False,
            "move_down": False,
        }

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Drawing offsets for padded sprites.
        self.offset_x = 0
        self.offset_y = 0

        self.walk_speed = walk_speed
        self.health = health

        # Flags for flashing the entity when hit.
        self.invulnerable = False
        self.invulnerable_duration = 0.0
        self.invulnerable_timer = 0.0
        self.flash_timer = 0.0

        self.dead = False

        # Tracks whether the entity has dropped items or not.
        self.dropped = False

        self.current_animation = None
        self.animations = self._create_animations(animation_defs)
        self.state_machine = StateMachine(states)

        # When set (screen-space, same coordinates as x/y at render time),
        # render_sprite only shows the part of the sprite that falls
        # inside this rect and clips the rest -- used to let the player
        # visually pass through a doorway opening without popping through
        # the solid wall around it. None (the default, for every entity
        # that never crosses a doorway) skips the stencil entirely.
        self.visibility_clip_rect: Optional[pygame.Rect] = None

    def _create_animations(
        self, animation_defs: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Animation]:
        animations = {}

        for name, definition in animation_defs.items():
            animation = Animation(
                definition["frames"],
                definition.get("interval", 0),
                loops=definition.get("loops"),
            )
            animation.texture_id = definition.get("texture", "entities")
            animations[name] = animation

        return animations

    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y), self.width, self.height)

    def collides(self, target: Any) -> bool:
        """
        AABB against any object exposing x/y/width/height — an Entity,
        GameObject, Doorway, or a plain sword hitbox rect alike.
        """
        target_rect = pygame.Rect(round(target.x), round(target.y), target.width, target.height)
        return self.get_collision_rect().colliderect(target_rect)

    def damage(self, dmg: int) -> None:
        self.health -= dmg

    def heal(self, life: int) -> None:
        self.health = min(self.health + life, 6)

    def go_invulnerable(self, duration: float) -> None:
        self.invulnerable = True
        self.invulnerable_duration = duration

    def change_state(self, name: str, *args: Any, **kwargs: Any) -> None:
        self.state_machine.change(name, *args, **kwargs)

    def change_animation(self, name: str) -> None:
        self.current_animation = self.animations[name]

    def update(self, dt: float) -> None:
        if self.invulnerable:
            self.flash_timer += dt
            self.invulnerable_timer += dt

            if self.invulnerable_timer > self.invulnerable_duration:
                self.invulnerable = False
                self.invulnerable_timer = 0
                self.invulnerable_duration = 0
                self.flash_timer = 0

        self.state_machine.update(dt)

        if self.current_animation:
            self.current_animation.update(dt)

    def process_ai(self, room: Any, dt: float) -> None:
        self.state_machine.current.process_ai(room, dt)

    def render_sprite(
        self, surface: pygame.Surface, texture_id: str, frame_index: int
    ) -> None:
        """
        Draws this entity's current animation frame at (x - offset_x, y -
        offset_y), flashing translucent every ~0.06s while invulnerable.
        """
        texture = settings.TEXTURES[texture_id]
        frame = settings.frame(texture_id, frame_index)
        image = pygame.Surface((frame.width, frame.height), pygame.SRCALPHA)
        image.blit(texture, (0, 0), frame)

        if self.invulnerable and self.flash_timer > 0.06:
            self.flash_timer = 0
            image.set_alpha(64)

        sprite_x = round(self.x - self.offset_x)
        sprite_y = round(self.y - self.offset_y)

        if self.visibility_clip_rect is not None:
            sprite_rect = pygame.Rect(sprite_x, sprite_y, frame.width, frame.height)
            visible = self.visibility_clip_rect.clip(sprite_rect)
            visible.move_ip(-sprite_x, -sprite_y)

            stencil = Stencil((frame.width, frame.height))
            stencil.draw(lambda mask: mask.fill((255, 255, 255, 255), visible))
            stencil.apply(image)

        surface.blit(
            image, (sprite_x, sprite_y)
        )

    def render(
        self,
        surface: pygame.Surface,
        adjacent_offset_x: float = 0,
        adjacent_offset_y: float = 0,
    ) -> None:
        # Temporarily shift by the room-transition slide offset; reverted
        # right after so it never leaks into collision/update logic.
        self.x, self.y = self.x + adjacent_offset_x, self.y + adjacent_offset_y
        self.state_machine.render(surface)
        self.x, self.y = self.x - adjacent_offset_x, self.y - adjacent_offset_y
