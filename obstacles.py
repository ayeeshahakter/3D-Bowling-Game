# Variables for obstacles
OBSTACLE_RADIUS = 10.0
obstacles = []

def _spawn_obstacles():
    global obstacles
    obstacles = []
    for _ in range(random.randint(0,2)):
        ox = random.uniform(-LANE_WIDTH*0.35, LANE_WIDTH*0.35)
        oy = random.uniform(LANE_Y0+120, LANE_Y1-160)
        obstacles.append({'x':ox,'y':oy,'active':True})

def idle():
    if in_flight:
        for o in obstacles:
            if not o['active']: continue
            dx = ball_pos[0]-o['x']; dy = ball_pos[1]-o['y']
            if dx*dx+dy*dy <= (BALL_RADIUS+OBSTACLE_RADIUS)**2:
                n_ang = math.atan2(dy,dx); sp = math.hypot(ball_vel[0],ball_vel[1])
                ball_vel[0] = math.cos(n_ang)*sp*0.8; ball_vel[1] = math.sin(n_ang)*sp*0.8; o['active']=False

def draw_shapes():
    for o in obstacles:
        if not o['active']: continue
        glPushMatrix(); glTranslatef(o['x'], o['y'], 0)
        glColor3f(0,0,0); glBegin(GL_QUADS)
        s=OBSTACLE_RADIUS*1.6; glVertex3f(-s,-s,0.1); glVertex3f(s,-s,0.1); glVertex3f(s,s,0.1); glVertex3f(-s,s,0.1)
        glEnd(); glTranslatef(0,0,OBSTACLE_RADIUS); glColor3f(0.8,0.2,0.2); glutSolidCube(OBSTACLE_RADIUS*1.6); glPopMatrix()