import numpy as np

# create array
a = np.array([1, 2, 3])

# create array filled with 0's
b = np.zeros(3)

# create array filled with 1's
c = np.ones(3)

# create empty array (may vary in num)
d = np.empty(3)

# ranged elems
e = np.arange(4)
e2 = np.arange(5, 11)  # 5-10

print(f"""
a = {a}
b = {b}
c={c}
d={d}
e={e}
e2={e2}""")
