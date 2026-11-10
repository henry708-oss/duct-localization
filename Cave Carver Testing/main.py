#a testing main


import mazecarver as mz
import numpy as np

mode = 1
shape = (100,100,100)
matrix = np.zeros(shape, dtype=bool)
mz.Carve(matrix, mode)
mz.Vis(matrix, "Module Test", mode)