import numpy as np


def Es(grid_x, grid_y):
    # Inputs :
    # grid_x : x-coordinates of meshgrid
    # grid_y : y-coordinates of meshgrid
    # grid_x and grid_y have same shape

    # returns : the derivative of Es towards V
    # dEs / dV

    # x : x-coordinates of meshgrid
    # y : y-coordinates of meshgrid
    # n : number of vertexes in meshgrid
    # N : number of quads
    x, y, n = list(grid_x[0, :]), list(grid_y[:, 0]), grid_x.size
    N = (grid_x.shape[0] - 1) * (grid_x.shape[1] - 1)
    derivation = np.zeros((2 * n, 2 * n))

    for i in range(len(y) - 1):
        for j in range(len(x) - 1):
            # quads whose top_left point is (x[j], y[i])
            # points order : top_left, bottom_left, top_right, bottom_right
            Aq = np.array([[x[j], -y[i], 1, 0],
                           [y[i], x[j], 0, 1],
                           [x[j], -y[i + 1], 1, 0],
                           [y[i + 1], x[j], 0, 1],
                           [x[j + 1], -y[i], 1, 0],
                           [y[i], x[j + 1], 0, 1],
                           [x[j + 1], -y[i + 1], 1, 0],
                           [y[i + 1], x[j + 1], 0, 1]
                           ])

            # decompose : Vq = Q * V
            # reason : Es is a quadratic function of V
            # for convenience of derivation, we can decompose Vq into product of Q and V
            # V = [x0, y0, x1, y1, x2, y2,...xn, yn]' : 2n x 1, in columns order
            # Vq points order : top_left, bottom_left, top_right, bottom_right
            # Vq = Q * V = [xq0, yq0, xq1, yq1,...xq3, yq3]
            Q = np.zeros((8, 2 * n))
            # top_left
            Q[0, 2 * (j * len(y) + i)] = 1
            Q[1, 2 * (j * len(y) + i) + 1] = 1

            # bottom_left
            Q[2, 2 * (j * len(y) + i) + 2] = 1
            Q[3, 2 * (j * len(y) + i) + 3] = 1

            # top_right
            Q[4, 2 * ((j + 1) * len(y) + i)] = 1
            Q[5, 2 * ((j + 1) * len(y) + i) + 1] = 1

            # bottom_right
            Q[6, 2 * ((j + 1) * len(y) + i) + 2] = 1
            Q[7, 2 * ((j + 1) * len(y) + i) + 3] = 1

            # n * Es =  ∑ l2_norm((Aq*(Aq'*Aq).I*Aq'-I)Q*V) = ∑ l2_norm(Sq * V)
            # Sq = (Aq*(Aq'*Aq).I*Aq'-I)Q
            # pseudo_inverse of Aq : np.linalg.pinv(Aq) = (Aq'*Aq).I*Aq'
            # d(nEs) / dV = ∑ 2 * Sq' * Sq
            Sq = (Aq @ np.linalg.pinv(Aq) - np.eye(8)) @ Q
            derivation += 2 * Sq.transpose() @ Sq
    return derivation / N


if __name__ == '__main__':
    from PIL import Image
    from mesh_segment import mesh
    img = Image.open('./image/image1.png').convert('RGB')
    img_array = np.array(img)
    x_len, y_len, x, y, grid_x, grid_y, nv, initial_mesh = mesh(img_array)
    dEs = Es(grid_x, grid_y)
    print(dEs.shape)