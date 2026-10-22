---
title: "The Hatter’s Tea Machine"
subtitle: "What a fair machine can make and what it forgets"
slug: "03-linear-maps"
story-image: "assets/story/03-linear-maps.png"
story-alt: "Alice watches the Mad Hatter feed an arrow into his elaborate brass tea machine."
part: "II. The Geometry Machine"
demo: "linear-map-theater"
summary: "Alice discovers the image and kernel by watching a machine make, lose, and repeat journeys."
---

The Mad Hatter lived in a shed at the edge of the garden, and inside the shed was a very large brass machine.

It had a funnel on one side, a row of levers in the middle, and a spout on the other.

“What does it do?” Alice asked.

“It turns arrows into arrows,” said the Hatter, adjusting his hat.

“That sounds useless.”

“It is not useless,” said the Hatter. “It is the whole point.”

He poured an arrow into the funnel. A different arrow came out. Then he poured in two arrows at once, and the machine behaved in a surprisingly fair way.

::: {.intuition}
A **linear map** is a machine that takes a vector and gives back another vector, while being fair about two things:

1. If you put in two journeys, it respects putting them together.
2. If you stretch a journey, it stretches the result in the same way.
:::

## The fairness rules

Alice labelled the funnel $V$ and the spout $W$. A linear map $T:V\to W$ acts between real vector spaces, and the two spaces may have different dimensions. Here $\mathbf u,\mathbf v\in V$ and the scalar $c\in\mathbb R$; the results lie in $W$.

The Hatter wrote the rule on a small card:

$$
T(\mathbf{u}+\mathbf{v})=T(\mathbf{u})+T(\mathbf{v}),
\qquad
T(c\mathbf{v})=cT(\mathbf{v}).
$$

Alice read it twice.

“That means, if I follow one journey and then another, the machine treats them as two separate trips and then joins the answers?”

“Exactly,” said the Hatter. “And if I make the journey twice as long, the answer becomes twice as long.”

That is what **linear** means. It is not a straight line in the ordinary sense. It is a machine that does not cheat when you combine or scale your inputs.

## A recipe card, not the machine itself

The Hatter handed Alice a card with four numbers:

$$
A=
\begin{pmatrix}
a & b\\
c & d
\end{pmatrix}.
$$

“Is that the machine?” Alice asked.

“No,” said the Hatter. “That is the recipe card.”

A matrix records where the machine sends two special arrows:

$$
\mathbf{e}_1=
\begin{pmatrix}
1\\
0
\end{pmatrix},
\qquad
\mathbf{e}_2=
\begin{pmatrix}
0\\
1
\end{pmatrix}.
$$

If

$$
T(\mathbf{e}_1)=
\begin{pmatrix}
a\\
c
\end{pmatrix},
\qquad
T(\mathbf{e}_2)=
\begin{pmatrix}
b\\
d
\end{pmatrix},
$$

then the columns of the matrix are the answers for the two basic arrows.

::: {.intuition}
A matrix is not just a grid of numbers. It is a **recipe card** saying: “Here is what the machine does to each basic ingredient.”
:::

Once you know those two answers, you know the whole machine, because every other vector is made from them.

For a map $\mathbb R^n\to\mathbb R^m$, its matrix has $m$ rows and $n$ columns with real entries. In the plane, Alice tried
$$
A=\begin{pmatrix}2&1\\1&2\end{pmatrix},\qquad
A\begin{pmatrix}2\\1\end{pmatrix}
=\begin{pmatrix}2\cdot2+1\cdot1\\1\cdot2+2\cdot1\end{pmatrix}
=\begin{pmatrix}5\\4\end{pmatrix}.
$$
She could compute this because $T(2\mathbf e_1+\mathbf e_2)=2T(\mathbf e_1)+T(\mathbf e_2)$.


![The two columns of A are T(e1) and T(e2), so they determine every output.](assets/figures/ch03-columns.svg){width=100%}

## Alice finds the wall of possible results

The Hatter set one lever, and the machine became a flattener. Whatever Alice put in, the output lay on the horizontal floor.

She asked for a diagonal arrow.

“I cannot make that,” said the machine.

She asked for a vertical arrow.

“I can make only its shadow.”

Alice watched every possible output and noticed that they all lived on one line. Some arrows could be made; some could not.

::: {.intuition}
The **image** is the wall of outputs the machine can actually make. It is not a promise about everything Alice might want. It is the collection of things the machine can truly produce.
:::

Only after Alice had watched the wall did the Hatter write:

$$
\operatorname{im} T=\{T(\mathbf{v}):\mathbf{v}\in V\}.
$$

If the machine is powerful, its image may be the whole plane. If it is a flattener, its image may be only a line. If it is perfectly useless, its image may be a single point.

## The corridor of forgotten journeys

Alice tried another experiment. She put in a vertical journey.

Nothing came out.

“Where did it go?” she asked.

“Nowhere,” said the Hatter. “That arrow was in the corridor the machine forgets.”

