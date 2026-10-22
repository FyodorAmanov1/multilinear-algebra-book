---
title: "Humpty Dumpty’s Word Costumes"
subtitle: "Components, covectors, and changing the language without changing the object"
slug: "10-components"
story-image: "assets/story/10-components.png"
story-alt: "Alice watches Humpty Dumpty arrange two costumes for the same little toy soldier."
part: "III. The Multilinear Wilderness"
demo: "component-transformer"
summary: "Alice learns why a tensor can keep its meaning while its components change costume."
---

Humpty Dumpty was sitting on a high shelf, arranging costumes on the same toy soldier.

“The soldier has not moved,” he said. “Its description has changed.”

Alice laid her arrow beside it. “Then show me a change of description that I can check.”

Humpty agreed to work in a finite-dimensional **real** vector space $V$, with $\dim V=n$. Every component in the main chapter is a real scalar. A basis supplies a language for describing objects; it does not create the objects.

::: {.intuition}
The object is the soldier; its components are the costume. A change of basis changes the description while preserving the object and the answers it gives.
:::

## Alice changes the keyring

Alice's vector was $\mathbf v=3\mathbf e_1+4\mathbf e_2$ in $\mathbb R^2$, with $\mathbf e_1=(1,0)$ and $\mathbf e_2=(0,1)$. Humpty supplied another basis:
$$
\mathbf b_1=(1,1),\qquad \mathbf b_2=(1,-1).
$$
If $\mathbf v=c_1\mathbf b_1+c_2\mathbf b_2$, comparing its two standard coordinates gives $c_1+c_2=3$ and $c_1-c_2=4$. Adding the equations gives $2c_1=7$, so
$$
\mathbf v=\frac72\mathbf b_1-\frac12\mathbf b_2.
$$
The coefficient list changed from $(3,4)$ to $(7/2,-1/2)$. Alice checked that $(7/2,7/2)+(-1/2,1/2)=(3,4)$.

![The same vector has standard coordinates (3,4) and diagonal-basis coordinates (7/2,-1/2).](assets/figures/ch10-components.svg){width=100%}

::: {.intuition}
Coordinates are coefficients relative to a specified basis. Writing a column of numbers without naming that basis can hide what the column describes.
:::

## Questions that eat arrows

Humpty placed a question beside the arrow: “Take twice the horizontal coordinate and subtract the vertical coordinate.” This is the covector
$$
\alpha:\mathbb R^2\to\mathbb R,\qquad \alpha(x,y)=2x-y.
$$
Alice tried $(3,4)$ and obtained $2$. Doubling the input doubled the answer; adding two inputs added their answers.

A **covector** on $V$ is a linear map $V\to\mathbb R$. All covectors form the **dual space**
$$
V^*=\{\alpha:V\to\mathbb R\mid \alpha\text{ is linear}\}.
$$
The stars name a new vector space; they do not mean complex conjugation. A covector asks a linear question of a vector. No length or perpendicular direction is required to define that question.

![The covector alpha(x,y)=2x-y assigns constant values to parallel lines.](assets/figures/ch10-covector.svg){width=100%}

The line $\alpha=2$ is the set of endpoints giving answer $2$. The parallel line $\alpha=0$ is the kernel of this covector. Alice could now see a measuring rule, rather than just another arrow.

## One question for each key

Alice wanted questions that read individual coefficients. For a basis $\mathbf e_1,\ldots,\mathbf e_n$ of $V$, the **dual basis** $\epsilon^1,\ldots,\epsilon^n$ of $V^*$ satisfies
$$
\epsilon^i(\mathbf e_j)=\delta^i{}_j,\qquad 1\le i,j\le n.
$$
The symbol $\delta^i{}_j$ is $1$ when $i=j$ and $0$ otherwise. Thus the first question answers “one” on the first key and “zero” on all other keys.

In standard coordinates, $\epsilon^1(x,y)=x$ and $\epsilon^2(x,y)=y$. For the diagonal basis, the dual questions are
$$
\beta^1(x,y)=\frac{x+y}{2},\qquad
\beta^2(x,y)=\frac{x-y}{2}.
$$
Alice checked $\beta^1(\mathbf b_1)=1$, $\beta^1(\mathbf b_2)=0$, $\beta^2(\mathbf b_1)=0$, and $\beta^2(\mathbf b_2)=1$.

