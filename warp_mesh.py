import os
import numpy as np
import tensorflow as tf

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


def warp_mesh(initial_mesh, img_matrix, V_optimized, grid_x, grid_y):
    # V_optimized : shape : 2Nx1

    src = np.expand_dims(img_matrix, axis=0)
    initial_mesh_ = np.expand_dims(initial_mesh, axis=0)

    V = np.zeros((1, grid_x.size, 2))
    V[0, :, 0], V[0, :, 1] = grid_y.flatten('F'), grid_x.flatten('F')

    V_optimized_ = np.zeros((1, grid_x.size, 2))
    V_optimized_[0, :, 0] = V_optimized[list(range(1, 2 * grid_x.size, 2))]
    V_optimized_[0, :, 1] = V_optimized[list(range(0, 2 * grid_x.size, 2))]

    src = tf.cast(src / 255.0, tf.float32)
    initial_mesh_ = tf.cast(initial_mesh_ / 255.0, tf.float32)

    V = tf.cast(V, tf.float32)
    V_optimized_ = tf.cast(V_optimized_, tf.float32)

    after_rotation, _ = tf.contrib.image.sparse_image_warp(src, V_optimized_, V)
    mesh_rotation, _ = tf.contrib.image.sparse_image_warp(initial_mesh_, V_optimized_, V)

    after_rotation = tf.Session().run(tf.cast(after_rotation * 255, tf.uint8)[0])
    mesh_rotation = tf.Session().run(tf.cast(mesh_rotation * 255, tf.uint8)[0])

    return mesh_rotation, after_rotation
