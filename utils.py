import numpy as np
from uncertainties import ufloat

COLORS = {
    'BaF2': '#1f77b4',
    'NaI': '#2ca02c',
}

energy_scaling = {'NaI': (ufloat(0.26016, 0.00005), ufloat(16.67, 0.15)),
                  'BaF2': (ufloat(0.24471, 0.00015), ufloat(-19.15, 0.34))}


def scale_energy(values, det, use_ufloat: bool = False):
    """scales the energy from channels to energy in keV"""
    energy = values * energy_scaling[det][0].n - energy_scaling[det][1].n
    if not use_ufloat:
        return energy
    return ufloat(energy, values * energy_scaling[det][0].s - energy_scaling[det][1].s)


def scale_time(values, use_ufloat: bool = False):
    """scales the time from channels to time in ps for the BaF2 detector"""
    time_scale = ufloat(6.07, 0.05)
    energy = values * time_scale.n
    if not use_ufloat:
        return energy
    return ufloat(energy, values * time_scale.s)


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
