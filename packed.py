import numpy as np
import matplotlib.pyplot as plt


def vapour_velocity(reflux, abv, temperature_c, diameter, pressure):
    """Estimate superficial velocity assuming additive liquid volumes."""
    phi = abv / 100
    rho_ethanol = 0.789  # g/mL
    rho_water = 1.000   # g/mL
    M_ethanol = 46.07   # g/mol
    M_water = 18.015    # g/mol
    R = 8.314462        # J/(mol K)

    molar_flow = (reflux / 60) * (
        phi * rho_ethanol / M_ethanol
        + (1 - phi) * rho_water / M_water
    )

    temperature_k = temperature_c + 273.15
    vapour_flow = molar_flow * R * temperature_k / pressure
    area = np.pi * diameter**2 / 4

    return vapour_flow / area


def main():
    power = np.array([40, 50])
    reflux = np.array([40.4, 61.0])          # mL/min
    temperature_c = np.array([75.2, 74.8])  # °C
    abv = np.array([90.429, 85.820])        # vol%

    # The 40% GC value, 90.429 vol%, is provisional.
    # Samples and reflux readings must represent the same operating point.
    diameter = 0.050    # m
    pressure = 101300   # Pa, assumed atmospheric pressure

    packing_height = 1.3                # m
    total_stages = np.array([14, 11])   # Including reboiler

    packing_stages = total_stages - 1
    hetp = packing_height / packing_stages

    velocity = vapour_velocity(
        reflux,
        abv,
        temperature_c,
        diameter,
        pressure
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(
        velocity,
        hetp,
        marker="s",
        markersize=8,
        linewidth=1.5,
        color="tab:orange"
    )

    for p, v, h in zip(power, velocity, hetp):
        ax.annotate(
            f"{p}% power\n{h:.3f} m",
            xy=(v, h),
            xytext=(0, 13),
            textcoords="offset points",
            ha="center",
            fontsize=11
        )

    ax.set_title("Packed column (B20)")
    ax.set_xlabel("Superficial vapour velocity [m/s]")
    ax.set_ylabel("HETP [m]")
    ax.set_xlim(0.15, 0.39)
    ax.set_ylim(0, 0.18)
    ax.grid(alpha=0.3)

    fig.text(
        0.5, 0.03,
        "Estimated velocities: atmospheric pressure and additive "
        "liquid volumes assumed.\n"
        "40% GC value provisional; line connects operating points.",
        ha="center",
        fontsize=9
    )

    fig.tight_layout(rect=[0, 0.12, 1, 1])

    fig.savefig(
        "packed_hetp_vs_velocity.png",
        dpi=300,
        bbox_inches="tight"
    )

    for p, n, v, h in zip(power, packing_stages, velocity, hetp):
        print(f"\n{p}% boiler power")
        print(f"Theoretical stages in packing: {n}")
        print(f"Superficial vapour velocity: {v:.4f} m/s")
        print(f"HETP: {h:.3f} m")

    plt.show()


if __name__ == "__main__":
    main()