from ..regions import _Room
from ..io import DungeonIO, BuildContext
from vmath import *
from ..schema import Rect
import math

class BaseRoomPlacer:
    """提供自定义房间插入规则的接口"""

    def place_room(self, region: _Room, io: DungeonIO, context: BuildContext):
        '''仅设置region的base, 不修改其他属性'''
        raise NotImplementedError


class LinearRoomPlacer(BaseRoomPlacer):

    direction: vec2
    distance_ratio: float

    def __init__(self, direction: vec2, distance_ratio: float):
        self.direction = direction / direction.length()
        self.distance_ratio = distance_ratio

    def place_room(self, region: _Room, io: DungeonIO, context: BuildContext):
        """
        使用direction控制该房间插入的方向, 使用distance_ratio控制该房间中点与context.region中点的间距
        不可被用于first_build
        只修改region.base
        """
        assert self.distance_ratio > 1  # 否则房间重叠

        region_wh = vec2i(region.m_terrain.width, region.m_terrain.height)

        distance: float = self.distance_ratio * (\
            (region_wh.x**2 + region_wh.y**2) ** 0.5\
            * 0.5\
            + (\
                context.region.get_rect().x ** 2\
                + context.region.get_rect().y ** 2\
            )\
            ** 0.5\
            * 0.5\
        )
        offset_vec2 = self.direction * distance
        """
        
        +-----------+
        |           |
        |     .A    | context.region
        |           |
        +-----------+ A'
        
        
                  B' +-----------+
                     |           |
                     |     .B    | region (under construction)
                     |           |
                     +-----------+
        
                      ->
        offset_vec2 = AB = direction * distance_ratio * (|AA'|+|BB'|)
        
        """

        rect_A = context.region.get_rect()

        rect_B = Rect(None, None, region_wh.x, region_wh.y)


        rect_B.center = rect_A.center + offset_vec2
        assert rect_B.x is not None and rect_B.y is not None

        region.base = vec2i(int(math.ceil(rect_B.x)), int(math.ceil(rect_B.y)))
