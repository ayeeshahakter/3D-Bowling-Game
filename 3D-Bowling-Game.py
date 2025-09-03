from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# ============================================================
# 3D Bowling — Full single-file game (keeps template functions)
# Features: pulsing lane, ball spin & trail, ball-pin collisions,
# pins topple (arcade randomness) + domino chain, scoring, bonus pin,
# power meter, multiple cameras, obstacles, crowd reactions.
# ============================================================

# ---------------- Camera & Window ---------------------------
camera_pos = [0.0, 500.0, 500.0]
fovY = 60
win_w, win_h = 1000, 800

import math, random
random.seed(42)

# ---------------- Constants ---------------------------------
LANE_LENGTH = 900.0
LANE_WIDTH = 240.0
LANE_Y0 = -420.0
LANE_Y1 = 420.0
GUTTER_W = 40.0
BALL_RADIUS = 18.0
BALL_MASS = 6.0
PIN_RADIUS = 9.0
PIN_HEIGHT = 50.0
FRICTION = 0.0001
PIN_FRICTION = 0.0020
SPIN_STRENGTH = 0.00028
LANE_TILT_STRENGTH = 0.00005  # Reduced for subtle aiming assist
OBSTACLE_RADIUS = 10.0

# ---------------- Visual / State ----------------------------
spin_trail_max = 28
trail_points = []  # list of (x,y,frame_count)
ball_colors = [(1,0.2,0.2),(0.2,0.6,1),(0.2,1,0.4),(1,0.8,0.2),(0.9,0.4,1)]
ball_color_idx = 0

CAM_THIRD = 0
CAM_FIRST = 1
CAM_TOP = 2
camera_mode = CAM_THIRD

# ---------------- Players & Scoring -------------------------
max_players = 4
player_names = ["Player 1","Player 2","Player 3","Player 4"]
num_players = 2
current_player = 0
throw_counter = [0]*max_players
frames = [[[ -1, -1, -1 ] for _ in range(10)] for __ in range(max_players)]
frame_idx = [0]*max_players
roll_idx = [0]*max_players

# ---------------- Ball State -------------------------------
ball_pos = [0.0, LANE_Y0+60.0, BALL_RADIUS]
ball_vel = [0.0, 0.0, 0.0]
ball_spinning = 0.0
aim_angle_deg = 0.0
power_holding = False
power_val = 0.0
in_flight = False
lane_tilt_on = False
slowmo_timer_ms = 0

# ---------------- Pins & Obstacles -------------------------
pins = []
bonus_pin_active = False
bonus_pin_index = -1
obstacles = []

# ---------------- Crowd & UI -------------------------------
result_text = ""
result_timer_ms = 0
frame_count = 0  # New: frame-based counter for timing

# ---------------- Initialization of pins -------------------
base_y = LANE_Y1 - 120.0
row_gap = 33.0
col_gap = 19.0
start_positions = [
    (0.0, base_y),
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
        obstacles.append({'x':ox,'y':oy,'active':True})

def _count_standing():
    return sum(0 if p['fallen'] else 1 for p in pins)

def _score_for_player(pid):
    rolls = []
    for f in range(10):
        a,b,c = frames[pid][f]
        if a>=0: rolls.append(a)
        if b>=0: rolls.append(b)
        if f==9 and c>=0: rolls.append(c)
    score=0; i=0
    for f in range(10):
        if i>=len(rolls): break
        if rolls[i]==10:
            bonus = (rolls[i+1] if i+1<len(rolls) else 0) + (rolls[i+2] if i+2<len(rolls) else 0)
            score += 10 + bonus; i += 1
        else:
            frame_sum = rolls[i] + (rolls[i+1] if i+1<len(rolls) else 0)
            if frame_sum==10:
                bonus = (rolls[i+2] if i+2<len(rolls) else 0)
                score += 10 + bonus
            else:
                score += frame_sum
            i += 2
    return score

# Quadric
quadric = None

# ---------------- Template functions ------------------------

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION); glPushMatrix(); glLoadIdentity()
    gluOrtho2D(0, win_w, 0, win_h)
    glMatrixMode(GL_MODELVIEW); glPushMatrix(); glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text: glutBitmapCharacter(font, ord(ch))
    glPopMatrix(); glMatrixMode(GL_PROJECTION); glPopMatrix(); glMatrixMode(GL_MODELVIEW)

