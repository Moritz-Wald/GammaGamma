import numpy as np
from scipy.stats import alpha
import matplotlib.pyplot as plt
a = 5
mean, var, skew, kurt = alpha.stats(a, moments='mvsk')
x = np.linspace(alpha.ppf(0.004, a),
                alpha.ppf(0.99, a), 1000)
fig, axes = plt.subplots(4, 1, figsize=(7, 8), sharex='all', sharey='all')
(ax1, ax2, ax3, ax4) = axes
signal = alpha.pdf(x, a)
signal /= max(signal)
ax1.plot(x, signal,
       'r-', lw=3, alpha=0.6, label='Original signal')
signal_a = -signal*0.4
signal_b = alpha.pdf(x-0.1, a)
signal_b /= max(signal_b)
ax2.plot(x, signal_a,
       'r-', lw=3, alpha=0.6, label='shifted and inverted signal')
ax3.plot(x, signal_b,
       'r-', lw=3, alpha=0.6, label='delayed signal')
ax4.plot(x, signal_a+signal_b,
       'r-', lw=3, alpha=0.6, label='composite signal')
ax4.plot(x, np.zeros_like(x), 'b--', lw=3, alpha=0.6, label='x-axis')
ax4.axvline(x=0.24, color='k', linestyle='--', label=r't(U=0)')
for ax in axes:
    ax.legend()
    ax.grid(alpha=.6)
    ax.set_ylabel('Voltage')
ax4.set_xlabel('time')
# plt.suptitle(f'Defining amplitude insensitive time-points')
plt.savefig('figures/CFDIllustration.png', format='png', dpi=500, transparent=True)
plt.show()