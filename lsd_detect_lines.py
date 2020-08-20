import cv2
import numpy as np
from lsd.pylsd.lsd import lsd


def detect_lines(img_array, angle, x_len, y_len, x, y, minLen=2, M=90):
    src = img_array.copy()
    gray = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
    lines = lsd(gray)
    legal_lines = list()
    for i in range(lines.shape[0]):
        pt1 = [int(lines[i, 0]), int(lines[i, 1])]
        pt2 = [int(lines[i, 2]), int(lines[i, 3])]
        vec = [pt1[0] - pt2[0], pt1[1] - pt2[1]]
        if np.linalg.norm(np.array(vec)) >= minLen:
            temp_lines = [pt1, pt2]

            # used for calculating the intersection of line and mesh_grids
            left_x, right_x = min(pt1[0], pt2[0]), max(pt1[0], pt2[0])
            top_y, bottom_y = min(pt1[1], pt2[1]), max(pt1[1], pt2[1])

            # x_mesh_left >= left_x, x_mesh_right <= right_x
            x_mesh_left = np.ceil(left_x / x_len) * x_len
            x_mesh_right = np.floor(right_x / x_len) * x_len

            # y_mesh_bottom >= bottom_y, y_mesh_top <= top_y
            y_mesh_top = np.ceil(top_y / y_len) * y_len
            y_mesh_bottom = np.floor(bottom_y / y_len) * y_len

            # record the intersection coordinate of line and x-axis-mesh-grid
            while x_mesh_left <= x_mesh_right:
                mesh_start, mesh_end = [x_mesh_left, 0], [x_mesh_left, y]
                flag, p = intersect(pt1, pt2, mesh_start, mesh_end)
                if flag:
                    temp_lines.append(p)
                x_mesh_left += x_len

            # record the intersection coordinate of line and y-axis-mesh-grid
            while y_mesh_top <= y_mesh_bottom:
                mesh_start, mesh_end = [0, y_mesh_top], [x, y_mesh_top]
                flag, p = intersect(pt1, pt2, mesh_start, mesh_end)
                if flag:
                    temp_lines.append(p)
                y_mesh_top += y_len

            # sort temp_lines in y_coordinate to get sub_lines
            temp_lines.sort(key=lambda coordinates: coordinates[1])

            for j in range(len(temp_lines) - 1):
                l_start, l_end = temp_lines[j], temp_lines[j + 1]
                l_vec = [l_start[0] - l_end[0], l_start[1] - l_end[1]]
                if np.linalg.norm(np.array(l_vec)) > minLen:
                    # calculate  the orientation between line and x-axis, [0, 180)
                    theta = np.arctan(l_vec[1] / (l_vec[0] + 1e-10)) / np.pi * 180.0
                    theta = theta if theta >= 0 else theta + 180.0
                    bin_num = int(np.ceil(theta + angle) / 180.0 * M)

                    # bin_num = [1, 90]
                    if bin_num <= 0:
                        bin_num += 90
                    elif bin_num > 90:
                        bin_num -= 90
                    legal_lines.append([l_start[0], l_start[1], l_end[0], l_end[1], theta, bin_num])
    return legal_lines


def intersect(pt1, pt2, pt3, pt4):
    # return the intersection of pt1 - pt2 and pt3 - pt4
    p_x_num = (pt1[0] * pt2[1]) * (pt3[0] - pt4[0]) - (pt1[0] - pt2[0]) * (pt3[0] * pt4[1] - pt3[1] * pt4[0])
    p_y_num = (pt1[0] * pt2[1]) * (pt3[1] - pt4[1]) - (pt1[1] - pt2[1]) * (pt3[0] * pt4[1] - pt3[1] * pt4[0])
    p_den = (pt1[0] - pt2[0]) * (pt3[1] - pt4[1]) - (pt1[1] - pt2[1]) * (pt3[0] - pt4[0])
    p = [p_x_num / (p_den + 1e-10), p_y_num / (p_den + 1e-10)]

    if min(pt1[0], pt2[0]) <= p[0] <= max(pt1[0], pt2[0]) and min(pt1[1], pt2[1]) <= p[1] <= max(pt1[1], pt2[1]):
        return True, p
    return False, None
