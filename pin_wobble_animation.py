    (-col_gap, base_y-row_gap),(col_gap, base_y-row_gap),
    (-2*col_gap, base_y-2*row_gap),(0.0, base_y-2*row_gap),(2*col_gap, base_y-2*row_gap),
    (-3*col_gap, base_y-3*row_gap),(-col_gap, base_y-3*row_gap),(col_gap, base_y-3*row_gap),(3*col_gap, base_y-3*row_gap)
]
pin_colors = [(1,0.2,0.2),(0.4,0.6,1),(0.4,0.6,1),(0.2,1,0.6),(1,0.8,0.2),(0.2,1,0.6),(0.9,0.4,1),(0.9,0.9,0.3),(0.9,0.4,1),(0.3,0.9,0.9)]

for i,(px,py) in enumerate(start_positions):
    pins.append({
        'x': px, 'y': py, 'vx': 0.0, 'vy': 0.0,
        'fallen': False, 'falling': False, 'angle': 0.0, 'fall_axis': (1,0,0), 'fall_speed': 0.0,
        'wobble_phase': random.uniform(0, math.tau), 'color': pin_colors[i%len(pin_colors)]
    })

# ---------------- Utilities --------------------------------

def _reset_ball():
    global ball_pos, ball_vel, in_flight, trail_points, ball_spinning, aim_angle_deg, power_val, power_holding
    ball_pos[:] = [0.0, LANE_Y0+60.0, BALL_RADIUS]
    ball_vel[:] = [0.0, 0.0, 0.0]
    in_flight = False
    trail_points.clear()
    ball_spinning = 0.0
    aim_angle_deg = 0.0
    power_val = 0.0
    power_holding = False

def _reset_pins(new_rack=True):
    global pins, bonus_pin_active, bonus_pin_index
    if new_rack:
        for i,(px,py) in enumerate(start_positions):
            pins[i].update(x=px, y=py, vx=0.0, vy=0.0, fallen=False, falling=False, angle=0.0, fall_axis=(1,0,0), fall_speed=0.0, wobble_phase=random.uniform(0,math.tau), color=pin_colors[i%len(pin_colors)])
        bonus_pin_active = False
        bonus_pin_index = -1

def _spawn_obstacles():
    global obstacles
    obstacles = []
    for _ in range(random.randint(0,2)):
        ox = random.uniform(-LANE_WIDTH*0.35, LANE_WIDTH*0.35)
        oy = random.uniform(LANE_Y0+120, LANE_Y1-160)
        s=OBSTACLE_RADIUS*1.6; glVertex3f(-s,-s,0.1); glVertex3f(s,-s,0.1); glVertex3f(s,s,0.1); glVertex3f(-s,s,0.1)
        glEnd(); glTranslatef(0,0,OBSTACLE_RADIUS); glColor3f(0.8,0.2,0.2); glutSolidCube(OBSTACLE_RADIUS*1.6); glPopMatrix()

    # Pins: upright, falling (tilt), or fallen (flat)
    for p in pins:
        glPushMatrix(); glTranslatef(p['x'], p['y'], 0)
        glColor3f(0,0,0); glBegin(GL_QUADS)
        s=PIN_RADIUS*1.8; glVertex3f(-s,-s,0.1); glVertex3f(s,-s,0.1); glVertex3f(s,s,0.1); glVertex3f(-s,s,0.1)
        glEnd()
        if not p['fallen'] and not p['falling']:
            wob = 4.0*math.sin(time_s*2.5 + p['wobble_phase']); glRotatef(wob, 1,0,0)
        if p['falling'] and not p['fallen']:
            ax,ay,az = p['fall_axis']; glRotatef(p['angle'], ax, ay, az)
        if p['fallen']:
            ax,ay,az = p['fall_axis']; glRotatef(90, ax, ay, az)
        body = p['color']; glColor3f(*body)
        glTranslatef(0,0,PIN_RADIUS)
        gluCylinder(quadric, PIN_RADIUS, PIN_RADIUS*0.8, PIN_HEIGHT*0.5, 12, 1)
        glTranslatef(0,0,PIN_HEIGHT*0.5); glColor3f(1,1,1)
        gluCylinder(quadric, PIN_RADIUS*0.8, PIN_RADIUS*0.55, PIN_HEIGHT*0.35, 12, 1)