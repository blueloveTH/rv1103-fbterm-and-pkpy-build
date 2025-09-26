from random import randint
import operator


class Expr[T]:
    def __call__(self, context) -> T:
        raise NotImplementedError(type(self))
    
    def __add__(self, other):
        return BinaryOp(self, other, 'add')
    def __sub__(self, other):
        return BinaryOp(self, other, 'sub')
    def __mul__(self, other):
        return BinaryOp(self, other, 'mul')
    def __truediv__(self, other):
        return BinaryOp(self, other, 'truediv')
    def __floordiv__(self, other):
        return BinaryOp(self, other, 'floordiv')
    def __and__(self, other):
        return BinaryOp(self, other, 'and_')
    def __or__(self, other):
        return BinaryOp(self, other, 'or_')
    def __xor__(self, other):
        return BinaryOp(self, other, 'xor')

    def __eq__(self, other): # type: ignore
        return BinaryOp(self, other, 'eq')
    def __ne__(self, other): # type: ignore
        return BinaryOp(self, other, 'ne')
    def __lt__(self, other):
        return BinaryOp(self, other, 'lt')
    def __le__(self, other):
        return BinaryOp(self, other, 'le')
    def __gt__(self, other):
        return BinaryOp(self, other, 'gt')
    def __ge__(self, other):
        return BinaryOp(self, other, 'ge')
    
    def __neg__(self):
        return UnaryOp(self, 'neg')
    def __invert__(self):
        return UnaryOp(self, 'invert')
    
    @staticmethod
    def value(value):
        return Value(value)
    
    @staticmethod
    def random(min: int, max: int):
        return Random(min, max)
    
    @staticmethod
    def conditional(condition: 'Expr[bool]', if_true: 'Expr', if_false: 'Expr'):
        return Conditional(condition, if_true, if_false)
    
    @staticmethod
    def context(key: str, path: str | None = None):
        return ContextAttr(key, path)
    
    @staticmethod
    def eval(expr: str):
        return BuiltinEval(expr)


class Value(Expr):
    def __init__(self, value):
        self.value = value
    def __call__(self, context):
        return self.value


class Random(Expr):
    def __init__(self, min: int, max: int):
        self.min = min
        self.max = max

    def __call__(self, context):
        return randint(self.min, self.max)


class Conditional(Expr):
    def __init__(self, condition: Expr[bool], if_true: Expr, if_false: Expr):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def __call__(self, context):
        if self.condition(context):
            return self.if_true(context)
        else:
            return self.if_false(context)


class ContextAttr(Expr):
    def __init__(self, key: str, path: str | None = None):
        self.key = key
        self.path = path

    def __call__(self, context):
        obj = context[self.key]
        if self.path is None:
            return obj
        return eval(f'_.{self.path}', {'_': obj})


class BuiltinEval(Expr):
    def __init__(self, expr: str):
        self.expr = expr

    def __call__(self, context):
        return eval(self.expr, context)


class BinaryOp(Expr):
    def __init__(self, lhs: Expr, rhs: Expr | int, op: str):
        assert isinstance(lhs, Expr)
        if type(rhs) is int:
            rhs = Value(rhs)
        assert isinstance(rhs, Expr)
        self.lhs = lhs
        self.rhs = rhs
        self.op = op

    def __call__(self, context):
        _0 = self.lhs(context)
        _1 = self.rhs(context)
        return getattr(operator, self.op)(_0, _1)
    

class UnaryOp(Expr):
    def __init__(self, expr: Expr, op: str):
        assert isinstance(expr, Expr)
        self.expr = expr
        self.op = op

    def __call__(self, context):
        _0 = self.expr(context)
        return getattr(operator, self.op)(_0)
