---
title: "The Queen’s Area Tickets"
subtitle: "Wedge products, orientation, and objects made from two arrows"
slug: "08-wedge-products"
story-image: "assets/story/08-wedge-products.png"
story-alt: "Alice receives an area ticket from a heart-card soldier in the Queen's corridor."
part: "III. The Multilinear Wilderness"
demo: "wedge-areas"
summary: "Alice discovers that a pair of arrows can create an oriented area ticket rather than another ordinary arrow."
---

In the next corridor, card soldiers were carrying small pieces of paper. Each ticket had two arrows painted on it and a signed number in the corner.

“What are they?” Alice asked.

“Area tickets,” said a card soldier. “Two arrows describe a parallelogram. The ticket records its area and which way the arrows are travelling.”

Alice took one ticket. The two arrows were red and green. When she swapped their order, the number changed from $+5$ to $-5$.

“Did the area change?” she asked.

“No,” said the soldier. “Only the direction of travel changed.”

::: {.intuition}
The wedge product $\mathbf{u}\wedge\mathbf{v}$ is not another arrow in the original space. It is an **area object**: its magnitude is the area of the parallelogram spanned by $\mathbf{u}$ and $\mathbf{v}$, and its sign records orientation.
:::

## Alice measures the patch

Let the two vectors lie in $\mathbb R^2$, with all four coordinates real:

$$
\mathbf{u}=(u_1,u_2),
\qquad
\mathbf{v}=(v_1,v_2).
$$

The signed area of the parallelogram they span is

$$
u_1v_2-u_2v_1.
$$

In wedge language,

$$
\mathbf{u}\wedge\mathbf{v}
=
(u_1v_2-u_2v_1)\,\mathbf{e}_1\wedge\mathbf{e}_2.
$$

Alice tried $\mathbf u=(2,1)$ and $\mathbf v=(1,3)$. The coefficient was $2\cdot3-1\cdot1=5$, so $\mathbf u\wedge\mathbf v=5\,\mathbf e_1\wedge\mathbf e_2$. Swapping them gives $-5$ times that basis area object. The coefficient is a real number; the wedge itself belongs to the new vector space $\Lambda^2(\mathbb R^2)$, not to $\mathbb R^2$.

![Swapping the arrows changes the sign of the area ticket.](assets/figures/ch08-wedge.svg){width=100%}

::: {.intuition}
A wedge product is a determinant in disguise. It remembers the orientation of a little patch of space.
:::

## Why order matters

Alice swapped the arrows again:

$$
\mathbf{u}\wedge\mathbf{v}
=
-\mathbf{v}\wedge\mathbf{u}.
$$

This is called antisymmetry. It is not a defect; it is orientation doing its job.

If Alice used the same arrow twice:

$$
\mathbf{u}\wedge\mathbf{u}=0.
$$

The two copies could not enclose any area at all.

She also tried $\mathbf u=(1,2)$ and $\mathbf v=(2,4)$. Their coefficient was $1\cdot4-2\cdot2=0$. Parallel vectors give the zero element of the area space, even when both vectors are nonzero.

![Parallel vectors span no area: (1,2) wedge (2,4) is zero.](assets/figures/ch08-collapse.svg){width=100%}

::: {.intuition}
Swapping the order reverses the journey around the parallelogram. Repeating the same arrow gives no patch to measure.
:::

## A familiar but limited relative

“Why draw a perpendicular arrow for something flat?” Alice asked. In oriented Euclidean three-space, the cross product encodes an oriented patch as its normal vector. This identification uses both a measuring rule and a choice of orientation. For $(2,0,0)$ and $(0,1,0)$, the patch has area $2$ and the cross product is $(0,0,2)$.

In three dimensions, the cross product $\mathbf{u}\times\mathbf{v}$ is another vector whose length is

$$
\|\mathbf{u}\times\mathbf{v}\|
=
\|\mathbf{u}\|\|\mathbf{v}\|\sin\theta.
$$

That length is exactly the area of the parallelogram.

