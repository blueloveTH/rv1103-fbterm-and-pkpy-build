import pickle as pkl
from pkpy import is_user_defined_type
import base64
import json

from .encoders import Encoders, Decoders

_JSON_ENCODABLE_TYPES = (int, float, str, bool, type(None))

def pickle_wraps(obj):
    b = pkl.dumps(obj)
    return {
        '$': 'pickle',
        'data': base64.b64encode(b).decode(),
    }

def decode_object(obj: dict) -> object:
    module: str = obj['module']
    clazz: str = obj['class']
    state: dict = obj['state']
    cls = getattr(__import__(module), clazz)
    obj = object.__new__(cls)
    for k, v in state.items():
        setattr(obj, k, from_json_encodable(v))
    return obj

def decode_pickle(obj: dict) -> object:
    data: str = obj['data']
    b = base64.b64decode(data)
    return pkl.loads(b)

def decode_dict(obj: dict):
    return {k: from_json_encodable(v) for k, v in obj.items()}

Decoders['object'] = decode_object
Decoders['pickle'] = decode_pickle
Decoders['dict'] = decode_dict

def to_json_encodable(obj):
    t = type(obj)
    if t in _JSON_ENCODABLE_TYPES:
        return obj
    if t is list or t is tuple:
        return [to_json_encodable(i) for i in obj]
    if t is dict:
        all_string_keys = all([isinstance(k, str) and k!='$' for k in obj.keys()])
        if all_string_keys:
            return {k: to_json_encodable(v) for k, v in obj.items()}
        return pickle_wraps(obj)
    # try custom encoder
    encoder = Encoders.get(t)
    if encoder is not None:
        return encoder(obj)
    # try user-defined type
    if is_user_defined_type(t):
        return {
            '$': 'object',
            'module': t.__module__,
            'class': t.__name__,
            'state': {k: to_json_encodable(v) for k, v in obj.__dict__.items()},
        }
    # fallback to pickle
    return pickle_wraps(obj)

def from_json_encodable(obj):
    t = type(obj)
    if t in _JSON_ENCODABLE_TYPES:
        return obj
    if t is list or t is tuple:
        return [from_json_encodable(i) for i in obj]
    if t is dict:
        meta: str = obj.get('$', 'dict')
        return Decoders[meta](obj)
    raise TypeError(f'Cannot decode object of type {t}')

def dumps(obj):
    obj = to_json_encodable(obj)
    return pkl.dumps(obj)

def dumps_json(obj):
    obj = to_json_encodable(obj)
    return json.dumps(obj, indent=2)

def loads(data: str | bytes):
    if isinstance(data, str):
        raw = json.loads(data)
    elif isinstance(data, bytes):
        is_pickle = len(data) > 4 and data[:4] == '🥕'.encode()
        if is_pickle:
            raw = pkl.loads(data)
        else:
            raw = json.loads(data.decode())
    else:
        assert False
    return from_json_encodable(raw)
