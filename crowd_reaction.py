result_text = ""
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