import numpy as np
from dataclasses import dataclass
import copy
import json
from utils import dict_to_obj_list, points_on_sphere, constant_array


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


def scale(g, scale_factor=0.5):
    return scale_factor ** g


def dX_scale(g, scale_factor=0.5):
    return 200 * scale_factor ** g


def f_generator(dX, shrink_factor, col_delta, rot_delta):
    # takes a row of the parameter arrays and returns a function parametrized by it
    def f(obj):
        child = copy.deepcopy(obj)
        # position
        child.px += dX[0]
        child.py += dX[1]
        child.pz += dX[2]
        # scale
        child.sx *= shrink_factor[0]
        child.sy *= shrink_factor[1]
        child.sz *= shrink_factor[2]
        # color
        child.R += col_delta[0]  # not sure yet what the value ranges are for color and if C4D clips automatically
        child.G += col_delta[1]
        child.B += col_delta[2]
        # rotation
        child.rx += rot_delta[0]
        child.ry += rot_delta[1]
        child.rz += rot_delta[2]

        return child

    return f


def generate_func_parameters(params, g):
    # these parameter arrays are seen as perturbations to the existing values in the object
    n_functions = np.random.randint(params['min_children'], params['max_children'])

    dx = params['dx_size'] * dX_scale(g, params['scale_factor']) * points_on_sphere(n_functions)  # change in 3D position of obj

    shrink_factor = constant_array(np.ones(shape=(1, 3)) * params['scale_factor'],
                                   n_functions)
    # allow ellipsoidal objects
    if params['stretch']:
        stretch_factor = constant_array(np.ones(shape=(1, 3)), n_functions) + 2 * (
                    np.random.rand(n_functions, 3) - 0.5) * params['stretch_size']
        shrink_factor *= stretch_factor

    # decaying mutation size over g
    col_delta = scale(g, params['col_scale_factor']) * params['col_delta_size'] * points_on_sphere(
        n_functions)  # units: (0-255) individual level variation
    rot_delta = scale(g, params['scale_factor']) * params['rot_delta_size'] * points_on_sphere(
        n_functions)  # what units??

    # child based mutation (each child is unique)
    # scale_purt = params['scale_purt_size'] * points_on_sphere(n_functions)  # could also not normalize to 1 to allow low values. could also make them all equal rand(n,1)*np.ones(n, 3)
    # col_delta = params['col_delta_size'] * points_on_sphere(n_functions)  # units: (0-255) individual level variation
    # rot_delta = params['rot_delta_size'] * points_on_sphere(n_functions)  # what units??

    # parent based mutation (all children are equal)
    # scale_purt = params['scale_purt_size'] * uniform_random_array(n_functions)  # could also not normalize to 1 to allow low values. could also make them all equal rand(n,1)*np.ones(n, 3)
    # col_delta = params['col_delta_size'] * uniform_random_array(n_functions)  # uniform functions implies mutation at the object level (ie all children have same color) vs indiv level (each child a different color)
    # rot_delta = params['rot_delta_size'] * uniform_random_array(n_functions)  # what units??

    return dx, shrink_factor, col_delta, rot_delta


def generate_func_list(params, g):
    dx, shrink_factor, col_delta, rot_delta = generate_func_parameters(params, g)
    func_list = []

    for j, row in enumerate(dx):
        func_list.append(f_generator(dx[j], shrink_factor[j], col_delta[j], rot_delta[j]))

    return func_list

    # def switch_object_type(self, obj, g):  # it should switch to any specified object type
    #     if obj.obj_type == 'cube':
    #         new_obj = Sphere(px=obj.px, py=obj.py, pz=obj.pz, rx=obj.rx, ry=obj.rx, rz=obj.rx, sx=obj.px, sy=obj.px, sz=obj.px, R=obj.px, G=obj.px, B=obj.px, obj_type='sphere', segments=16, radius=100)
    #     elif obj.obj_type == 'sphere':
    #         new_obj = Cube()
    #     return new_obj


def initialize_objects(params):
    # insert root object into the dict
    seed_obj = Sphere()
    base_color = params['base_color']
    # color
    seed_obj.R = base_color[0]
    seed_obj.G = base_color[1]
    seed_obj.B = base_color[2]

    # seed_obj = Cube()
    objects = {}

    for g in range(params['generations']):
        key_name = f"gen{g}"
        objects[key_name] = []

    objects['gen0'] = [seed_obj]
    return objects


def generate_objects(params):
    objects_dict = initialize_objects(params)

    for g, gen in enumerate(list(objects_dict.keys())[:-1]):
        next_gen = list(objects_dict.keys())[g + 1]
        print('generation:', gen)
        new_objects = []
        # apply functions to every object in previous gen and store in a new list for this gen
        for obj in objects_dict[gen]:
            # for each obj generate a list of functions to apply.
            f_list = generate_func_list(params, g)
            for f in f_list:
                new_objects.append(f(obj))

        print(f"{len(new_objects)} objects in {next_gen}")
        objects_dict[next_gen] = new_objects

    objects_list = dict_to_obj_list(objects_dict)
    return objects_list


def save_objects(objects, save_path):
    with open(f'{save_path}objects.json', 'w') as f:
        json.dump(objects, f, default=lambda x: x.__dict__)
