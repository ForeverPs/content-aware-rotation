import numpy as np


def Eb(grid_x, grid_y, x, y):
    # Eb = l2_norm(Gv - b)
    # n : number of vertices, n = grid_x.size = grid_y.size
    # dEb / dV = 2G'(Gv-b) = 2G'Gv - 2G'b

    # v : vertex coordinates of quads in meshgrid
    #     style : [x0, y0, x1, y1, x2, y2, ...], in columns order
    #     shape : 2n x 1

    # G : parameters matrix, value in {0, 1}
    #     shape : 2n x 2n

    # example 1 :
    # if (x0, y0) only locates on the right boundary of image, then we desire x0 to still be w after rotation
    # then we have G = [[1, 0], [0, 0]], b = [w, 0]', v = [x0, y0]'
    # Gv - b = [[1, 0], [0, 0]] * [x0, y0]' - [w, 0]' = [x0 - w, 0]
    # l2_norm(Gv - b) = (x0 - w) ** 2

    # example 2 :
    # if (x0, y0) is the bottom_right point of image, then we desire (x0, y0) still to be (w, h) after rotation
    # then we have G = [[1, 0], [0, 1]], b = [w, h]', v = [x0, y0]'
    # Gv - b = [[1, 0], [0, 1]] * [x0, y0]' - [w, h]' = [x0 - w, y0 - h]
    # l2_norm(Gv - b) = (x0 - w) ** 2 + (y0 - h) ** 2

    # grid_x : x-ccordinates of meshgrid
    # grid_y : y-coordinates of meshgrid
    # y : img.shape[0], number of rows
    # x : img.shape[1], number of columns

    # Initialize variables
    n = grid_x.size
    b_x, b_y, b = np.zeros((n,)), np.zeros((n,)), np.zeros((2 * n,))
    x_coordinates, y_coordinates, c = grid_x.flatten('F'), grid_y.flatten('F'), np.zeros((2 * n,))

    # b :
    b_x[x_coordinates == x - 1] = x - 1
    b_y[y_coordinates == y - 1] = y - 1
    b[0::2], b[1::2] = b_x, b_y

    # G :
    x_coordinates[x_coordinates == 0] = 1
    x_coordinates[x_coordinates == x - 1] = 1
    x_coordinates[x_coordinates != 1] = 0

    y_coordinates[y_coordinates == 0] = 1
    y_coordinates[y_coordinates == y - 1] = 1
    y_coordinates[y_coordinates != 1] = 0

    c[0::2], c[1::2] = x_coordinates, y_coordinates
    G = np.diag(c)

    return G, b


if __name__ == '__main__':
    from PIL import Image
    from mesh_segment import mesh
    img = Image.open('./image/image1.png').convert('RGB')
    img_array = np.array(img)
    x_len, y_len, x, y, grid_x, grid_y, nv, initial_mesh = mesh(img_array)
    g, b = Eb(grid_x, grid_y, x, y)
    print(g, b)