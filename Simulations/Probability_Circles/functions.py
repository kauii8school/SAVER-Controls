import numpy as np
import matplotlib.path as mpath
import matplotlib.patches as mpatches

def equi(ax, center_x, center_y, radius, *args, **kwargs):

    X, Y = [], []
    for azimuth in range(0, 360):
        X.append(radius * np.cos(azimuth))
        Y.append(radius * np.sin(azimuth))

    X, Y = np.asarray(X), np.asarray(Y)
    X = X + center_x
    Y = Y + center_y
    #Patches
    Path = mpath.Path
    verts = list(zip(X,Y))
    codes =  [Path.CURVE4 for _ in range(len(verts))]
    #codes[-1] = Path.CLOSEPOLY
    codes[0] = Path.MOVETO
    path = mpath.Path(verts, codes)
    patch = mpatches.PathPatch(path, facecolor='g', alpha=.3, linewidth=2)
    ax.add_patch(patch)