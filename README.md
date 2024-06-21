# Using a Rank 1 Constraint System to Implement a Zero Knowledge Proof


This repository contains an implementation of a zero knowledge proof for a valid witness to the following polynomial constraint:

$$x^3 + 4x^2 + y^2 = 67$$

# Rank 1 Constaint Systems

### Algebraic Circuit Representation

The polynomial constaint $x^3 + 4x^2 + y^2 = 67$ is an algebraic circuit. given $x=3$ and $y=2$, the circuit is solved. 

For the ZKP, we wish to prove that we have a valid solution to this constraint without revealing it. Before we can do this, we must convert it to a rank 1 constraint system (R1CS). However, in order to do that, first we must rewrite the constaint such that it only contains one multiplication per polynomial constraint:

$$
v1{}_{Intermediate} = x * x  
$$

$$
v1 = v1{}_{Intermediate} * x     
$$

$$
v2 = 4x * x
$$

$$
-v1 -v2 + 67 = y * y
$$

This is also illustrated with the following [circom template](polynomial.circom).

### The Witness

The *witness* is a 1xn vector that contains the values of all the input variables, output variable, and the intermediate values. It is a way to show that you executed the entire circuit and correctly to have achieved the claimed outout.

For the above circuit, the following is a valid witness


```math
w = \begin{pmatrix} 1, 0, 3, 2, 9, 27, 36 \end{pmatrix}
```

where:

```math
w = \begin{pmatrix} constant, out, x, y, v1{}_{intermediate}, v_1, v_2 \end{pmatrix}
```
    
NOTE: the constant is always 1 for scalar additions

### Rank 1 Constraint System Representation of the Algebraic Circuit

The goal of the R1CS is to represent the algebraic circuit from above as the following systems of equations.

$$A \mathbf{w} \circ B \mathbf{w} = C \mathbf{w} $$

Where Matrix $A$ encodes the left hand side variables and $B$ encodes the right hand side variables of each binary operation in the polynomial constraints. $C$ encodes the result variables. The variable $w$ is the witness vector. $\circ$ is the hadamard product (element wise matmul). 

The number of rows in the R1CS corresponds to the number of constraints in the circuit. In our case it is 4. The number of columns correspond to the variables in the circuit (constant, out, x, y, v1intermediate, v1, v2). The first column is always 1 to allow for encoded scalar addition. 

When each (m, n) R1CS matrix is multiplied by the (n, 1) witness vector, it results in an (m, 1) vector. Because we have encoded the algebraic circuit to always contain one multiplication per constraint, the hadamard product of $Aw$ with $Bw$ represents the lhs and rhs of the binary operation that computes each variable in the constaint. Given a valid witness, $Aw \circ Bw$ should equal $Cw$. 

In this way, the systems of equations could be interpreted as a very verbose way to encode the circuit.

Our R1CS matrices for $x^3 + x^2 + y^2 = 67$ are:

```math
A = \begin{pmatrix}
a{}_{1,1} & a{}_{1,out} & a{}_{1,x} & a{}_{1,y} & a{}_{1,v1inter} & a{}_{1,v1} & a{}_{1,v2} \\
a{}_{2,1} & a{}_{2,out} & a{}_{2,x} & a{}_{2,y} & a{}_{2,v1inter} & a{}_{2,v1}  & a{}_{2,v2} \\
a{}_{3,1} & a{}_{3,out} & a{}_{3,x} & a{}_{3,y} & a{}_{3,v1inter} & a{}_{3,v1} & a{}_{3,v2} \\
a{}_{4,1} & a{}_{4,out} & a{}_{4,x} & a{}_{4,y} & a{}_{4,v1inter} & a{}_{4,v1} & a{}_{4,v2} 
\end{pmatrix}

=

\begin{pmatrix}
0 & 0 & 1 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 1 & 0 & 0 \\
0 & 0 & 4 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 1 & 0 & 0 & 0 
\end{pmatrix}

```

```math
B = \begin{pmatrix}
b{}_{1,1} & b{}_{1,out} & b{}_{1,x} & b{}_{1,y} & b{}_{1,v1inter} & b{}_{1,v1} & b{}_{1,v2} \\
b{}_{2,1} & b{}_{2,out} & b{}_{2,x} & b{}_{2,y} & b{}_{2,v1inter} & b{}_{2,v1}  & b{}_{2,v2} \\
b{}_{3,1} & b{}_{3,out} & b{}_{3,x} & b{}_{3,y} & b{}_{3,v1inter} & b{}_{3,v1} & b{}_{3,v2} \\
b{}_{4,1} & b{}_{4,out} & b{}_{4,x} & b{}_{4,y} & b{}_{4,v1inter} & b{}_{4,v1} & b{}_{4,v2} 
\end{pmatrix}

=

\begin{pmatrix}
0 & 0 & 1 & 0 & 0 & 0 & 0 \\
0 & 0 & 1 & 0 & 0 & 0 & 0 \\
0 & 0 & 1 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 1 & 0 & 0 & 0 
\end{pmatrix}

```

