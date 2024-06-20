from prover import Prover
from verifier import Verifier




def run_test(x, y, expected: bool):

    p = Prover()
    v = Verifier()

    # generate proof for valid solution (save to proof.txt)
    Aw_G1, Bw_G2, Cw_G1 = p.genProof(x, y)

    # verify proof for valid solution
    verified = v.verifyProof(Aw_G1, Bw_G2, Cw_G1)

    assert verified == expected, f"Test failed for x={x}, y={y} expected={expected} got={verified}"



if __name__ == "__main__":

    # valid solution 
    x_valid, y_valid = 3, 2

    # invalid solution
    x_invalid, y_invalid = 1, 1

    run_test(x_valid, y_valid, True)
    run_test(x_invalid, y_invalid, False)

    print("All tests passed!")

