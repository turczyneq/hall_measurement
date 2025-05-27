import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib.colors as mcolors

tableau = list(mcolors.TABLEAU_COLORS)

h = 0.65 * 10 ** (-3)
sigmah = 0.05 * 10 ** (-3)
zeta = 0.38 * 10 ** (-3)
sigmazeta = 0.02 * 10 ** (-3)
l1 = 1.2 * 10 ** (-3)
sigmal1 = 0.1 * 10 ** (-3)
l2 = 1 * 10 ** (-3)
sigmal2 = 0.1 * 10 ** (-3)
U_error = 10 ** (-4)
I_error = 10 ** (-4)


def calculate_data(data_path, axes, alfanum, temp):
    data = np.loadtxt(data_path, delimiter=",", skiprows=1)
    current_data = data[:, 0]
    U_12 = data[:, 1]
    U_45 = data[:, 2]

    """
    equation is as follows:

    U = (1/conductivity) (l/(h zeta)) * I

    but there are two different l - l1 = 1.2+-0.1 mm for U_12 and l2 = 1.0+-0.1 mm for U45

    additionally
        h = 0.65+-0.05 mm
        zeta = 0.38+-0.02 mm

    so it easier to use

    y = U * (h zeta / l)
    than sigmay = sqrt( SUM( (d(U * (h zeta / l))/dparam)**2 sigmaparam ,params))

    alpha = SUM(xi * yi)
    beta = SUM(xi**2)
    """

    yU_12 = U_12 * (h * zeta / l1)
    yU_45 = U_45 * (h * zeta / l2)
    sigmayU_12 = np.sqrt(
        (U_error * U_12 * h * zeta / l1) ** 2
        + (U_12 * (sigmah * zeta / l1)) ** 2
        + (U_12 * (h * sigmazeta / l1)) ** 2
        + (U_12 * (h * sigmazeta / l1**2) * sigmal1) ** 2
    )
    sigmayU_45 = np.sqrt(
        (U_error * U_45 * h * zeta / l2) ** 2
        + (U_45 * (sigmah * zeta / l2)) ** 2
        + (U_45 * (h * sigmazeta / l2)) ** 2
        + (U_45 * (h * sigmazeta / l2**2) * sigmal2) ** 2
    )

    alpha = np.sum(yU_12 * current_data) + np.sum(yU_45 * current_data)
    beta = 2 * np.sum(current_data**2)

    fit = alpha / beta

    sigmafit = (1 / beta) * np.sqrt(
        np.sum((current_data * sigmayU_12) ** 2)
        + np.sum((current_data * sigmayU_45) ** 2)
        + np.sum(
            (I_error * current_data * (yU_12 * beta - 2 * current_data * alpha)) ** 2
        )
        + np.sum(
            (I_error * current_data * (yU_45 * beta - 2 * current_data * alpha)) ** 2
        )
    )

    conductivity = 1 / fit
    sigmaconductivity = (1 / fit) ** 2 * sigmafit

    if alfanum == "(a)":
        to_print_cond = int(round(conductivity))
        to_print_sigmacond = int(round(sigmaconductivity))
    else:
        to_print_cond = int(round(conductivity, -1))
        to_print_sigmacond = int(round(sigmaconductivity, -1))

    list_current = np.linspace(-35, 35, 50) * 10 ** (-3)

    fit_U_12 = l1 / (h * zeta) * fit * list_current
    fit_U_45 = l2 / (h * zeta) * fit * list_current

    axes.plot(
        list_current * 10 ** (3),
        fit_U_12 * 10 ** (3),
        label=r"fit for $U_{12}$",
        color="#a0cbe8",
        lw=5,
        zorder=1,
    )

    axes.plot(
        list_current * 10 ** (3),
        fit_U_45 * 10 ** (3),
        label=r"fit for $U_{45}$",
        color="#ffbe7d",
        lw=5,
        zorder=1,
    )

    axes.scatter(
        current_data * 10**3,
        U_12 * 10**3,
        label=r"current for $U_{12}$",
        color=tableau[0],
        s=50,
        zorder=2,
    )
    axes.scatter(
        current_data * 10**3,
        U_45 * 10**3,
        label=r"current for $U_{45}$",
        color=tableau[1],
        s=50,
        zorder=2,
    )

    axes.set_xlabel(r"current ($I$) [mA]"),
    axes.set_ylabel(r"voltage drop ($U$) [mV]")
    axes.set_xlim(np.min(current_data * 10**3) - 1, np.max(current_data * 10**3) + 1)
    axes.set_ylim(np.min(U_12 * 10**3) - 1, np.max(U_12 * 10**3) + 1)

    axes.hlines(0, -(10**3), 10**3, colors="k", linestyles="--", zorder=0)
    axes.vlines(0, -(10**3), 10**3, colors="k", linestyles="--", zorder=0)

    axes.text(
        0.05,
        0.6,
        rf"$\sigma^\star = {to_print_cond}\pm{to_print_sigmacond}\;\frac{{\textrm{{A}}^2\textrm{{s}}^3}}{{\textrm{{kg}}\,\textrm{{m}}^3}}$",
        fontsize=fontsize,
        zorder=1,
        color="k",
        transform=axes.transAxes,
    )

    axes.text(
        0.01,
        0.93,
        alfanum,
        fontsize=fontsize,
        zorder=1,
        color="k",
        transform=axes.transAxes,
    )

    axes.text(
        0.1,
        0.93,
        temp,
        fontsize=fontsize,
        zorder=1,
        color="k",
        transform=axes.transAxes,
    )

    axes.legend(frameon=False, loc=[0.53, 0])

    return 0


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
    constrained_layout=True,
)

gs = fig.add_gridspec(
    1,
    2,
    wspace=0.02,
    width_ratios=[1, 1],
)

nitro_plt = fig.add_subplot(gs[0, 0])
room_plt = fig.add_subplot(gs[0, 1])

calculate_data("data/azot_characteristics.csv", nitro_plt, "(a)", "nitrogen")
calculate_data("data/room_characteristics.csv", room_plt, "(b)", "room temperature")


parent_dir = Path(__file__).parent
tosave = parent_dir / "graphs/characteristics.pdf"

plt.savefig(tosave, bbox_inches="tight")

plt.show()
