from vmath import vec2i
from array2d import array2d
from noises.basics.voronoi import Voronoi
from noises.basics.perlin import Perlin
from noises.basics.algorithm import laplace_area

# {"post_operations": [("Threshold(x, param)", 1.2)]}
# [
#     {
#         "falloff": 55.46,
#         "lacunarity": 0.0,
#         "noise_type": "Voronoi",
#         "octaves": 1,
#         "operations": [("Laplace(pos)", 0.0), ("Multiply(x, param)", -10.0)],
#         "persistence": 0.0,
#         "radius": 1,
#         "scale": 10.89,
#     },
#     {
#         "lacunarity": 0.0,
#         "noise_type": "Perlin",
#         "octaves": 1,
#         "operations": [("Threshold(x, param)", 0)],
#         "persistence": 0.0,
#         "scale": 5.66,
#     },
# ]

def wasteland_rift_noise(origin:vec2i, width:int, height:int, seed:int) -> float:
    voronoi = Voronoi(seed)
    perlin = Perlin(seed)
    
    
    padding = 1  # laplace 需要padding
    width_padded = width + 2*padding
    height_padded = height + 2*padding
    layer_1 = array2d(width_padded, height_padded)
    for i in range(width_padded):
        for j in range(height_padded):
            pos = vec2i(i, j) + origin
            layer_1[i, j] = voronoi.noise_ex(
                pos.x/10.89, pos.y/10.89, 0,
                1,
                persistence=0.0,
                lacunarity=0.0,
                radius=1,
                falloff=55.46)
    
    layer_1 = laplace_area(layer_1)
    layer_1 = layer_1 * -10.0
    
    
    layer_2 = array2d(width, height)
    for i in range(width):
        for j in range(height):
            pos = vec2i(i, j) + origin
            layer_2[i, j] = perlin.noise_ex(
                pos.x/5.66, pos.y/5.66, 0,
                1,
                persistence=0.0,
                lacunarity=0.0)
    
    result = layer_1 + layer_2
    result = result.map(lambda x: 1.2 if x > 1.2 else 0)
    
    return result
    