import numpy as np
import matplotlib.pyplot as plt

# --- Example data ---
N = 100
values = np.random.rand(N)
data = values[np.newaxis, :]

# Sections (must sum to N)
section_sizes  = [30, 40, 30]
section_labels = ["A", "B", "C"]

# Boundaries and centers
boundaries = np.cumsum(section_sizes)[:-1]
starts = np.r_[0, boundaries]
ends   = np.r_[boundaries, N]
centers = (starts + ends) / 2

fig, ax = plt.subplots(figsize=(10, 2.2))
im = ax.imshow(data, aspect="auto", cmap="jet", vmin=0, vmax=1)

# Colorbar
cbar = fig.colorbar(im, ax=ax, pad=0.02)
cbar.set_label("Performance")

# Stripe row: hide y-axis
ax.set_yticks([])
ax.set_title("Stripe plot with top section indicators")

# Bottom: dense index ticks (as before)
ax.set_xticks(np.arange(0, N, 5))
ax.tick_params(axis="x", which="major", bottom=True, labelbottom=True, top=False, labeltop=False, pad=2)
ax.set_xlabel("Index")

# Top: section indicators on a dedicated top axis
ax_top = ax.twiny()
ax_top.set_xlim(ax.get_xlim())
ax_top.set_xticks(centers - 0.5)
ax_top.set_xticklabels(section_labels, fontsize=12, fontweight="bold")
ax_top.tick_params(axis="x", length=0, pad=6)  # no tick marks, just labels
ax_top.spines["top"].set_visible(False)        # cleaner look
ax_top.spines["bottom"].set_visible(False)
ax_top.spines["left"].set_visible(False)
ax_top.spines["right"].set_visible(False)

# Vertical separators: from bottom of stripe (0) up to the section-label height region (>1)
# (No extension below the stripe plot anymore.)
for b in boundaries:
    x = b - 0.5
    ax.plot([x, x], [0.0, 1.18],
            transform=ax.get_xaxis_transform(),  # x=data, y=axes coords
            linestyle="--", linewidth=2.5, color="black",
            zorder=10, clip_on=False)

# Make room on top for the section labels
fig.subplots_adjust(top=0.78)

plt.show()
