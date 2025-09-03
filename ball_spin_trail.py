# Variables for ball spin and trail
ball_spinning = 0.0
trail_points = []
spin_trail_max = 28
SPIN_STRENGTH = 0.00028

def keyboardListener(key, x, y):
    k = key if isinstance(key, bytes) else bytes(key, 'utf-8')
    k = k.lower()
    if k == b'j': ball_spinning = max(-1.8, ball_spinning - 0.18)
    if k == b'l': ball_spinning = min( 1.8, ball_spinning + 0.18)

def idle():
    global trail_points, in_flight, ball_spinning
    if in_flight:
        vx, vy = ball_vel[0], ball_vel[1]
        speed = math.hypot(vx, vy)
        if speed > 1e-6:
            ux, uy = vx/speed, vy/speed
            lx, ly = -uy, ux
            lat_acc = SPIN_STRENGTH * ball_spinning
            ball_vel[0] += lx * lat_acc * dt_ms
            ball_vel[1] += ly * lat_acc * dt_ms
        trail_points.append((ball_pos[0], ball_pos[1], frame_count))
        if len(trail_points) > spin_trail_max: trail_points.pop(0)

def draw_shapes():
    # Spin trail
    if trail_points:
        glBegin(GL_QUADS)
        glColor3f(1,1,1)  # Solid white
        for tx, ty, _ in trail_points:
            s = 1.0  # Small square size
            glVertex3f(tx-s, ty-s, BALL_RADIUS); glVertex3f(tx+s, ty-s, BALL_RADIUS)
            glVertex3f(tx+s, ty+s, BALL_RADIUS); glVertex3f(tx-s, ty+s, BALL_RADIUS)
        glEnd()