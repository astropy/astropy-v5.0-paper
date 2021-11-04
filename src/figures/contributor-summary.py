"""
TODO: This currently just produces a placeholder figure!
"""
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)

fig, ax = plt.subplots(1, 1, figsize=(6, 6))
xy = rng.uniform(size=(2, 128))
ax.plot(*xy, linestyle='none')

fig.savefig("contributor-summary.pdf", bbox_inches="tight")
