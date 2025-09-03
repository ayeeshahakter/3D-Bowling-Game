# Variables for multiplayer
max_players = 4
player_names = ["Player 1","Player 2","Player 3","Player 4"]
num_players = 2
current_player = 0
frames = [[[ -1, -1, -1 ] for _ in range(10)] for __ in range(max_players)]
throw_counter = [0]*max_players

def keyboardListener(key, x, y):
    k = key if isinstance(key, bytes) else bytes(key, 'utf-8')
    k = k.lower()
    if k == b'n': num_players = 2 if num_players==4 else num_players+1

def idle():
    global current_player
    if not in_flight and standing_at_throw_start>=0:
        pid = current_player; f = frame_idx[pid]; r = roll_idx[pid]
        if f>=10 or roll_idx[pid]==0:
            current_player = (current_player+1) % num_players
            if current_player != prev_player:
                _reset_ball()
                _reset_pins(True)
                _spawn_obstacles()
                trail_points.clear()
                result_text = ""
                slowmo_timer_ms = 0
                bonus_pin_active = False
                bonus_pin_index = -1
                next_bonus_check_ms = t_ms + random.randint(4000,9000)
                standing_at_throw_start = -1

def showScreen():
    y0 = win_h-110
    for pid in range(num_players):
        glColor3f(1, 1, 0) if pid == current_player else glColor3f(1, 1, 1)
        line = f"{player_names[pid]} | "
        for f in range(10):
            a,b,c = frames[pid][f]
            aa = '-' if a<0 else str(a); bb = '-' if b<0 else str(b); cc = '' if f<9 else ('-' if c<0 else str(c))
            if f<9: line += f"[{aa},{bb}]"
            else: line += f"[{aa},{bb},{cc}]"
        line += f"  = {_score_for_player(pid)}"
        draw_text(10, y0-20*pid, line)
    draw_text(10, 70, f"Current: {player_names[current_player]} | Throws: {throw_counter[current_player]}")