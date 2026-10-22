---
title: "Paths That Refuse to Turn"
subtitle: "Eigenvectors and the directions a machine merely stretches"
slug: "06-eigenvectors"
story-image: "assets/story/06-eigenvectors.png"
story-alt: "Alice and a sleepy Dormouse watch a cloud of arrows inside a teapot-shaped room."
part: "II. The Geometry Machine"
demo: "eigenvector-dance"
summary: "Alice finds the special paths that a transformation stretches but never turns."
---

In a small room shaped like a teapot, the Dormouse was watching a machine move a cloud of arrows.

Most arrows twisted as they moved. They began pointing north-east and ended pointing almost south. The Dormouse yawned.

“Boring,” he said. “Almost all directions turn.”

Alice looked more closely. Two paths did not turn at all. They simply grew longer or shorter while staying on exactly the same line.

“Who are they?” Alice asked.

“The honest ones,” said the Dormouse. “They are not trying to be special. The machine happens to respect their line.”

::: {.intuition}
An **eigenvector** is a direction the transformation respects. The map may change its length, but it does not change its line.
:::

## Stretching without turning

Suppose $A\in\mathbb R^{n\times n}$ acts on a nonzero vector $\mathbf v\in\mathbb R^n$ and, for a real scalar $\lambda\in\mathbb R$, the result is a multiple of $\mathbf v$:

$$
A\mathbf{v}=\lambda\mathbf{v}.
$$

Then $\mathbf{v}$ is an eigenvector, and $\lambda$ is its **eigenvalue**.

The number $\lambda$ says how the direction changes:

- $\lambda>1$: stretched,
- $0<\lambda<1$: shrunk,
- $\lambda<0$: flipped and scaled,
- $\lambda=0$: crushed to zero.

The remaining case $\lambda=1$ leaves the vector unchanged. A negative eigenvalue reverses its orientation but still preserves its line through the origin. Eigenvectors are always nonzero; the zero vector would satisfy the equation for every $\lambda$ and identify no direction.

![Eigenvalues 3, -2, and 0 stretch, reverse and scale, or erase the vector.](assets/figures/ch06-factors.svg){width=100%}

::: {.intuition}
An eigenvalue is a stretching factor attached to a direction that refuses to turn.
:::

## How Alice finds them

Alice wanted to know which vectors satisfied

$$
A\mathbf{v}=\lambda\mathbf{v}.
$$

She rearranged it:

$$
A\mathbf{v}-\lambda\mathbf{v}=\mathbf{0}.
$$

Then

$$
(A-\lambda I)\mathbf{v}=\mathbf{0}.
$$

Here $I$ is the $n\times n$ identity matrix, with ones on its diagonal and zeros elsewhere; $I\mathbf v=\mathbf v$.

For a nonzero solution to exist, the matrix $A-\lambda I$ must squash a direction. Alice remembered the card square:

$$
\det(A-\lambda I)=0.
$$

This equation is the **characteristic equation**.

::: {.blackboard}
The eigenvalues of $A$ are the roots of

$$
\det(A-\lambda I)=0.
$$
:::

![An eigenvector stays on its line, while an ordinary vector changes line under the same matrix.](assets/figures/ch06-eigenvectors.svg){width=100%}

## A concrete dance

Let

$$
A=
\begin{pmatrix}
2 & 1\\
1 & 2
\end{pmatrix}.
$$

Then

$$
\det(A-\lambda I)
=
\det
\begin{pmatrix}
2-\lambda & 1\\
1 & 2-\lambda
\end{pmatrix}
=
(2-\lambda)^2-1.
$$

So

$$
(2-\lambda)^2=1,
$$

giving

$$
\lambda=1,\;3.
$$

The corresponding eigenvectors are

$$
(1,-1)
\quad\text{and}\quad
(1,1).
$$

