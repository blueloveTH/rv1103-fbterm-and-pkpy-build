from driver import step_game
import time

while True:
    start = time.perf_counter()
    if not step_game():
        break
    elapsed = time.perf_counter() - start
    if elapsed < 1 / 30:
        time.sleep(1 / 30 - elapsed)