def draw_shapes():
    global quadric
    if quadric is None: quadric = gluNewQuadric()
    time_s = frame_count / 60.0  # Assume 60 FPS for seconds

    # Lane base + pulsing checker
    glPushMatrix()
    glBegin(GL_QUADS)
    glColor3f(0.15,0.15,0.18)
    glVertex3f(-LANE_WIDTH/2 - GUTTER_W, LANE_Y0, 0); glVertex3f(-LANE_WIDTH/2, LANE_Y0, 0)
    glVertex3f(-LANE_WIDTH/2, LANE_Y1, 0); glVertex3f(-LANE_WIDTH/2 - GUTTER_W, LANE_Y1, 0)
    glVertex3f(LANE_WIDTH/2, LANE_Y0, 0); glVertex3f(LANE_WIDTH/2 + GUTTER_W, LANE_Y0, 0)
    glVertex3f(LANE_WIDTH/2 + GUTTER_W, LANE_Y1, 0); glVertex3f(LANE_WIDTH/2, LANE_Y1, 0)
    glEnd()

    pulseslow = 0.5*(1+math.sin(time_s*2.2))
    c1 = 0.55+0.15*pulseslow; c2 = 0.45-0.15*pulseslow
    tiles_x = 12; tiles_y = 30
    tile_w = LANE_WIDTH/tiles_x; tile_h = (LANE_Y1-LANE_Y0)/tiles_y
    for iy in range(tiles_y):
        for ix in range(tiles_x):
            u0 = -LANE_WIDTH/2 + ix*tile_w; u1 = u0 + tile_w
            v0 = LANE_Y0 + iy*tile_h; v1 = v0 + tile_h
            if (ix+iy)%2==0: glColor3f(c1,0.38,0.22)
            else: glColor3f(c2,0.31,0.18)
            glBegin(GL_QUADS)
            glVertex3f(u0,v0,0); glVertex3f(u1,v0,0); glVertex3f(u1,v1,0); glVertex3f(u0,v1,0)
            glEnd()
    glPopMatrix()

    # Obstacles
    for o in obstacles:
        if not o['active']: continue
        glPushMatrix(); glTranslatef(o['x'], o['y'], 0)
        glColor3f(0,0,0); glBegin(GL_QUADS)
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
        glTranslatef(0,0,PIN_HEIGHT*0.35); glColor3f(*body); gluSphere(quadric, PIN_RADIUS*0.55, 12, 12)
        glPopMatrix()

    # Bonus ring (using GL_QUADS to approximate a circle)
    if bonus_pin_active and 0<=bonus_pin_index<len(pins):
        p = pins[bonus_pin_index]
        if not p['fallen']:
            glPushMatrix(); glTranslatef(p['x'], p['y'], 0.2); glColor3f(1,1,0)
            glBegin(GL_QUADS)
            for k in range(36):
                ang0 = k/36*math.tau; ang1 = (k+1)/36*math.tau
                r = PIN_RADIUS*2.0; w = PIN_RADIUS*0.2
                glVertex3f(math.cos(ang0)*r, math.sin(ang0)*r, 0.2)
                glVertex3f(math.cos(ang1)*r, math.sin(ang1)*r, 0.2)
                glVertex3f(math.cos(ang1)*(r+w), math.sin(ang1)*(r+w), 0.2)
                glVertex3f(math.cos(ang0)*(r+w), math.sin(ang0)*(r+w), 0.2)
            glEnd(); glPopMatrix()

    # Ball + shadow
    glPushMatrix(); glTranslatef(ball_pos[0], ball_pos[1], 0)
    glColor3f(0,0,0); glBegin(GL_QUADS)
    s=BALL_RADIUS*1.6; glVertex3f(-s,-s,0.1); glVertex3f(s,-s,0.1); glVertex3f(s,s,0.1); glVertex3f(-s,s,0.1)
    glEnd(); glTranslatef(0,0,BALL_RADIUS)
    bc = ball_colors[ball_color_idx]; glColor3f(*bc); gluSphere(quadric, BALL_RADIUS, 24, 18); glPopMatrix()

    # Spin trail (using GL_QUADS for small squares)
    if trail_points:
        glBegin(GL_QUADS)
        glColor3f(1,1,1)  # Solid white
        for tx, ty, _ in trail_points:
            s = 1.0  # Small square size
            glVertex3f(tx-s, ty-s, BALL_RADIUS); glVertex3f(tx+s, ty-s, BALL_RADIUS)
            glVertex3f(tx+s, ty+s, BALL_RADIUS); glVertex3f(tx-s, ty+s, BALL_RADIUS)
        glEnd()

    # Aiming cue for lane tilt (dotted quads when lane_tilt_on and not in_flight)
    if lane_tilt_on and not in_flight:
        ang = math.radians(aim_angle_deg)
        vx = math.sin(ang)
        vy = math.cos(ang)
        start_x, start_y = ball_pos[0], ball_pos[1]
        glColor3f(1, 1, 1)  # white for aiming dots
        glBegin(GL_QUADS)
        for dist in range(50, int(LANE_Y1 - 150 - start_y), 50):  # Stop before pins
            px = start_x + vx * dist
            py = start_y + vy * dist
            s = 6.0  # Small quad size
            glVertex3f(px-s, py-s, 0.2); glVertex3f(px+s, py-s, 0.2)
            glVertex3f(px+s, py+s, 0.2); glVertex3f(px-s, py+s, 0.2)
        glEnd()