Alice checked both results directly:
$$
A(1,-1)=(1,-1),\qquad A(1,1)=(3,3)=3(1,1).
$$
These two eigenvectors are orthogonal. For a real symmetric matrix, eigenvectors with distinct eigenvalues are orthogonal; within a repeated-eigenvalue subspace, one can choose an orthonormal basis.

## Choosing the right glasses

The Dormouse handed Alice two spectacles: use $\mathbf b_1=(1,1)$ and $\mathbf b_2=(1,-1)$. In those coordinates the first coefficient triples and the second stays unchanged. More precisely, the basis matrix $P$ has these vectors as its columns, and $P^{-1}AP=\operatorname{diag}(3,1)$.

If a matrix has enough independent eigenvectors, those eigenvectors form a basis. In that basis, the matrix becomes diagonal:

$$
D=
\begin{pmatrix}
\lambda_1 & 0\\
0 & \lambda_2
\end{pmatrix}.
$$

::: {.intuition}
Diagonalization is the art of choosing the right glasses. In ordinary coordinates the map looks complicated. Through eigenvectors, it looks like independent stretching.
:::

![Changing to the eigenvector basis turns the map into independent coordinate stretches.](assets/figures/ch06-diagonalization.svg){width=100%}

::: {.oxford}
The fixed paths reminded Alice of a calm lecture room she had once known: books, chalk, and the same quiet line on the wall while people hurried in and out. Some directions, she thought, are easiest to understand precisely because they stay still.
:::

## Symmetric machines

Alice watched the same matrix act repeatedly on $(1,0)$. Its components along the two eigenvectors began equal, but after $k$ steps the first was multiplied by $3^k$ while the second was multiplied by $1$. Normalizing each result made the direction approach the line of $(1,1)$. This example works because its dominant eigenvalue has strictly greater magnitude and the starting vector has a nonzero component along that eigendirection; repeated action need not always converge.

A matrix is symmetric if

$$
A=A^T.
$$

Symmetric matrices are unusually well-behaved:

- all eigenvalues are real,
- eigenvectors belonging to different eigenvalues are orthogonal,
- they can be diagonalized by an orthogonal matrix.

This fact will become crucial when Alice meets bilinear forms and tensors.

![Normalized iterates of (1,0) approach the eigenline with eigenvalue 3.](assets/figures/ch06-iteration.svg){width=100%}

### When the real garden has no fixed line

A quarter-turn $R=\begin{pmatrix}0&-1\\1&0\end{pmatrix}$ has no real eigenvector. Its characteristic equation is $\lambda^2+1=0$. In $\mathbb C^2$ the eigenvalues are $\mathrm i$ and $-\mathrm i$, with eigenvectors $(1,-\mathrm i)$ and $(1,\mathrm i)$. These complex vectors are not unchanged lines in the real plane.

The complex counterpart of a real symmetric matrix is a **Hermitian** matrix, $A=\overline A^{\,T}$. Hermitian matrices have real eigenvalues and an orthonormal eigenbasis. A merely complex symmetric matrix need not have these properties.

::: {.demo id="eigenvector-dance" title="Eigenvector Dance"}
Watch a matrix act repeatedly on a cloud of vectors. In the illustrated example, normalized directions approach the dominant eigenline.
:::

::: {.trythis}
1. Find the eigenvalues of $\begin{pmatrix}3&0\\0&-2\end{pmatrix}$.
2. Find an eigenvector for each eigenvalue.
3. Explain why the zero vector is not considered an eigenvector.
4. If $A\mathbf{v}=5\mathbf{v}$, what is $A^2\mathbf{v}$?
:::

## Alice’s still-path notes

1. Eigenvectors are directions that do not turn.
2. Eigenvalues are their stretching factors.
3. The characteristic equation finds the values for which a direction can survive.
4. Symmetric machines have especially tidy eigenvectors.

“One arrow at a time is pleasant,” said the Dormouse, “but some rules need two arrows before they say anything at all.”
