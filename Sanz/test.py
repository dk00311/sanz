manager.add(spawn_bs_pattern_8, 110, 19)

def spawn_bs_pattern_8():
    global count
    count += 1

    x = -600 * math.sin(count / 3) + arena_x + arena_width / 2
    y = -600 * math.cos(count / 3) + arena_y + arena_height / 2

    start_x = -800 * math.sin(count / 3) + screen_width / 2
    start_y = -800 * math.cos(count / 3) + screen_height / 2

    dx = arena_x + arena_width / 2 - x
    dy = arena_y + arena_height / 2 - y
    rotate = math.degrees(math.atan2(dx, dy))

    bs = Blaster((start_x, start_y), (x, y), 400, 300, 100, rotate, (35, 150))
    bs.add(blasters)