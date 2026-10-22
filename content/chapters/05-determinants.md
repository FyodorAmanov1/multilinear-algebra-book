---
title: "The Queen’s Card Square"
subtitle: "Area, orientation, and what happens when space flips"
slug: "05-determinants"
story-image: "assets/story/05-determinants.png"
story-alt: "Alice and the Queen of Hearts examine a tilted square made from playing cards."
part: "II. The Geometry Machine"
demo: "determinant-volume"
summary: "Alice watches a square of cards stretch, flip, and collapse, and discovers the determinant as a signed area."
---

The next room belonged to the Queen of Hearts. Its floor was covered with playing cards, each exactly one step wide and one step tall.

“Paint this square red on one side and blue on the other,” said the Queen. “Then let my machine move it.”

Alice did as she was told. The square slid, tilted, and became a parallelogram. Sometimes it grew. Sometimes it shrank. Once it turned over, and Alice saw the blue side instead of the red one.

“What happened?” she asked.

“Orientation changed,” said the Queen. “Left and right exchanged places.”

::: {.intuition}
The determinant is a **signed area factor**. It tells you how much a linear map stretches area, and whether the journey has been flipped.
:::

## One square becomes a parallelogram

Start with the unit square whose sides are the two basic arrows $\mathbf{e}_1$ and $\mathbf{e}_2$.

A linear map sends them to the columns of a matrix:

$$
A=
\begin{pmatrix}
a & b\\
c & d
\end{pmatrix}.
$$

The entries $a,b,c,d$ are real. The standard basis is $\mathbf e_1=(1,0)$, $\mathbf e_2=(0,1)$, and the column arrows are $T(\mathbf e_1)=(a,c)$ and $T(\mathbf e_2)=(b,d)$. Those two output arrows form a parallelogram. Alice only needed to measure its area and notice which side of the card was showing.

Alice first chose $A=\begin{pmatrix}2&1\\1&3\end{pmatrix}$. Its columns $(2,1)$ and $(1,3)$ enclosed a parallelogram with signed area $2\cdot3-1\cdot1=5$. The ordinary area was $5$. A reflection with matrix $\operatorname{diag}(1,-1)$ kept area $1$ but reversed orientation.

![A determinant records signed area and whether orientation flips.](assets/figures/ch05-determinants.svg){width=100%}

For a $2\times2$ matrix, the signed area is

$$
\det A=ad-bc.
$$

::: {.intuition}
The number $\det A$ is not decoration. It is the area of the moved square, with a minus sign when the card has been turned over.
:::

## Why the sign matters

Alice put the card square back on the floor and gave the machine a new recipe.

- If $\det A>0$, the red side stayed up and the orientation was preserved.
- If $\det A<0$, the blue side appeared and left and right had been exchanged.
- If $\det A=0$, the square collapsed into a line or a point.

The sign is a kind of mathematical memory: it remembers whether the world has been reflected.

## The vanished dimension

The Queen chose two columns that lay on the same line:

$$
\begin{pmatrix}
1 & 2\\
2 & 4
\end{pmatrix}.
$$

Alice calculated

$$
\det A=1\cdot4-2\cdot2=0.
$$

The card square became a thin stick. Its area vanished.

![The columns (1,2) and (2,4) lie on one line, so the determinant is zero.](assets/figures/ch05-collapse.svg){width=100%}

::: {.intuition}
Zero determinant means the map destroys a dimension. The world loses a direction, and information becomes unrecoverable.
:::

## From area to volume

“Try a box,” Alice suggested. Stretching its three coordinate directions by $2$, $3$, and $1$ changes a unit cube into a box of volume $6$. The matrix $\operatorname{diag}(2,3,1)$ has determinant $6$, the product of those factors.

In three dimensions, the determinant is the signed volume of the parallelepiped spanned by the three columns of a matrix.

If $A\in\mathbb R^{n\times n}$ and $S\subseteq\mathbb R^n$ is a bounded measurable region, its ordinary $n$-dimensional volume satisfies

$$
\operatorname{vol}(A(S))=|\det A|\operatorname{vol}(S).
$$

The absolute value gives the stretching factor. The sign gives orientation.

![Stretching a unit cube by diag(2,3,1) multiplies volume by six.](assets/figures/ch05-volume.svg){width=100%}

::: {.blackboard}
For $T:\mathbb{R}^n\to\mathbb{R}^n$ with matrix $A$,

$$
\operatorname{vol}(T(S))
=
|\det A|\operatorname{vol}(S).
$$

The determinant is zero exactly when the columns are linearly dependent.
:::

## Machines in sequence

Suppose one machine stretches area by 2 and another stretches area by 3. If Alice sends the card through the first and then the second, the final area is multiplied by 6.

This is the multiplicativity rule:

$$
\det(AB)=\det A\,\det B.
$$

A square matrix is invertible exactly when $\det A\ne0$. If $A$ stretches volume by 3, then $A^{-1}$ shrinks it by $1/3$:

$$
\det(A^{-1})=\frac{1}{\det A}.
$$

![A horizontal factor of two followed by a vertical factor of three multiplies area by six.](assets/figures/ch05-composition.svg){width=100%}

### Complex determinants carry a different message

The Queen tried to order a complex number to be positive. Alice objected: $\mathbb C$ has no compatible positive-versus-negative ordering. Determinants over $\mathbb C$ still detect invertibility and multiply under composition, but their sign cannot describe a reflection.

For example, multiplication by $\mathrm i$ on $\mathbb C$ has complex determinant $\mathrm i$. On the real plane it is a quarter-turn and preserves area. More generally, a complex-linear matrix $A$ acting on $\mathbb C^n$, viewed as the real space $\mathbb R^{2n}$, multiplies real volume by $|\det_{\mathbb C}A|^2$.

::: {.demo id="determinant-volume" title="Determinant Volume"}
Move the columns of a matrix and watch the unit square turn into a parallelogram. The determinant updates as its signed area.
:::

::: {.trythis}
1. Compute the determinant of $\begin{pmatrix}3&1\\2&4\end{pmatrix}$.
2. Draw the parallelogram spanned by $(2,1)$ and $(1,3)$.
3. Give an example of a matrix with determinant $-1$.
4. If $\det A=5$ and $\det B=2$, what is $\det(AB)$?
:::

## Alice’s card-square notes

1. A determinant is a signed area factor.
2. A negative determinant means orientation has flipped.
3. A zero determinant means a dimension has been lost.
4. Composed machines multiply their factors.

“Some directions survive a transformation without being knocked off their line,” said the Queen. “Those are the ones you must find next.”
