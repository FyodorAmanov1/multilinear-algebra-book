---
title: "The Cat’s Vanishing Keys"
subtitle: "A few directions that open every door"
slug: "02-spaces"
story-image: "assets/story/02-spaces.png"
story-alt: "Alice studies two keys offered by the Cheshire Cat above a garden of curious doors."
part: "I. A Country of Directions"
demo: "basis-explorer"
summary: "Alice meets the Cheshire Cat and learns why a small, honest keyring can describe an infinite garden."
---

The garden had many doors, and every door had a keyhole shaped like an arrow.

Alice had only one key.

“That will not be enough,” said a voice above her.

A large cat was sitting on a branch, grinning in the way that only very pleased cats can.

“Who are you?” Alice asked.

“A cat,” he said. “But you may call me a keyring, if that makes you feel more mathematical.”

He held up a ring with two keys. One key was short and bright. The other was long and green. Neither looked like every door in the garden.

“How can two keys open infinitely many doors?” Alice asked.

“Because every door is made from copies of these two,” said the cat.

::: {.intuition}
A **basis** is a small collection of honest directions from which every other direction can be built. It is not every arrow in the garden. It is the smallest useful set of arrows that can make all the others.
:::

## The cat builds a garden from two keys

“First tell me what counts as a garden,” Alice insisted. The Cat agreed: a **real vector space** $V$ is a set equipped with vector addition and multiplication by scalars from $\mathbb R$. Adding or scaling its vectors must stay inside $V$. The operations obey the familiar rules: addition is associative and commutative, there is a zero vector and an additive inverse for each vector, and scaling distributes over sums, respects multiplication of scalars, and has $1\mathbf v=\mathbf v$.

For example, $\mathbb R^2$ is a vector space. So is the line $\{(t,2t):t\in\mathbb R\}$, because sums and scaled copies still lie on that line. A line shifted away from the origin fails: it does not even contain the zero vector.

The cat waved his tail, and three arrows appeared:

$$
\mathbf{a}=(1,0),\qquad
\mathbf{b}=(0,1),\qquad
\mathbf{c}=(1,1).
$$

“I can make any point in this garden from the first two,” he said.

Indeed, for any point $(x,y)\in\mathbb R^2$, with real coordinates $x$ and $y$,

$$
(x,y)=x\mathbf{a}+y\mathbf{b}.
$$

“But the third is not needed,” the cat continued. “It is already a combination of the first two:

$$
\mathbf{c}=\mathbf{a}+\mathbf{b}.
$$

So $\mathbf{c}$ is a bit of a fraud.”

![Two non-copy directions generate a whole garden of possible arrows.](assets/figures/ch02-spaces.svg){width=100%}

::: {.intuition}
The **span** of some vectors is everything you can build by adding scaled copies of them. If one vector is already built from the others, it does not add a new direction.
:::

## A key that is secretly a copy

The cat made two arrows vanish and left only

$$
\mathbf{u}=(1,2),\qquad
\mathbf{v}=(2,4).
$$

“Are these independent?” Alice asked.

“No,” said the cat. “One is twice the other. They point along the same line, so the second key opens no new door.”

A finite list $\mathbf v_1,\ldots,\mathbf v_k\in V$ is **linearly independent** when
$$
c_1\mathbf v_1+\cdots+c_k\mathbf v_k=\mathbf0,\quad c_j\in\mathbb R
\quad\Longrightarrow\quad c_1=\cdots=c_k=0.
$$
Equivalently, no vector in the list is a linear combination of the others. It is not enough to check only pairs: $(1,0),(0,1),(1,1)$ have no two parallel vectors, but the third is the sum of the first two. In the plane, a pair is independent precisely when both vectors are nonzero and they do not lie on one line through the origin.

Alice compared the dependent pair with $(1,2)$ and $(-2,1)$. If $a(1,2)+b(-2,1)=(0,0)$, then $a-2b=0$ and $2a+b=0$, forcing $a=b=0$. This pair really does add two directions.

![A dependent pair spans a line; an independent pair spans the plane.](assets/figures/ch02-independence.svg){width=100%}

::: {.intuition}
**Linear independence** means no direction is secretly a copy of another. Each key adds something genuinely new.
:::

## The smallest useful keyring

The cat produced a small ring with two keys.

“This is a basis,” he said.

A basis is:

1. large enough to span the whole space,
2. small enough to contain no redundant keys.

In the plane, any two arrows that do not lie on the same line form a basis. In space, any three arrows that do not lie in one plane form a basis.

::: {.intuition}
A basis is the smallest keyring that still opens every door in the garden.
:::

## Counting dimensions

The cat counted his keys.

“Two,” he said. “So this garden has dimension two.”

Dimension is the number of independent directions you need to describe a point.

- A line has dimension 1.
- A plane has dimension 2.
- Ordinary space has dimension 3.
- A point has dimension 0.

![Zero, one, two, and three independent directions give the familiar dimensions.](assets/figures/ch02-dimensions.svg){width=100%}

::: {.blackboard}
If a space has a basis with $n$ vectors, its dimension is $n$.

Every basis of the same space has the same number of vectors.
:::

## The same point in new words

Alice looked at the point $(3,4)$.

The cat gave her a different keyring:

$$
\mathbf{b}_1=(1,1),\qquad
\mathbf{b}_2=(1,-1).
$$

Now the same point could be written as

$$
(3,4)=\frac{7}{2}\mathbf{b}_1-\frac{1}{2}\mathbf{b}_2.
$$

The point had not moved. Only its address had changed.

Alice checked the address by adding the pieces:
$$
\frac72(1,1)-\frac12(1,-1)=(3,4).
$$
The coefficients $7/2$ and $-1/2$ are real scalars. A basis gives a **unique** list of coefficients for each vector; a redundant spanning list need not. All vector spaces used for bases and component arrays in this book are finite-dimensional unless stated otherwise.


![The vector (3,4) has coordinates (7/2,-1/2) in the diagonal basis.](assets/figures/ch02-basis-change.svg){width=100%}

::: {.intuition}
Coordinates are not the point itself. They are the words you use to describe the point after choosing a basis.
:::

::: {.oxford}
Alice remembered a wrought-iron gate she had once admired: a few curved pieces, repeated and combined, made an enormous pattern. The gate did not need a new piece for every leaf and star; it needed a good alphabet of shapes.
:::

### The same rules over a different field

The Cat placed a small $\mathbb C$ label beside the $\mathbb R$ label. “Choose your scalars before counting keys.” A complex vector space uses complex coefficients in its linear combinations. Independence, span, and dimension are defined using that chosen field.

For example, $\mathbb C$ has dimension one over $\mathbb C$, with basis $\{1\}$. Viewed as a real vector space it has dimension two, with basis $\{1,\mathrm i\}$. These are two different choices of permitted scalars, not contradictory counts.

::: {.demo id="basis-explorer" title="Basis Explorer"}
Move the basis arrows and watch the same point acquire new coordinates.
:::

::: {.trythis}
1. Explain why $(1,2)$ and $(2,4)$ cannot be a basis of the plane.
2. Show that $(1,0)$, $(0,1)$, and $(1,1)$ are linearly dependent.
3. Find a basis for the line $y=2x$.
4. If a space has dimension 5, what is the largest number of independent vectors it can contain?
:::

## Alice’s keyring notes

1. Some directions can be made from others.
2. A basis is a smallest set of genuinely new directions.
3. Dimension is the number of keys on that keyring.

“Now that you have a keyring,” said the cat, “let us see what happens when a machine begins to move the doors.”
