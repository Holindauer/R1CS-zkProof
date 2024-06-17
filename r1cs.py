import numpy as np
import random

# matrices A, B, C
A = np.array([[0,0,1,0,0,0,0],
              [0,0,0,0,1,0,0],
              [0,0,4,0,0,0,0],
              [0,0,0,1,0,0,0]])

B = np.array([[0,0,1,0,0,0,0],
              [0,0,1,0,0,0,0],
              [0,0,1,0,0,0,0],
              [0,0,0,1,0,0,0]])

C = np.array([[0,0,0,0,1,0,0],
              [0,0,0,0,0,1,0],
              [0,0,0,0,0,0,1],
              [67,0,0,0,0,-1,-1]])


              
# # pick random values for x and y
# x = random.randint(1,1000)
# y = random.randint(1,1000)

x = 3
y = 2

# original polynomial
out = x*x*x + 4*x*x + y*y# the witness vector with the intermediate variables inside
v1inter = x*x
v1 = v1inter*x
v2 = 4*x*x

#out = v1 + v2 + y*y

w = np.array([1, out, x, y, v1inter, v1, v2])


print(out)

result = C.dot(w) == np.multiply(A.dot(w),B.dot(w))
assert result.all(), "result contains an inequality"
print(result)