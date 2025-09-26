from typing import TYPE_CHECKING, Literal, Self

if TYPE_CHECKING:
    from backend.asyncio import Task
    from backend.models.event import Event, LocalEvent
    from .stats import Stats, FieldCpnt

from .expr import Expr


class Affix:
    pass


class Modifier(Affix):
    def __init__(self, path: str, value: int):
        self.path = path
        self.value = value

    def __call__(self, stats: Stats, cpnt: FieldCpnt) -> None:
        exec(f"_0.{self.path}.{cpnt} += _1", {'_0': stats, '_1': self.value})

    def __repr__(self) -> str:
        return f'Modifier({self.path!r}, {self.value!r})'


class Trigger(Affix):
    def __init__(self, event: Event | LocalEvent, condition: Expr[bool] | None = None, priority: int = 0):
        self.event = event
        self.condition = condition
        self.priority = priority

    def check(self, context: dict) -> bool:
        assert context['event'] == self.event
        if self.condition is None:
            return True
        return self.condition(context)

    def __call__(self, context: dict) -> bool | None:
        raise NotImplementedError


class MethodCall:
    def __init__(self, target: Expr, method: str, *args: Expr):
        self.target = target
        self.method = method
        self.args = args

    def __call__(self, context: dict):
        obj = self.target(context)
        method = getattr(obj, self.method)
        method(*[arg(context) for arg in self.args])


class MethodTrigger(Trigger):
    def __init__(
            self,
            event: Event | LocalEvent,
            method_call: MethodCall,
            condition: Expr[bool] | None = None,
            priority: int = 0
            ):
        super().__init__(event, condition, priority)
        self.method_call = method_call

    def __call__(self, context: dict):
        self.method_call(context)


class AffixGroup:
    def __init__(self):
        self.modifiers = [] # type: list[Modifier]
        self.triggers = []  # type: list[Trigger]

    def append(self, affix: Affix) -> None:
        if isinstance(affix, Modifier):
            self.modifiers.append(affix)
        elif isinstance(affix, Trigger):
            self.triggers.append(affix)
        else:
            assert False

    def apply_modifiers(self, stats: Stats, cpnt: FieldCpnt) -> None:
        for m in self.modifiers:
            m(stats, cpnt)

    def __bool__(self) -> bool:
        return bool(self.modifiers) or bool(self.triggers)


__all__ = ['Affix', 'Modifier', 'Trigger', 'AffixGroup', 'MethodTrigger', 'MethodCall']