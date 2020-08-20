import numpy as np


def fix_theta_solve_for_v(dEl, lambda_l, G, b, lambda_b, dEs, lambda_s):
    # El, Es and Eb are functions of V
    # inputs :
    # dEb : 2G'(Gv-b) = 2G'G - 2G'b --- boundary preservation
    # dEl : derivation of El towards V --- line preservation
    # dEs : derivation of Es towards V --- shape preservation
    # lambda_l : weight of line preservation
    # lambda_b : weight of boundary preservation
    # lambda_s : weight of shape preservation

    # returns : V

    # equation :
    # lambda_b * dEb + lambda_l * dEl + lambda_s * dEs = 0
    # => (2lambda_b * G'G + lambda_l * dEl + lambda_s * dEs) * V = 2lambda_b * G'b
    # => A * V = B

    A = 2 * lambda_b * G.transpose() @ G + lambda_l * dEl + lambda_s * dEs
    B = 2 * lambda_b * G.transpose() @ b
    V = np.linalg.solve(A, B)
    return V


def fix_v_solve_for_theta(lines, angle, w_thetas, thetas, lambda_r, lambda_l, Pk, V, total_Uk):
    # Er and El are functions of theta
    # V : shape : 2Nx1
    # thetas : [theta_1, theta_2,..., theta_M]' shape : Mx1
    # w_thetas : w_thetas[k] is the weight of thetas[k]
    # Pk : shape : 2Kx2N
    # lines : [[x0, y0, x1, y1, orientation, bin_num],...]
    # total_Uk : shape : Kx2x2, Uk is in shape 2x2, total K lines
    # lambda_r : weight of rotation manipulation
    # lambda_l : weight of line preservation

    # warm up : beta : from 1 to 1e5

    # bin_index of k-th detected line
    A = np.zeros((len(lines), len(thetas)))
    x_index, y_index = np.array(list(range(len(lines)))), np.array([line[-1] - 1 for line in lines])
    A[x_index, y_index] = 1

    # ek : vector after rotation
    # e = [x0, y0, x1, y1,...xK, yK]' with shape 2Kx1
    # e_angle : the orientation of vector ek, list with length K
    e = Pk @ V
    e_angle = [np.arccos(e[2 * i] / (1e-10 + np.linalg.norm(e[2 * i: 2 * i + 2]))) for i in range(len(lines))]

    beta = 1
    phi_all_lines = np.zeros((len(lines),))
    while beta <= 1e4:
        # Step 1 : fix theta, update phi
        for k in range(len(lines)):
            angle_uk_ek = e_angle[k] * 180.0 / np.pi - lines[k][-2]
            theta_mk = thetas[lines[k][-1] - 1, ]

            # print(angle_uk_ek, theta_mk)

            # split angle between [ek_uk, theta_mk] or [theta_mk, ek_uk] into 100 pieces equally
            phi_candidates = np.linspace(angle_uk_ek, theta_mk, num=10)

            value_smallest = float('inf')
            for phi in phi_candidates:
                phi_ = phi / 180.0 * np.pi
                Rk = np.array([[np.cos(phi_), -np.sin(phi_)],
                               [np.sin(phi_), np.cos(phi_)]])
                value = np.sum(np.square((Rk @ total_Uk[k] @ Rk.transpose() - np.eye(2)) @ e[2 * k: 2 * k + 2]))
                value = lambda_l / len(lines) * value + beta * (phi - theta_mk) ** 2
                if value < value_smallest:
                    value_smallest = value
                    phi_all_lines[k] = phi

        # Step 2 : fix phi, update theta
        # Part 1 : Rotation Manipulation
        # w_thetas : shape : Mx1
        # thetas : shape : Mx1, thetas[m] is the angle of m-th bin
        # angle : angle * np.ones((M, 1)) : shape : Mx1
        # decompose : theta_m+1 = P * thetas
        # P : shape : MxM, variation of identity matrix
        # D : I - P
        # Er_theta = (thetas - angle) @ (thetas - angle)' @ w_thetas + l2_norm(thetas - P @ thetas)
        # notice that (thetas - P @ thetas) = (I - P) @ thetas, replace (I - P) with D, we get :
        # Er_theta = (thetas - angle) @ (thetas - angle)' @ w_thetas + l2_norm(D @ thetas)
        # dEr / d thetas = 2 * np.diag(w_thetas) @ (thetas - angle) + 2 * D' @ D @ thetas

        # Part 2 : Auxiliary Part
        # A : shape : KxM
        # phi : shape : Kx1, (in this function named phi_all_lines)
        # theta_mk = A @ thetas, shape : Kx1, theta_mk[k] is the bin angle of k-th line
        # penalty part = bate * ∑ (phi_all_lines[k] - theta_mk[k]) ** 2 = beta * l2_norm(phi_all_lines - A @ thetas)
        # d penalty / d thetas = 2 * beta * A' @ (A @ thetas - phi_all_lines)

        # equation :
        # lambda_r * d Er + d penalty = 0
        # F @ thetas = f
        D = np.eye(len(thetas)) - np.eye(len(thetas))[np.array(list(range(1 - len(thetas), 1, 1))), :]
        F = lambda_r * (np.diag(w_thetas) + D.transpose() @ D) + beta * A.transpose() @ A
        f = lambda_r * np.diag(w_thetas) @ (np.ones((len(thetas),)) * angle) + beta * A.transpose() @ np.array(phi_all_lines)
        thetas = np.linalg.solve(F, f)

        beta *= 10

    return thetas





















