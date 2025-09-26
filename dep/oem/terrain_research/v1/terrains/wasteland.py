"""
荒原

- 无状态
    - 山脉: Voronoi(荒原不是山地, 因此山脉比较稀疏)
        - 山体
        - 矿脉
        - 房间壁(外部 bit mask)

    - 裂谷: Voronoi √

    - 水洼: 块状分布+零星小水坑
    
    - 枯木林: 块状分布,以前可能是森林
    
    - 草丛: 块状分布+零星散布
    
    - 复杂结构(种子)
        - 小型废墟
        - 迷宫
    
- 有状态
    - 小型废墟
    - 迷宫

"""


from random import Random
from array2d import array2d
from schema.base import AsciiSprite, EnvironmentObjectSeed, StructureSeed
from vmath import vec2i
from schema.terrian import TerrianCell
from schema.base import TilesetId, TileIndex
from terrains.utils import show_terrain
from noises.basics.algorithm import advanced_sigmoid, hash_vec2i_to_f


from noises import wasteland_rift_noise, wasteland_water_content_noise

def _select_last_not_none(pos:vec2i, arrs: list[array2d]):
    result = None
    for arr in arrs[::-1]:
        if arr[pos] is not None:
            result = arr[pos]
            break
    return result
    
    
def _cell_maker(pos: vec2i, tile_layers: list[array2d[TileIndex|None]], env_obj_layers: list[array2d[EnvironmentObjectSeed|None]], structure_layers: list[array2d[StructureSeed|None]]) -> TerrianCell:
    
    tile_id = _select_last_not_none(pos, tile_layers)
    assert tile_id is not None
    
    env_obj_seed = _select_last_not_none(pos, env_obj_layers)
    
    structure_seed = _select_last_not_none(pos, structure_layers)
    
    return TerrianCell(
        tile_id,
        env_obj_seed,
        structure_seed
    )


def request_area(orign:vec2i, width:int, height:int, seed:int|None=None) -> array2d[TerrianCell]:
    
    seed = seed or 123456
    rnd = Random(seed)
    
    # ground 
    is_ground = array2d(width, height, lambda pos: True)
    ground_layer = is_ground.map(lambda x: TileIndex(TilesetId.Ground, 1) if x else None)    
    step("ground")
    
    
    # 裂谷 
    is_rift = wasteland_rift_noise.noise_area(orign, width, height, 1, seed) > 0.5
    step("裂谷噪声")
    rift_layer = is_rift.map(lambda x: TileIndex(TilesetId.Chasm, 0) if x else None)
    step("生成裂谷")


    
    # 含水量
    water_content = wasteland_water_content_noise.noise_area(orign, width, height, 1, seed)
    step("含水量噪声")
    
    # 水洼--水洼附近的含水量通常最高
    is_water = water_content.map(lambda x: advanced_sigmoid(x, 30, 0.5) > rnd.random())
    water_layer = is_water.map(lambda x: TileIndex(TilesetId.Water, 0) if x else None)
    step("水洼")
    
    # 草丛--草丛倾向于聚集在含水量高的地方
    grass_random = array2d(width, height, lambda pos: hash_vec2i_to_f(pos, seed+1))
    is_grass = (water_content > grass_random) & (~ is_water) & (~ is_rift)
    grass_layer = is_grass.map(lambda x: EnvironmentObjectSeed(vec2i(0,1), vec2i(1,1)) if x else None)
    step("草丛")
    
    # 枯木--枯木倾向于聚集在含水量低的地方
    dry_grass_random = array2d(width, height, lambda pos: hash_vec2i_to_f(pos, seed+3))
    is_dry_grass = (water_content.map(lambda x: advanced_sigmoid(
        x,
        k=-10,              # 越是干的地方枯木越多
        center=0.5,         
        output_low=0,       
        output_high=0.02    # 最高概率 5%
        )) > dry_grass_random) & (~ is_water) & (~ is_rift)
    dry_grass_layer = is_dry_grass.map(lambda x: EnvironmentObjectSeed(vec2i(0,2), vec2i(1,1)) if x else None)
    step("枯木")
    
    
    
    result:array2d[TerrianCell] = array2d(width, height, 
        lambda pos: _cell_maker(
            pos,
            [
                ground_layer,
                rift_layer,
                water_layer
            ],
            [
                grass_layer,
                dry_grass_layer
            ],
            [
                
            ]
        )
    )
    step("合成结果")
    return result


if __name__ == "__main__":
    from dev_tools.progress_tracker import ProgressTracker, step
    print(hash_vec2i_to_f(vec2i(10,10), 123456))
    with ProgressTracker("荒原", 7) as _:
        show_terrain(request_area(vec2i(100000000,100000010), 300, 300, 123456), True)