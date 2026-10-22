---
title: "Hints and Answers"
subtitle: "Small helpings, not spoilers"
slug: "answers"
part: "Backmatter"
summary: "Hints and concise answers for every Try This exercise."
---

This section gives a gentle hint first, then a concise answer. Try the problem before reading the answer; the hint is usually enough.

## Chapter 1: Down the Arrow Hole

### Exercise 1

::: {.hint}
Draw both arrows, then move the tail of the second to the tip of the first.
:::

::: {.answer}
$(2,3)+(-1,4)=(1,7)$.
:::

### Exercise 2

::: {.hint}
Scaling multiplies every coordinate, so the length scales by the same positive factor.
:::

::: {.answer}
$\|2\mathbf{v}\|=10$, and $\|-\mathbf{v}\|=5$.
:::

### Exercise 3

::: {.hint}
Look for instructions where “how much” is not enough without “which way”.
:::

::: {.answer}
Examples include a wind speed with direction, a force on a door, a journey from one place to another, or a velocity.
:::

## Chapter 2: The Cat’s Vanishing Keys

### Exercise 1

::: {.hint}
Check whether one vector is a multiple of the other.
:::

::: {.answer}
$(2,4)=2(1,2)$, so the two vectors span only one line, not the whole plane.
:::

### Exercise 2

::: {.hint}
Try to make the third vector from the first two.
:::

::: {.answer}
$(1,1)=1(1,0)+1(0,1)$, so the three vectors are linearly dependent.
:::

### Exercise 3

::: {.hint}
A line through the origin needs one direction that generates it.
:::

::: {.answer}
A basis is $\{(1,2)\}$.
:::

### Exercise 4

::: {.hint}
The dimension is the maximum number of independent directions.
:::

::: {.answer}
At most 5 independent vectors.
:::

## Chapter 3: The Hatter’s Tea Machine

### Exercise 1

::: {.hint}
Check whether the machine sends the zero vector to zero.
:::

::: {.answer}
$T(0,0)=(1,0)\ne(0,0)$, so the map is not linear.
:::

### Exercise 2

::: {.hint}
Find where the basic arrows are sent.
:::

::: {.answer}
The matrix is $\begin{pmatrix}0&-1\\1&0\end{pmatrix}$.
:::

### Exercise 3

::: {.hint}
Every output has equal coordinates.
:::

::: {.answer}
The image is the line $y=x$. The kernel is the line $x+y=0$.
:::

### Exercise 4

::: {.hint}
The plane has dimension 2, and the machine keeps one direction.
:::

::: {.answer}
Rank $=1$ and nullity $=1$.
:::

## Chapter 4: The Caterpillar’s Measuring Tape

### Exercise 1

::: {.hint}
Multiply matching coordinates and add.
:::

::: {.answer}
$2\cdot1+(-1)\cdot4+3\cdot(-2)=-8$.
:::

### Exercise 2

::: {.hint}
Find a vector whose dot product with $(1,2,3)$ is zero.
:::

::: {.answer}
One example is $(-2,1,0)$.
:::

### Exercise 3

::: {.hint}
Project onto the horizontal direction.
:::

::: {.answer}
The projection is $(3,0)$.
:::

### Exercise 4

::: {.hint}
The projection of an arrow onto its own line is the arrow itself.
:::

::: {.answer}
$\operatorname{proj}_{\mathbf{v}}\mathbf{v}=\mathbf{v}$.
:::

## Chapter 5: The Queen’s Card Square

### Exercise 1

::: {.hint}
Use $ad-bc$.
:::

::: {.answer}
$3\cdot4-1\cdot2=10$.
:::

### Exercise 2

::: {.hint}
Use the two vectors as sides of a parallelogram starting at the origin.
:::

::: {.answer}
The vertices are $(0,0)$, $(2,1)$, $(3,4)$, and $(1,3)$.
:::

### Exercise 3

::: {.hint}
A reflection has determinant $-1$.
:::

::: {.answer}
One example is $\begin{pmatrix}1&0\\0&-1\end{pmatrix}$.
:::

### Exercise 4