def keyboardListener(key, x, y):
    global aim_angle_deg, power_holding, power_val, ball_spinning, in_flight
    global ball_color_idx, camera_mode, lane_tilt_on, num_players, result_text
    global slowmo_timer_ms, next_bonus_check_ms, current_player, standing_at_throw_start

    k = key if isinstance(key, bytes) else bytes(key, 'utf-8')
    k = k.lower()

    if not in_flight:
        if k == b'a': aim_angle_deg = max(-20.0, aim_angle_deg-3.5)
        if k == b'd': aim_angle_deg = min(+20.0, aim_angle_deg+3.5)

    if k == b'j': ball_spinning = max(-1.8, ball_spinning - 0.18)
    if k == b'l': ball_spinning = min( 1.8, ball_spinning + 0.18)

    if k == b' ':
        if not in_flight and not power_holding:
            power_holding = True; power_val = 0.0
        elif power_holding and not in_flight:
            power_holding = False
            launch_speed = 0.0043 * max(1.0, power_val)
            ang = math.radians(aim_angle_deg)
            vx = math.sin(ang) * launch_speed
            vy = math.cos(ang) * launch_speed
            ball_vel[0] = vx; ball_vel[1] = vy; in_flight = True
            standing_at_throw_start = _count_standing()

    if k == b'c': ball_color_idx = (ball_color_idx+1) % len(ball_colors)
    if k == b'1': camera_mode = CAM_FIRST
    if k == b'2': camera_mode = CAM_THIRD
    if k == b'3': camera_mode = CAM_TOP
    if k == b't': lane_tilt_on = not lane_tilt_on
    if k == b'n': num_players = 2 if num_players==4 else num_players+1
    if k == b'r': _reset_pins(True); _reset_ball(); result_text = ""; slowmo_timer_ms = 0; next_bonus_check_ms = 0

def specialKeyListener(key, x, y):
    cx, cy, cz = camera_pos
    if key == GLUT_KEY_LEFT: cx -= 10
    if key == GLUT_KEY_RIGHT: cx += 10
    if key == GLUT_KEY_UP: cz += 10
    if key == GLUT_KEY_DOWN: cz -= 10
    camera_pos[0], camera_pos[1], camera_pos[2] = cx, cy, cz

def mouseListener(button, state, x, y):
    global camera_mode
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        camera_mode = CAM_THIRD if camera_mode!=CAM_THIRD else CAM_FIRST

