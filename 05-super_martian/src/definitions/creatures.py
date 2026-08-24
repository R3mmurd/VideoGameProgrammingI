"""
ISPPV1 2023
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition for creatures.
"""

from typing import Any, Dict, List

from src.states.entities import creatures_states

# Frame layout in creatures.png for the flying-creature row: two flap
# frames (fly) plus a third, distinct front-facing pose reused as a
# static "stunned" frame for FlyingFallState.
FLYING_CREATURES: List[Dict[str, Any]] = [
    {
        "texture_id": "creatures",
        "fly_speed": 40,
        "animation_defs": {
            "fly": {"frames": [32, 33], "interval": 0.12},
            "fall": {"frames": [34]},
        },
    },
    {
        "texture_id": "creatures",
        "fly_speed": 45,
        "animation_defs": {
            "fly": {"frames": [35, 36], "interval": 0.12},
            "fall": {"frames": [37]},
        },
    },
    {
        "texture_id": "creatures",
        "fly_speed": 35,
        "animation_defs": {
            "fly": {"frames": [40, 41], "interval": 0.12},
            "fall": {"frames": [42]},
        },
    },
    {
        "texture_id": "creatures",
        "fly_speed": 50,
        "animation_defs": {
            "fly": {"frames": [43, 44], "interval": 0.12},
            "fall": {"frames": [45]},
        },
    },
]

CREATURES: Dict[int, Dict[str, Any]] = {
    48: {
        "texture_id": "creatures",
        "walk_speed": 10,
        "animation_defs": {"walk": {"frames": [48, 49], "interval": 0.25}},
        "states": {"walk": creatures_states.SnailWalkState},
        "first_state": "walk",
    },
    52: {
        "texture_id": "creatures",
        "walk_speed": 15,
        "animation_defs": {"walk": {"frames": [52, 53], "interval": 0.18}},
        "states": {"walk": creatures_states.SnailWalkState},
        "first_state": "walk",
    },
}
