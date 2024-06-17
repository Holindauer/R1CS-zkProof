pragma circom 2.1.9;

// algebraic circuit for: x^3 + 4x^2 + y^2 = 14

template Polynomial(){

    signal input x, y;

    // x^3 term
    signal term_1, term_1_inter;

    term_1_inter <== x * x;
    term_1 <== x * term_1_inter;

    // 4x^2 term
    signal term_2, term_2_inter;

    term_2_inter <== 4 * x;
    term_2 <== term_2_inter * x;

    // y^2 term
    signal term_3;

    term_3 <== y * y;

    // sum of all terms
    signal output out;

    out <== term_1 + term_2 + term_3 - 14;
}

component main = Polynomial();