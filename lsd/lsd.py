from .bindings.lsd_ctypes import *


def lsd(src):
    rows, cols = src.shape
    src = src.reshape(1, rows * cols).tolist()[0]

    temp = os.path.abspath(os.getcwd()[0]).replace('\\', '/')

    lens = len(src)
    src = (ctypes.c_double * lens)(*src)
    lsdlib.lsdGet(src, ctypes.c_int(rows), ctypes.c_int(cols), temp)

    fp = open(temp, 'r')
    cnt = fp.read().strip().split(' ')
    fp.close()
    os.remove(temp)

    count = int(cnt[0])
    dim = int(cnt[1])
    lines = np.array([float(each) for each in cnt[2:]])
    lines = lines.reshape(count, dim)

    return lines
