import numpy as np


def normalize_vectors(vectors):
    # Calculate the length of each vector
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)

    # Normalize each vector by dividing it by its length
    normalized_vectors = vectors / norms

    return normalized_vectors


def dict_to_obj_list(obj_dict):
    # collapses dict of lists into a single list
    obj_list = []
    for key in obj_dict:
        obj_list.extend(obj_dict[key])
    return obj_list


def points_on_sphere(n):
    return normalize_vectors(np.random.rand(n, 3) - 0.5)


def point_on_sphere_array(n):
    return np.repeat(points_on_sphere(1), n, axis=0)  # array of repeated single vector lying on surface of unit sphere


def constant_array(arr, n):
    return np.repeat(arr, n, axis=0)


def get_random_base_color():
    base_color = np.random.rand(3)
    base_color += 0.05
    base_color = np.clip(base_color, 0.1, 0.9)
    return base_color
