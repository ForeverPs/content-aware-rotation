import numpy as np
from PIL import Image
from mesh_segment import mesh
import matplotlib.pyplot as plt
from warp_mesh import warp_mesh
from line_preservation import El
from shape_preservation import Es
from boundary_preservation import Eb
from line_preservation import get_pk, get_u
from lsd_detect_lines import detect_lines
from optimization import fix_theta_solve_for_v, fix_v_solve_for_theta


def image_rotation(img_path, angle, M=90, lambda_r=1e2, lambda_b=1e8, lambda_l=1e2, lambda_s=1):
    # inputs :
    # img_path : the path of image need to rotation
    # angle : rotation angle with between desired orientation and x-axis
    # M : number of bins

    # load img in RGB style and then convert it to numpy array
    img = Image.open(img_path).convert('RGB')
    img_array = np.array(img)

    # initialize meshgrid
    # x_len / y_len : distance between quads along x-axis / y-axis
    # x / y : column and row of input image
    # grid_x / grid_y : x-coordinate / y-coordinate of quads
    # nv : quantity of quads points, nv = grid_x.size = grid_y.size
    # img_matrix : image in numpy array
    x_len, y_len, x, y, grid_x, grid_y, nv, initial_mesh = mesh(img_array.copy())

    # Initialize thetas
    thetas = np.ones((M,)) * angle

    # initialize w_thetas, weights of thetas
    w_thetas = np.zeros((M,))
    index = [0, M - 1, M // 2 - 1, M // 2]
    w_thetas[index] = 1e3

    # using lsd method to detect lines
    lines = detect_lines(img_array, angle, x_len, y_len, x, y, M=M)

    # derivation of shape preservation
    dEs = Es(grid_x, grid_y)

    # boundary preservation
    G, b = Eb(grid_x, grid_y, x, y)

    # calculating Pk and U
    Pk = get_pk(lines, x_len, y_len, grid_x, grid_y)

    # calculating all Uk, denotes as U
    U = get_u(lines)

    for epoch in range(10):
        print('\nEpoch : %d' % epoch)
        dEl, total_Uk = El(lines, U, Pk, nv, thetas)

        print(' ' * 6 + 'Optimization : fix theta, solve for V')
        V = fix_theta_solve_for_v(dEl, lambda_l, G, b, lambda_b, dEs, lambda_s)

        print(' ' * 6 + 'Optimization : fix V, solve for theta')
        thetas = fix_v_solve_for_theta(lines, angle, w_thetas, thetas, lambda_r, lambda_l, Pk, V, total_Uk)

    mesh_result, img_result = warp_mesh(initial_mesh, img_array, V, grid_x, grid_y)

    plt.subplot(2, 2, 1)
    plt.imshow(img_array)
    plt.xlabel('x-axis')
    plt.ylabel('y-axis')
    plt.title('Original Image')

    plt.subplot(2, 2, 2)
    plt.imshow(img_result)
    plt.xlabel('x-axis')
    plt.ylabel('y-axis')
    plt.title('Content Aware Rotation')

    plt.subplot(2, 2, 3)
    plt.imshow(initial_mesh)
    plt.xlabel('x-axis')
    plt.ylabel('y-axis')
    plt.title('Initial Mesh')

    plt.subplot(2, 2, 4)
    plt.imshow(mesh_result)
    plt.xlabel('x-axis')
    plt.ylabel('y-axis')
    plt.title('Warp Mesh')

    plt.show()


if __name__ == '__main__':
    img_path = './image/image2.png'
    angle = -5.8
    image_rotation(img_path, angle)
