pragma circom 2.1.9;

// algebraic circuit for: x^3 + 4x^2 + y^2 = 67

template Polynomial(){

    signal input x, y;

    // x^3 term
    signal v_1, v_1_inter;
    v_1_inter <== x * x;
    v_1 <== x * v_1_inter;

    // 4x^2 term
    signal v_2, v_2_inter;
    v_2_inter <== 4 * x;
    v_2 <== v_2_inter * x;

    // y^2 term
    signal v_3;
    v_3 <== y * y;

    // sum of all terms
    signal output out;

    out <== v_1 + v_2 + v_3 - 67;
}

component main = Polynomial();