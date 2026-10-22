---
title: "Down the Arrow Hole"
subtitle: "Alice meets journeys that have a direction"
slug: "01-vectors"
story-image: "assets/story/01-vectors.png"
story-alt: "Alice looks up from her book as the White Rabbit hurries through a rainlit library."
part: "I. A Country of Directions"
demo: "vector-playground"
summary: "Alice follows a hurried rabbit into a garden of arrows and discovers why a journey needs more than a number."
---

Alice had been reading in a quiet Oxford library, with rain tapping at the window and a pocket watch ticking somewhere out of sight, when a white rabbit rushed past her table.

“I’m late,” the rabbit said. “I’m terribly, impossibly late.”

Before Alice could ask where, he had disappeared through a narrow door at the end of the room. Alice followed, because that is what curious people do.

On the other side, there were no streets and no spires. There was only a garden filled with arrows. Some stood upright like startled daffodils. Some leaned left like tired sentences. A few pointed straight at Alice as if they had been waiting all afternoon.

“Where am I?” she asked.

“In the country of directions,” said a voice near her ear. “You have just met an arrow that knows where it is going.”

::: {.intuition}
A **vector** is not merely “how much”. It is “how much, and which way”. A number tells you the size of a journey. A vector tells you the journey itself.
:::

## Two journeys with the same length

The rabbit pointed at two arrows on the lawn.

“Both of these have length 3,” he said. “But they are not the same journey.”

One arrow pointed east. The other pointed west. They had the same size, but they meant opposite things.

![Equal lengths do not make opposite journeys the same vector.](assets/figures/ch01-directions.svg){width=100%}

Alice thought of two notes that were equally loud. One said *go to the garden*; the other said *run away from the garden*. Loudness alone did not explain either note.

::: {.intuition}
The first secret of linear algebra is that **length alone is not enough**. Direction carries meaning.
:::

Alice chose east and north as her reference directions. In this chapter the plane is $\mathbb R^2$, the set of pairs of real numbers. A real number can be positive, negative, or zero; examples are $3$, $-1/2$, and $\sqrt 2$. The two coordinates tell how many copies of each reference direction to use.

We write a vector in the plane as a pair of instructions:

$$
\mathbf{v}=
\begin{pmatrix}
3\\
4
\end{pmatrix}.
$$

This does not mean the number thirty-four. It means:

1. go 3 steps sideways,
2. go 4 steps upward.

Its length is

$$
\|\mathbf{v}\|=\sqrt{3^2+4^2}=5.
$$

The number 5 is useful, but it is only the size of the story. It is not the story.

![The vector (3,4) is the diagonal of a right triangle with sides 3 and 4.](assets/figures/ch01-coordinates.svg){width=100%}

## Alice makes one journey from two

Alice found two arrows lying end to end.

“If I follow one and then the other,” she said, “can I replace them by one arrow?”

“Of course,” said the rabbit. “That is called addition.”

Suppose

$$
\mathbf{u}=
\begin{pmatrix}
2\\
1
\end{pmatrix},
\qquad
\mathbf{v}=
\begin{pmatrix}
3\\
4
\end{pmatrix}.
$$

Then

$$
\mathbf{u}+\mathbf{v}=
\begin{pmatrix}
5\\
5
\end{pmatrix}.
$$

![Alice combines two arrow journeys into one.](assets/figures/ch01-vectors.svg){width=100%}

Place the tail of the second arrow at the tip of the first. The sum is the single arrow from the starting point to the finishing point.

::: {.intuition}
Vector addition is like following one set of directions and then another. The total journey is the arrow from where you began to where you ended.
:::

## Stretching without bending

“What if I want to go twice as far?” Alice asked.

“Then multiply the arrow by 2,” said the rabbit.

For any real scalar $c\in\mathbb R$, and a vector $\mathbf v=(v_1,v_2)$ with $v_1,v_2\in\mathbb R$,

$$
c\mathbf{v}=
\begin{pmatrix}
cv_1\\
cv_2
\end{pmatrix}.
$$

If $c>0$, the arrow keeps its direction and changes its length. If $c<0$, it turns around. If $c=0$, it collapses into a point.

Alice tested the rule on $(3,4)$: $2(3,4)=(6,8)$, $-(3,4)=(-3,-4)$, and $0(3,4)=(0,0)$. A **scalar** is a number used for scaling; its allowed number system will always be stated. In these pictures, the scalar is real.


To compare the three cases on a small grid, Alice also tried $\mathbf v=(1,1)$: $2\mathbf v=(2,2)$, $-\mathbf v=(-1,-1)$, and $0\mathbf v=(0,0)$.

![Positive, negative, and zero scalars act differently on the vector (1,1).](assets/figures/ch01-scaling.svg){width=100%}

::: {.intuition}
Scaling stretches, shrinks, or reverses a journey. It does not bend the journey.
:::

At the centre of the garden stood a very small arrow with no length at all.

“Who are you?” Alice asked.

“I am the zero vector,” it said. “I mean: stay exactly where you are.”

We write

$$
\mathbf{0}=
\begin{pmatrix}
0\\
0
\end{pmatrix}.
$$

It has no direction, but it is still a respectable vector, because

$$
\mathbf{v}+\mathbf{0}=\mathbf{v}.
$$

::: {.intuition}
The zero vector is not “nothing”. It is the instruction to do nothing. That instruction becomes surprisingly important later.
:::

::: {.blackboard}
For $\mathbf{v}=(v_1,\dots,v_n)\in\mathbb R^n$, where $n$ is a positive integer and every $v_i\in\mathbb R$, the Euclidean norm in standard coordinates is

$$
\|\mathbf{v}\|=\sqrt{v_1^2+\cdots+v_n^2}.
$$

Addition is coordinate-wise:

$$
\mathbf{u}+\mathbf{v}=(u_1+v_1,\dots,u_n+v_n).
$$

Scaling multiplies every coordinate by the same number.
:::

### A small window onto complex numbers

“Could a coordinate be a stranger sort of number?” Alice asked. Later, yes: a vector in $\mathbb C^n$ has complex coordinates. A complex number is $a+b\,\mathrm i$, with $a,b\in\mathbb R$ and $\mathrm i^2=-1$. Thus $(1+\mathrm i,2)$ belongs to $\mathbb C^2$, while $(3,4)$ belongs to $\mathbb R^2$.

The choice of number system matters. The arrow pictures in this chapter describe real scaling; multiplying by $\mathrm i$ cannot be explained by making that same arrow longer. Complex length also needs a different formula, which Alice will meet with inner products. For now, every unmarked coordinate and scalar is real.

::: {.demo id="vector-playground" title="Vector Playground"}
Drag two arrows and watch their sum, difference, and scaled cousin appear instantly.
:::

::: {.trythis}
1. Draw $(2,3)$ and $(-1,4)$. Add them tip-to-tail, then check your answer with numbers.
2. If $\mathbf{v}=(3,4)$, find $\|2\mathbf{v}\|$ and $\|-\mathbf{v}\|$.
3. Give two everyday instructions that need both a size and a direction.
:::

## Alice’s arrow notes

1. A vector is a direction together with a length.
2. Vectors are added by following one journey after another.
3. Vectors are scaled by stretching, shrinking, or reversing them.

The rabbit vanished again, leaving a small key on the grass.

“A few directions can describe an entire world,” said a voice from nowhere. “But only if they are chosen well.”
