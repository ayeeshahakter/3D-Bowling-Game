# Sanjida Islam - Bowling Game Features

**Student ID:** 22299420  
**Student Name:** Sanjida Islam

## Overview
This folder contains my individual feature implementations for the 3D Bowling Game project. 

## Features Implemented

### 1. Pulsing Lane (`pulsing-lane.py`)
- **Description:** Dynamic checkerboard lane pattern with colors that pulse over time
- **Key Function:** `draw_pulsing_lane()`
- **Visual Effect:** Lane tiles smoothly transition between different wood-like colors
- **Implementation:** Uses sine wave function for smooth color transitions

### 2. Ball-Pin Collision Detection (`ball-pin-collision.py`)
- **Description:** Realistic collision detection between bowling ball and pins
- **Key Functions:** `check_ball_pin_collision()`, `update_fallen_pins()`
- **Physics:** Calculates distance, applies impulse forces, handles pin falling
- **Implementation:** Pins react to ball impact with proper velocity transfer

### 3. Pin Toppling with Arcade Randomness (`pin-toppling-randomness.py`)
- **Description:** Pins fall with random effects for arcade-style gameplay
- **Key Functions:** `topple_pins_with_randomness()`, `apply_pin_wobble()`
- **Features:** Chain reactions, random fall directions, pin wobble effects
- **Gameplay:** Adds unpredictability and excitement 

### 4. Bonus Pin System (`bonus-pin.py`)
- **Description:** Special golden pin that randomly appears and awards extra points
- **Key Functions:** `check_bonus_pin_activation()`, `draw_bonus_pin()`, `handle_bonus_pin_hit()`
- **Visual:** Golden colored circle with sparkle effect
- **Scoring:** Awards 20 bonus points when knocked down

### 5. Shadow Effects (`shadow-effects.py`)
- **Description:** Realistic shadows for ball, pins, and obstacles
- **Key Functions:** `draw_ball_shadow()`, `draw_pin_shadows()`, `draw_obstacle_shadows()`
- **Visual Enhancement:** Adds depth perception and 3D 
- **Rendering:** Uses OpenGL blending for semi-transparent shadows

## Technical Details

### Dependencies
- OpenGL (PyOpenGL)
- OpenGL.GLUT
- OpenGL.GLU
- Python math library
- Python random library

## How to Use

Each file contains standalone functions that can be imported and used in the main game:

```python
from sanjida_features.pulsing_lane import draw_pulsing_lane
from sanjida_features.ball_pin_collision import check_ball_pin_collision
from sanjida_features.bonus_pin import initialize_bonus_pin
from sanjida_features.shadow_effects import draw_ball_shadow
```

## Contact
- **Email:** sanjidaayesha700@gmail.com
- **Student ID:** 22299420
- **Course:** Computer Graphics Project


