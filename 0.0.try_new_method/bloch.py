from qutip import *
import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(projection='3d'))
ax.axis('square')

b=Bloch(fig=fig,axes=ax)
b.make_sphere()