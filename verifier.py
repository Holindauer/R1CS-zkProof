from py_ecc.bn128 import pairing, G2


class Verifier:
    '''
    Verifier.verifyProof() accepts 3 lists of curve points points, Aw_G1, Bw_G2, Cw_G1 
    (G1, G2, G1 respectively), computes bilinear pairings of Aw_Bw w/ Bw_G2 as well as 
    Cw_G1 w/ a list of G2 generators, and asserts elementwise equality of each pairings 
    in the lists.
    '''

    def verifyProof(self, Aw_G1, Bw_G2, Cw_G1):

        # compute bilinear pairings and assert equality
        Aw_Bw, Cw_G2 = self.blPairing(Aw_G1, Bw_G2, Cw_G1)

        if self.verifyPairings(Aw_Bw, Cw_G2):
            print("Proof is valid")
            return True
        else:
            print("Proof is invalid")
            return False

    @staticmethod
    def blPairing(Aw, Bw, Cw):  # NOTE this func is slow bc G12 pts are huge
        
        # bilinear pairings for lhs and rhs of r1cs exe
        Aw_Bw = [pairing(b, a) for a, b in zip(Aw, Bw)]

        # bilinear pairings for Cw and G2 list
        G2_list = [G2] * len(Cw)
        Cw_G2 = [pairing(g, c) for c, g in zip(Cw, G2_list)]

        return Aw_Bw, Cw_G2

    # if the bilinear pairings are pairwise equal, the proof is valid
    def verifyPairings(self, Aw_Bw, Cw_G2):
        return True if Aw_Bw == Cw_G2 else False




if __name__ == "__main__":
    from prover import Prover
    prover = Prover()
    out = prover.genProof(3, 2)

    verifier = Verifier()
    verifier.verifyProof(*out)