![Each dual basis covector reads one coefficient and ignores the other basis vector.](assets/figures/ch10-dual-basis.svg){width=100%}

## Alice learns to read the indices

Humpty first wrote every sum explicitly:
$$
\mathbf v=\sum_{i=1}^n v^i\mathbf e_i,\qquad v^i\in\mathbb R,
\qquad
\alpha=\sum_{i=1}^n\alpha_i\epsilon^i,\qquad \alpha_i\in\mathbb R.
$$
The coefficients are $v^i=\epsilon^i(\mathbf v)$ and $\alpha_i=\alpha(\mathbf e_i)$. An upper index in $v^i$ labels a coefficient; it is not the power $v$ raised to $i$.

Applying the covector to the vector gives
$$
\alpha(\mathbf v)=\sum_{i=1}^n\alpha_i v^i.
$$
Only now did Humpty offer **Einstein summation**: an index appearing once upstairs and once downstairs in a term is summed over its full range. Thus $\mathbf v=v^i\mathbf e_i$ and $\alpha(\mathbf v)=\alpha_i v^i$ abbreviate the sums above. An index appearing only once is a **free index**; the formula holds separately for each of its values. Dummy indices can be renamed without changing a sum.

Alice's question has old components $(\alpha_1,\alpha_2)=(2,-1)$ and new components $(\alpha'_1,\alpha'_2)=(1,3)$ because $\alpha(\mathbf b_1)=1$ and $\alpha(\mathbf b_2)=3$. Therefore
$$
2\cdot3-1\cdot4
=1\cdot\frac72+3\cdot\left(-\frac12\right)
=2.
$$

![Different component lists give the same scalar pairing alpha(v)=2.](assets/figures/ch10-pairing.svg){width=100%}

## The transformation law has a direction

“Which way does the matrix point?” Alice asked before using its inverse. Define the invertible real matrix $A$ by putting the new basis vectors in its columns:
$$
\mathbf e'_j=\sum_{i=1}^n A^i{}_j\mathbf e_i.
$$
For the diagonal basis,
$$
A=\begin{pmatrix}1&1\\1&-1\end{pmatrix},\qquad
A^{-1}=\frac12\begin{pmatrix}1&1\\1&-1\end{pmatrix}.
$$
The **basis** uses $A$, while the vector's column of **components** uses its inverse:
$$
v'^j=\sum_{i=1}^n(A^{-1})^j{}_i v^i.
$$
A covector's components instead satisfy
$$
\alpha'_j=\sum_{i=1}^n\alpha_i A^i{}_j.
$$
Treating $\alpha$'s component list as a row gives the compact matrix formulas $v'=A^{-1}v$ and $\alpha'=\alpha A$. Multiplying them gives $\alpha'A^{-1}v=\alpha v$ after substituting $\alpha'=\alpha A$; the $A$ and $A^{-1}$ cancel.

![The basis matrix A and its inverse act on different descriptions.](assets/figures/ch10-transformation.svg){width=100%}

Vector components are called **contravariant**, with upper indices. Covector components are **covariant**, with lower indices. These words record the transformation rules, not a social rank.

::: {.blackboard}
A bilinear form has two covariant indices. If its old matrix is $G$, its new matrix is $G'=A^TGA$. This differs from the similarity rule $A^{-1}LA$ for the matrix of a linear operator $L$. Both rules follow by preserving the corresponding evaluations.
:::

## Tensors as multilingual machines

Humpty built a two-arrow machine
$$
S(\mathbf u,\mathbf v)=(u^1v^1,u^2v^2)\in\mathbb R^2.
$$
It is linear in each arrow separately. A covector can ask a question of its output, giving
$$
T:V^*\times V\times V\to\mathbb R,\qquad
T(\alpha,\mathbf u,\mathbf v)=\alpha(S(\mathbf u,\mathbf v)).
$$
This scalar rule is linear in each of its three inputs and is a tensor of **type $(1,2)$**: one covector slot and two vector slots. In finite dimensions, such a tensor is an element of $V\otimes V^*\otimes V^*$.

