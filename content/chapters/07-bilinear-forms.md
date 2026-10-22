---
title: "The Duchess’s Two-Pan Balance"
subtitle: "Bilinear forms and rules that are fair in both hands"
slug: "07-bilinear-forms"
story-image: "assets/story/07-bilinear-forms.png"
story-alt: "Alice watches the Duchess place an arrow in each pan of a kitchen balance."
part: "III. The Multilinear Wilderness"
demo: "bilinear-form-lab"
summary: "Alice discovers a rule that takes two arrows and returns one number while treating each input fairly."
---

The Duchess had a kitchen with too much pepper and a balance scale with two pans.

On the left pan she placed an arrow. On the right pan she placed another arrow. A little card emerged from the middle of the scale with a single number written on it.

“What does the number mean?” Alice asked.

“That depends on the rule,” said the Duchess. “But whatever the rule is, it must be fair.”

“Fair to whom?”

“Fair to each arrow,” said the Duchess. “Double either arrow and the number doubles. Split either arrow into two pieces and the rule splits the answer in the same way.”

::: {.intuition}
A **bilinear form** is a rule that eats two vectors and returns one number. It is linear in the first arrow and linear in the second arrow separately.
:::

## Alice tests the balance

Alice put $\mathbf{u}$ in the left pan and $\mathbf{v}$ in the right. The card showed a number.

Then she replaced $\mathbf{u}$ by $2\mathbf{u}$. The card doubled.

She put $\mathbf{u}$ back, replaced $\mathbf{v}$ by $3\mathbf{v}$, and the card tripled.

Finally she split $\mathbf{u}$ into $\mathbf{u}_1+\mathbf{u}_2$. The card gave the sum of the two answers for $\mathbf{u}_1$ and $\mathbf{u}_2$.

That was exactly the fairness Alice needed.

![A bilinear form is a rule for two arrows, fair when either arrow is doubled.](assets/figures/ch07-bilinear.svg){width=100%}

## The formal rule

The Duchess labelled her inputs carefully: $V$ is a finite-dimensional real vector space, $\mathbf u,\mathbf u',\mathbf v\in V$, and $c\in\mathbb R$. The output is a scalar in the same field.

A map

$$
B:V\times V\to\mathbb{R}
$$

is bilinear if

