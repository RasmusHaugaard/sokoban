from time import time

before = time()

last_log = before
max_dt = 0
frame_count = 0

min_fps = []
avg_fps = []

while len(min_fps) < 20:
    frame_count += 1

    now = time()
    dt = now - before
    before = now

    if dt > max_dt: max_dt = dt
    if now - last_log > 2:
        min_fps.append(1 / max_dt)
        avg_fps.append(frame_count / 2)
        max_dt = 0
        last_log = now
        frame_count = 0

with open('fps_log.txt', 'w') as f:
    for mi, avg in zip(min_fps, avg_fps):
        f.write(str(mi) + ' - ' + str(avg) + '\n')