For $\mathbf u=(1,2)$ and $\mathbf v=(3,4)$, Alice found $S(\mathbf u,\mathbf v)=(3,8)$. Her question $\alpha(x,y)=2x-y$ gave $6-8=-2$.

![The tensor first combines two vectors and then lets a covector evaluate the result.](assets/figures/ch10-tensor.svg){width=100%}

In a basis its expansion is
$$
T=\sum_{i=1}^n\sum_{j=1}^n\sum_{k=1}^n
T^i{}_{jk}\,\mathbf e_i\otimes\epsilon^j\otimes\epsilon^k,
\qquad T^i{}_{jk}\in\mathbb R.
$$
The components are evaluations $T^i{}_{jk}=T(\epsilon^i,\mathbf e_j,\mathbf e_k)$. For this $S$ in the standard basis, $T^1{}_{11}=1$, $T^2{}_{22}=1$, and every other component is zero. The expansion and the multilinear-map description are two ways to describe the same tensor.

::: {.blackboard}
With the basis change defined above, Einstein notation gives
$$
T'^i{}_{jk}=(A^{-1})^i{}_r A^s{}_j A^t{}_k T^r{}_{st}.
$$
Here $i,j,k$ are free indices; $r,s,t$ are summed from $1$ to $n$. One upper index uses the inverse matrix; each lower index uses the basis matrix. These factors preserve the tensor's evaluation on the same geometric inputs.
:::

## Rank is a different question

Alice counted three slots, but Humpty refused to call that “rank three.” **Order** or **valence** counts slots; **type** distinguishes the two sorts of slots. **Tensor rank** is the smallest number of pure products needed to express the tensor as a sum.

For example, the type-$(1,2)$ tensor above is
$$
\mathbf e_1\otimes\epsilon^1\otimes\epsilon^1
+\mathbf e_2\otimes\epsilon^2\otimes\epsilon^2.
$$
It has order three and rank two. It cannot be one pure product: the two independent output vectors $(1,0)$ and $(0,1)$ produced by $S$ would otherwise have to lie on one output line. Matrix rank agrees with tensor rank for two-factor tensors. Invertible changes of basis preserve tensor rank.

### A complex costume

Over $\mathbb C$, the same finite-dimensional component rules hold with $v^i,\alpha_i,T^i{}_{jk}\in\mathbb C$ and $A\in\mathrm{GL}(n,\mathbb C)$, the set of invertible complex matrices. The dual $V^*$ means **complex-linear** maps $V\to\mathbb C$. The natural pairing is still $\alpha_i v^i$, without conjugation. It differs from a Hermitian inner product, which involves conjugation and an additional measuring rule.

::: {.demo id="component-transformer" title="Component Transformer"}
Rotate a coordinate frame and watch the components of a vector, covector, and bilinear form change while the underlying geometry remains fixed.
:::

::: {.trythis}
1. Write the standard basis covectors dual to $(1,0)$ and $(0,1)$.
2. If $\mathbf v=3\mathbf e_1+4\mathbf e_2$, evaluate $\epsilon^1(\mathbf v)$.
3. Explain why a tensor itself is basis-independent.
4. Give one reason physicists use upper and lower indices.
5. For $\alpha(x,y)=2x-y$, verify $\alpha(3,4)$ using the diagonal basis.
6. Evaluate the tensor $T(\alpha,\mathbf u,\mathbf v)=\alpha(u^1v^1,u^2v^2)$ for $\alpha(x,y)=x+y$, $\mathbf u=(2,1)$, and $\mathbf v=(3,-1)$.
:::

## Alice's costume notes

1. Components are scalars in a specified field and basis.
2. Covectors are linear questions; the dual basis reads coordinates.
3. Repeated upper and lower indices abbreviate explicit finite sums.
4. Transformation rules preserve evaluations.
5. Tensor type, order, and rank answer different questions.

“Words can be difficult,” said Humpty, “but instruments answer one direction by using another.”

Alice packed the arrow and its questions together. She would need both in the Rabbit's instrument room.
