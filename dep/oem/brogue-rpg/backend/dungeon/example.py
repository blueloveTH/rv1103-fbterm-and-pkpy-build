# import random
# from array2d import array2d
# from vmath import vec2i

# from backend.world import PrimedZone

# from backend.classes import (
#     building as B,
#     terrain as T
# )

# def impulse_noise(width: int, height: int, prob: int, seed: int) -> array2d[bool]:
#     rnd = random.Random(seed)
#     default_val = lambda _: rnd.randint(1, 100) <= prob
#     return array2d[bool](width, height, default_val)

# def _process(m_in: array2d[int], m_out: array2d[int], k1: array2d[int], k2: array2d[int], f1: int, f2: int):
#     m_out = m_out.copy()
#     w, h = m_in.width, m_in.height
#     f1cnt = m_in.convolve(k1, 0)
#     f2cnt = m_in.convolve(k2, 0) if f2 != 0 else array2d(w, h, 0)
#     for y in range(1, h-1):
#         for x in range(1, w-1):
#             pos = vec2i(x, y)
#             f1val, f2val = f1cnt[pos], f2cnt[pos]
#             if f1val >= f1 or (f2 != 0 and f2val <= f2):
#                 m_out[pos] = 1
#             else:
#                 m_out[pos] = 0
#     return m_out

# def postfix_noise(nummap: array2d[int], loop: int, f1: int, f2: int = 0) -> array2d[int]:
#     """Process the impulse noise map.

#     The function loops `loop` times, and replace the cell judging with threshold f1 and f2.
#     """
#     k1 = array2d.fromlist([
#         [1, 1, 1],
#         [1, 1, 1],
#         [1, 1, 1]])
    
#     k2 = array2d.fromlist([
#         [0, 1, 1, 1, 0],
#         [1, 1, 1, 1, 1],
#         [1, 1, 1, 1, 1],
#         [1, 1, 1, 1, 1],
#         [0, 1, 1, 1, 0]])

#     w, h = nummap.width, nummap.height
#     ONES = array2d(w, h, 1)
#     nummap = _process(nummap, ONES, k1, k2, f1, f2)
#     for _ in range(loop-1):
#         nummap = _process(nummap, nummap, k1, k2, f1, f2)
#     return nummap

# def build(width: int, height: int, seed: int) -> PrimedZone:
#     terrain = impulse_noise(width, height, 40, seed)
#     terrain = terrain.map(lambda x: 1 if x else 0)
#     terrain = postfix_noise(terrain, 4, 5, 1)
#     terrain = postfix_noise(terrain, 3, 5)
#     # 填充墙壁
#     visited, _ = terrain.get_connected_components(1, "von Neumann")
#     terrain[visited == 1] = 2 # 💦 -> 🧱

#     mappings = [T.Empty(), T.Water(), T.Wall()]
#     return PrimedZone(
#         width=width,
#         height=height,
#         m_terrain=array2d(width, height, lambda xy: mappings[terrain[xy]]),
#         m_building=array2d(width, height, B.Building.zero()),
#         m_region=array2d(width, height, 1),
#         entries=[]
#     )