```math
C = \begin{pmatrix}
c{}_{1,1} & c{}_{1,out} & c{}_{1,x} & c{}_{1,y} & c{}_{1,v1inter} & c{}_{1,v1} & c{}_{1,v2} \\
c{}_{2,1} & c{}_{2,out} & c{}_{2,x} & c{}_{2,y} & c{}_{2,v1inter} & c{}_{2,v1}  & c{}_{2,v2} \\
c{}_{3,1} & c{}_{3,out} & c{}_{3,x} & c{}_{3,y} & c{}_{3,v1inter} & c{}_{3,v1} & c{}_{3,v2} \\
c{}_{4,1} & c{}_{4,out} & c{}_{4,x} & c{}_{4,y} & c{}_{4,v1inter} & c{}_{4,v1} & c{}_{4,v2} 
\end{pmatrix}

=

\begin{pmatrix}
0 & 0 & 0 & 0 & 1 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 1 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 1 \\
67 & 0 & 0 & 0 & 0 & -1 & -1 
\end{pmatrix}

```

```math
w = \begin{pmatrix}
1 & out & x & y & v1inter & v1 & v2 
\end{pmatrix}
=
\begin{pmatrix}
1 & 0 & 3 & 2 & 9 & 27 & 36 
\end{pmatrix}
```

$$
A \mathbf{w} \circ B \mathbf{w} = C \mathbf{w}
$$

This encoding makes up our rank 1 constraint system. This equality is validated within [r1cs.py](r1cs.py)



# Bilinear Pairings

A bilinear pairing is a relation between two groups such that it maps to a third group.

$$ e : G_1 x G_2 \rightarrow G_T $$

Where: $G_1$, $G_2$, and $G_T$ can all be different groups (which would make it an asymetric pairing). However, they must satisfy the property that:

$$ e(aG_1, bG_2) = e(G_1, abG_2) = e(abG_1, G_2) $$

Where: the codomain of $e$ is the target group $G_T$. $a$ and $b$ are constants.

In this context, $G_1$, $G_2$, and $G_T$ are all different elliptic curves over a finite field.

# Using R1CS and Bilinear Pairings in a Zero Knowledge Proof

### Agreed Upon Setup

The prover wishes to prove to the verifier that they have a valid solution to the polynomial constaint. The prover and verifier both agree upon the R1CS outlined above. 

### Prover Steps


The prover will first execute the circuit, saving each intermediate variable value to create the witness.

The prover will then create two encrypted versions of the witness vector by multiplying each term of the witness with the generator of $G_1$ or $G_2$. 

However, we will want to keep the output and constant of the vector public so the claim can be verified by the verifier.

$$
\mathbf{w} = \begin{pmatrix} 1, 67, h, h, h, h, h \end{pmatrix}
$$

We are using $h$ to denote hidden. The output of 67 is the prover's claim about the computation.

The prover will send the two encrypted witnesses to the verifier, along with their R1CS matrices. This is the proof. This is done in [prover.py](prover.py)

### Verifier Steps


Upon recieving the proof, the verifier will check that the public claim is valid. i.e. that the output of the circuit is 67.

Upon this validation, the verifier will finish encrypting the witness, then compute the matmul and hadamard product of the R1CS matrices with the encrypted witness. 

IMPORTANT: It should be noted that because we are now dealing with eliptic curve points, the matmul is done using elliptic curve point addition and scalar multiplication. The hadamard product is done using bilinear pairings.

If the witness is valid, the equation will still hold due to the group homomorphism between elliptic curve point addition (this includes scalar mul) and and bilinear pairings with integer addition and multiplicaiton. However, due to the discrete log problem, the witness is obfuscated, making this proof zero knowledge.

This is done in [verifier.py](verifier.py)

# Important Note

It should be noted that this proof is not succint, as it requires many elementwise operations. As well, it does not protect against a malicious prover, as the prover could simply lie about the non-public values of the proof by making up values that hold the equality.

# Sources

https://www.rareskills.io/post/bilinear-pairing

https://www.rareskills.io/post/rank-1-constraint-system

https://www.rareskills.io/post/r1cs-zkp
