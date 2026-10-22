---
title: "Alice’s Dream Map"
subtitle: "Differential forms, integration, and the edge of the story"
slug: "12-forms"
story-image: "assets/story/12-forms.png"
story-alt: "Alice and the White Rabbit examine maps covered with paths and small arrow markings."
part: "III. The Multilinear Wilderness"
demo: "forms-and-fields"
summary: "Alice learns that forms are layers for measuring paths, patches, and volumes all at once."
---

At the corridor's end, Alice found maps covered with small measuring instructions. A rule at one point read an arrow; another rule read two arrows and their oriented patch.

“Are these the same questions everywhere?” she asked.

“They can change with the place,” said the Rabbit. “That makes them fields.”

The main examples use a coordinate region $U\subseteq\mathbb R^n$ with real coordinates. Functions and fields will be **smooth**, meaning differentiable as often as needed. Alice will use derivatives as local rates of change and integrals as accumulated measurements; the examples introduce those ideas without requiring a prior calculus course.

::: {.intuition}
A differential form is a smoothly varying, alternating multilinear measuring rule. Its degree tells how many tangent directions it accepts and what dimension of oriented region it can measure.
:::

## Layers of measurement

At a point $p$, the tangent space $T_pU$ contains possible infinitesimal directions of travel. In an ordinary Euclidean coordinate region it is naturally a copy of $\mathbb R^n$. A differential $k$-form assigns a map
$$
\omega_p:\underbrace{T_pU\times\cdots\times T_pU}_{k\text{ inputs}}\to\mathbb R
$$
that is linear in each input and changes sign when two inputs are exchanged. Equivalently, $\omega_p\in\Lambda^k(T_p^*U)$, the exterior space of covectors. A vector wedge from Chapter 8 is a patch; a covector wedge is a rule that measures such patches.

Alice sorted the maps into four drawers:

- a 0-form is a function, assigning a scalar to each point;
- a 1-form evaluates one tangent vector;
- a 2-form evaluates a pair of vectors, measuring a weighted oriented area;
- a 3-form evaluates three vectors, measuring a weighted oriented volume.

The result is a scalar, not the patch itself. A form can weight different points differently or give zero to some nonzero patches. In an $n$-dimensional space, every $k$-form with $k>n$ is zero.

![The degree of a form matches points, paths, patches, and volumes.](assets/figures/ch12-forms.svg){width=100%}

## Alice reads the coordinate questions

The Rabbit labelled two coordinate covectors. In the plane, $dx$ reads the first component of a tangent vector, and $dy$ reads the second:
$$
dx(a,b)=a,\qquad dy(a,b)=b.
$$
These are the dual basis questions from Humpty's room. At each point, Alice could combine them into
$$
\alpha_p=2\,dx-dy.
$$
This constant 1-form gives $\alpha_p(1,0)=2$, $\alpha_p(0,1)=-1$, and $\alpha_p(1,1)=1$. It happens to have the same rule at every point.

![The constant 1-form 2 dx-dy gives a scalar answer to each tangent direction.](assets/figures/ch12-one-form.svg){width=100%}

A varying form might instead be $\eta=x\,dx+y\,dy$. At $p=(1,2)$ it gives $\eta_p(a,b)=a+2b$; at $q=(3,0)$ it gives $\eta_q(a,b)=3a$. Alice had to specify both the point and the input vector.

::: {.intuition}
A covector is one measuring question. A 1-form is a field of covector questions, one at each point.
:::

## Why antisymmetry?

Alice laid two arrows on the floor, then swapped their order. The measuring rule for oriented area reversed its answer.

In standard oriented Euclidean coordinates, the basic 2-form satisfies
$$
(dx\wedge dy)_p(\mathbf u,\mathbf v)
=dx(\mathbf u)\,dy(\mathbf v)-dx(\mathbf v)\,dy(\mathbf u)
=u^1v^2-u^2v^1.
$$
Here $\mathbf u,\mathbf v\in T_pU$ have real components. For $\mathbf u=(2,1)$ and $\mathbf v=(1,3)$ the answer is $5$; reversing them gives $-5$. The notation puts parentheses around the form before evaluating it.

![The form dx wedge dy gives +1 on the standard basis pair and -1 when the inputs are reversed.](assets/figures/ch12-two-form.svg){width=100%}

Using the same vector twice gives zero. More generally, linearly dependent inputs give zero for any alternating form, because they span no full-dimensional patch of the required degree. An arbitrary 2-form need not give the ordinary Euclidean area; $f(x,y)\,dx\wedge dy$ weights that signed area by the real value $f(p)$.

## Alice integrates a path

