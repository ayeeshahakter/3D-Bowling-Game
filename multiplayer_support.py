player_names = ["Player 1","Player 2","Player 3","Player 4"]
current_player = 0
throw_counter = [0]*max_players
frames = [[[ -1, -1, -1 ] for _ in range(10)] for __ in range(max_players)]
frame_idx = [0]*max_players
roll_idx = [0]*max_players
        a,b,c = frames[pid][f]
    global slowmo_timer_ms, next_bonus_check_ms, current_player, standing_at_throw_start
    global throw_counter, frames, frame_idx, roll_idx, current_player
        pid = current_player; f = frame_idx[pid]; r = roll_idx[pid]
                    frames[pid][f][0] = min(10, val)
                    if frames[pid][f][0] == 10:
                        result_text = "STRIKE!"; slowmo_timer_ms = max(slowmo_timer_ms, 1000); roll_idx[pid]=0; frame_idx[pid]+=1
                        roll_idx[pid] = 1
                    frames[pid][f][1] = min(10 - (frames[pid][f][0] if frames[pid][f][0]>=0 else 0), val)
                    if (frames[pid][f][0] if frames[pid][f][0]>=0 else 0) + frames[pid][f][1] == 10:
                    roll_idx[pid] = 0; frame_idx[pid] += 1
                    frames[pid][f][0] = min(10,val); roll_idx[pid]=1
                    frames[pid][f][1] = min(10,val)
                    if frames[pid][f][0]==10 or frames[pid][f][0]+frames[pid][f][1]==10: roll_idx[pid]=2
                    else: roll_idx[pid]=0; frame_idx[pid]+=1
                    frames[pid][f][2] = min(10,val); roll_idx[pid]=0; frame_idx[pid]+=1
            throw_counter[pid] += 1
        if f>=10 or roll_idx[pid]==0:
            current_player = (current_player+1) % num_players
    draw_text(10, 70, f"Current: {player_names[current_player]} | Throws: {throw_counter[current_player]}")
        glColor3f(1, 1, 0) if pid == current_player else glColor3f(1, 1, 1)  # Yellow for current player, white for others
        line = f"{player_names[pid]} | "
            a,b,c = frames[pid][f]