class Verifier:

    def verifyProof(self, proof_file):
        # read proof from txt file and verify pairings
        Aw_Bw, Cw_G2 = self.read_proof(proof_file)
        verified: bool = self.verifyPairings(Aw_Bw, Cw_G2)

        if verified:
            print("Proof is valid")
        else:
            print("Proof is invalid")

    def read_proof(self, proof_file):
        with open(proof_file, "r") as f:
            lines = f.readlines()
        # split at first whitespace and eval list of G12 points
        Aw_Bw = eval(lines[0].split(' ', 1)[1])
        Cw_G2 = eval(lines[1].split(' ', 1)[1])
        return Aw_Bw, Cw_G2
    
    # if the bilinear pairings are pairwise equal, the proof is valid
    def verifyPairings(self, Aw_Bw, Cw_G2):
        return True if Aw_Bw == Cw_G2 else False


if __name__ == "__main__":
    verifier = Verifier()
    verifier.verifyProof("proof.txt")