# Using a Rank 1 Constraint System to Implement a Zero Knowledge Proof


This repository contains a from scratch implementation of a zero knowledge proof for a valid witness to a polynomial constraint. The purpose is to gain a better understanding of ZKPs.

The specific polynomial constaint used is placed on the variables $x$ and $y$ as follows: $x^3 + 4x^2 + y^2 = 67$ 

# Rank 1 Constaint Systems

The polynomial constaint $x^3 + 4x^2 + y^2 = 67$ is an algebraic circuit. given $x=3$ and $y=2$, the circuit is solved. 

We wish to prove that we have a valid solution to this constraint without revealing it. Before we can do this, we must convert it to a rank 1 constraint system. However, first we must rewrite the constaint such that it only has one multiplication per polynomial constraint. This is also illustrated with the following [circom template](polynomial.circom): 

    v1_inter = x * x
    v1 = v1_inter * x   
    v2 = 4x * x
    -v1 -v2 + 67 = y * y // additions moved to left side. was 67 = v1 + v2 + y^2

The *witness* is a 1xn vector that contains the values of all the input variables, output variable, and the intermediate values. It is a way to show that you have executed the entire circuit with correct execution and output. 

For the above circuit, the following is a valid witness

    witness:

    w = [1, 0, 3, 2, 9, 27, 36]

    where:
    
    w = [constant, out, x, y, v_1_inter, v_1, v_2] // constant is always 1 for scalar additions


The goal is to represent the algebraic circuit as the following systems of equations:

$$A \mathbf{w} \circ B \mathbf{w} = C \mathbf{w} $$

Where Matrix A encodes the left hand side variables and B encodes the right hand side variables of each binary operation in the polynomial constraints. C encodes the result variables. The variable w is the witness vector. $\circ$ is the hadamard product (element wise matmul).

The number of rows corresponds to the number of constraints in the circuit.

So, our matrices for $x^3 + x^2 + y^2 = 67$ are:

$$
A = \begin{pmatrix}
a{}_{1,1} & a{}_{1,out} & a{}_{1,x} & a{}_{1,y} & a{}_{1,v1inter} & a{}_{1,v1} & a{}_{1,v2} \\
a{}_{2,1} & a{}_{2,out} & a{}_{2,x} & a{}_{2,y} & a{}_{2,v1inter} & a{}_{2,v1}  & a{}_{2,v2} \\
a{}_{3,1} & a{}_{3,out} & a{}_{3,x} & a{}_{3,y} & a{}_{3,v1inter} & a{}_{3,v1} & a{}_{3,v2} \\
a{}_{4,1} & a{}_{4,out} & a{}_{4,x} & a{}_{4,y} & a{}_{4,v1inter} & a{}_{4,v1} & a{}_{4,v2} \\
\end{pmatrix}

=

\begin{pmatrix}
0 & 0 & 1 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 1 & 0 & 0 \\
0 & 0 & 4 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 1 & 0 & 0 & 0 \\
\end{pmatrix}

$$

$$
B = \begin{pmatrix}
b{}_{1,1} & b{}_{1,out} & b{}_{1,x} & b{}_{1,y} & b{}_{1,v1inter} & b{}_{1,v1} & b{}_{1,v2} \\
b{}_{2,1} & b{}_{2,out} & b{}_{2,x} & b{}_{2,y} & b{}_{2,v1inter} & b{}_{2,v1}  & b{}_{2,v2} \\
b{}_{3,1} & b{}_{3,out} & b{}_{3,x} & b{}_{3,y} & b{}_{3,v1inter} & b{}_{3,v1} & b{}_{3,v2} \\
b{}_{4,1} & b{}_{4,out} & b{}_{4,x} & b{}_{4,y} & b{}_{4,v1inter} & b{}_{4,v1} & b{}_{4,v2} \\
\end{pmatrix}

=

\begin{pmatrix}
0 & 0 & 1 & 0 & 0 & 0 & 0 \\
0 & 0 & 1 & 0 & 0 & 0 & 0 \\
0 & 0 & 1 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 1 & 0 & 0 & 0 \\
\end{pmatrix}

$$

$$
C = \begin{pmatrix}
c{}_{1,1} & c{}_{1,out} & c{}_{1,x} & c{}_{1,y} & c{}_{1,v1inter} & c{}_{1,v1} & c{}_{1,v2} \\
c{}_{2,1} & c{}_{2,out} & c{}_{2,x} & c{}_{2,y} & c{}_{2,v1inter} & c{}_{2,v1}  & c{}_{2,v2} \\
c{}_{3,1} & c{}_{3,out} & c{}_{3,x} & c{}_{3,y} & c{}_{3,v1inter} & c{}_{3,v1} & c{}_{3,v2} \\
c{}_{4,1} & c{}_{4,out} & c{}_{4,x} & c{}_{4,y} & c{}_{4,v1inter} & c{}_{4,v1} & c{}_{4,v2} \\
\end{pmatrix}

=

\begin{pmatrix}
0 & 0 & 0 & 0 & 1 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 1 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 1 \\
67 & 0 & 0 & 0 & 0 & -1 & -1 \\
\end{pmatrix}

$$

$$
w = \begin{pmatrix}
1 & out & x & y & v1inter & v1 & v2 \\
\end{pmatrix}
=
\begin{pmatrix}
1 & 0 & 3 & 2 & 9 & 27 & 36 \\
\end{pmatrix}
$$

$$
A \mathbf{w} \circ B \mathbf{w} = C \mathbf{w}
$$

This encoding makes up our rank 1 constraint system. This equality is validated within [r1cs.py](r1cs.py)



# Bilinear Pairings

A bilinear pairing is a relation between two groups such that it maps to a third group.

$$ e : G_1 x G_2 \rightarrow G_T $$

Where: $G_1$, $G_2$, and $G_T$ can all be different groups. However, they must satisfy the property that:

$$ e(aG_1, bG_2) = e(G_1, abG_2) = e(abG_1, G_2) $$

Where: the codomain of $e$ is the target group $G_T$.

In this context, $G_1$, $G_2$, and $G_T$ are all different elliptic curves over a finite field.

# Using the R1CS and Bilinear Pairings in a Zero Knowledge Proof

For our ZKP, we will create encrypted versions of the witness vector by broadcasting the multiplication of the generator for $G_1$ and $G_2$ to the witness vector.

Harking back to our R1CS, with $\mathbf{w}$ now as the encrypted witness. The following equation still holds due to the group homomorphism between elliptic curve point addition and scalar multiplication with integer multiplication and addition. However, due to the discrete log problem, the witness is obfuscated.

$$
A \mathbf{w} \circ B \mathbf{w} = C \mathbf{w}
$$



Then, after applying the dot product such w/ our group operators instead, the hadamard product is computed using bilear pairings instead of multiplication. This will keep the equality between

# Sources

https://www.rareskills.io/post/bilinear-pairing

https://www.rareskills.io/post/rank-1-constraint-system

https://www.rareskills.io/post/r1cs-zkp