The Rabbit drew a path $\gamma(t)=(t,t)$ for $0\le t\le1$. Its tangent vector is $\gamma'(t)=(1,1)$, describing its rate of travel. To integrate a 1-form, evaluate it on that tangent vector and accumulate the resulting scalar:
$$
\int_\gamma\alpha
=\int_0^1\alpha_{\gamma(t)}(\gamma'(t))\,dt.
$$
For $\alpha=2\,dx-dy$, the integrand is constantly $2-1=1$, so the answer is $1$. The symbol $\int_0^1$ means summing the infinitesimal contributions over the parameter interval. Reversing the path changes the sign.

A 2-form is integrated over an oriented surface, and a 3-form over an oriented three-dimensional region. In the plane,
$$
\int_M f(x,y)\,dx\wedge dy
$$
accumulates the density $f$ over the region $M$ with its chosen orientation. When $f=1$ on the unit square and the orientation is the standard one, the answer is its area, $1$. A form is integrated over a region of the matching dimension.

## The exterior derivative begins with a function

Alice found a height map $f(x,y)=x^2+y^2$, a 0-form. “How quickly does it change if I take one small step?” she asked.

The **exterior derivative** produces the 1-form
$$
df=\frac{\partial f}{\partial x}\,dx+
\frac{\partial f}{\partial y}\,dy
=2x\,dx+2y\,dy.
$$
At $(1,1)$, a direction $\mathbf v=(a,b)$ gives $df_{(1,1)}(\mathbf v)=2a+2b$. Moving initially in the $(1,0)$ direction changes height at rate $2$. The covector $df$ is defined without a metric; turning it into a gradient vector uses a measuring rule.

![Height contours of x squared+y squared show how df evaluates a chosen direction.](assets/figures/ch12-df.svg){width=100%}

Alice then followed the diagonal path from $(0,0)$ to $(1,1)$. On this path, $df(\gamma')=4t$, so
$$
\int_\gamma df=\int_0^1 4t\,dt=2
=f(1,1)-f(0,0).
$$
For this elementary integral, the area under the straight line $4t$ over $[0,1]$ is a triangle of base $1$ and height $4$, hence area $2$. Alice recognized accumulated change as final height minus initial height.

## A changing question creates a new layer

The Rabbit now offered $\omega=x\,dy$. At position $(x,y)$, the rule weights an upward vector component by $x$. Alice received a larger answer on the right side of the square than on the left.

For a smooth planar 1-form $\omega=P(x,y)\,dx+Q(x,y)\,dy$, exterior differentiation gives
$$
d\omega=\left(\frac{\partial Q}{\partial x}
-\frac{\partial P}{\partial y}\right)dx\wedge dy.
$$
The real functions $P$ and $Q$ are its coordinate coefficients. For $\omega=x\,dy$, $P=0$ and $Q=x$, so $d\omega=dx\wedge dy$. This 2-form measures local oriented circulation per area.

![For omega=x dy, upward travel has weight zero on the left edge and one on the right edge of the unit square.](assets/figures/ch12-circulation.svg){width=100%}

::: {.blackboard}
Write $\Omega^k(U)$ for the space of smooth differential $k$-forms on $U$. The exterior derivative is
$$
d:\Omega^k(U)\to\Omega^{k+1}(U).
$$
It differentiates fields of measuring rules. This space differs from $\Lambda^k(V)$, the exterior space of vectors at a single vector space. Exterior differentiation satisfies $d(d\eta)=0$ for every smooth form $\eta$.
:::

## The edge controls the inside

Alice walked counterclockwise around the unit square $M=[0,1]\times[0,1]$, carrying $\omega=x\,dy$.

On the bottom and top edges, $dy=0$, so the contributions vanished. On the right edge, $x=1$ and upward travel contributed $1$. On the left edge, $x=0$, so downward travel contributed zero. The full boundary integral was $1$.

Inside, $d\omega=dx\wedge dy$ measures area. The unit square has area $1$, giving the same answer. Alice divided the square into four patches: along their common edges, opposite traversal directions canceled. Only the outer edge remained.

![Oppositely oriented interior edges cancel; the unit square has boundary integral and area integral both equal to one.](assets/figures/ch12-stokes.svg){width=100%}

This is the pattern of **Stokes' theorem**:
$$
\int_{\partial M}\omega=\int_M d\omega.
$$
Here $M$ is an oriented compact $(k+1)$-dimensional smooth region with boundary, $\omega$ is a smooth $k$-form defined around it, and $\partial M$ carries the induced boundary orientation. The square example uses the familiar piecewise smooth version: its corners cause no difficulty. Reverse the orientation of $M$, and both sides change sign.

The theorem connects accumulated interior change with a boundary measurement. It includes the fundamental theorem of calculus, Green's theorem, the divergence theorem, and the classical Stokes' theorem when the forms and regions are chosen appropriately. Calling every instance a physical conservation law would require extra physical assumptions; the mathematical statement itself is an integration identity.

::: {.intuition}
Local measurements add across patches. Shared edges cancel because they have opposite orientations, leaving one measurement around the outside.
:::

## The map Alice has now

Alice could trace a route from arrows to bases, linear maps, measuring rules, determinants, eigenvectors, bilinear forms, wedges, tensor products, component transformations, physical applications, and finally forms.

The map suggested further roads: differential geometry, continuum mechanics, relativity, symplectic geometry, representation theory, machine learning, and topology. She did not need to travel every road immediately. The small calculations in these rooms had given the symbols something concrete to mean.

::: {.oxford}
When Alice woke, she was sitting near a college stair with her book still open on her knee. The arrows and instruments had gone, but she remembered walking around the square. The boundary and the interior had told the same story in two different ways.
:::

::: {.demo id="forms-and-fields" title="Forms and Fields"}
Move through the plane and watch a 1-form assign numbers to directions while a 2-form assigns signed measurements to parallelograms.
:::

::: {.trythis}
1. Evaluate $dx\wedge dy$ on $(1,0)$ and $(0,1)$.
2. Evaluate it on $(0,1)$ and $(1,0)$.
3. Explain why every 3-form on a 2-dimensional plane is zero.
4. Give one reason differential forms are useful in physics.
5. Find $df$ for $f(x,y)=x^2+y^2$ and evaluate it at $(1,2)$ on the direction $(3,-1)$.
6. Walk clockwise around the unit square with $\omega=x\,dy$. What is the boundary integral, and what orientation makes the interior integral agree?
:::

## Alice's dream-map notes

1. Forms assign scalar measurements to tangent directions at specified points.
2. Their degree and antisymmetry record dimension and orientation.
3. Integrals accumulate these measurements over matching regions.
4. The exterior derivative raises degree and describes local change.
5. Stokes' theorem connects a boundary measurement to an interior integral.

Alice closed the notebook. The formulas were no longer distant marks: she had added the arrows, changed their addresses, measured their patches, and walked their boundary.
