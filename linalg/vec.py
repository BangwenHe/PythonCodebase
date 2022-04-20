import numpy as np

def calculate_vector_angle(vec1, vec2):
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)

        uvec1 = vec1.T / np.linalg.norm(vec1, axis=-1)
        uvec2 = vec2.T / np.linalg.norm(vec2, axis=-1)
        dot_product = np.dot(uvec1.T, uvec2.T)
        angle = np.arccos(dot_product)

        return angle * 180 / np.pi
