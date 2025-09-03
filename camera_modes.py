# Variables for camera modes
camera_pos = [0.0, 500.0, 500.0]
fovY = 60
win_w, win_h = 1000, 800
CAM_THIRD = 0
CAM_FIRST = 1
CAM_TOP = 2
camera_mode = CAM_THIRD

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

def keyboardListener(key, x, y):
    k = key if isinstance(key, bytes) else bytes(key, 'utf-8')
    k = k.lower()
    if k == b'1': camera_mode = CAM_FIRST
    if k == b'2': camera_mode = CAM_THIRD
    if k == b'3': camera_mode = CAM_TOP

def mouseListener(button, state, x, y):
    global camera_mode
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        camera_mode = CAM_THIRD if camera_mode!=CAM_THIRD else CAM_FIRST