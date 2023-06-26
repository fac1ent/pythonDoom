import numpy as np
import numpy.random as rand

# vector of random numbers
x = rand.randint(-50, 50, 100000000)

# 1st(by standart loop)
y1 = [el ** 3 for el in x]
print("Done!")

# 2nd(by numpy.power())
y2 = np.power(x, 3)
print("Done!")

# 3rd(by double multiply)
y3 = x * x * x
print("Done!")
