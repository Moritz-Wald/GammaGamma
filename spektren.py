import itertools as it

from matplotlib import pyplot as plt

from utils import COLORS, load_data, scale_energy

detectors = ['NaI', 'BaF2']
compounds = ['Na22', 'Co60']


fig, axes = plt.subplots(2, 2, figsize=(10, 7), sharex='all', sharey='row')
for ax, col in zip(axes[0], detectors):
    ax.set_title(col)
for ax, row in zip(axes[:, 0], compounds):
    ax.annotate(row, xy=(0, 0.5), xytext=(-ax.yaxis.labelpad - 1, 0),
                xycoords=ax.yaxis.label, textcoords='offset points',
                size='large', ha='right', va='center')
axes = axes.flatten('F')
fig.suptitle(r'Spectra of $\gamma$-radiation from $^{22}Na$ and $^{60}Co$ on NaI and $BaF_2$ detectors',
             fontsize='xx-large')
data = []
for i, (detector, compound) in enumerate(it.product(detectors, compounds)):
    cnts, roi = load_data(f'data/Energiespektrum-{compound}-{detector}.Spe', only_roi=False)
    data.append((scale_energy(roi, detector), cnts))
    axes[i].scatter(data[i][0], data[i][1],
                    c=COLORS[detector],
                    s=0.15,
                    label=f'${compound}$ on ${detector}$-detector')
    axes[i].legend(loc='upper right', fontsize='large')
    axes[i].grid(alpha=0.3)
    axes[i].labelsize = 'x-large'
    if i in [1, 3]:
        axes[i].set_xlabel('Energy (keV)')
    if i in [0, 1]:
        axes[i].set_ylabel('Counts')
plt.tight_layout()
plt.savefig('figures/spektren.png', format='png', dpi=500, transparent=True)
plt.show()
