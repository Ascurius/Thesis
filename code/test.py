import numpy as np
import pandas as pd

player = 0
filename = "/home/martin/Masterarbeit/MP-SPDZ_latest/Player-Data/Input-P{}-0".format(player)

num_rows = 100000000
m = np.fromfile(filename, sep=" ", dtype=int, count=num_rows*13)
m = m.reshape((num_rows,13))
print(m.shape)