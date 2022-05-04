import numpy as np
import scipy.io


def load_mb(path, idx, ):
    if path.endswith('.txt'):
        data = np.loadtxt(path, delimiter=" ", dtype=int)  # 加载数据，分隔符为空格，数据类型为int
    elif path.endswith('.npy'):
        data = np.load(path)
    elif path.endswith('.mat'):
        data = scipy.io.loadmat(path)['datas']
    else:
        raise ValueError('Unknown file type')

    frame = data[data[:, -2] == idx]
    frame = frame[frame[:, -1] == 0]

    width_max = np.max(frame[:, 2] + frame[:, 4])
    height_max = np.max(frame[:, 3] + frame[:, 5])
    image = np.zeros((height_max, width_max), np.uint8)

    for line in frame:
        local_y = line[2] // 4
        local_x = line[3] // 4
        mb_height = line[4] // 4
        mb_width =line[5] // 4

        block = int(np.log2(mb_width * mb_height)) if mb_width * mb_height > 1 else 1
        image[local_x:local_x+mb_width, local_y:local_y+mb_height] = block
    
    return image


def load_mv(path, idx):
    if path.endswith('.txt'):
        data = np.loadtxt(path, delimiter=" ", dtype=int)  # 加载数据，分隔符为空格，数据类型为int
    elif path.endswith('.npy'):
        data = np.load(path)
    elif path.endswith('.mat'):
        data = scipy.io.loadmat(path)['datas']
    else:
        raise ValueError('Unknown file type')

    frame = data[data[:, -2] == idx]
    frame = frame[frame[:, -1] == 2]
    if len(frame) == 0:
        return np.zeros((180, 320, 2), float)

    width_max = np.max(frame[:, 2] + frame[:, 4]) // 4
    height_max = np.max(frame[:, 3] + frame[:, 5]) // 4
    image = np.zeros((height_max, width_max, 2), float)

    for line in frame:
        mv_y = line[0] // 4
        mv_x = line[1] // 4
        local_y = line[2] // 4
        local_x = line[3] // 4
        mb_height = line[4] // 4
        mb_width =line[5] // 4

        image[local_x:local_x+mb_width, local_y:local_y+mb_height, 0] = mv_x
        image[local_x:local_x+mb_width, local_y:local_y+mb_height, 1] = mv_y
    
    return image
