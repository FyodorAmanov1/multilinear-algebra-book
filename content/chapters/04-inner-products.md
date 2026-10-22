---
title: "The Caterpillar’s Measuring Tape"
subtitle: "Length, angle, and the shadow of one arrow on another"
slug: "04-inner-products"
story-image: "assets/story/04-inner-products.png"
story-alt: "Alice holds two arrows while the Caterpillar offers a luminous measuring tape from his mushroom."
part: "II. The Geometry Machine"
demo: "inner-product-lab"
summary: "Alice learns that comparing arrows requires a fair rule for length and angle."
---

The next room was shaped like a long blue smoke ring. In the middle of it sat a Caterpillar on a mushroom, holding a measuring tape that appeared to be made of moonlight.

“Who are you?” asked the Caterpillar.

“I am Alice,” said Alice. “But I am not sure how long I am today.”

“Then you need a rule,” said the Caterpillar, “not merely a ruler.”

Alice held up two arrows. One pointed almost upward. One leaned sideways. She wanted to say whether they agreed, disagreed, or stood at right angles, but she did not yet have a way to compare them.

::: {.intuition}
An **inner product** is a rule that takes two arrows and returns a single number. That number quietly knows about length and angle.
:::

## First, how long is one arrow?

The Caterpillar laid the measuring tape beside an arrow.

For a real vector in standard Euclidean coordinates,

$$
\mathbf{v}=(v_1,\dots,v_n)\in\mathbb R^n,
$$

the ordinary length is

$$
\|\mathbf{v}\|
=
\sqrt{v_1^2+\cdots+v_n^2}.
$$

In the plane, this is Pythagoras:

$$
\|(x,y)\|=\sqrt{x^2+y^2}.
$$

Alice divided $(3,4)$ by its length $5$ to get $(3/5,4/5)$. This new arrow has length one. All unit arrows in the Euclidean plane lie on the unit circle $x^2+y^2=1$. In a general vector space, length requires a chosen inner product; the sum-of-squares formula assumes an orthonormal coordinate basis.

![Normalizing (3,4) produces the unit vector (3/5,4/5).](assets/figures/ch04-length.svg){width=100%}

::: {.intuition}
Length is not a new kind of object. It is a number you can compute from an arrow once you have agreed how to measure it.
:::

## A conversation between two arrows

The Caterpillar blew a smoke ring and said:

“Take two arrows. Multiply their matching pieces and add the results.”

For

$$
\mathbf{u}=(u_1,\dots,u_n),
\qquad
\mathbf{v}=(v_1,\dots,v_n),
$$

the dot product is

$$
\langle \mathbf{u},\mathbf{v}\rangle
=
u_1v_1+\cdots+u_nv_n.
$$

For example,

$$
\langle(1,2),(3,4)\rangle
=
1\cdot3+2\cdot4
=11.
$$

The answer is a number, not a vector.

“What does 11 mean?” Alice asked.

“By itself, not very much,” said the Caterpillar. “But if you also know the lengths, it tells you the angle.”

If neither arrow is zero, then

$$
\langle \mathbf{u},\mathbf{v}\rangle
=
\|\mathbf{u}\|\,\|\mathbf{v}\|\cos\theta.
$$

So

$$
\cos\theta
=
\frac{\langle \mathbf{u},\mathbf{v}\rangle}
{\|\mathbf{u}\|\,\|\mathbf{v}\|}.
$$

::: {.intuition}
The dot product is like a conversation between two arrows. If it is positive, they are leaning towards each other. If it is zero, they are standing at right angles. If it is negative, they are leaning away.
:::

## When arrows agree to disagree

Alice kept $\mathbf u=(1,0)$ fixed and tried $\mathbf v=(1,1)$, $(0,1)$, and $(-1,1)$. The answers were $1$, $0$, and $-1$. The Caterpillar's number distinguished an acute, right, and obtuse angle without drawing a protractor.

Two arrows are **orthogonal** when

$$
\langle \mathbf{u},\mathbf{v}\rangle=0.
$$

In ordinary geometry, this means they are perpendicular.

::: {.intuition}
Orthogonality is the cleanest way for two directions to be independent without fighting for the same line.
:::

![Positive, zero, and negative dot products distinguish the three kinds of angle.](assets/figures/ch04-dot-signs.svg){width=100%}

## Alice finds a shadow

The Caterpillar held one arrow in the sunlight and let its shadow fall on another.

“That shadow,” he said, “is a projection.”

For $\mathbf u,\mathbf v\in V$ and $\mathbf v\ne\mathbf0$, the projection of $\mathbf{u}$ onto the line spanned by $\mathbf{v}$ is

