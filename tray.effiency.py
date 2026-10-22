import numpy as np
import matplotlib.pyplot as plt



power = np.array([40, 50])                     
velocity = np.array([0.0601074, 0.0991325])     
efficiency = np.array([16.7516, 14.1954])       


fig, ax = plt.subplots(figsize=(8, 5))


ax.plot(
    velocity,
    efficiency,
    marker="o",
    markersize=9,
    linewidth=1.5,
    color="tab:blue"
)


for v, e, p in zip(velocity, efficiency, power):
    ax.annotate(
        f"{p}% power\n{e:.1f}%",
        xy=(v, e),
        xytext=(0, 14),
        textcoords="offset points",
        ha="center",
        fontsize=11
    )

ax.set_title("Oldershaw column: estimated tray efficiency (B4)")
ax.set_xlabel("Superficial vapour velocity [m/s]")
ax.set_ylabel("Overall tray efficiency [%]")

ax.set_xlim(0.04, 0.12)
ax.set_ylim(0, 25)
ax.grid(alpha=0.3)

fig.text(
    0.5, 0.03,
    "Estimates based on assumed atmospheric pressure and "
    "approximate ABV conversion.\n"
    "Steady state was not clearly established.",
    ha="center",
    fontsize=9
)

fig.tight_layout(rect=[0, 0.12, 1, 1])


fig.savefig(
    "oldershaw_efficiency.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


for p, v, e in zip(power, velocity, efficiency):
    print(
        f"{p}% power: "
        f"vapour velocity = {v:.4f} m/s, "
        f"tray efficiency = {e:.1f}%"
    )