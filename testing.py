from generate_tree import generate_objects
from utils import uniform_array

params = dict()
params['generations'] = 6  #
params['scale_factor'] = 0.7
params['max_children'] = 8
params['dx_size'] = 1.3
params['scale_size'] = 0.2
params['col_delta_size'] = .22
params['rot_delta_size'] = 10

objects = generate_objects(params)
#
# [print(ob) for ob in objects]

# print(0.1 * uniform_array(10))