$$
B(\mathbf{u}+\mathbf{u}',\mathbf{v})
=
B(\mathbf{u},\mathbf{v})+B(\mathbf{u}',\mathbf{v}),
$$

and

$$
B(c\mathbf{u},\mathbf{v})
=
cB(\mathbf{u},\mathbf{v}),
$$

with the same rules in the second argument.

::: {.intuition}
“Bilinear” does not mean “somehow twice as linear”. It means: freeze one arrow, and the rule is linear in the other; then freeze the other, and the same thing happens.
:::

## A familiar guest at the tea table

Alice used the dot product on $(1,2)$ and $(3,4)$. The card read $11$. Doubling the left arrow gave $22$; tripling the right gave $33$; doing both gave $66$, because $B(2\mathbf u,3\mathbf v)=6B(\mathbf u,\mathbf v)$.

The dot product is a bilinear form:

$$
B(\mathbf{u},\mathbf{v})
=
\langle \mathbf{u},\mathbf{v}\rangle.
$$

It is symmetric:

$$
B(\mathbf{u},\mathbf{v})=B(\mathbf{v},\mathbf{u}),
$$

and it satisfies

$$
B(\mathbf{v},\mathbf{v})\ge0.
$$

But not every bilinear form is so friendly.

## The balance has a recipe card

“Show me every multiplication,” Alice asked. For the matrix below, $\mathbf u=(1,2)$ and $\mathbf v=(3,4)$,
$$
A\mathbf v=(11,25),\qquad
B(\mathbf u,\mathbf v)=1\cdot11+2\cdot25=61.
$$
Here $\mathbf u,\mathbf v$ denote column coordinate lists in the chosen basis, $A\in\mathbb R^{n\times n}$, and the transpose symbol $T$ converts a column into a row. Each entry is $A_{ij}=B(\mathbf e_i,\mathbf e_j)$.

Choose a basis. Then every bilinear form on a finite-dimensional space can be represented by a matrix $A$:

$$
B(\mathbf{u},\mathbf{v})
=
\mathbf{u}^T A\mathbf{v}.
$$

For example, if

$$
A=
\begin{pmatrix}
1 & 2\\
3 & 4
\end{pmatrix},
$$

then

$$
B(\mathbf{u},\mathbf{v})
=
\begin{pmatrix}
u_1 & u_2
\end{pmatrix}
\begin{pmatrix}
1 & 2\\
3 & 4
\end{pmatrix}
\begin{pmatrix}
v_1\\
v_2
\end{pmatrix}.
$$

::: {.blackboard}
Every bilinear form on a finite-dimensional vector space can be written as

$$
B(\mathbf{u},\mathbf{v})=\mathbf{u}^TA\mathbf{v}.
$$

Conversely, every matrix defines a bilinear form.
:::

## Symmetric balances

Alice swapped the basis arrows. For $A=\begin{pmatrix}1&2\\3&4\end{pmatrix}$, the cards read $B(\mathbf e_1,\mathbf e_2)=2$ and $B(\mathbf e_2,\mathbf e_1)=3$. The Duchess's fairness did not promise symmetry.

A bilinear form is symmetric if

$$
B(\mathbf{u},\mathbf{v})=B(\mathbf{v},\mathbf{u}).
$$

In matrix terms, this means

$$
A=A^T.
$$

Symmetric forms describe shapes, distances, and energy.

![Linearity in both inputs does not force the rule to be symmetric.](assets/figures/ch07-symmetry.svg){width=100%}

## Curved floors and quadratic forms

Alice put the same arrow in both pans. For $A=\operatorname{diag}(2,1)$ the answer became $q(x,y)=2x^2+y^2$. A level set means all points with the same answer, such as $q=1$; here it is an ellipse. Replacing $A$ by $-A$ makes the form negative definite, and the corresponding ellipse has level $q=-1$.

A symmetric bilinear form determines a quadratic form:

$$
q(\mathbf{v})=B(\mathbf{v},\mathbf{v}).
$$

For a symmetric matrix $A$,

$$
q(\mathbf{x})=\mathbf{x}^TA\mathbf{x}.
$$

The level sets of $q$ can be ellipses, hyperbolas, or degenerate shapes. The eigenvalues of $A$ tell which.

::: {.intuition}
A quadratic form is the shape you feel when you stand at one point of a curved floor. A bilinear form records how that shape responds to two directions at once.
:::

![Positive and negative definite forms have opposite signs and elliptical nonempty levels.](assets/figures/ch07-definite.svg){width=100%}

## Positive, negative, and indefinite

A symmetric form is **positive definite** if

$$
B(\mathbf{v},\mathbf{v})>0
\quad\text{for every }\mathbf{v}\ne\mathbf{0}.
$$

The dot product is positive definite.

A symmetric form is **negative definite** if $q(\mathbf v)<0$ for every nonzero $\mathbf v$. It is **indefinite** only when it takes both positive and negative values.

Alice tried $q(x,y)=2x^2-3y^2$. It gave $q(1,0)=2$ and $q(0,1)=-3$, so it was indefinite. Its nonzero levels are hyperbolas. In contrast, $q(x,y)=x^2$ is positive semidefinite: it never becomes negative, but vanishes on the whole vertical axis. Its matrix is singular, so the form is degenerate. An indefinite form can take zero on nonzero vectors without being degenerate; distinguish zero values from a singular matrix.

![An indefinite form has hyperbolic levels; a degenerate form can have parallel-line levels.](assets/figures/ch07-indefinite.svg){width=100%}

### Complex fairness is not a complex inner product

The Duchess could also use a complex-bilinear form $B:V\times V\to\mathbb C$, with linearity in both complex inputs. But the Hermitian inner product from Chapter 4 is conjugate-linear in one input, so it is **sesquilinear**, not complex-bilinear. Ordinary transpose belongs in a bilinear formula $\mathbf u^T A\mathbf v$; complex inner-product formulas also require conjugation.

::: {.demo id="bilinear-form-lab" title="Bilinear Form Lab"}
Adjust the entries of a symmetric matrix and watch the level curves of the associated quadratic form change from ellipse to hyperbola.
:::

::: {.trythis}
1. Show that $B(\mathbf{u},\mathbf{v})=u_1v_2$ is bilinear.
2. Is it symmetric?
3. Write the matrix of the standard dot product.
4. For $A=\begin{pmatrix}2&0\\0&-3\end{pmatrix}$, describe the shape of $q(x,y)=\mathbf{x}^TA\mathbf{x}$.
:::

## Alice’s balance notes

1. A bilinear form takes two arrows and returns a number.
2. It is linear in each arrow separately.
3. Symmetric forms describe geometry.
4. Quadratic forms show the shape of the rule.

“Pairings are useful,” Alice said, “but can two arrows create something new rather than only a number?”
