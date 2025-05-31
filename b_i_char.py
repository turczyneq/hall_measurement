import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib.colors as mcolors

tableau = list(mcolors.TABLEAU_COLORS)

data = np.loadtxt("data/b_i_char_up.csv", delimiter=",", skiprows=1)
current_up = data[:, 0]
magnetic_field_up = data[:, 1]

data = np.loadtxt("data/b_i_char_down.csv", delimiter=",", skiprows=1)
current_down = data[:, 0]
magnetic_field_down = data[:, 1]

fontsize = 25
plt.rcParams.update(
    {
        "text.usetex": True,
        "font.family": "Times",
        "axes.titlesize": fontsize,
        "axes.labelsize": fontsize,
        "xtick.labelsize": fontsize,
        "ytick.labelsize": fontsize,
        "legend.fontsize": fontsize,
        "text.latex.preamble": r"\usepackage[T1]{fontenc} \usepackage{lmodern}",
    }
)

fig = plt.figure(
    figsize=(10, 6),
)

plt.plot(
    current_up,
    magnetic_field_up,
    c=tableau[0],
    lw=2,
    label="upper curve",
)

plt.plot(
    current_down,
    magnetic_field_down,
    c=tableau[1],
    lw=2,
    label="lower curve",
)

plt.legend(frameon=False, loc=[0.6, 0.7])

plt.xlim(-10, 10)
plt.ylim(-1.9, 1.9)

plt.xlabel(r"current ($I$) [A]"),
plt.ylabel(r"magnetic field ($B$) [T]")

plt.hlines(0, -(10**3), 10**3, colors="0.7", linestyles="--", zorder=0)
plt.vlines(0, -(10**3), 10**3, colors="0.7", linestyles="--", zorder=0)

parent_dir = Path(__file__).parent
tosave = parent_dir / "graphs/b_i_char.pdf"

plt.savefig(tosave, bbox_inches="tight")

plt.show()
