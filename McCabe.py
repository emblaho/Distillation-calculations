import numpy as np
import matplotlib.pyplot as plt


x_eq = np.array([
    0.0000, 0.0225, 0.0646, 0.1146,
    0.1942, 0.2684, 0.3751, 0.4987,
    0.7093, 0.7936, 0.8858, 0.8882,
    0.9803, 1.0000
])

y_eq = np.array([
    0.0000, 0.2326, 0.3850, 0.4576,
    0.5334, 0.5675, 0.6041, 0.6524,
    0.7541, 0.8149, 0.8889, 0.8925,
    0.9868, 1.0000
])


def abv_to_mole_fraction(abv):
    """Approximate conversion assuming additive liquid volumes."""
    if not 0 <= abv <= 100:
        raise ValueError("ABV must be between 0 and 100.")

    phi = abv / 100
    n_ethanol = phi * 0.789 / 46.07
    n_water = (1 - phi) * 1.000 / 18.015

    return n_ethanol / (n_ethanol + n_water)


def plot_mccabe_thiele(abv_top, abv_bottom, power):
    x_top = abv_to_mole_fraction(abv_top)
    x_bottom = abv_to_mole_fraction(abv_bottom)

    if not 0 < x_bottom < x_top < 1:
        raise ValueError("Require 0 < x_bottom < x_top < 1.")

    fig, ax = plt.subplots(figsize=(7, 7))

    ax.plot(
        x_eq, y_eq,
        color="navy",
        linewidth=2,
        label="Equilibrium curve"
    )

    ax.plot(
        [0, 1], [0, 1],
        "k--",
        linewidth=1,
        label="Operating line: y = x"
    )

    ax.axvline(
        x_top,
        color="darkorange",
        linestyle=":",
        label=f"Top: x = {x_top:.3f}"
    )

    ax.axvline(
        x_bottom,
        color="purple",
        linestyle=":",
        label=f"Bottom: x = {x_bottom:.3f}"
    )

    current = x_top
    n_full = 0
    n_total = None

    for _ in range(100):
        next_x = float(np.interp(current, y_eq, x_eq))

        if next_x >= current - 1e-12:
            raise RuntimeError(
                "Stage stepping stalled. Check compositions and VLE data."
            )

        endpoint = max(next_x, x_bottom)

        ax.plot(
            [current, endpoint],
            [current, current],
            color="seagreen",
            linewidth=1.8,
            label="Stage construction" if n_full == 0 else None
        )

        if next_x <= x_bottom:
            fraction = (current - x_bottom) / (current - next_x)
            n_total = n_full + fraction

            ax.plot(
                [x_bottom, next_x],
                [current, current],
                color="seagreen",
                linestyle=":",
                linewidth=1
            )

            ax.scatter(
                x_bottom, current,
                color="purple",
                zorder=5
            )
            break

        ax.plot(
            [next_x, next_x],
            [current, next_x],
            color="seagreen",
            linewidth=1.8
        )

        n_full += 1
        current = next_x

    if n_total is None:
        plt.close(fig)
        raise RuntimeError("Maximum stage count exceeded.")

    ax.set_title(
        f"McCabe–Thiele diagram — {power}% boiler power\n"
        "Total reflux"
    )

    ax.set_xlabel("Ethanol mole fraction in liquid, x [–]")
    ax.set_ylabel("Ethanol mole fraction in vapour, y [–]")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.grid(alpha=0.25)

    ax.text(
        0.04, 0.96,
        f"Estimated theoretical stages: {n_total:.2f}\n"
        "Including reboiler",
        transform=ax.transAxes,
        va="top",
        fontsize=11,
        bbox={
            "facecolor": "white",
            "alpha": 0.9,
            "edgecolor": "0.8"
        }
    )

    ax.legend(loc="lower right", fontsize=9)
    fig.tight_layout()

    filename = f"mccabe_thiele_{power}percent.png"
    fig.savefig(filename, dpi=300, bbox_inches="tight")

    print(f"\n{power}% boiler power")
    print(f"Top mole fraction: {x_top:.4f}")
    print(f"Bottom mole fraction: {x_bottom:.4f}")
    print(f"Theoretical stages including reboiler: {n_total:.2f}")
    print(f"Saved: {filename}")

    plt.show()


if __name__ == "__main__":
    plot_mccabe_thiele(
        abv_top=88.795,
        abv_bottom=16.099,
        power=40
    )

    plot_mccabe_thiele(
        abv_top=88.174,
        abv_bottom=15.865,
        power=50
    )