import time
from dataclasses import dataclass
from typing import Optional, Dict, List
from vmath import color32

# 全局跟踪器字典和上下文栈
_trackers: Dict[str, 'ProgressTracker'] = {}
_tracker_stack: List['ProgressTracker'] = []  # 改为使用列表

@dataclass
class StepInfo:
    name: str
    duration: float
    last_step_name: str
    percentage: float = 0.0

class ProgressTracker:
    def __init__(self, name: str, total_steps: int = -1, auto_start: bool = True, summery_color: color32|None = None):
        if name in _trackers:
            raise ValueError(f"Tracker with name '{name}' already exists")
        
        assert isinstance(total_steps, int) and total_steps >= -1
        self.total_steps = total_steps
        self.name = name
        self.current_step = 0
        self.start_time = time.time() if auto_start else None
        self.last_step_time = self.start_time
        self.step_history = []
        self._active = auto_start
        self._is_auto_started = False
        self.summery_color = summery_color if summery_color else color32(84, 189, 55, 255)
        _trackers[name] = self
        
        if auto_start:
            _tracker_stack.append(self)  # 使用列表的append方法
            self.step("Start timing")
            self._is_auto_started = True
    
    def _get_indent(self) -> str:
        """获取当前tracker的缩进级别"""
        try:
            level = _tracker_stack.index(self)  # 使用列表的index方法
            return "  " * level
        except ValueError:
            return ""
    
    def __enter__(self):
        if not self._active and not self._is_auto_started:
            self.start_time = time.time()
            self.last_step_time = self.start_time
            self._active = True
            _tracker_stack.append(self)  # 使用列表的append方法
            self.step("Enter context")
        return self
    
    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        if not self._active:
            return
        self.step("Exit context")
        total_time = time.time() - self.start_time
        status = "completed" if exc_type is None else "interrupted"
        
        # 计算时间占比
        if total_time > 0 and self.step_history:
            for step_info in self.step_history:
                step_info.percentage = (step_info.duration / total_time) * 100
        
        indent = self._get_indent()
        print(self.summery_color.ansi_fg(f"\n{indent}{self.name}: {status} in {total_time:.2f}s"))
        for i, step_info in enumerate(self.step_history):
            line = "|  "
            if i == len(self.step_history) - 1:
                line = "└--"
            if not step_info.last_step_name == "_":
                print(self.summery_color.ansi_fg(f"{indent}{line}Step {i}: '{step_info.last_step_name}' --> '{step_info.name}' - {step_info.duration:.2f}s ({step_info.percentage:.1f}%)"))
        
        self._active = False
        if self in _tracker_stack:
            _tracker_stack.remove(self)  # 使用列表的remove方法
    
    def step(self, step_name: Optional[str] = None):
        if not self._active:
            raise RuntimeError(f"Tracker '{self.name}' is not active")
            
        now = time.time()
        indent = self._get_indent()
        
        # 记录上一步的信息（包括第一步）
        if self.current_step > 0:
            last_duration = now - self.last_step_time
            step_info = StepInfo(
                name=step_name or f"Step {self.current_step}",
                duration=last_duration,
                last_step_name=self.step_history[-1].name
            )
            
            self.step_history.append(step_info)
        else:
            # 记录第一步的信息
            step_info = StepInfo(
                name=step_name,
                duration=now - self.start_time,
                last_step_name="_"
            )
            self.step_history.append(step_info)
        
        
        
        # 打印信息
        if self.current_step == 0:
            print(
                f"{indent}{self.name}: starting step '{step_info.name}'"
            )
        else:
            if self.total_steps == -1:
                print(
                    f"{indent}{self.name}: [{self.current_step}] ",
                    f"'{step_info.last_step_name}' --> '{step_info.name}' took {step_info.duration:.2f}s",
                )
            else:
                completed = self.current_step
                remaining = self.total_steps - self.current_step
                
                print(
                    f"{indent}{self.name}: [{completed}/{self.total_steps}] ",
                    f"'{step_info.last_step_name}' --> '{step_info.name}' took {step_info.duration:.2f}s",
                )
            
        self.current_step += 1
        self.last_step_time = now
        
        # 如果是最后一步，确保记录它
        if self.total_steps != -1 and self.current_step == self.total_steps:
            now = time.time()
            step_info = StepInfo(
                name=step_name or f"Step {self.current_step}",
                duration=now - self.last_step_time,
                last_step_name=self.step_history[-1].name
            )
            self.step_history.append(step_info)
            self.last_step_time = now

def get_tracker(name: Optional[str] = None) -> Optional[ProgressTracker]:
    """获取跟踪器实例"""
    if name is not None:
        return _trackers.get(name)
    
    # 返回栈顶的跟踪器（最近的）
    if _tracker_stack:
        return _tracker_stack[-1]  # 使用列表的-1索引获取最后一个元素
    
    # 如果没有活动的，尝试返回唯一的活跃跟踪器
    active = [t for t in _trackers.values() if t._active]
    if len(active) == 1:
        return active[0]
    
    return None

def step(step_name: Optional[str] = None, name: Optional[str] = None):
    """
    执行step操作
    :param step_name: 步骤名称
    :param name: 跟踪器名称，不指定时自动匹配最近的跟踪器
    """
    tracker = get_tracker(name)
    if tracker is None:
        if name is not None:
            raise ValueError(f"No tracker found with name '{name}'")
        raise RuntimeError("No active tracker found in context")
    tracker.step(step_name)