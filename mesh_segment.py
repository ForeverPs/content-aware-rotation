import numpy as np
from PIL import Image


def mesh(img_matrix):
    # shape of quads : 2500 = 50(horizontal) x 50(vertical)
    # cx : number of quads horizontally
    # cy : number of quads vertically
    # cx + 1 : number of mesh lines horizontally
    # cy + 1 : number of mesh line vertically
    # nv : number of vertices nv = (cx + 1) * (cy + 1)
    # x_len : distance along x-axis
    # y_len : distance along y-axis
    # vx : x-coordinates of mesh lines
    # xy : y-coordinates of mesh lines
    (y, x, channel) = img_matrix.shape
    cx = int(x / 50)
    cy = int(y / 50)

    n_quads = cx * cy
    nv = (cx + 1) * (cy + 1)
    x_len = (x - 1) / cx
    y_len = (y - 1) / cy

    vx = [round(i * x_len) for i in range(cx + 1) if round(i * x_len) <= x - 1]
    vy = [round(i * y_len) for i in range(cy + 1) if round(i * y_len) <= y - 1]

    img_matrix[vy, :, :] = np.array((248, 255, 9))
    img_matrix[:, vx, :] = np.array((248, 255, 9))

    grid_x, grid_y = np.meshgrid(vx, vy)

    img_matrix[grid_y, grid_x, :] = np.array((255, 0, 0))

    return x_len, y_len, x, y, grid_x, grid_y, nv, img_matrix


if __name__ == '__main__':
    img = Image.open('./image/image1.png').convert('RGB')
    img_array = np.array(img)
    x_len, y_len, x, y, grid_x, grid_y, nv, initial_mesh = mesh(img_array)
    print(grid_x, grid_x.shape)
    print(grid_y, grid_y.shape)
