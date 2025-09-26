from typing import Generator, Callable, TypeVar

T = TypeVar('T')
Future = Generator[None, None, T]


class Task:
    def call(self, context: dict) -> float:
        return NotImplemented
    
    def call_async(self, context: dict) -> Future[float]:
        raise NotImplementedError(type(self))
    
    def __call__(self, context: dict) -> Future[float]:
        res = self.call(context)
        if res is NotImplemented:
            res = yield from self.call_async(context)
        return res

    callback: type['_Callback']
    future_callback: type['_FutureCallback']
    pipeline: type['_Pipeline']
    concurrent: type['_Concurrent']

    def with_context(self, context: dict) -> '_Contextual':
        return _Contextual(context, self)

class _Contextual(Task):
    def __init__(self, context: dict, task: Task):
        self.context = context
        self.task = task

    def call(self, context: dict) -> float:
        return self.task.call(self.context)
    
    def call_async(self, context: dict) -> Future[float]:
        return self.task.call_async(self.context)

class _Callback(Task):
    def __init__(self, func: Callable[[dict], float | None]):
        self.func = func

    def call(self, context: dict) -> float:
        res = self.func(context)
        if res is None:
            return 0.0
        return res * 1.0
    
class _FutureCallback(Task):
    def __init__(self, func: Callable[[dict], Future[float]]):
        self.func = func

    def call_async(self, context: dict) -> Future[float]:
        return self.func(context)

class _Pipeline(Task):
    def __init__(self, tasks: list[Task]):
        for task in tasks:
            if not isinstance(task, Task):
                raise TypeError(f'expect Task, got {type(task).__name__}')
        self.tasks = tasks

    def call_async(self, context: dict) -> Future[float]:
        duration = 0.0
        for task in self.tasks:
            res = yield from task(context)
            duration += res
        return duration
    
class _Concurrent(Task):
    def __init__(self, tasks: list[Task]):
        for task in tasks:
            if not isinstance(task, Task):
                raise TypeError(f'expect Task, got {type(task).__name__}')
        self.tasks = tasks

    def call_async(self, context: dict):
        duration = 0.0
        futures = [iter(task(context)) for task in self.tasks]
        completed = [False] * len(futures)

        while True:
            all_completed = True
            for i in range(len(futures)):
                if completed[i]:
                    continue
                all_completed = False
                try:
                    next(futures[i])
                except StopIteration as e:
                    duration = max(duration, e.value)
                    completed[i] = True
            if all_completed:
                return duration
            yield


Task.callback = _Callback
Task.future_callback = _FutureCallback
Task.pipeline = _Pipeline
Task.concurrent = _Concurrent

__all__ = ['Task']