def setupCamera():
    glMatrixMode(GL_PROJECTION); glLoadIdentity(); gluPerspective(fovY, win_w/float(win_h), 0.1, 2000)
    glMatrixMode(GL_MODELVIEW); glLoadIdentity()
    if camera_mode == CAM_FIRST:
        if in_flight:
            speed = math.hypot(ball_vel[0], ball_vel[1])
            if speed > 1e-6:
                vx, vy = ball_vel[0]/speed, ball_vel[1]/speed
            else:
                vx, vy = 0.0, 1.0
        else:
            ang = math.radians(aim_angle_deg)
            vx = math.sin(ang)
            vy = math.cos(ang)
        look_from = [ball_pos[0] + vx * BALL_RADIUS, ball_pos[1] + vy * BALL_RADIUS, BALL_RADIUS]
        look_to = [look_from[0] + vx * 40, look_from[1] + vy * 40, BALL_RADIUS]
        gluLookAt(look_from[0], look_from[1], look_from[2], look_to[0], look_to[1], look_to[2], 0, 0, 1)
    elif camera_mode == CAM_TOP:
        gluLookAt(0, 0, 900,  0, 0, 0,  0,1,0)
    else:
        bx,by,bz = ball_pos
        backx = bx - ball_vel[0]*120
        backy = by - 200
        gluLookAt(backx, backy, 300,   bx, by+120, 0,   0,0,1)

# ---------------- Physics & Gameplay -----------------------
standing_at_throw_start = -1
next_bonus_check_ms = 0

