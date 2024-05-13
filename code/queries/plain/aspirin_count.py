import os
from pprint import pprint
import sys
import time
import numpy as np
from itertools import groupby

def preprocess(filename, num_rows):
    m = np.fromfile(filename, sep=" ", dtype=int, count=num_rows*13)
    m = m.reshape((num_rows,13))
    return m

def select_distinct(matrix: np.ndarray, column: int) -> np.ndarray:
    unique_values = np.unique(matrix[:, column], axis=0)
    return unique_values

table = preprocess("/home/mpretz/Thesis/MP-SPDZ/Player-Data/Input-P0-0", 100)
r = select_distinct(table, 1)

pprint(r)