::: {.hint}
Use $\det(AB)=\det A\det B$.
:::

::: {.answer}
$\det(AB)=10$.
:::

## Chapter 6: Paths That Refuse to Turn

### Exercise 1

::: {.hint}
The matrix is diagonal, so its eigenvalues are on the diagonal.
:::

::: {.answer}
The eigenvalues are $3$ and $-2$.
:::

### Exercise 2

::: {.hint}
For a diagonal matrix, the standard basis vectors work.
:::

::: {.answer}
An eigenvector for $3$ is $(1,0)$; an eigenvector for $-2$ is $(0,1)$.
:::

### Exercise 3

::: {.hint}
An eigenvector must be a nonzero direction.
:::

::: {.answer}
The zero vector satisfies every equation, so it would not identify a special direction.
:::

### Exercise 4

::: {.hint}
Apply $A$ twice.
:::

::: {.answer}
$A^2\mathbf{v}=A(5\mathbf{v})=25\mathbf{v}$.
:::

## Chapter 7: The Duchess’s Two-Pan Balance

### Exercise 1

::: {.hint}
Check linearity in each variable separately.
:::

::: {.answer}
$B((a\mathbf{u}+b\mathbf{u}'),\mathbf{v})=a u_1v_2+b u'_1v_2$, and similarly in the second variable, so it is bilinear.
:::

### Exercise 2

::: {.hint}
Swap the two inputs.
:::

::: {.answer}
No: $u_1v_2$ is generally not equal to $v_1u_2$.
:::

### Exercise 3

::: {.hint}
Use the identity matrix.
:::

::: {.answer}
The matrix is $\begin{pmatrix}1&0\\0&1\end{pmatrix}$.
:::

### Exercise 4

::: {.hint}
Write the quadratic form explicitly.
:::

::: {.answer}
$q(x,y)=2x^2-3y^2$ is indefinite: it takes positive and negative values. Its nonzero level sets are hyperbolas; the zero level is a pair of intersecting lines.
:::

## Chapter 8: The Queen’s Area Tickets

### Exercise 1

::: {.hint}
Use $u_1v_2-u_2v_1$.
:::

::: {.answer}
$(1,2)\wedge(3,4)=1\cdot4-2\cdot3=-2$ times $\mathbf{e}_1\wedge\mathbf{e}_2$.
:::

### Exercise 2

::: {.hint}
The two vectors are multiples.
:::

::: {.answer}
$1\cdot4-2\cdot2=0$.
:::

### Exercise 3

::: {.hint}
Two copies of the same arrow cannot enclose area.
:::

::: {.answer}
The parallelogram collapses to a line, so its signed area is zero.
:::

### Exercise 4

::: {.hint}
The magnitude is the area.
:::

::: {.answer}
The area is 7.
:::

## Chapter 9: The Mock Turtle’s Combination Table

### Exercise 1

::: {.hint}
Multiply the dimensions.
:::

::: {.answer}
$\dim(U\otimes V)=12$.
:::

### Exercise 2

::: {.hint}
Expand all four basis pairings.
:::

::: {.answer}
Using $\mathbf e_i$ for the first factor's basis and $\mathbf f_j$ for the second, it is $3\,\mathbf e_1\otimes\mathbf f_1+4\,\mathbf e_1\otimes\mathbf f_2+6\,\mathbf e_2\otimes\mathbf f_1+8\,\mathbf e_2\otimes\mathbf f_2$.
:::

### Exercise 3

::: {.hint}
Try a sum of two different pure tensors.
:::

::: {.answer}
One example is $\mathbf e_1\otimes\mathbf f_1+\mathbf e_2\otimes\mathbf f_2$. Its coefficient matrix is the identity matrix, which has rank two and cannot be one outer product.
:::

### Exercise 4

::: {.hint}
Use linearity in the second factor.
:::

::: {.answer}
By bilinearity, $\mathbf u\otimes\mathbf0=\mathbf u\otimes(\mathbf0+\mathbf0)=\mathbf u\otimes\mathbf0+\mathbf u\otimes\mathbf0$. Subtracting one copy gives $\mathbf u\otimes\mathbf0=\mathbf0$.
:::

## Chapter 10: Humpty Dumpty’s Word Costumes

### Exercise 1

::: {.hint}
Each covector should read one coordinate.
:::

::: {.answer}
They are $\epsilon^1(x,y)=x$ and $\epsilon^2(x,y)=y$.
:::

### Exercise 2

::: {.hint}
Evaluate the first dual basis covector.
:::

::: {.answer}
$\epsilon^1(\mathbf{v})=3$.
:::

### Exercise 3

::: {.hint}
Components are only a description.
:::

::: {.answer}
The tensor exists independently of coordinates; changing the basis changes only its component array.
:::

### Exercise 4

::: {.hint}
Indices record transformation behaviour.
:::

::: {.answer}
They make it visible whether an object transforms with the basis or with its inverse.
:::

### Exercise 5

::: {.hint}
Use the same diagonal basis as in the chapter; the question's new components are its values on the new basis vectors.
:::

::: {.answer}
The vector has new components $(7/2,-1/2)$ and the covector has new components $(1,3)$. Their pairing is $1(7/2)+3(-1/2)=2$, equal to $2\cdot3-4$ in standard coordinates.
:::

### Exercise 6

::: {.hint}
Multiply matching components, then apply the covector.
:::

::: {.answer}
$S(\mathbf u,\mathbf v)=(6,-1)$ and $\alpha(6,-1)=6-1=5$.
:::

## Chapter 11: The White Rabbit’s Instrument Bag

### Exercise 1

::: {.hint}
A vector gives one direction, but a surface has an orientation and a force may point differently.
:::

::: {.answer}
Stress specifies the traction (force per unit area) for every surface normal. One vector records only one such response.
:::

### Exercise 2

::: {.hint}
Look for a material where spreading is easier in one direction.
:::

::: {.answer}
Examples include wood grain, layered rock, muscle tissue, or fabric.
:::

### Exercise 3

::: {.hint}
Eigenvectors give principal directions; eigenvalues give rates.
:::

::: {.answer}
They give the diffusion rates along the principal directions.
:::

### Exercise 4

::: {.hint}
The metric should give ordinary squared length.
:::

::: {.answer}
The identity gives $ds^2=dx^2+dy^2$, the ordinary Euclidean rule.
:::

### Exercise 5

::: {.hint}
Multiply the normal by the stress matrix; then multiply traction by area to get force.
:::

::: {.answer}
The traction is $(1,3)$ Pa and the force is $(2,6)$ N.
:::

### Exercise 6

::: {.hint}
The squared metric length is $4x^2+y^2$.
:::

::: {.answer}
The squared length is $4\cdot1^2+2^2=8$, so the length is $2\sqrt2$.
:::

## Chapter 12: Alice’s Dream Map

### Exercise 1

::: {.hint}
Use the signed-area formula.
:::

::: {.answer}
The value is $1\cdot1-0\cdot0=1$.
:::

### Exercise 2

::: {.hint}
Swapping the two inputs changes the sign.
:::

::: {.answer}
The value is $-1$.
:::

### Exercise 3

::: {.hint}
A $k$-form needs $k$ independent directions.
:::

::: {.answer}
Three tangent vectors in the plane are linearly dependent, so every alternating three-input rule vanishes. The zero 3-form exists; every 3-form on the plane is zero.
:::

### Exercise 4

::: {.hint}
Forms are designed for oriented measurement and integration.
:::

::: {.answer}
They let one language describe work along paths, flux through surfaces, and volume in regions.
:::

### Exercise 5

::: {.hint}
Differentiate the two coefficient functions and evaluate the resulting covector on the direction.
:::

::: {.answer}
$df=2x\,dx+2y\,dy$. At $(1,2)$ this is $2\,dx+4\,dy$, whose value on $(3,-1)$ is $6-4=2$.
:::

### Exercise 6

::: {.hint}
Reversing orientation reverses the sign of an integral.
:::

::: {.answer}
The clockwise boundary integral is $-1$. Give the square the negative of the standard orientation; its induced boundary orientation is then clockwise, and $\int_M dx\wedge dy=-1$.
:::