def idle():
    global power_val, trail_points, in_flight, result_text, result_timer_ms
    global throw_counter, frames, frame_idx, roll_idx, current_player
    global slowmo_timer_ms, bonus_pin_active, bonus_pin_index, next_bonus_check_ms
    global standing_at_throw_start, ball_spinning, frame_count

    frame_count += 1  # Increment frame counter
    dt_ms = 16
    if slowmo_timer_ms > 0:
        dt_ms = 6; slowmo_timer_ms -= dt_ms
        if slowmo_timer_ms < 0: slowmo_timer_ms = 0

    t_ms = frame_count * 16  # Approximate ms (16ms per frame)

    if power_holding and not in_flight:
        power_val = min(100.0, power_val + 0.06*dt_ms)

    if not in_flight and next_bonus_check_ms < t_ms:
        next_bonus_check_ms = t_ms + random.randint(4000,9000)
        if random.random() < 0.28:
            cand = [i for i,p in enumerate(pins) if not p['fallen']]
            if cand:
                bonus_pin_index = random.choice(cand); bonus_pin_active = True

    if in_flight:
        vx, vy = ball_vel[0], ball_vel[1]
        speed = math.hypot(vx, vy)
        if speed > 1e-6:
            ux, uy = vx/speed, vy/speed
            lx, ly = -uy, ux
            lat_acc = SPIN_STRENGTH * ball_spinning
            if lane_tilt_on:
                # Aim-assist: Nudge toward aim_angle_deg
                target_angle = math.radians(aim_angle_deg)
                current_angle = math.atan2(vy, vx)
                angle_diff = target_angle - current_angle
                # Normalize angle_diff to [-pi, pi]
                while angle_diff > math.pi: angle_diff -= 2 * math.pi
                while angle_diff < -math.pi: angle_diff += 2 * math.pi
                # Apply tilt as a gentle nudge toward target angle
                lat_acc += LANE_TILT_STRENGTH * angle_diff
            ball_vel[0] += lx * lat_acc * dt_ms
            ball_vel[1] += ly * lat_acc * dt_ms
        ball_pos[0] += ball_vel[0]*dt_ms; ball_pos[1] += ball_vel[1]*dt_ms
        sp = math.hypot(ball_vel[0], ball_vel[1])
        if sp>0:
            dec = FRICTION*dt_ms; sp = max(0.0, sp - dec)
            ang = math.atan2(ball_vel[1], ball_vel[0])
            ball_vel[0] = math.cos(ang)*sp; ball_vel[1] = math.sin(ang)*sp
        trail_points.append((ball_pos[0], ball_pos[1], frame_count))
        if len(trail_points) > spin_trail_max: trail_points.pop(0)
        left = -LANE_WIDTH/2; right = LANE_WIDTH/2
        if ball_pos[0] < left: ball_pos[0] = left; ball_vel[0] *= -0.35; ball_vel[1] *= 0.9
        if ball_pos[0] > right: ball_pos[0] = right; ball_vel[0] *= -0.35; ball_vel[1] *= 0.9
        for o in obstacles:
            if not o['active']: continue
            dx = ball_pos[0]-o['x']; dy = ball_pos[1]-o['y']
            if dx*dx+dy*dy <= (BALL_RADIUS+OBSTACLE_RADIUS)**2:
                n_ang = math.atan2(dy,dx); sp = math.hypot(ball_vel[0],ball_vel[1])
                ball_vel[0] = math.cos(n_ang)*sp*0.8; ball_vel[1] = math.sin(n_ang)*sp*0.8; o['active']=False
        for i,p in enumerate(pins):
            if p['fallen'] or p['falling']: continue
            dx = p['x'] - ball_pos[0]; dy = p['y'] - ball_pos[1]
            if dx*dx + dy*dy <= (BALL_RADIUS + PIN_RADIUS)**2:
                impact = math.hypot(ball_vel[0], ball_vel[1])
                if impact < 0.02: impact = 0.02
                ang = math.atan2(dy, dx)
                offset = math.radians(random.uniform(-20,20))
                fall_dir = ang + offset
                fx = math.cos(fall_dir); fy = math.sin(fall_dir)
                ax, ay, az = -fy, fx, 0.0
                p['fall_axis'] = (ax, ay, az)
                p['falling'] = True; p['angle'] = 0.0
                p['fall_speed'] = 0.6 * (0.6 + random.random()*0.8)
                p['vx'] = math.cos(fall_dir) * impact * 0.8 + random.uniform(-0.2,0.2)
                p['vy'] = math.sin(fall_dir) * impact * 0.8 + random.uniform(-0.2,0.2)
                if random.random() < 0.3:
                    p['vx'] += random.uniform(-0.4, 0.4); p['vy'] += random.uniform(-0.4,0.4)
        if (ball_pos[1] > LANE_Y1+30) or (math.hypot(ball_vel[0],ball_vel[1]) < 0.02):
            in_flight = False

    for i,p in enumerate(pins):
        if p['falling'] and not p['fallen']:
            p['angle'] += p['fall_speed'] * dt_ms
            if p['angle'] >= 90.0:
                p['angle'] = 90.0; p['fallen'] = True; p['falling'] = False
            p['x'] += p['vx'] * dt_ms; p['y'] += p['vy'] * dt_ms
            for j,q in enumerate(pins):
                if i==j or q['fallen'] or q['falling']: continue
                dx = q['x'] - p['x']; dy = q['y'] - p['y']
                dist = math.hypot(dx, dy)
                if dist < 2.5*PIN_RADIUS and p['angle'] > 20.0:
                    angn = math.atan2(dy, dx) + math.radians(random.uniform(-12,12))
                    axn,ayn = -math.sin(angn), math.cos(angn)
                    q['fall_axis'] = (axn,ayn,0.0); q['falling'] = True; q['angle'] = 0.0
                    q['fall_speed'] = 0.45 + random.random()*0.6
                    q['vx'] = math.cos(angn)*0.6 + random.uniform(-0.2,0.2)
                    q['vy'] = math.sin(angn)*0.6 + random.uniform(-0.2,0.2)
        elif p['fallen']:
            p['x'] += p['vx'] * dt_ms; p['y'] += p['vy'] * dt_ms
            sp = math.hypot(p['vx'], p['vy'])
            if sp > 0:
                dec = PIN_FRICTION * dt_ms; sp = max(0.0, sp - dec)
                ang = math.atan2(p['vy'], p['vx'])
                p['vx'] = math.cos(ang)*sp; p['vy'] = math.sin(ang)*sp

    if not in_flight and standing_at_throw_start>=0:
        knocked = standing_at_throw_start - _count_standing()
        if knocked < 0: knocked = 0
        pid = current_player; f = frame_idx[pid]; r = roll_idx[pid]
        if f < 10:
            val = knocked
            if f < 9:
                if r == 0:
                    frames[pid][f][0] = min(10, val)
                    if frames[pid][f][0] == 10:
                        result_text = "STRIKE!"; slowmo_timer_ms = max(slowmo_timer_ms, 1000); roll_idx[pid]=0; frame_idx[pid]+=1
                    else:
                        roll_idx[pid] = 1
                else:
                    frames[pid][f][1] = min(10 - (frames[pid][f][0] if frames[pid][f][0]>=0 else 0), val)
                    if (frames[pid][f][0] if frames[pid][f][0]>=0 else 0) + frames[pid][f][1] == 10:
                        result_text = "Spare!"
                    roll_idx[pid] = 0; frame_idx[pid] += 1
            else:
                if r==0:
                    frames[pid][f][0] = min(10,val); roll_idx[pid]=1
                elif r==1:
                    frames[pid][f][1] = min(10,val)
                    if frames[pid][f][0]==10 or frames[pid][f][0]+frames[pid][f][1]==10: roll_idx[pid]=2
                    else: roll_idx[pid]=0; frame_idx[pid]+=1
                else:
                    frames[pid][f][2] = min(10,val); roll_idx[pid]=0; frame_idx[pid]+=1
            if result_text=="": result_text = "Gutter!" if val==0 else ("Nice Shot!" if val>=7 else "Good!")
            throw_counter[pid] += 1
        if f>=10 or roll_idx[pid]==0:
            current_player = (current_player+1) % num_players
        _reset_ball(); standing_at_throw_start = -1
        if _count_standing() == 0:
            slowmo_timer_ms = max(slowmo_timer_ms, 800); _reset_pins(True); _spawn_obstacles()
    glutPostRedisplay()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glViewport(0, 0, win_w, win_h)
    setupCamera(); draw_shapes()

    draw_text(10, win_h-30, f"Angle[A/D]: {aim_angle_deg:4.1f}°  Spin[J/L]: {ball_spinning:+.2f}  Tilt[T]: {'ON' if lane_tilt_on else 'OFF'}")
    draw_text(10, win_h-60, f"Ball Color[C]  Players[N]: {num_players}  Bonus Pin: {'ON' if bonus_pin_active else 'OFF'}")
    draw_text(10, 40, f"Power: {power_val:5.1f}%  (Press SPACE to start/stop)")
    draw_text(10, 70, f"Current: {player_names[current_player]} | Throws: {throw_counter[current_player]}")
    if result_text: draw_text(win_w//2 - 80, win_h-90, result_text)
    y0 = win_h-110
    for pid in range(num_players):
        glColor3f(1, 1, 0) if pid == current_player else glColor3f(1, 1, 1)  # Yellow for current player, white for others
        line = f"{player_names[pid]} | "
        for f in range(10):
            a,b,c = frames[pid][f]
            aa = '-' if a<0 else str(a); bb = '-' if b<0 else str(b); cc = '' if f<9 else ('-' if c<0 else str(c))
            if f<9: line += f"[{aa},{bb}]"
            else: line += f"[{aa},{bb},{cc}]"
        line += f"  = {_score_for_player(pid)}"
        draw_text(10, y0-20*pid, line)
    
    fallen_pins = 10 - _count_standing()
    draw_text(10, win_h-90, f"Fallen Pins: {fallen_pins}")

    draw_text(10, 20, "Space: Start/Release | A/D: Angle | J/L: Spin | C: Color | 1/2/3: View | T: Tilt | N: Players | R: Reset")
    glutSwapBuffers()

def main():
    glutInit(); glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(win_w, win_h); glutInitWindowPosition(0, 0); glutCreateWindow(b"3D Bowling - Final Fix")
    glClearColor(0.05,0.07,0.1,1)
    glutDisplayFunc(showScreen); glutKeyboardFunc(keyboardListener); glutSpecialFunc(specialKeyListener); glutMouseFunc(mouseListener); glutIdleFunc(idle)
    _reset_pins(True); _spawn_obstacles(); _reset_ball()
    glutMainLoop()

if __name__ == "__main__": main()