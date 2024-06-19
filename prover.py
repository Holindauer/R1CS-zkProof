from py_ecc.bn128 import G1, G2, Z1, pairing, add, multiply, eq, bn128_curve as curve
from functools import reduce
import numpy as np

class Prover:
    def __init__(self):

        # R1CS matrices (Aw * Bw = Cw) for x^3 + 4x^2 + y^2 = 67
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
        self.exeCircuit(x, y)        # execute circuit and generate witness
        self.verifyConstraint()      # verify witness satisfies r1cs (Aw * Bw = Cw)    
        self.encryptWitness()        # encrypt witness with G1 and G2
        out_vectors = self.dotMats() # dot each row of matrices with encrypted witness
        print(out_vectors[0])

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
        # make 2 encrypted copies of witness w/ G1 and G2
        self.w_G1 = np.array([self.safe_mul(G1, int(i)) for i in self.w])
        self.w_G2 = np.array([self.safe_mul(G2, int(i)) for i in self.w])

    def dotMats(self):

        # eliptic curve dot product (witness dot matrix row)
        def dot(row, wit):  
            mul_pts = [self.safe_mul(w_i, int(A_i)) for A_i, w_i in zip(row, wit)]
            add_pts = lambda p1, p2: add(p1, p2)
            return reduce(add_pts, mul_pts, Z1) # sum points 
        
        # matrix encrypted witness pairings
        mat_wit_pairs = [(self.A, self.w_G1), (self.B, self.w_G2), (self.C, self.w_G1)]  

        # dot each mats row w/ encrypted witness
        out_vectors = []
        for mat, wit in mat_wit_pairs:
            encypted_dot = [dot(row, wit) for row in mat]
            out_vectors.append(encypted_dot)

        return out_vectors
        
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

    p.genProof(3, 2)



    # Example usage
    negative_scalar = -3
    point = curve.G1  # Assuming G1 is the generator point of bn128 defined in your context
    result = Prover.safe_mul(point, negative_scalar)
    print("Resulting point:", result)