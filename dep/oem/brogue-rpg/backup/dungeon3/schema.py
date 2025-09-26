from enum import Enum

from typing import Literal

from array2d import array2d
from dataclasses import dataclass
from vmath import vec2, vec2i

import math




@dataclass
class TerrainValues:
    # 默认0是"虚空"
    BLANK: int
    WALL: int


def if_terrain_in_region(terrain_value: int, t_values: TerrainValues) -> bool:
    if terrain_value == t_values.BLANK:
        return True # 目前只有 BLANK 地形算作房间内部的地形, 这里的 BLANK 在本包内被视作是可通行区域, 具体值由外部调用者传入
    
    return False


class Rect:

    @staticmethod
    def init_from_(bounding_rect: tuple[vec2i, vec2i]) -> "Rect":
        xy, wh = bounding_rect
        assert xy is not None and wh is not None
        x, y = xy.x, xy.y
        w, h = wh.x, wh.y
        return Rect(x, y, w, h)

    def __init__(self, x:float, y:float, w:float, h:float):
        assert w > 0 and h > 0
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    @property
    def xy(self) -> vec2:
        return vec2(self.x, self.y)

    @xy.setter
    def xy(self, pos:vec2):
        self.x = pos.x
        self.y = pos.y

    @property
    def wh(self) -> vec2:
        return vec2(self.w, self.h)

    @wh.setter
    def wh(self, size:vec2):
        self.w, self.h = size.x, size.y

    @property
    def center(self) -> vec2:
        """获取矩形的中心坐标"""
        assert self.x is not None and self.y is not None
        return vec2(self.x + self.w / 2, self.y + self.h / 2)

    @center.setter
    def center(self, pos:vec2):
        """设置矩形的中心坐标"""
        conor = pos - vec2(self.w, self.h)/2
        self.x, self.y = conor.x, conor.y

    def __repr__(self):
        if self.x is None or self.y is None:
            return f"Rect(x=None, y=None, w={self.w:.2f}, h={self.h:.2f})"
        return f"Rect(x={self.x:.2f}, y={self.y:.2f}, w={self.w:.2f}, h={self.h:.2f})"


    def overlap(self, other:"Rect") -> "Rect|None":
        """计算两个矩形的重叠部分"""
        assert self.x is not None and self.y is not None
        assert other.x is not None and other.y is not None
        rect1 = self
        rect2 = other
        assert rect1.x is not None and rect1.y is not None
        assert rect2.x is not None and rect2.y is not None

        # 计算重叠区域的左下角和右上角
        overlap_x1 = max(rect1.x, rect2.x)
        overlap_y1 = max(rect1.y, rect2.y)
        overlap_x2 = min(rect1.x + rect1.w, rect2.x + rect2.w)
        overlap_y2 = min(rect1.y + rect1.h, rect2.y + rect2.h)

        # 检查是否存在重叠
        if overlap_x1 < overlap_x2 and overlap_y1 < overlap_y2:
            overlap_w = overlap_x2 - overlap_x1
            overlap_h = overlap_y2 - overlap_y1
            return Rect(overlap_x1, overlap_y1, overlap_w, overlap_h)
        else:
            return None
        
    def copy(self)-> 'Rect':
        return Rect(self.x, self.y, self.w, self.h)
    
    def local_to_global(self, local_pos: vec2) -> vec2:
        """将局部坐标转换为全局坐标"""
        assert self.x is not None and self.y is not None
        global_x = self.x + local_pos.x
        global_y = self.y + local_pos.y
        return vec2(global_x, global_y)
    
    def global_to_local(self, global_pos: vec2) -> vec2:
        """将全局坐标转换为局部坐标"""
        assert self.x is not None and self.y is not None
        local_x = global_pos.x - self.x
        local_y = global_pos.y - self.y
        return vec2(local_x, local_y)
    
    def up_scale(self, ratio_or_vec2:float|int|vec2) -> None:
        """将矩形的尺寸放大(或缩小)"""
        assert self.x is not None and self.y is not None
        if isinstance(ratio_or_vec2, float) or isinstance(ratio_or_vec2, int):
            assert ratio_or_vec2 > 0
            center = self.center
            self.w *= ratio_or_vec2
            self.h *= ratio_or_vec2
            self.center = center
        elif isinstance(ratio_or_vec2, vec2):
            center = self.center
            self.w += ratio_or_vec2.x
            self.h += ratio_or_vec2.y
            self.center = center
        else:
            raise ValueError(f"Invalid argument type (accept float, int or vec2), got {type(ratio_or_vec2)}")

    def up_scaled(self, ratio_or_vec2:float|int|vec2) -> "Rect":
        """将矩形的尺寸放大(或缩小)"""
        assert self.x is not None and self.y is not None
        if isinstance(ratio_or_vec2, float) or isinstance(ratio_or_vec2, int):
            assert ratio_or_vec2 > 0
            new_rect = self.copy()
            center = new_rect.center
            new_rect.w *= ratio_or_vec2
            new_rect.h *= ratio_or_vec2
            new_rect.center = center
            return new_rect
        elif isinstance(ratio_or_vec2, vec2):
            new_rect = self.copy()
            center = new_rect.center
            new_rect.w += ratio_or_vec2.x
            new_rect.h += ratio_or_vec2.y
            new_rect.center = center
            return new_rect
        else:
            raise ValueError(f"Invalid argument type (accept float, int or vec2, got {type(ratio_or_vec2)}")
        
    def floor_align(self) -> 'Rect':
        """将矩形的左上角坐标以及长宽对齐到整数"""
        assert self.x is not None and self.y is not None
        return Rect(math.floor(self.x), math.floor(self.y), math.floor(self.w), math.floor(self.h))