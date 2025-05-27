import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

data = np.loadtxt("data/azot_characteristics.csv", delimiter=",", skiprows=1)
current_data = data[:, 0]
U_12 = data[:, 1]
U_45 = data[:, 2]
U_14 = data[:, 3]
U_25 = data[:, 4]

fontsize = 28
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

fig, ax = plt.subplots(figsize=(12, 6))
ax.scatter(
    current_data,
    U_12,
    label=r"current for $U_{12}$",
    color="#ec008c",
    s=4,
)
ax.scatter(
    current_data,
    U_12,
    label=r"current for $U_{45}$",
    color="#ec008c",
    s=4,
)

plt.xlabel(r"temperatura ($T$) [$^{\circ}C$]"),
ax.set_ylabel(r"ujemne ciśnienie ($p_{\mathrm{ext}}$) [bar]")
plt.xlim(0, 320 - 273)
plt.ylim(0, 300)

plt.legend(frameon=False)
plt.tight_layout()

parent_dir = Path(__file__).parent
tosave = parent_dir / "graphs/p_t.pdf"

plt.savefig(tosave, bbox_inches="tight")

plt.show()