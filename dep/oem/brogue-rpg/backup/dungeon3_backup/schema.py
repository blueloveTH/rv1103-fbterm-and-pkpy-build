from abc import abstractmethod
from dataclasses import dataclass
from array2d import array2d
from vmath import vec2, vec2i
import random

class Rect:
    def __init__(self, x:float, y:float, w:float, h:float):
        assert w > 0 and h > 0
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    @property
    def center(self):
        """获取矩形的中心坐标"""
        return vec2(self.x + self.w / 2, self.y + self.h / 2)

    @center.setter
    def center(self, pos:vec2):
        """设置矩形的中心坐标"""
        conor = pos - vec2(self.w, self.h)/2
        self.x, self.y = conor.x, conor.y

    def __repr__(self):
        return f"Rect(x={self.x:.2f}, y={self.y:.2f}, w={self.w:.2f}, h={self.h:.2f})"



@dataclass
class GenParams:
    # 外部传递给房间的参数结构体, 分为地形, 通道, 以及确定位置和rect
    pass
    

class AbstractRoom:  # 房间类，负责地形生成和连接
    local_terrian: array2d[int]
    rect: Rect
    m_points: list[vec2i]
    default_gen_params: GenParams
    
    def _get_gen_params(self, gen_params: GenParams|None) -> GenParams:
        """获取生成参数"""
        return self.default_gen_params if gen_params is None else gen_params
        

    def __init__(self):
        self.m_points = []  # 初始化连接点列表

    def finish_rect(self, gen_params: GenParams|None):
        """模板方法，调用子类专属的 _finish_rect_impl 方法"""
        specific_gen_params = self._get_gen_params(gen_params)
        self._finish_rect_impl(specific_gen_params)
    
    def finish_terrian(self, gen_params: GenParams|None):
        """模板方法，调用子类专属的 _finish_terrian_impl 方法"""
        specific_gen_params = self._get_gen_params(gen_params)
        self._finish_terrian_impl(specific_gen_params)
    
    def add_insertion_point(self, point: vec2i):
        """添加插入点"""
        self.m_points.append(point)
    
    def connect_to(self, other_connectable: "AbstractRoom"):
        """将当前房间与另一个房间逻辑连接"""
        self._connect_to_impl(other_connectable)
        
        
    
    @abstractmethod
    def _finish_rect_impl(self, gen_params: GenParams):
        """子类专属的房间矩形完成逻辑"""
        pass
    
    @abstractmethod
    def _finish_terrian_impl(self, gen_params: GenParams):
        """子类专属的地形完成逻辑"""
        pass
    
    @abstractmethod
    def _connect_to_impl(self, other_connectable: "AbstractRoom"):
        """子类专属的连接逻辑"""
        pass


class SimpleRoom(AbstractRoom):
    
    def _finish_rect_impl(self, gen_params: GenParams):
        # 实现完成房间矩形的逻辑
        print(f"[SimpleRoom] 完成矩形，使用参数: {gen_params}")
        # 这里可以添加更复杂的矩形生成逻辑
    
    def _finish_terrian_impl(self, gen_params: GenParams):
        # 实现完成地形的逻辑
        print(f"[SimpleRoom] 完成地形，使用参数: {gen_params}")
        # 这里可以添加更复杂的地形生成逻辑

    def _connect_to_impl(self, other_connectable: "AbstractRoom"):
        # 实现与其他房间连接的逻辑
        print(f"[SimpleRoom] 正在连接到另一个房间: {other_connectable}")
        # 这里可以添加连接逻辑，如共享边界或其他操作


    
def carve_dungeon():
    # 主循环
    # emmmmm
    