But the cross product is a little too magical: it depends on a perpendicular direction that is special to three dimensions. In other dimensions, there may not be a unique perpendicular arrow with the correct length.

The wedge product is the honest generalization:

$$
\|\mathbf{u}\wedge\mathbf{v}\|
=
\|\mathbf{u}\times\mathbf{v}\|
\quad\text{in }\mathbb{R}^3.
$$

::: {.blackboard}
For vectors in $\mathbb{R}^3$,

$$
\|\mathbf{u}\times\mathbf{v}\|
=
\|\mathbf{u}\wedge\mathbf{v}\|.
$$

The cross product adds a choice of perpendicular direction. The wedge product keeps only the oriented area.
:::

![The wedge is an oriented patch; the cross product is its normal-vector encoding in oriented Euclidean 3-space.](assets/figures/ch08-cross-product.svg){width=100%}

## Volume and higher patches

Alice chose $(2,0,0)$, $(0,1,0)$, and $(0,0,3)$. Their wedge is $6\,\mathbf e_1\wedge\mathbf e_2\wedge\mathbf e_3$, an oriented volume object in $\Lambda^3(\mathbb R^3)$.

Three vectors can span a parallelepiped:

$$
\mathbf{u}\wedge\mathbf{v}\wedge\mathbf{w}.
$$

This represents their oriented volume.

In higher dimensions, a **simple** $k$-vector $\mathbf v_1\wedge\cdots\wedge\mathbf v_k$ represents an oriented $k$-dimensional parallelepiped. A general element of $\Lambda^k(V)$ is a sum of such objects and need not represent one single patch. The pattern continues:

- 1-vector: length,
- 2-vector: area,
- 3-vector: volume.

![Three coordinate directions with lengths 2, 1, and 3 span volume 6.](assets/figures/ch08-volume.svg){width=100%}

## The exterior algebra

The soldier labelled separate drawers for scalars, arrows, area objects, and volume objects. If $\dim V=n$, then $\Lambda^k(V)=\{0\}$ for $k>n$. The symbol $\oplus$ says that elements keep their degrees in separate compartments; adding an arrow to an area object does not turn the result into an ordinary arrow.

The collection of all wedge products forms a larger algebra:

$$
\Lambda(V)
=
\Lambda^0(V)\oplus\Lambda^1(V)\oplus\Lambda^2(V)\oplus\cdots.
$$

Here:

- $\Lambda^0(V)$ contains scalars,
- $\Lambda^1(V)$ contains ordinary vectors,
- $\Lambda^2(V)$ contains area objects,
- $\Lambda^3(V)$ contains volume objects.

::: {.intuition}
Exterior algebra gives every size of patch a proper home. Lengths, areas, and volumes are no longer forced to pretend they are all the same kind of arrow.
:::

### Which part depends on the field?

Wedges can be defined over $\mathbb C$ too, with complex coefficients and the same distributive and antisymmetric rules. The pictures of signed real areas in this chapter use a real oriented space. Over $\mathbb C$, a coefficient can have a complex phase, so its sign alone cannot describe that real picture. Even over $\mathbb R$, the *magnitude* of a wedge requires a chosen inner product; the exterior product itself does not.

::: {.demo id="wedge-areas" title="Wedge Areas"}
Move two vectors and watch the oriented parallelogram they span. Reverse their order and see the sign flip.
:::

::: {.trythis}
1. Compute $(1,2)\wedge(3,4)$.
2. Show that $(1,2)\wedge(2,4)=0$.
3. Explain geometrically why $\mathbf{u}\wedge\mathbf{u}=0$.
4. If $\mathbf{u}\wedge\mathbf{v}$ has magnitude 7, what is the area of the parallelogram they span?
:::

## Alice’s area-ticket notes

1. A wedge product represents oriented area or volume.
2. Swapping arrows changes the sign.
3. Repeating an arrow gives zero.
4. Wedges generalize determinants to patches of every dimension.

“Two arrows can make an area ticket,” said the card soldier. “Two spaces can make an even stranger room.”
