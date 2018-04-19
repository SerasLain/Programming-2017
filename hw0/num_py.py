import numpy as np


ar = np.random.randint(0, 10, size=(3,5))
print(ar[ar % 2].max())