She tried a vertical arrow twice as tall. Still nothing. She tried a vertical arrow pointing downward. Still nothing. Every arrow in that vertical corridor vanished.

::: {.intuition}
The **kernel** is the corridor of forgotten journeys: all the inputs that the machine sends to zero.
:::

Only after Alice had seen the corridor did the Hatter write:

$$
\ker T=\{\mathbf{v}\in V:T(\mathbf{v})=\mathbf{0}_W\}.
$$

If the kernel is only the zero vector, the machine loses nothing. If the kernel is larger, some journeys are erased completely.

![The tea machine shows Alice the wall of outputs and the corridor of forgotten journeys.](assets/figures/ch03-maps.svg){width=100%}

## Two directions, counted honestly

For the flattening machine

$$
P(x,y)=(x,0),
$$

Alice made a small table:

| Machine’s behaviour | Meaning | Dimension |
|---|---|---|
| It can make all horizontal arrows | image | 1 |
| It forgets all vertical arrows | kernel | 1 |

The garden she started with had dimension 2. So

$$
\dim(\operatorname{im}P)+\dim(\ker P)=1+1=2.
$$

The Hatter called the first number the **rank** and the second number the **nullity**.

::: {.blackboard}
For a linear map $T:V\to W$ with finite-dimensional $V$,

$$
\operatorname{rank}T+\operatorname{nullity}T=\dim V.
$$

Rank counts the directions the machine can still speak about. Nullity counts the directions it ignores.
:::

## Famous machines

### Rotation

The Hatter turned a lever labelled $\theta\in\mathbb R$. Alice watched $(2,0)$ rotate counterclockwise by $60^\circ$ to $(1,\sqrt3)$. Here $\theta$ is an angle; use radians when evaluating trigonometric functions without a degree sign.

A rotation by angle $\theta$ sends

$$
\mathbf{e}_1\mapsto(\cos\theta,\sin\theta),
\qquad
\mathbf{e}_2\mapsto(-\sin\theta,\cos\theta).
$$

Its matrix is

$$
\begin{pmatrix}
\cos\theta & -\sin\theta\\
\sin\theta & \cos\theta
\end{pmatrix}.
$$

Nothing is forgotten: the kernel contains only $\mathbf{0}$.

![A 60-degree rotation preserves length while changing direction; the arc shows the angle.](assets/figures/ch03-rotation.svg){width=100%}

### Reflection

Reflection in the horizontal axis sends $(x,y)$ to $(x,-y)$:

$$
\begin{pmatrix}
1 & 0\\
0 & -1
\end{pmatrix}.
$$

The image is still the whole plane. The kernel is still only $\mathbf{0}$.

Alice held a card above the floor: $(2,1)$ became $(2,-1)$. The horizontal coordinate stayed fixed, the vertical coordinate changed sign, and applying the reflection a second time restored the card.

![Reflection sends the arrow and square across the horizontal axis.](assets/figures/ch03-reflection.svg){width=100%}

### Shear

“What if each row slides by a different amount?” Alice asked. The Hatter set the real parameter $k=1$. Then the rule is $(x,y)\mapsto(x+y,y)$, so $(2,1)$ becomes $(3,1)$ while every point with $y=0$ stays put.

A shear tilts the plane sideways:

$$
\begin{pmatrix}
1 & k\\
0 & 1
\end{pmatrix}.
$$

![A shear with k=1 turns the square into a parallelogram without changing its area.](assets/figures/ch03-shear.svg){width=100%}

### Projection

A projection onto the horizontal axis sends $(x,y)$ to $(x,0)$:

$$
\begin{pmatrix}
1 & 0\\
0 & 0
\end{pmatrix}.
$$

This is the forgetful machine Alice met first.

Alice sent the same square through it. Both upper corners landed on the floor, giving only a segment. Two different inputs, such as $(2,1)$ and $(2,7)$, now have the same output $(2,0)$; their difference $(0,-6)$ lies in the kernel.

![Projection sends (2,1) to (2,0) and collapses the unit square to a segment.](assets/figures/ch03-projection.svg){width=100%}

::: {.demo id="linear-map-theater" title="Linear Map Theater"}
Move the levers and watch the whole plane transform. Lines map to lines or points; the origin stays fixed. A singular map can collapse directions, as projection does.
:::

::: {.trythis}
1. Explain why $T(x,y)=(x+1,y)$ is not linear.
2. Write the matrix for a $90^\circ$ counterclockwise rotation.
3. Find the image and kernel of $(x,y)\mapsto(x+y,x+y)$.
4. If a machine forgets exactly the vertical direction, what are its rank and nullity in the plane?
:::

## Alice’s machine notes

1. A linear map is a fair machine: it respects addition and scaling.
2. A matrix is the recipe card for what the machine does to a basis.
3. The image is the wall of outputs the machine can make.
4. The kernel is the corridor of inputs the machine forgets.

“A machine is well and good,” said Alice, “but how do I know how long an arrow is?”

“Ah,” said the Hatter, “that is the next room.”
