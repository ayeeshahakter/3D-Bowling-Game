def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION); glPushMatrix(); glLoadIdentity()
    gluOrtho2D(0, win_w, 0, win_h)
    glMatrixMode(GL_MODELVIEW); glPushMatrix(); glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text: glutBitmapCharacter(font, ord(ch))
    glPopMatrix(); glMatrixMode(GL_PROJECTION); glPopMatrix(); glMatrixMode(GL_MODELVIEW)

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
