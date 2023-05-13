import numpy as np
from dataclasses import dataclass
import copy
import json
from config import save_path

@dataclass
class BaseObject:
    px: float = 0
    py: float = 0
    pz: float = 0
    rx: float = 0
    ry: float = 0
    rz: float = 0
    sx: float = 1
    sy: float = 1
    sz: float = 1
    R: float = 0.5
    G: float = 0.5
    B: float = 0.5


@dataclass
class Sphere(BaseObject):
    obj_type: int = 'sphere'
    segments: int = 16
    radius: float = 100


@dataclass
class Cube(BaseObject):
    obj_type: int = 'cube'
    length: float = 200


@dataclass
class Pyramid(BaseObject):
    obj_type: int = 'pyramid'


class Functions:

    def __init__(self):
        self.obj_types = ['sphere', 'cube', 'pyramid']
        self.beta = np.log(
            0.5)  # downscale exponent (must be negative). Eg. when beta = ln(0.5) the scale factor is =0.5
        self.scale_factor = np.exp(
            self.beta)  # (in (0,1)) equals the ratio between the scales of two consecutive generations, using math.

    def translation(self, g):
        return 300 * np.exp(self.beta * g)

    def f0(self, obj, g):
        child = copy.deepcopy(obj)
        child.px += self.translation(g)
        child.py += self.translation(g)
        child.pz += 0
        child.sx *= self.scale_factor
        child.sy *= self.scale_factor
        child.sz *= self.scale_factor
        return child

    def f1(self, obj, g):
        child = copy.deepcopy(obj)
        child.px += 0
        child.py += self.translation(g)
        child.pz += 0
        child.sx *= self.scale_factor
        child.sy *= self.scale_factor
        child.sz *= self.scale_factor
        return child

    def f2(self, obj, g):
        child = copy.deepcopy(obj)
        child.px += 0
        child.py += 0
        child.pz += self.translation(g)
        child.sx *= self.scale_factor
        child.sy *= self.scale_factor
        child.sz *= self.scale_factor
        return child

    def f3(self, obj, g):
        child = copy.deepcopy(obj)
        child.px -= self.translation(g)
        child.py += 0
        child.pz += 0
        child.sx *= self.scale_factor
        child.sy *= self.scale_factor
        child.sz *= self.scale_factor
        return child

    def f4(self, obj, g):
        child = copy.deepcopy(obj)
        child.px += 0
        child.py -= self.translation(g)
        child.pz += 0
        child.sx *= self.scale_factor
        child.sy *= self.scale_factor
        child.sz *= self.scale_factor
        return child

    def f5(self, obj, g):
        child = copy.deepcopy(obj)
        # child = self.switch_object_type(child, g)
        child.px += 0
        child.py += 0
        child.pz -= self.translation(g)
        child.sx *= self.scale_factor
        child.sy *= self.scale_factor
        child.sz *= self.scale_factor
        return child

    # def switch_object_type(self, obj, g):  # it should switch to any specified object type
    #     if obj.obj_type == 'cube':
    #         new_obj = Sphere(px=obj.px, py=obj.py, pz=obj.pz, rx=obj.rx, ry=obj.rx, rz=obj.rx, sx=obj.px, sy=obj.px, sz=obj.px, R=obj.px, G=obj.px, B=obj.px, obj_type='sphere', segments=16, radius=100)
    #     elif obj.obj_type == 'sphere':
    #         new_obj = Cube()
    #     return new_obj


def initialize_objects(generations=4):
    seed_obj = Sphere()
    objects = {}

    for g in range(generations):
        key_name = f"gen{g}"
        objects[key_name] = []

    objects['gen0'] = [seed_obj]
    return objects

def dict_to_obj_list(obj_dict):
    # collapses dict of lists into a single list
    obj_list = []
    for key in obj_dict:
        obj_list.extend(obj_dict[key])
    return obj_list


def generate_objects(generations=4, f_list=None):
    objects_dict = initialize_objects(generations)
    for g, gen in enumerate(list(objects_dict.keys())[:-1]):
        next_gen = list(objects_dict.keys())[g + 1]
        print('generation:', gen)
        new_objects = []
        # apply functions to every object in previous gen and store in a new list for this gen
        for obj in objects_dict[gen]:
            for f in f_list:  # add stochastic effect here only. turn off at random
                new_objects.append(f(obj, g + 1))

        print(f"{len(new_objects)} objects in {next_gen}")
        objects_dict[next_gen] = new_objects

    objects_list = dict_to_obj_list(objects_dict)
    return objects_list


def save_objects(objects, save_path):
    with open(f'{save_path}objects.json', 'w') as f:
        json.dump(objects, f, default=lambda x: x.__dict__)