import numpy as np


def get_u(lines):
    # inputs : lines = [(x1, y1, x2, y2, orientation, bin_num),...]
    # returns : directional vector uk of all detected lines with shape Kx2
    # K : quantity of detected lines
    u = np.array([[lines[i][2] - lines[i][0], lines[i][3] - lines[i][1]] for i in range(len(lines))])
    l2_norm = np.expand_dims(np.linalg.norm(u, axis=-1), axis=-1)
    u = u / l2_norm
    return u


def get_pk(lines, x_len, y_len, grid_x, grid_y):
    # Bilinear Interpolation
    # consider a quad and a point in the quad:
    # four vertex points of this quad : (x1, y2), (x2, y2), (x1, y1), (x2, y1)
    # order of points above :  top_left, top_right, bottom_left, bottom_right
    # inner point of quad with coordinates : (x, y)
    # decompose : (x, y) = a(x1, y2) + b(x2, y2) + c(x1, y1) + d(x2, y1)
    # using bilinear interpolation, we can get :
    # dx = x2 - x1, dy = y1 - y2
    # a = ((x2 - x) * (y1 - y)) / (dx * dy)
    # b = ((x - x1) * (y1 - y)) / (dx * dy)
    # c = ((x2 - x) * (y - y2)) / (dx * dy)
    # d = ((x - x1) * (y - y2)) / (dx * dy)

    def abcd(x, y, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y1 - y2
        a = ((x2 - x) * (y1 - y)) / (dx * dy)
        b = ((x - x1) * (y1 - y)) / (dx * dy)
        c = ((x2 - x) * (y - y2)) / (dx * dy)
        d = ((x - x1) * (y - y2)) / (dx * dy)
        return a, b, c, d

    # ek = Pk * V
    # in this function, for convenience, we set:
    # K : quantity of detected lines, K = len(lines)
    # N : quantity of meshgrid vertexes, N = grid_x.size
    # ek : shape : 2Kx1
    # Pk : shape : 2Kx2N
    # V : shape :  2Nx1

    Pk = np.zeros((2 * len(lines), 2 * grid_x.size))
    x_index = np.array(list(range(0, 2 * grid_x.size, 2)))
    y_index = x_index + 1
    for i in range(len(lines)):
        p1 = (lines[i][0], lines[i][1])
        p2 = (lines[i][2], lines[i][3])

        x1_index = int(np.floor(min(p1[0], p2[0]) / x_len)) + 1
        x2_index = x1_index + 1

        y2_index = int(np.floor(min(p1[1], p2[1]) / y_len)) + 1
        y1_index = y2_index + 1

        x1 = grid_x[0, x1_index - 1]
        x2 = grid_x[0, x2_index - 1]
        y1 = grid_y[y1_index - 1, 0]
        y2 = grid_y[y2_index - 1, 0]

        # p1 = Pk1 * V, p2 = Pk2 * V, thus, (p2 - p1) = (Pk2 - Pk1) * V
        Pk_i = np.zeros(grid_x.shape)
        a1, b1, c1, d1 = abcd(p1[0], p1[1], x1, y1, x2, y2)
        a2, b2, c2, d2 = abcd(p2[0], p2[1], x1, y1, x2, y2)
        Pk_i[y2_index - 1, x1_index - 1] = a2 - a1
        Pk_i[y2_index - 1, x2_index - 1] = b2 - b1
        Pk_i[y1_index - 1, x1_index - 1] = c2 - c1
        Pk_i[y1_index - 1, x2_index - 1] = d2 - d1

        Pk[2 * i, x_index] = Pk_i.flatten('F')
        Pk[2 * i + 1, y_index] = Pk_i.flatten('F')

    return Pk


def El(lines, U, Pk, nv, thetas):
    # K : len(lines), quantity of detected lines
    # K * El = ∑ l2_norm(sk*Rk*uk-ek) = ∑ l2_norm((Rk*Uk*Rk'-I)*ek)

    # decompose : ek = Pk * V
    # V = [x0, y0, x1, y1, x2, y2,...xn, yn]' with shape 2n x 1
    # n : number of meshgrid points

    # then we have :
    # K * El =  ∑ l2_norm((Rk*Uk*Rk'-I)*ek) = ∑ l2_norm((Rk*Uk*Rk'-I)*Pk*V) = ∑ l2_norm(Lk * V)
    # derivation :
    # d(K*El) / dV = ∑ 2 * ((Rk*Uk*Rk'-I)*Pk)' * ((Rk*Uk*Rk'-I)*Pk) = ∑ 2 * Lk' * Lk
    # for k-th lines :
    # Rk is 2x2, Uk is 2x2, Pk[2k&->2k + 1, :] is 2x2N
    # then, Lk = 2x2N, Lk' * Lk = 2Nx2N

    # remind :
    # Rk = [[cos(θmk), -sin(θmk)], [sin(θmk), cos(θmk)]] with shape 2x2
    # uk = [xk_, yk_]' denotes the k-th directional vector of detected lines with shape 2x1
    # ek = [xk, yk]' denotes the k-th detected lines with shape 2x1 after rotation
    # Uk = uk*(uk'*uk).I*uk' with shape 2x2

    # U : shape Kx2, each row represents a directional vector of line
    # thetas : vector or list with shape Mx1 or with length M
    # Pk : shape : 2Kx2N
    derivation = np.zeros((2 * nv, 2 * nv))

    # total_Uk is used for storing all array Uk with shape 2x2
    total_Uk = np.zeros((len(lines), 2, 2))

    for k in range(len(lines)):
        # lines[i] = [x0, y0, x1, y1, orientation, bin_num]
        # bin_num : from 1 to M, thus, minus 1 as an index
        # convert theta to rad
        theta = thetas[lines[k][-1] - 1, ] / 180.0 * np.pi

        # rotation matrix Rk with shape 2x2
        Rk = np.array([[np.cos(theta), -np.sin(theta)],
                       [np.sin(theta), np.cos(theta)]])

        # uk is directional vector of the k-th detected lines with shape 2x1
        uk = np.expand_dims(U[k, :].transpose(), axis=-1)

        # (uk.transpose() @ uk).I @ uk.transpose() = np.linalg.pinv(uk)
        Uk = uk @ np.linalg.pinv(uk)
        total_Uk[k] = Uk

        # calculating derivation
        Lk = (Rk @ Uk @ Rk.transpose() - np.eye(2)) @ Pk[2 * k: 2 * k + 2, :]
        derivation += 2 * Lk.transpose() @ Lk
    return derivation / len(lines), total_Uk