import numpy as np
import pandas as pd
import time

player = 0
filename = "/home/martin/Masterarbeit/MP-SPDZ_latest/Player-Data/Input-P{}-0".format(player)

num_rows = 100000000
start_time = time.time()
m = np.fromfile(filename, sep=" ", dtype=int, count=num_rows*13)
m = m.reshape((num_rows,13))
end_time = time.time()
execution_time = end_time - start_time
print(execution_time)

