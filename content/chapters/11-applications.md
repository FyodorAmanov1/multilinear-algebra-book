---
title: "The White Rabbit’s Instrument Bag"
subtitle: "Stress, diffusion, inertia, and data"
slug: "11-applications"
story-image: "assets/story/11-applications.png"
story-alt: "The White Rabbit opens his instrument bag while Alice prepares to take notes."
part: "III. The Multilinear Wilderness"
demo: "tensor-applications"
summary: "Alice sees why tensors appear whenever one direction influences another."
---

The White Rabbit returned with a bag containing a pressure pad, tea leaves, a spinning teacup, and photographs.

“What do they have in common?” Alice asked.

“Try changing the direction,” he replied.

Alice opened her notebook. The matrices in this chapter have **real entries** and describe local physical rules in specified Cartesian coordinates. Most examples are two-dimensional sketches; the inertia example uses three dimensions.

::: {.intuition}
A tensor can describe a whole direction-dependent rule. A single vector describes one input or one response; a linear operator describes how all inputs produce responses.
:::

## The pressure pad: stress

Alice cut an imaginary small surface inside the pad and drew its unit normal $\mathbf n$, the vector perpendicular to the surface with length one. Changing the surface orientation changed the force transmitted across it.

The **stress tensor** $\sigma$ maps the unit normal to a **traction**, a force per unit area:
$$
\mathbf t(\mathbf n)=\sigma\mathbf n.
$$
For a small surface element of area $dS$, the corresponding force is
$$
d\mathbf F=\mathbf t(\mathbf n)\,dS.
$$
Traction and force have different units. Stress and traction are measured in pascals, with $1\ \mathrm{Pa}=1\ \mathrm{N}/\mathrm m^2$; force is measured in newtons.

For a two-dimensional section, let
$$
\sigma=\begin{pmatrix}2&1\\1&3\end{pmatrix}\ \mathrm{Pa}.
$$
Alice found $\mathbf t(1,0)=(2,1)\ \mathrm{Pa}$ and $\mathbf t(0,1)=(1,3)\ \mathrm{Pa}$. The traction need not be perpendicular to the surface: its normal component is normal stress, and its tangential component is shear stress. A patch of area $0.5\ \mathrm m^2$ with normal $(1,0)$ carries force $(1,0.5)\ \mathrm N$ when stress is constant across it.

![Two surface orientations give different traction vectors for the same stress tensor.](assets/figures/ch11-stress.svg){width=100%}

::: {.intuition}
The stress tensor stores a rule for every surface normal. Its columns are the traction vectors on the coordinate-normal surfaces. In the ordinary continuum model without couple stresses, the stress matrix is symmetric.
:::

## The packet of tea leaves: diffusion

The Rabbit stirred the leaves. Alice imagined dissolved particles spreading through water and then through a material that makes spreading easier along one direction.

Let $c(x,y)$ be concentration. Its **gradient**
$$
\nabla c=\begin{pmatrix}\partial c/\partial x\\ \partial c/\partial y\end{pmatrix}
$$
records how concentration changes locally along each coordinate direction. A partial derivative is the local rate of change along one coordinate while the other is held fixed. The **flux** $\mathbf J$ records how much material crosses unit area per unit time.

The diffusion rule is
$$
\mathbf J=-D\nabla c.
$$
The minus sign makes flux run down concentration rather than up it. For standard anisotropic diffusion, $D$ is symmetric positive definite: all its eigenvalues are positive. Its entries have units of area per time.

Alice tried $D=\operatorname{diag}(4,1)\ \mathrm m^2/\mathrm s$ and a gradient with components $(-1,-1)$ in concentration-per-metre units. The flux had components $(4,1)$ in concentration-times-metres-per-second units. It pointed down concentration but not exactly opposite the gradient. For molar concentration, the gradient unit is $\mathrm{mol}/\mathrm m^4$ and the flux unit is $\mathrm{mol}/(\mathrm m^2\mathrm s)$.

![Isotropic diffusion gives circular concentration contours; anisotropic diffusion gives elliptical ones.](assets/figures/ch11-diffusion.svg){width=100%}

For a point release in a uniform medium, equal-concentration contours have principal-axis lengths proportional to $\sqrt{D_i t}$, where $D_i$ is a diffusion eigenvalue and $t>0$ is time. Thus the contour for $\operatorname{diag}(4,1)$ is twice as wide as it is tall. This square-root dependence differs from drawing the image of a circle under the matrix itself.

## The spinning teacup: inertia

Alice spun the teacup in two different ways. The Rabbit distinguished angular velocity $\boldsymbol\omega$, which describes rotation, from angular momentum $\mathbf L$, the quantity relating that rotation to mass distribution.

In three-dimensional Euclidean space, the **inertia tensor** satisfies
$$
\mathbf L=I\boldsymbol\omega,\qquad I\in\mathbb R^{3\times3}.
$$
Angular velocity has units of radians per second, while inertia has units of mass times length squared and angular momentum has units of mass times length squared per second.

For a possible inertia matrix
$$
I=\operatorname{diag}(2,3,4)\ \mathrm{kg\,m^2},
\qquad \boldsymbol\omega=(1,1,0)\ \mathrm s^{-1},
$$
Alice obtained $\mathbf L=(2,3,0)\ \mathrm{kg\,m^2/s}$. The vectors were not parallel. Along a principal axis, however, the rule reduces to multiplying by the corresponding scalar moment of inertia.

