import numpy as np


def load_data(path: str, only_roi: bool):
    """ Load the data from the .spe file.

    Parameters:
        path (string): Path to the .spe file.
        only_roi: Only load the ROI data.
    """
    data = []
    roi = None
    with open(path, 'r') as f:
        for _ in range(12):
            f.readline()
        while True:
            content = f.readline()
            if not content:
                break
            try:
                data.append(int(content))
            except ValueError:
                if content == '$ROI:\n':
                    f.readline()
                    vals = f.readline().removesuffix('\n')
                    roi = vals.split(' ')
                    roi = list(map(int, roi))
                else:
                    break
                continue
            if roi is not None and only_roi:
                return np.array(data[roi[0]:roi[1]]), np.arange(roi[0], roi[1])
    return np.array(data), np.arange(len(data))
