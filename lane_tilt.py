# Variables for lane tilt
lane_tilt_on = False
aim_angle_deg = 0.0
LANE_TILT_STRENGTH = 0.00005

def keyboardListener(key, x, y):
    k = key if isinstance(key, bytes) else bytes(key, 'utf-8')
    k = k.lower()
    if not in_flight:
        if k == b'a': aim_angle_deg = max(-20.0, aim_angle_deg-3.5)
        if k == b'd': aim_angle_deg = min(+20.0, aim_angle_deg+3.5)
    if k == b't': lane_tilt_on = not lane_tilt_on

def idle():
    if in_flight and lane_tilt_on:
        vx, vy = ball_vel[0], ball_vel[1]
        speed = math.hypot(vx, vy)
        if speed > 1e-6:
            ux, uy = vx/speed, vy/speed
            lx, ly = -uy, ux
            lat_acc = SPIN_STRENGTH * ball_spinning
            target_angle = math.radians(aim_angle_deg)
            current_angle = math.atan2(vy, vx)
            angle_diff = target_angle - current_angle
            while angle_diff > math.pi: angle_diff -= 2 * math.pi
            while angle_diff < -math.pi: angle_diff += 2 * math.pi
            lat_acc += LANE_TILT_STRENGTH * angle_diff
            ball_vel[0] += lx * lat_acc * dt_ms
            ball_vel[1] += ly * lat_acc * dt_ms

def draw_shapes():
    if lane_tilt_on and not in_flight:
        ang = math.radians(aim_angle_deg)
        vx = math.sin(ang)
        vy = math.cos(ang)
        start_x, start_y = ball_pos[0], ball_pos[1]
        glColor3f(1, 1, 1)  # white for aiming dots
        glBegin(GL_QUADS)
        for dist in range(50, int(LANE_Y1 - 150 - start_y), 50):
            px = start_x + vx * dist
            py = start_y + vy * dist
            s = 6.0  # Small quad size
            glVertex3f(px-s, py-s, 0.2); glVertex3f(px+s, py-s, 0.2)
            glVertex3f(px+s, py+s, 0.2); glVertex3f(px-s, py+s, 0.2)
        glEnd()