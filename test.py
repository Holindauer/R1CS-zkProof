from prover import Prover
from verifier import Verifier




def run_test(x, y, expected: bool):

    p = Prover()
    v = Verifier()

    # generate proof for valid solution (save to proof.txt)
    w_G1, w_G2, A, B, C = p.genProof(x, y)

    # verify proof for valid solution
    verified = v.verifyProof(w_G1, w_G2, A, B, C)

    assert verified == expected, f"Test failed for x={x}, y={y} expected={expected} got={verified}"



if __name__ == "__main__":

    # valid solution 
    x_valid, y_valid = 3, 2

    # invalid solution
    x_invalid, y_invalid = 1, 1

    run_test(x_valid, y_valid, True)

    # expect an exception to be raised for invalid solution
    try :
        run_test(x_invalid, y_invalid, False)
    except AssertionError:
        pass

    print("All tests passed!")