![Different inertia factors make angular momentum point differently from angular velocity.](assets/figures/ch11-inertia.svg){width=100%}

::: {.intuition}
A scalar moment of inertia describes rotation about one chosen axis. The full tensor describes all axes and their combinations.
:::

## The photographs: data

The Rabbit handed Alice a photograph and then a stack of videos. “What does each index select?” she asked.

A grayscale image has entries $X_{rc}$, with row $r$ and column $c$. A colour image adds a channel index, such as red, green, or blue. A batch of colour videos can have entries
$$
X_{btrck},
$$
where $b$ selects the video, $t$ the frame, $r$ the row, $c$ the column, and $k$ the colour channel. The frame index here is an integer label, rather than the continuous time variable used in diffusion.

For a batch containing $2$ videos, each with $5$ frames of size $3$ by $4$ and $3$ channels, the array shape is $(2,5,3,4,3)$ and there are $360$ scalar entries. Each index runs from $1$ to its stated size. Pixel values might be integers from $0$ to $255$, or normalized real values, depending on the representation.

![Five indices select a single brightness value in a batch of colour videos.](assets/figures/ch11-data.svg){width=100%}

::: {.intuition}
In data science, “tensor” often means a multidimensional array. An array can represent tensor components after suitable spaces and bases are chosen, but organizing data by several indices alone does not specify geometric transformation laws.
:::

## Metric tensors: the rule for measuring

Alice returned to the Caterpillar's rulers. “Could the rule for length itself change?” she asked.

A positive-definite **metric tensor** $g$ is a symmetric bilinear form for measuring vectors. In a real coordinate basis,
$$
g(\mathbf v,\mathbf v)=\sum_{i=1}^n\sum_{j=1}^n g_{ij}v^i v^j,
\qquad g_{ij}\in\mathbb R.
$$
For $g=\operatorname{diag}(4,1)$, the vector $(1,0)$ has squared length $4$ and hence length $2$. The vectors of length one satisfy $4x^2+y^2=1$, an ellipse in the drawn coordinates. For $g=I$, they satisfy $x^2+y^2=1$.

![Different metric matrices assign unit length to different coordinate ellipses.](assets/figures/ch11-metric.svg){width=100%}

On a curved space, each point has its own tangent space and a local measuring rule. The familiar notation
$$
ds^2=g_{ij}\,dx^i\,dx^j
$$
uses Einstein summation for the squared length of a small tangent displacement. Here $dx^i$ are coordinate displacement components in this measurement formula; their covector interpretation will appear in the next chapter. The coefficients $g_{ij}$ may depend on position. Curvature requires more than merely having a nonidentity matrix: even ordinary Euclidean geometry can have nonidentity metric components in a different coordinate system.

## Principal directions

Alice asked the Rabbit to rotate the instruments until the responses separated into independent stretches. For a real symmetric matrix, an orthonormal eigenbasis does exactly that.

Take
$$
S=R\begin{pmatrix}3&0\\0&1\end{pmatrix}R^T,
\qquad
R=\begin{pmatrix}\cos30^\circ&-\sin30^\circ\\
\sin30^\circ&\cos30^\circ\end{pmatrix}.
$$
The columns of $R$ are eigenvectors of $S$ with eigenvalues $3$ and $1$. If a unit circle is transformed by $S$, its image is an ellipse with semiaxes $3$ and $1$, directed along those eigenvectors.

![The image of a unit circle under S has principal semiaxes 3 and 1.](assets/figures/ch11-applications.svg){width=100%}

For diffusion, principal directions describe independent spreading rates. For stress, they are surface normals with no shear traction; their eigenvalues are principal normal stresses and can have either sign. For a covariance matrix, they describe directions of greatest and least variance.

The Rabbit held up the diffusion picture again. Alice checked its labels: the diffusion contour uses square roots of eigenvalues, whereas the matrix-image ellipse uses eigenvalues themselves. A picture must say which object it represents.

::: {.demo id="tensor-applications" title="Tensor Applications"}
Adjust a symmetric matrix and inspect its principal directions, a directional-response ellipse, and a diffusion illustration. Compare what each plotted shape represents.
:::

::: {.trythis}
1. Why is stress not described by a single vector?
2. Give an everyday example of anisotropic diffusion.
3. Explain what the eigenvalues of a diffusion tensor tell you.
4. Why is the identity matrix a valid metric tensor?
5. For $\sigma=\begin{pmatrix}2&1\\1&3\end{pmatrix}$ Pa, find the traction on a surface with normal $(0,1)$ and the force on a uniform patch of area $2$ square metres.
6. For $g=\operatorname{diag}(4,1)$, find the metric length of $(1,2)$.
:::

## Alice's instrument notes

1. Physical formulas need defined quantities and units.
2. Stress maps normals to traction; surface area converts traction to force.
3. Diffusion and inertia can produce responses not parallel to their inputs.
4. Data arrays and geometric tensors use related but distinct language.
5. A metric defines measurement; eigenvectors reveal principal directions.

“One room remains,” said the Rabbit.

Alice packed the instruments. Their formulas no longer looked like unexplained abbreviations: each had an input she could choose, a rule she could calculate, and an output she could interpret.
