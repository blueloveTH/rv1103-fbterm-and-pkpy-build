from vmath import *
    
def encode_vec2i(obj: vec2i):
    return {
        '$': 'vec2i',
        'x': obj.x,
        'y': obj.y,
    }
def decode_vec2i(obj: dict) -> vec2i:
    return vec2i(obj['x'], obj['y'])

def encode_vec3i(obj: vec3i):
    return {
        '$': 'vec3i',
        'x': obj.x,
        'y': obj.y,
        'z': obj.z,
    }
def decode_vec3i(obj: dict) -> vec3i:
    return vec3i(obj['x'], obj['y'], obj['z'])

def encode_vec2(obj: vec2):
    return {
        '$': 'vec2',
        'x': obj.x,
        'y': obj.y,
    }
def decode_vec2(obj: dict) -> vec2:
    return vec2(obj['x'], obj['y'])

def encode_vec3(obj: vec3):
    return {
        '$': 'vec3',
        'x': obj.x,
        'y': obj.y,
        'z': obj.z,
    }
def decode_vec3(obj: dict) -> vec3:
    return vec3(obj['x'], obj['y'], obj['z'])


Encoders = {
    vec2i: encode_vec2i,
    vec3i: encode_vec3i,
    vec2: encode_vec2,
    vec3: encode_vec3,
}

Decoders = {
    'vec2i': decode_vec2i,
    'vec3i': decode_vec3i,
    'vec2': decode_vec2,
    'vec3': decode_vec3,
}