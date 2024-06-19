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

# inputs that solve the polynomial constraint
x = 3
y = 2

# original polynomial
out = x*x*x + 4*x*x + y*y

# intermediate variables
v1inter = x*x
v1 = v1inter*x
v2 = 4*x*x

# witness vector
w = np.array([1, out, x, y, v1inter, v1, v2])

# ensure that the constraint is satisfied when represented as an r1cs
result = C.dot(w) == np.multiply(A.dot(w),B.dot(w))
assert result.all(), "result contains an inequality"


print(out)
print(C.dot(w))
print(np.multiply(A.dot(w),B.dot(w)))
print(result)