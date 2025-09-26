from backend.dungeon.example import build

seed = 2024

zone = build(50, 30, seed)

import pickle as pkl
import lz4

encoded = pkl.dumps(zone)
compressed = lz4.compress(encoded)
print(len(encoded)/1024, 'KB', len(compressed)/1024, 'KB')

zone = pkl.loads(lz4.decompress(compressed))

print(zone.m_terrain.map(lambda t: t.char).render())
