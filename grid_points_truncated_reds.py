import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from matplotlib.colors import LinearSegmentedColormap

n = 9
x = np.arange(n)
y = np.arange(n)
X, Y = np.meshgrid(x, y)

# Replace with your own 2D percentage array.
percent = (
    32 * np.exp(-(((X - 4.1) / 1.45) ** 2 + ((Y - 4.0) / 1.25) ** 2) / 2)
    + 5 * np.exp(-(((X - 5.2) / 0.9) ** 2 + ((Y - 3.4) / 1.1) ** 2) / 2)
)
percent[percent < 0.8] = 0
percent = np.round(percent, 1)

xf = X.ravel()
yf = Y.ravel()
pf = percent.ravel()

zero = pf == 0
nonzero = ~zero

# Square-root scaling for marker sizes
s_min = 35
s_max = 1100
normalized = np.sqrt(pf / pf.max()) if pf.max() > 0 else np.zeros_like(pf)
sizes = s_min + normalized * (s_max - s_min)

# Truncate the Reds colormap to avoid near-white low values
base_cmap = plt.cm.Reds
trunc_reds = LinearSegmentedColormap.from_list(
    "truncReds",
    base_cmap(np.linspace(0.25, 1.0, 256))
)

fig, ax = plt.subplots(figsize=(8, 7))

# 0% points in blue (C0), borderless
ax.scatter(
    xf[zero],
    yf[zero],
    s=s_min,
    color="C0",
    alpha=0.9,
    edgecolors="none",
    linewidths=0,
    zorder=1,
    label="0%",
)

# Nonzero points in truncated red, borderless
sc = ax.scatter(
    xf[nonzero],
    yf[nonzero],
    s=sizes[nonzero],
    c=pf[nonzero],
    cmap=trunc_reds,
    vmin=pf[nonzero].min() if np.any(nonzero) else 0,
    vmax=pf[nonzero].max() if np.any(nonzero) else 1,
    alpha=0.92,
    edgecolors="none",
    linewidths=0,
    zorder=2,
)

# Labels for nonzero values only
if np.any(nonzero):
    pmax = pf[nonzero].max()
    for x0, y0, p0 in zip(xf[nonzero], yf[nonzero], pf[nonzero]):
        text_color = "white" if p0 >= 0.55 * pmax else "black"
        outline_color = "black" if text_color == "white" else "white"

        txt = ax.text(
            x0, y0, f"{p0:.1f}%",
            ha="center",
            va="center",
            fontsize=8.5,
            color=text_color,
            weight="medium",
            zorder=3,
        )
        txt.set_path_effects([
            path_effects.Stroke(linewidth=2.0, foreground=outline_color),
            path_effects.Normal(),
        ])

ax.set_xticks(x)
ax.set_yticks(y)
ax.set_xlim(-0.6, n - 0.4)
ax.set_ylim(-0.6, n - 0.4)
ax.set_aspect("equal")
ax.grid(False)

ax.set_xlabel("Grid x-coordinate")
ax.set_ylabel("Grid y-coordinate")
ax.set_title("Grid points with 0% in blue and nonzero values in red")

if np.any(nonzero):
    cbar = fig.colorbar(sc, ax=ax, shrink=0.84, pad=0.03)
    cbar.set_label("Percentage (> 0)")

ax.legend(loc="upper right", frameon=True)

fig.tight_layout()
plt.show()
