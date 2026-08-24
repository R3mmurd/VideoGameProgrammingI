"""
ISPPV1 2023
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class GameLevel.
"""

import random
from typing import Any, Dict, Optional

import pygame

from gale.tilemap import CollisionType, collision_type_at, load_tiled_map
from gale.timer import Timer

import settings
from src.Creature import Creature
from src.FlyingCreature import FlyingCreature
from src.GameEntity import GameEntity
from src.GameItem import GameItem
from src.definitions import creatures, items


class GameLevel:
    def __init__(self, num_level: int) -> None:
        self.tilemap = load_tiled_map(settings.TILEMAPS[num_level])
        self.creatures = []
        self.items = []

        for obj in self.tilemap.object_layers.get("creatures", []):
            self.add_creature(
                {
                    "tile_index": obj.properties["tile_index"],
                    "x": obj.x,
                    "y": obj.y,
                    "width": obj.width,
                    "height": obj.height,
                }
            )

        for obj in self.tilemap.object_layers.get("coins", []):
            self.add_item(
                {
                    "item_name": "coins",
                    "frame_index": obj.properties["frame_index"],
                    "x": obj.x,
                    "y": obj.y,
                    "width": obj.width,
                    "height": obj.height,
                }
            )

        self._schedule_flying_creature_spawn()

    def add_item(self, item_data: Dict[str, Any]) -> None:
        item_name = item_data.pop("item_name")
        definition = items.ITEMS[item_name][item_data["frame_index"]]
        definition.update(item_data)
        self.items.append(GameItem(**definition))

    def add_creature(self, creature_data: Dict[str, Any]) -> None:
        definition = creatures.CREATURES[creature_data["tile_index"]]
        self.creatures.append(
            Creature(
                creature_data["x"],
                creature_data["y"],
                creature_data["width"],
                creature_data["height"],
                self,
                **definition,
            )
        )

    def _schedule_flying_creature_spawn(self) -> None:
        delay = random.uniform(
            settings.FLYING_CREATURE_MIN_SPAWN_DELAY,
            settings.FLYING_CREATURE_MAX_SPAWN_DELAY,
        )
        Timer.after(delay, self._spawn_flying_creature)

    def _pick_open_row(self, col: int) -> Optional[int]:
        """
        Scans column col from the top down and returns a random row
        strictly above the first solid/platform tile found there (with one
        extra row of buffer so the creature is unambiguously flying in open
        air, not skimming the surface), or None if the column has no clear
        row at all to spawn in.
        """
        first_solid_row = self.tilemap.rows

        for row in range(self.tilemap.rows):
            if (
                collision_type_at(self.tilemap, GameEntity.COLLISION_LAYER, row, col)
                != CollisionType.NONE
            ):
                first_solid_row = row
                break

        max_row = first_solid_row - 2

        if max_row < 0:
            return None

        return random.randint(0, max_row)

    def _spawn_flying_creature(self) -> None:
        from_left = random.choice([True, False])
        col = 0 if from_left else self.tilemap.cols - 1
        row = self._pick_open_row(col)

        if row is not None:
            definition = random.choice(creatures.FLYING_CREATURES)
            x = 0 if from_left else self.tilemap.pixel_width - 16
            y = row * self.tilemap.tile_height
            direction = "right" if from_left else "left"
            self.creatures.append(
                FlyingCreature(x, y, 16, 16, self, direction, **definition)
            )

        self._schedule_flying_creature_spawn()

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(0, 0, self.tilemap.pixel_width, self.tilemap.pixel_height)

    def update(self, dt: float) -> None:
        for creature in self.creatures:
            creature.update(dt)

        # Remove dead creatures
        self.creatures = [
            creature for creature in self.creatures if not creature.is_dead
        ]

    def render(self, surface: pygame.Surface, camera: Any) -> None:
        self.tilemap.render(surface, camera)
        for creature in self.creatures:
            creature.render(surface, camera)
        for item in self.items:
            if item.active:
                item.render(surface, camera)
