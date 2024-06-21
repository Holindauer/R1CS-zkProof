from py_ecc.bn128 import G1, G2, Z1, add, multiply
from functools import reduce
import numpy as np


class Prover:
    '''
    Polynomial constaint: x^3 + 4x^2 + y^2 = 67

    Prover.genProof() executes algebraic circuit for constraint, creates witness, 
    makes encrypted versions of witness w/ G1 and G2, multiplies encrypted witness 
    w/ R1CS matrices (Aw, Bw, Cw) to generate proof
    '''
    def __init__(self):

        # agreed upon R1CS matrices (Aw * Bw = Cw) for x^3 + 4x^2 + y^2 = 67
        self.A = np.array([[0,0,1,0,0,0,0],  # lhs
                           [0,0,0,0,1,0,0],
                           [0,0,4,0,0,0,0],
                           [0,0,0,1,0,0,0]])

        self.B = np.array([[0,0,1,0,0,0,0],  # rhs
                           [0,0,1,0,0,0,0],
                           [0,0,1,0,0,0,0],
                           [0,0,0,1,0,0,0]])

        self.C = np.array([[0,0,0,0,1,0,0],  # vars
                           [0,0,0,0,0,1,0],
                           [0,0,0,0,0,0,1],
                           [67,0,0,0,0,-1,-1]])
        
    def genProof(self, x, y):
        self.exeCircuit(x, y)       # execute circuit and generate witness
        # self.verifyConstraint()   # verify witness satisfies r1cs (Aw * Bw = Cw)
        self.encryptWitness()       # encrypt witness with G1 and G2        

        # return encrypted witnesses and r1cs matrices as proof
        return self.w_G1, self.w_G2, self.A, self.B, self.C
        

    def exeCircuit(self, x, y):
        # exe algebraic circuit
        v1inter = x*x
        v1 = v1inter*x
        v2 = 4*x*x
        out = v1 + v2 + y*y 

        # create witness vector 
        self.w = np.array([1, out, x, y, v1inter, v1, v2])
        
    def verifyConstraint(self):
        # ensure r1cs constraint is satisfied by witness
        result = self.C.dot(self.w) == np.multiply(self.A.dot(self.w),self.B.dot(self.w))
        assert result.all(), "result contains an inequality"

    def encryptWitness(self):
        # Include first two elements unencrypted and encrypt the rest with G1 and G2
        self.w_G1 = [self.w[0], self.w[1]] + [self.safe_mul(G1, int(i)) for i in self.w[2:]]
        self.w_G2 = [self.w[0], self.w[1]] + [self.safe_mul(G2, int(i)) for i in self.w[2:]]

    @staticmethod
    def safe_mul(point, scalar):
        # eliptic curve scalar mul w/ negative scalar check and encoding
        if scalar < 0:
            result_point = multiply(point, -scalar)             # scalar multiply w/ inverse scalar
            negated_point = (result_point[0], -result_point[1]) # negate result point y-coordinate
            assert add(result_point, negated_point) == Z1, "Additive inverse property not satisfied"
            return negated_point
        else:
            return multiply(point, scalar) #directly mul  
    

if __name__ == "__main__":
    p = Prover()
    print(p.genProof(3, 2))