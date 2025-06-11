import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib.colors as mcolors

tableau = list(mcolors.TABLEAU_COLORS)

data = np.loadtxt("data/Ualong_B_nitrogen.csv", delimiter=",")
Ualong_nitrogen_field = data[:, 0]
Ualong_nitrogen_voltage = data[:, 1]

data = np.loadtxt("data/Ualong_B_room.csv", delimiter=",")
Ualong_room_field = data[:, 0]
Ualong_room_voltage = data[:, 1]

data = np.loadtxt("data/Uhall_B_nitrogen.csv", delimiter=",")
Uhall_nitrogen_field = data[:, 0]
Uhall_nitrogen_voltage = data[:, 1]

data = np.loadtxt("data/Uhall_B_room.csv", delimiter=",")
Uhall_room_field = data[:, 0]
Uhall_room_voltage = data[:, 1]

h = 0.65 * 10 ** (-3)
zeta = 0.38 * 10 ** (-3)
l1 = 1.2 * 10 ** (-3)
I = 0.01

alpha_nitrogen = 375.66
beta_nitrogen = 47
gamma_nitrogen = 2950.28
delta_nitrogen = 1328
sigma0_nitrogen = 6817


def Ualong_nitrogen(B):
    return (
        ((I * l1) / (zeta * h))
        * (sigma0_nitrogen + delta_nitrogen * B**2)
        / (sigma0_nitrogen**2 + B**2 * gamma_nitrogen**2)
    )


def Uhall_nitrogen(B):
    return (
        ((B * I) / (zeta))
        * (alpha_nitrogen + beta_nitrogen * B**2)
        / (sigma0_nitrogen**2 + B**2 * gamma_nitrogen**2)
    )


alpha_room, beta_room, gamma_room, delta_room = -98.4, 389.8, -5430, 6506.1
sigma0_room = 4875.74


def Ualong_room(B):
    return (
        ((I * l1) / (zeta * h))
        * (sigma0_room + delta_room * B**2)
        / (sigma0_room**2 + B**2 * gamma_room**2)
    )


def Uhall_room(B):
    return (
        ((B * I) / (zeta))
        * (alpha_room + beta_room * B**2)
        / (sigma0_room**2 + B**2 * gamma_room**2)
    )


B_list = np.linspace(0, 2, 200)

Ualong_nitrogen_theory = Ualong_nitrogen(B_list)
Ualong_room_theory = Ualong_room(B_list)
Uhall_nitrogen_theory = Uhall_nitrogen(B_list)
Uhall_room_theory = Uhall_room(B_list)

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
    figsize=(20, 6),
    constrained_layout=False,
)

gs = fig.add_gridspec(
    2,
    2,
    wspace=0.13,
    hspace=0.0,
    width_ratios=[1, 1],
)

Ualong_plot_nit = fig.add_subplot(gs[1, 0])
Ualong_plot_temp = fig.add_subplot(gs[0, 0], sharex=Ualong_plot_nit)
Uhall_plot = fig.add_subplot(gs[:, 1])

plt.setp(Ualong_plot_temp.get_xticklabels(), visible=False)

Ualong_plot_nit.scatter(
    Ualong_nitrogen_field,
    10 ** (3) * Ualong_nitrogen_voltage,
    c=tableau[0],
    label=r"($N$) longitudinal voltage",
    zorder=1,
)

Ualong_plot_temp.scatter(
    Ualong_room_field,
    10 ** (3) * Ualong_room_voltage,
    c=tableau[1],
    label=r"$(RT)$ longitudinal voltage",
    zorder=1,
)

Ualong_plot_nit.plot(
    B_list,
    10 ** (3) * Ualong_nitrogen_theory,
    color="#a0cbe8",
    lw=2,
    label=r"($N$) fitted curve",
    zorder=0,
)

Ualong_plot_temp.plot(
    B_list,
    10 ** (3) * Ualong_room_theory,
    color="#ffbe7d",
    lw=2,
    label=r"$(RT)$ fitted curve",
    zorder=0,
)

Uhall_plot.scatter(
    Uhall_nitrogen_field,
    10 ** (3) * Uhall_nitrogen_voltage,
    c=tableau[0],
    label=r"($N$) Hall voltage",
    zorder=1,
)

Uhall_plot.scatter(
    Uhall_room_field,
    10 ** (3) * Uhall_room_voltage,
    c=tableau[1],
    label=r"$(RT)$ Hall voltage",
    zorder=1,
)

Uhall_plot.plot(
    B_list,
    10 ** (3) * Uhall_nitrogen_theory,
    color="#a0cbe8",
    lw=2,
    label=r"($N$) fitted curve",
    zorder=0,
)

Uhall_plot.plot(
    B_list,
    10 ** (3) * Uhall_room_theory,
    color="#ffbe7d",
    lw=2,
    label=r"$(RT)$ fitted curve",
    zorder=0,
)

Ualong_plot_nit.legend(frameon=False, loc=[0.05, 0.5])

Ualong_plot_temp.legend(frameon=False, loc=[0.32, -0.02])

Uhall_plot.legend(frameon=False, loc=[0.49, 0.02])

Ualong_plot_temp.text(
    0.01,
    0.85,
    r"(a)",
    fontsize=fontsize,
    zorder=1,
    color="k",
    transform=Ualong_plot_temp.transAxes,
)

Ualong_plot_temp.text(
    -0.145,
    -0.5,
    r"voltage ($U$) [mV]",
    fontsize=fontsize,
    zorder=1,
    rotation=90,
    color="k",
    transform=Ualong_plot_temp.transAxes,
)


Ualong_plot_nit.text(
    0.01,
    0.85,
    r"(b)",
    fontsize=fontsize,
    zorder=1,
    color="k",
    transform=Ualong_plot_nit.transAxes,
)

Uhall_plot.text(
    0.01,
    0.93,
    r"(c)",
    fontsize=fontsize,
    zorder=1,
    color="k",
    transform=Uhall_plot.transAxes,
)

Ualong_plot_nit.set_xlim(0, 2)
Ualong_plot_nit.set_ylim(7.1, 7.28)

# Ualong_plot_nit.set_ylabel(r"voltage ($U$) [mV]")
Ualong_plot_nit.set_xlabel(r"magnetic field ($B$) [T]"),

Uhall_plot.set_xlim(0, 2)
Uhall_plot.set_ylim(-0.07, 0.4)

Uhall_plot.set_xlabel(r"magnetic field ($B$) [T]"),
Uhall_plot.set_ylabel(r"voltage ($U$) [mV]")


Ualong_plot_temp.set_xlim(0, 2)
Ualong_plot_temp.set_ylim(9.9, 10.7)

# Ualong_plot_temp.set_ylabel(r"voltage ($U$) [mV]")

# plt.hlines(0, -(10**3), 10**3, colors="0.7", linestyles="--", zorder=0)
# plt.vlines(0, -(10**3), 10**3, colors="0.7", linestyles="--", zorder=0)

parent_dir = Path(__file__).parent
tosave = parent_dir / "graphs/hall_measurement.pdf"

plt.savefig(
    tosave,
    bbox_inches="tight",
    pad_inches=0.1,
)
# plt.show()
