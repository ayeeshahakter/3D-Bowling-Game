```python
# src/domino_chain.py
import math
import random
from common.constants import pins, PIN_RADIUS, PIN_FRICTION

def idle():
    """
    Handle pin-to-pin collisions to create a domino chain effect.
    When a falling pin is close to a standing pin, it triggers the standing pin to fall
    with a randomized direction and velocity.
    """
    for i, p in enumerate(pins):
        if p['falling'] and not p['fallen']:
            for j, q in enumerate(pins):
                if i == j or q['fallen'] or q['falling']:
                    continue
                dx = q['x'] - p['x']
                dy = q['y'] - p['y']
                dist = math.hypot(dx, dy)
                if dist < 2.5 * PIN_RADIUS and p['angle'] > 20.0:
                    angn = math.atan2(dy, dx) + math.radians(random.uniform(-12, 12))
                    axn, ayn = -math.sin(angn), math.cos(angn)
                    q['fall_axis'] = (axn, ayn, 0.0)
                    q['falling'] = True
                    q['angle'] = 0.0
                    q['fall_speed'] = 0.45 + random.random() * 0.6
                    q['vx'] = math.cos(angn) * 0.6 + random.uniform(-0.2, 0.2)
                    q['vy'] = math.sin(angn) * 0.6 + random.uniform(-0.2, 0.2)
```