$$
\operatorname{proj}_{\mathbf{v}}\mathbf{u}
=
\frac{\langle \mathbf{u},\mathbf{v}\rangle}
{\|\mathbf{v}\|^2}
\mathbf{v}.
$$

It is the part of $\mathbf{u}$ that points in the direction of $\mathbf{v}$.

Alice projected $\mathbf u=(3,4)$ onto $\mathbf v=(1,0)$. The scalar multiplier was $3/1=3$, so the projection was $(3,0)$. The residual $\mathbf u-\operatorname{proj}_{\mathbf v}\mathbf u=(0,4)$ is perpendicular to $\mathbf v$. A zero target vector is excluded because the displayed denominator would be zero.

![A projection is the shadow one arrow casts on another.](assets/figures/ch04-inner-products.svg){width=100%}

::: {.intuition}
Projection separates an arrow into a component along a chosen line and a residual perpendicular to that line.
:::

## Rulers that do not argue

Alice chose $\mathbf b_1=(2,0)$ and $\mathbf b_2=(0,1)$. These basis vectors are perpendicular but do not have the same length. For $\mathbf v=(3,4)$, the formula gives $c_1=6/4=3/2$ and $c_2=4/1=4$. She needed one and a half copies of the first ruler, not three.

The Caterpillar laid three arrows on the mushroom so that each touched the others only at the tail.

“These are an orthogonal basis,” he said.

If

$$
\langle \mathbf{b}_i,\mathbf{b}_j\rangle=0
\quad\text{for }i\ne j,
$$

then finding coordinates becomes easy:

$$
c_i=
\frac{\langle \mathbf{v},\mathbf{b}_i\rangle}
{\|\mathbf{b}_i\|^2}.
$$

::: {.intuition}
An orthogonal basis is like a set of rulers that do not interfere with one another.
:::

![An orthogonal basis need not be normalized: (3,4)=1.5b1+4b2.](assets/figures/ch04-orthogonal.svg){width=100%}

::: {.blackboard}
A real inner product on $V$ is a function

$$
\langle\cdot,\cdot\rangle:V\times V\to\mathbb{R}
$$

such that, for $\mathbf u,\mathbf v,\mathbf w\in V$ and $a,b\in\mathbb R$:

- $\langle \mathbf{u},\mathbf{v}\rangle=\langle \mathbf{v},\mathbf{u}\rangle$,
- $\langle a\mathbf{u}+b\mathbf{w},\mathbf{v}\rangle
 =a\langle \mathbf{u},\mathbf{v}\rangle+b\langle \mathbf{w},\mathbf{v}\rangle$,
- $\langle \mathbf{v},\mathbf{v}\rangle\ge0$,
- $\langle \mathbf{v},\mathbf{v}\rangle=0$ only when $\mathbf{v}=\mathbf{0}$.
:::

### Complex measuring tapes

In a marked complex example the coordinates are $u_j,v_j\in\mathbb C$. We use the convention
$$
\langle\mathbf u,\mathbf v\rangle=\sum_{j=1}^n u_j\overline{v_j},
\qquad
\|\mathbf v\|=\sqrt{\sum_{j=1}^n|v_j|^2}.
$$
The bar means complex conjugation: $\overline{a+b\mathrm i}=a-b\mathrm i$, and $|z|^2=z\overline z$. For $\mathbf v=(1+\mathrm i,2)$, the squared norm is $2+4=6$.

The Caterpillar warned Alice to inspect the convention: our inner product is linear in its first input and conjugate-linear in its second. It has conjugate symmetry rather than ordinary symmetry. The real angle formula above describes real arrows; a general complex inner product is not a real cosine. Orthogonality still means the inner product is zero.

::: {.demo id="inner-product-lab" title="Inner Product Lab"}
Move two arrows, watch their dot product and angle change, and see orthogonality happen when the dot product reaches zero.
:::

::: {.trythis}
1. Compute $\langle(2,-1,3),(1,4,-2)\rangle$.
2. Find a vector orthogonal to $(1,2,3)$.
3. Project $(3,4)$ onto $(1,0)$.
4. If $\mathbf{v}\ne\mathbf{0}$, what is $\operatorname{proj}_{\mathbf{v}}\mathbf{v}$?
:::

## Alice’s measuring notes

1. An inner product gives a fair way to compare two arrows.
2. Dot products measure agreement.
3. Orthogonality means the conversation gives zero.
4. Projections are shadows.

“Now,” said the Caterpillar, “you can measure one arrow. Next, ask how much space a whole machine can move.”
