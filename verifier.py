from py_ecc.bn128 import G1, G2, Z1, add, multiply, pairing
from functools import reduce
import numpy as np


class Verifier:
    '''
    Verifier.verifyProof() accepts 2 encrypted witnesses (one w/ G1, one w/ G2) that both
    contain a puclic claim about the output of the circuit, as well as the agreed upon
    R1CS matrices (Aw, Bw, Cw) for the circuit. The verifier checks that the public claim
    is valid, encrypts the public claim, multiplies the encrypted witnesses by the R1CS
    matrices, computes bilinear pairings of the resulting vectors, and asserts the pairings
    are pairwise equal.
    '''
    def __init__(self):

        # agreed upon R1CS matrices (Aw * Bw = Cw) for x^3 + 4x^2 + y^2 = 67
        self.agreed_A = np.array([[0,0,1,0,0,0,0],  # lhs
                                  [0,0,0,0,1,0,0],
                                  [0,0,4,0,0,0,0],
                                  [0,0,0,1,0,0,0]])

        self.agreed_B = np.array([[0,0,1,0,0,0,0],  # rhs
                                  [0,0,1,0,0,0,0],
                                  [0,0,1,0,0,0,0],
                                  [0,0,0,1,0,0,0]])

        self.agreed_C = np.array([[0,0,0,0,1,0,0],  # vars
                                  [0,0,0,0,0,1,0],
                                  [0,0,0,0,0,0,1],
                                  [67,0,0,0,0,-1,-1]])

    def verifyProof(self, w_G1, w_G2, A, B, C):

        # verify public claim in witness is valid
        self.checkClaim(w_G1, w_G2, A, B, C)

        # encrypt public claim
        self.encryptPublicClaim(w_G1, w_G2)

        # multiply encrypted witness w/ r1cs matrices
        Aw_G1, Bw_G2, Cw_G1 = self.dotEncryptedWitness(A, B, C, w_G1, w_G2)
        
        # compute bilinear pairings and assert equality
        Aw_Bw, Cw_G2 = self.blPairing(Aw_G1, Bw_G2, Cw_G1)

        return True if self.verifyPairings(Aw_Bw, Cw_G2) else False

    def checkClaim(self, w_G1, w_G2, A, B, C):
        # verify public claim in witness is valid 
        assert w_G1[0] == 1 and w_G1[1] == 67, "Claim is invalid"
        assert w_G2[0] == 1 and w_G2[1] == 67, "Claim is invalid"
        # verify r1cs matrices are as agreed upon
        for provided, agreed in [(A, self.agreed_A), (B, self.agreed_B), (C, self.agreed_C)]:
            np.array_equal(provided, agreed), "Claim is invalid"


    def encryptPublicClaim(self, w_G1, w_G2):
        # Encrypt the first two elements of w_G1 and w_G2
        for i in range(2):
            w_G1[i] = self.safe_mul(G1, w_G1[i])
            w_G2[i] = self.safe_mul(G2, w_G2[i])

    def dotEncryptedWitness(self, A, B, C, w_G1, w_G2):
        # eliptic curve dot product (witness dot matrix row)
        def dot(row, wit):  
            mul_pts = [self.safe_mul(w_i, int(A_i)) for A_i, w_i in zip(row, wit)]
            add_pts = lambda p1, p2: add(p1, p2)
            return reduce(add_pts, mul_pts, Z1) # sum points 
        
        # matrix encrypted witness pairings
        mat_wit_pairs = [(A, w_G1), (B, w_G2), (C, w_G1)]  

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

    @staticmethod
    def blPairing(Aw, Bw, Cw):  # NOTE this func is slow bc G12 pts are huge
        
        # bilinear pairings for lhs and rhs of r1cs exe
        Aw_Bw = [pairing(b, a) for a, b in zip(Aw, Bw)]

        # bilinear pairings for Cw and G2 list
        G2_list = [G2] * len(Cw)
        Cw_G2 = [pairing(g, c) for c, g in zip(Cw, G2_list)]

        return Aw_Bw, Cw_G2

    @staticmethod
    def verifyPairings(Aw_Bw, Cw_G2):
        # if the bilinear pairings are pairwise equal, the proof is valid
        return True if Aw_Bw == Cw_G2 else False
    


if __name__ == "__main__":

    from prover import Prover
    prover = Prover()
    
    # get encrypted wintesses and r1cs matrices
    w_G1, w_G2, A, B, C = prover.genProof(3, 2)  

    verifier = Verifier()
    verified = verifier.verifyProof(w_G1, w_G2, A, B, C)

    if verified:
        print("Proof is valid!")

