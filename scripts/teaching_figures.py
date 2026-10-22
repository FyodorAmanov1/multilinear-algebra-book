"""Reproducible SVG/PDF teaching illustrations for the twelve chapters."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Polygon, Arc
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "figures"
BLUE, TEAL, GOLD, ROSE = "#002147", "#0f766e", "#956b0c", "#b3375f"
PAPER = "#fbfaf5"
plt.rcParams.update({"font.size": 11, "font.family": "DejaVu Sans", "svg.hashsalt": "alice-algebra"})
FIGURE_NAMES = {
    "01-vectors": ["ch01-directions", "ch01-coordinates", "ch01-vectors", "ch01-scaling"],
    "02-spaces": ["ch02-spaces", "ch02-independence", "ch02-dimensions", "ch02-basis-change"],
    "03-linear-maps": ["ch03-columns", "ch03-maps", "ch03-rotation", "ch03-reflection", "ch03-shear", "ch03-projection"],
    "04-inner-products": ["ch04-length", "ch04-dot-signs", "ch04-inner-products", "ch04-orthogonal"],
    "05-determinants": ["ch05-determinants", "ch05-collapse", "ch05-volume", "ch05-composition"],
    "06-eigenvectors": ["ch06-eigenvectors", "ch06-factors", "ch06-diagonalization", "ch06-iteration"],
    "07-bilinear-forms": ["ch07-bilinear", "ch07-symmetry", "ch07-definite", "ch07-indefinite"],
    "08-wedge-products": ["ch08-wedge", "ch08-collapse", "ch08-cross-product", "ch08-volume"],
    "09-tensor-products": ["ch09-tensor-products", "ch09-expansion", "ch09-rank", "ch09-universal"],
    "10-components": ["ch10-components", "ch10-covector", "ch10-dual-basis", "ch10-pairing", "ch10-transformation", "ch10-tensor"],
    "11-applications": ["ch11-stress", "ch11-diffusion", "ch11-inertia", "ch11-data", "ch11-metric", "ch11-applications"],
    "12-forms": ["ch12-forms", "ch12-one-form", "ch12-two-form", "ch12-df", "ch12-circulation", "ch12-stokes"],
}
SAVED = set()

def canvas(title, n=1, three=False):
    fig, aa = plt.subplots(1, n, figsize=(7.6 if n == 1 else 10.4, 5.0),
                          squeeze=False, subplot_kw={"projection": "3d"} if three else {})
    fig.patch.set_facecolor(PAPER)
    fig.suptitle(title, y=.98, fontsize=17, weight="bold", color=BLUE)
    fig.subplots_adjust(left=.09, right=.94, bottom=.15, top=.80, wspace=.48)
    for ax in aa.flat:
        ax.set_facecolor(PAPER)
    return fig, list(aa.flat)

def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / (name + ".svg"), bbox_inches="tight", pad_inches=.25, metadata={"Date": None})
    fig.savefig(OUT / (name + ".pdf"), bbox_inches="tight", pad_inches=.25,
                metadata={"CreationDate": None, "ModDate": None})
    plt.close(fig)
    SAVED.add(name)

def label(ax, xy, text, color=BLUE, offset=(0, 14)):
    return ax.annotate(text, xy, xytext=offset, textcoords="offset points",
                       color=color, fontsize=10.5, ha="center", va="center", zorder=8,
                       bbox={"facecolor": PAPER, "edgecolor": "none", "alpha": .96, "pad": 2})

def arrow(ax, start, end, color=BLUE, text=None, offset=(0, 15), pos=.65, width=2.3):
    a, b = np.asarray(start, dtype=float), np.asarray(end, dtype=float)
    if np.allclose(a, b):
        ax.scatter(*a, color=color, s=40, zorder=5)
    else:
        ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=16,
                                    color=color, linewidth=width, shrinkA=0, shrinkB=0, zorder=4))
    if text:
        label(ax, a + pos*(b-a), text, color, offset)
    return [a, b]

def plane(ax, points, title=None, limits=None):
    p = np.asarray(points, dtype=float).reshape(-1, 2)
    if limits is None:
        lo, hi = p.min(0), p.max(0)
        pad = np.maximum(hi-lo, 2)*.30 + .20
        limits = (lo[0]-pad[0], hi[0]+pad[0], lo[1]-pad[1], hi[1]+pad[1])
    ax.set_xlim(limits[:2]); ax.set_ylim(limits[2:])
    ax.set_aspect("equal")
    ax.set_xticks(np.arange(np.ceil(limits[0]), np.floor(limits[1])+1))
    ax.set_yticks(np.arange(np.ceil(limits[2]), np.floor(limits[3])+1))
    ax.tick_params(length=0, labelsize=9, colors="#666258")
    ax.grid(color="#ddd8cc", linewidth=.6)
    ax.axhline(0, color="#8c887d", linewidth=1); ax.axvline(0, color="#8c887d", linewidth=1)
    for spine in ax.spines.values():
        spine.set_visible(False)
    if title:
        ax.set_title(title, fontsize=11, color=TEAL, pad=18)

def polygon(ax, points, color=GOLD):
    p = np.asarray(points)
    ax.add_patch(Polygon(p, closed=True, facecolor=color, edgecolor=color, alpha=.20, linewidth=2))
    q = np.vstack([p, p[0]])
    ax.plot(q[:,0], q[:,1], color=color, linewidth=1.5)
    return p

def area(ax, u, v, swapped=False):
    u, v = np.asarray(u), np.asarray(v)
    p = polygon(ax, [[0,0], u, u+v, v])
    first_offset = (-30,0) if abs(u[1]) > abs(u[0]) else (0,-18)
    second_offset = (-26,12) if abs(v[1]) > abs(v[0]) else (0,-22)
    arrow(ax, (0,0), u, BLUE, "first" if swapped else "u", first_offset)
    arrow(ax, (0,0), v, TEAL, "second" if swapped else "v", second_offset)
    return p

def table(ax, cells, cols=None, rows=None, title=None):
    ax.set_axis_off()
    t = ax.table(cellText=cells, colLabels=cols, rowLabels=rows, cellLoc="center",
                 loc="center", bbox=[.12,.16,.82,.66])
    t.auto_set_font_size(False); t.set_fontsize(10.5)
    for (r,c), cell in t.get_celld().items():
        cell.set_edgecolor(BLUE)
        cell.set_facecolor("#e6eeeb" if r == 0 or c == -1 else "#f3efe5")
        cell.set_text_props(color=BLUE)
    if title:
        ax.set_title(title, fontsize=11, color=TEAL, pad=18)

def panel_arrows(name, title, recipes, limits=None):
    fig, axes = canvas(title, len(recipes))
    for ax, (subtitle, arrows) in zip(axes, recipes):
        points = [[0,0]]
        for start,end,color,text,offset in arrows:
            points.extend(arrow(ax,start,end,color,text,offset))
        plane(ax, points, subtitle, limits)
    save(fig,name)

def a(end, text, color=BLUE, offset=(0,15), start=(0,0)):
    return (start,end,color,text,offset)

def basis(name):
    fig, axes = canvas("The same vector in two coordinate languages",2)
    for ax, b1,b2,c,title in zip(axes, [(1,0),(1,1)], [(0,1),(1,-1)],
                               [(3,4),(3.5,-.5)], ["standard: (3, 4)", "new basis: (7/2, −1/2)"]):
        p = c[0]*np.array(b1)
        ax.plot([0,p[0],3],[0,p[1],4],"--",color=GOLD)
        arrow(ax,(0,0),(3,4),BLUE,"v",(-15,12))
        arrow(ax,(0,0),b1,TEAL,"e₁" if c[0]==3 else "b₁",(0,-22))
        arrow(ax,(0,0),b2,ROSE,"e₂" if c[0]==3 else "b₂",(-25,0))
        plane(ax,[(0,0),(3,4)],title,(-1.8,5,-2,5.5))
    save(fig,name)

def transform(name,title,A,caption):
    fig,axes=canvas(title,2)
    sq=np.array([[0,0],[1,0],[1,1],[0,1]])
    points=np.vstack([sq,sq@A.T,[2,1],A@np.array([2,1])])
    lo,hi=points.min(0)-1,points.max(0)+1
    limits=(lo[0],hi[0],lo[1],hi[1])
    for ax,M,sub in zip(axes,[np.eye(2),A],["Before",caption]):
        polygon(ax,sq@M.T)
        arrow(ax,(0,0),M@np.array([2,1]),BLUE,"v" if sub=="Before" else "T(v)")
        plane(ax,points,sub,limits)
    save(fig,name)

def volume(name,title,scales=(2,3,1),normal=False):
    fig,(ax,)=canvas(title,three=True)
    x,y,z=scales
    v=np.array([[0,0,0],[x,0,0],[x,y,0],[0,y,0],[0,0,z],[x,0,z],[x,y,z],[0,y,z]])
    faces=[[v[i] for i in f] for f in ([[0,1,2,3]] if normal else
                                     [[0,1,2,3],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]])]
    ax.add_collection3d(Poly3DCollection(faces,facecolors=TEAL,edgecolors=BLUE,alpha=.20))
    if normal:
        ax.quiver(0,0,0,0,0,2,color=ROSE,arrow_length_ratio=.12)
        ax.text(0,0,2.2,"u × v",color=ROSE); ax.text(1,.5,.1,"u ∧ v",color=BLUE)
    else:
        fig.text(.09,.035,f"Side lengths {x}, {y}, {z}; volume = {x*y*z}",color=BLUE,fontsize=11)
    ax.set_xlim(-.2,x*1.2);ax.set_ylim(-.2,y*1.2);ax.set_zlim(0,max(z*1.2,2.7) if normal else z*1.2)
    ax.set_xlabel("x");ax.set_ylabel("y");ax.set_zlabel("z");ax.set_box_aspect(scales)
    ax.set_xticks([0,x/2,x]);ax.set_yticks([0,y]);ax.set_zticks([0,z/2,z])
    ax.tick_params(labelsize=9,pad=1)
    ax.view_init(elev=22,azim=-58)
    save(fig,name)

def ch01():
    panel_arrows("ch01-directions","Equal lengths, opposite journeys",[("",[a((3,0),"3 steps east"),a((-3,0),"3 steps west",ROSE)])],(-4,4,-1.5,1.5))
    fig,(ax,)=canvas("Three sideways, four upward, five in length")
    arrow(ax,(0,0),(3,4),BLUE,"v = (3, 4)",(-25,14))
    ax.plot([0,3,3],[0,0,4],"--",color=TEAL)
    label(ax,(1.5,0),"3 sideways",TEAL,(0,-20));label(ax,(3,2),"4 upward",TEAL,(48,0))
    plane(ax,[(0,0),(3,4),(4.6,2)])
    save(fig,"ch01-coordinates")
    panel_arrows("ch01-vectors","Two journeys become one",[("",[a((2,1),"u = (2, 1)",offset=(0,-18)),
        a((5,5),"v = (3, 4)",TEAL,(35,0),(2,1)),a((5,5),"u + v = (5, 5)",GOLD,(-48,15))])])
    panel_arrows("ch01-scaling","Scaling stretches, reverses, or gives zero",
        [(f"c = {c}",[a((1,1),"v",TEAL,(-18,12)),a((c,c),f"{c}v",ROSE,(20,-12))]) for c in [2,-1,0]],(-2,3,-2,3))

def ch02():
    fig,(ax,)=canvas("Two keys span the plane")
    for i in range(-2,3):
        for j in range(-2,3):ax.scatter(i,j,s=16,color=TEAL,alpha=.5)
    arrow(ax,(0,0),(1,0),BLUE,"e₁",(0,-18));arrow(ax,(0,0),(0,1),GOLD,"e₂",(-22,0))
    arrow(ax,(0,0),(2,1),ROSE,"2e₁ + e₂",(24,15))
    plane(ax,[(-2,-2),(2,2)]);save(fig,"ch02-spaces")
    panel_arrows("ch02-independence","A second key must add a direction",
        [(title,[a((1,2),"u",offset=(-25,0)),a(v,"v",ROSE,(25,0))]) for v,title in
         [((2,4),"dependent: v = 2u"),((-2,1),"independent")]],(-3,3,-1,5))
    fig,axes=canvas("Dimension counts independent directions",4)
    for ax,n in zip(axes,range(4)):
        ax.set_axis_off();ax.set_xlim(-1.4,1.4);ax.set_ylim(-1.4,1.4);ax.set_aspect("equal")
        ax.scatter(0,0,color=BLUE)
        for end,col in zip([(1,0),(0,1),(-.7,-.7)][:n],[BLUE,TEAL,ROSE]):arrow(ax,(0,0),end,col)
        ax.set_title(f"dimension {n}",color=TEAL,fontsize=11)
        label(ax,(0,-1),["point","line","plane","space (sketch)"][n],offset=(0,0))
    save(fig,"ch02-dimensions");basis("ch02-basis-change")

def ch03():
    panel_arrows("ch03-columns","The columns are images of the basis",[
        ("Input basis",[a((1,0),"e₁",offset=(0,-18)),a((0,1),"e₂",TEAL,(-24,0))]),
        ("A = [[2, 1], [1, 2]]",[a((2,1),"T(e₁)",offset=(0,-18)),a((1,2),"T(e₂)",TEAL,(-24,12))])],(-1,3,-1,3))
    fig,axes=canvas("Projection keeps one direction and forgets another",2)
    arrow(axes[0],(0,0),(2,3),BLUE,"(2, 3)",(25,8))
    axes[0].axvline(0,color=ROSE,linewidth=3,alpha=.6);label(axes[0],(-1.3,2),"kernel",ROSE,(0,0))
    arrow(axes[1],(0,0),(2,0),BLUE,"(2, 0)")
    axes[1].axhline(0,color=GOLD,linewidth=3,alpha=.6);label(axes[1],(-.8,2),"image",GOLD,(0,0))
    for ax,title in zip(axes,["inputs in ℝ²","outputs on the x-axis"]):plane(ax,[(0,0),(2,3)],title,(-2.5,3.5,-1.5,4))
    save(fig,"ch03-maps")
    fig,(ax,)=canvas("Rotation through θ = 60°")
    arrow(ax,(0,0),(2,0),BLUE,"v",(0,-18));arrow(ax,(0,0),(1,np.sqrt(3)),TEAL,"Rθv",(20,8))
    ax.add_patch(Arc((0,0),1.5,1.5,theta1=0,theta2=60,color=ROSE));label(ax,(.85,.65),"θ",ROSE,(0,0))
    plane(ax,[(0,0),(2,0),(1,np.sqrt(3))],limits=(-1,3,-1,3));save(fig,"ch03-rotation")
    transform("ch03-reflection","Reflection across the horizontal axis",np.diag([1,-1]),"(2, 1) → (2, −1)")
    transform("ch03-shear","Shear slides each horizontal row",np.array([[1,1],[0,1]]),"k = 1: (2, 1) → (3, 1)")
    transform("ch03-projection","Projection collapses the square to a segment",np.diag([1,0]),"(2, 1) → (2, 0)")

def ch04():
    fig,(ax,)=canvas("Unit length means one according to the measuring rule")
    t=np.linspace(0,2*np.pi,180);ax.plot(np.cos(t),np.sin(t),color=TEAL)
    arrow(ax,(0,0),(.6,.8),BLUE,"v / ‖v‖",(24,8));plane(ax,[(-1,-1),(1,1)],limits=(-1.7,1.7,-1.5,1.5));save(fig,"ch04-length")
    panel_arrows("ch04-dot-signs","The sign of the dot product",[(title,[a((1,0),"u",offset=(0,-18)),a(v,"v",TEAL,(18,14))])
        for v,title in [((1,1),"positive"),((0,1),"zero"),((-1,1),"negative")]],(-1.7,1.7,-1,2))
    fig,(ax,)=canvas("Projection leaves a perpendicular residual")
    arrow(ax,(0,0),(3,4),BLUE,"u = (3, 4)",(-30,10));arrow(ax,(0,0),(3,0),GOLD,"projection = (3, 0)",(0,-20))
    arrow(ax,(3,0),(3,4),ROSE,"residual = (0, 4)",(65,0))
    ax.plot([2.65,2.65,3],[0,.35,.35],color=TEAL)
    ax.add_patch(Arc((0,0),1.8,1.8,theta1=0,theta2=np.degrees(np.arctan2(4,3)),color=TEAL))
    label(ax,(1,.65),"θ",TEAL,(0,0));plane(ax,[(0,0),(3,4),(5.5,2)]);save(fig,"ch04-inner-products")
    fig,(ax,)=canvas("Orthogonal rulers read independent coordinates")
    arrow(ax,(0,0),(2,0),TEAL,"b₁ = (2, 0)",(0,-22));arrow(ax,(0,0),(0,1),ROSE,"b₂ = (0, 1)",(-55,0))
    arrow(ax,(0,0),(3,4),BLUE,"v",(-15,10));ax.plot([0,3,3],[4,4,0],"--",color=GOLD)
    label(ax,(1.5,4),"v = 1.5b₁ + 4b₂",offset=(0,20))
    plane(ax,[(-1.6,0),(3,4.7)]);save(fig,"ch04-orthogonal")

def ch05():
    fig,axes=canvas("Signed area remembers orientation",2)
    for ax,u,v,title in zip(axes,[(2,1),(1,0)],[(1,3),(0,-1)],["det = 2·3 − 1·1 = 5","reflection: det = −1"]):
        plane(ax,area(ax,u,v),title)
    save(fig,"ch05-determinants")
    panel_arrows("ch05-collapse","Dependent columns cannot enclose area",[("",[a((1,2),"(1, 2)",offset=(-30,0)),a((2,4),"(2, 4)",ROSE,(30,0))])])
    volume("ch05-volume","A unit cube stretched by diag(2, 3, 1)")
    fig,axes=canvas("Area factors multiply through successive machines",3)
    for ax,x,y,title in zip(axes,[1,2,2],[1,1,3],["start: area 1","first: area 2","then: area 6"]):
        polygon(ax,[[0,0],[x,0],[x,y],[0,y]]);plane(ax,[(0,0),(2,3)],title,(-.5,3,-.5,3.5))
    save(fig,"ch05-composition")

def ch06():
    panel_arrows("ch06-eigenvectors","Some directions stay on their line",[
        ("A = [[2,1],[1,2]]; Av = 3v",[a((3,3),"Av",ROSE,(24,0)),a((1,1),"v",BLUE,(-20,10))]),
        ("ordinary vector: Av = (2, 1)",[a((2,1),"Av",ROSE,(0,20)),a((1,0),"v",BLUE,(0,-18))])],(-1,4,-1,4))
    panel_arrows("ch06-factors","Eigenvalues describe what happens on the line",[(f"λ = {c}",[a((1,0),"v",TEAL,(0,18)),a((c,0),"Av",ROSE,(0,-18))]) for c in [3,-2,0]],(-3,4,-1.5,1.5))
    panel_arrows("ch06-diagonalization","Eigenvector coordinates separate the stretches",[
        ("basis (1,1), (1,−1)",[a((3,3),"factor 3"),a((1,-1),"factor 1",TEAL,(0,-18))]),
        ("coordinate matrix diag(3, 1)",[a((3,0),"factor 3"),a((0,1),"factor 1",TEAL,(-30,0))])])
    fig,(ax,)=canvas("Repeated action favours the larger eigenvalue")
    A=np.array([[2,1],[1,2]])
    points=np.array([np.linalg.matrix_power(A,k)@np.array([1.,0.]) for k in range(5)])
    points/=np.linalg.norm(points,axis=1)[:,None]
    for k,v in enumerate(points):arrow(ax,(0,0),v,plt.cm.viridis(.15+.17*k),width=1.5)
    # A legend avoids putting five labels on almost coincident arrow tips.
    for k in range(5):ax.plot([],[],color=plt.cm.viridis(.15+.17*k),label=f"step {k}")
    ax.legend(loc="upper left",fontsize=9,frameon=False)
    plane(ax,[(0,0),(1,1)],limits=(-.3,1.5,-.2,1.4))
    fig.text(.09,.035,"Each arrow is normalized after the step; only its direction is shown.",fontsize=10,color=BLUE)
    save(fig,"ch06-iteration")

def ch07():
    fig,(ax,)=canvas("The balance is linear in each input")
    table(ax,[["(1, 2)","(3, 4)",11],["(2, 4)","(3, 4)",22],["(1, 2)","(9, 12)",33],["(2, 4)","(9, 12)",66]],["left pan","right pan","dot-product card"]);save(fig,"ch07-bilinear")
    fig,axes=canvas("Swapping the pans need not preserve the answer",2)
    table(axes[0],[["B(e₁,e₂)",2],["B(e₂,e₁)",3]],["A = [[1,2],[3,4]]","answer"],title="not symmetric")
    table(axes[1],[["B(e₁,e₂)",1],["B(e₂,e₁)",1]],["A = [[2,1],[1,2]]","answer"],title="symmetric");save(fig,"ch07-symmetry")
    fig,axes=canvas("Definite forms have one sign away from zero",2)
    t=np.linspace(0,2*np.pi,180)
    for ax,title in zip(axes,["2x² + y² = 1","−2x² − y² = −1"]):
        ax.plot(np.cos(t)/np.sqrt(2),np.sin(t),color=TEAL);plane(ax,[(-1,-1),(1,1)],title,(-1.5,1.5,-1.5,1.5))
    save(fig,"ch07-definite")
    fig,axes=canvas("Mixed signs and zero directions change the level sets",2)
    y=np.linspace(-1.5,1.5,180);x=np.sqrt((1+3*y*y)/2)
    axes[0].plot(x,y,color=ROSE);axes[0].plot(-x,y,color=ROSE)
    axes[1].axvline(1,color=TEAL);axes[1].axvline(-1,color=TEAL)
    for ax,title in zip(axes,["indefinite: 2x² − 3y² = 1","degenerate: x² = 1"]):plane(ax,[(-2,-2),(2,2)],title,(-2.5,2.5,-2,2))
    save(fig,"ch07-indefinite")

def ch08():
    fig,axes=canvas("The same patch with opposite orientations",2)
    for ax,u,v,title in zip(axes,[(2,1),(1,3)],[(1,3),(2,1)],["u ∧ v = +5 e₁ ∧ e₂","v ∧ u = −5 e₁ ∧ e₂"]):
        p=area(ax,u,v,True);u,v=np.array(u),np.array(v)
        arrow(ax,.35*u,.8*u,ROSE,width=1.3);arrow(ax,u+.25*v,u+.75*v,ROSE,width=1.3)
        plane(ax,p,title)
    save(fig,"ch08-wedge")
    panel_arrows("ch08-collapse","Parallel arrows make a zero area ticket",[("",[a((1,2),"u",offset=(-22,0)),a((2,4),"2u",TEAL,(22,0))])])
    volume("ch08-cross-product","In ℝ³ a normal arrow can encode an oriented patch",(2,1,2),True)
    volume("ch08-volume","Three independent arrows make a volume ticket",(2,1,3))

def ch09():
    fig,(ax,)=canvas("Three spoon directions × four cup directions")
    subs = {1:"₁", 2:"₂", 3:"₃", 4:"₄"}
    table(ax,[[f"u{subs[i]}"] + [f"u{subs[i]} ⊗ v{subs[j]}" for j in range(1,5)] for i in range(1,4)],
          ["spoon", "v₁","v₂","v₃","v₄"]);save(fig,"ch09-tensor-products")
    fig,(ax,)=canvas("A pure product fills every basis pairing")
    table(ax,[["u₁ = 1","1 × 3 = 3","1 × 4 = 4"],["u₂ = 2","2 × 3 = 6","2 × 4 = 8"]],
          ["coefficient","v₁ = 3","v₂ = 4"]);save(fig,"ch09-expansion")
    fig,axes=canvas("One outer product or a sum of two?",2)
    table(axes[0],[[3,4],[6,8]],["column 1","column 2"],title="rank 1: dependent columns")
    table(axes[1],[[1,0],[0,1]],["column 1","column 2"],title="rank 2: e₁⊗e₁ + e₂⊗e₂");save(fig,"ch09-rank")
    fig,(ax,)=canvas("A bilinear rule factors through the tensor product")
    ax.set_axis_off();ax.set_xlim(0,10);ax.set_ylim(0,5)
    for xy,text in [((1,4),"U × V"),((8,4),"W"),((1,1),"U ⊗ V")]:
        label(ax,xy,text,offset=(0,0))
    arrow(ax,(2,4),(7,4),BLUE,"B (bilinear)",(0,20))
    arrow(ax,(1,3.5),(1,1.5),TEAL,"u ⊗ v",(45,0))
    arrow(ax,(2,1),(7.5,3.5),ROSE,"B̃ (linear)",(0,-23));save(fig,"ch09-universal")

def ch10():
    basis("ch10-components")
    fig,(ax,)=canvas("A covector labels parallel measuring lines")
    x=np.linspace(-1.5,4.5,150)
    for c in [-2,0,2,4]:
        ax.plot(x,2*x-c,color=TEAL,alpha=.7);label(ax,(-.5,-1-c),f"α = {c}",TEAL,(0,0))
    arrow(ax,(0,0),(3,4),BLUE,"v = (3, 4)",(22,0))
    plane(ax,[(-1,-4),(4,5)],limits=(-1.5,4.5,-6,6))
    fig.text(.09,.035,"α(x,y) = 2x − y; the endpoint of v is on α = 2.",color=BLUE,fontsize=10);save(fig,"ch10-covector")
    fig,axes=canvas("The dual basis asks which key was used",2)
    table(axes[0],[["ε¹ = x",1,0],["ε² = y",0,1]],["question","e₁","e₂"],title="standard basis")
    table(axes[1],[["β¹ = (x+y)/2",1,0],["β² = (x−y)/2",0,1]],["question","b₁","b₂"],title="diagonal basis");save(fig,"ch10-dual-basis")
    fig,axes=canvas("The pairing survives a change of language",2)
    table(axes[0],[[2,3,6],[-1,4,-4],["","total",2]],["αᵢ","vⁱ","product"],title="standard basis")
    table(axes[1],[[1,"7/2","7/2"],[3,"−1/2","−3/2"],["","total",2]],["α′ⱼ","v′ʲ","product"],title="new basis");save(fig,"ch10-pairing")
    fig,axes=canvas("The basis matrix and its inverse have different jobs",2)
    table(axes[0],[[1,1],[1,-1]],["b₁ column","b₂ column"],title="A: new basis in old coordinates")
    table(axes[1],[["1/2","1/2"],["1/2","−1/2"]],["old x","old y"],title="A⁻¹: old components to new")
    fig.text(.14,.035,"v′ = A⁻¹v                                 α′ = αA",color=BLUE,fontsize=12);save(fig,"ch10-transformation")
    fig,(ax,)=canvas("A type-(1,2) tensor: two arrows, then a question")
    ax.set_axis_off();ax.set_xlim(0,10);ax.set_ylim(0,5)
    label(ax,(2,4),"u = (1,2), v = (3,4)",offset=(0,0))
    label(ax,(7,4),"S(u,v) = (3,8)",offset=(0,0))
    label(ax,(7,1),"α(x,y) = 2x − y\nT(α,u,v) = 6 − 8 = −2",offset=(0,0))
    arrow(ax,(4,4),(5.5,4),TEAL);arrow(ax,(7,3.5),(7,2),ROSE)
    save(fig,"ch10-tensor")

def ch11():
    fig,axes=canvas("Stress connects a surface normal to a traction",2)
    for ax,n,title in zip(axes,[(1,0),(0,1)],["n = (1,0)","n = (0,1)"]):
        n=np.array(n);t=np.array([[2,1],[1,3]])@n
        tangent=np.array([-n[1],n[0]])*.8
        ax.plot([-tangent[0],tangent[0]],[-tangent[1],tangent[1]],color=GOLD,linewidth=5)
        arrow(ax,(0,0),n,TEAL,"n",(0,-22));arrow(ax,(0,0),t,BLUE,"t = σn",(30,10))
        plane(ax,[(-1,-1),(3,3)],title,(-1.5,3.5,-1.5,3.5))
    save(fig,"ch11-stress")
    fig,axes=canvas("Diffusion can favour one direction",2);theta=np.linspace(0,2*np.pi,180)
    for ax,r,title in zip(axes,[1,2],["isotropic: D = I","anisotropic: D = diag(4,1)"]):
        ax.plot(r*np.cos(theta),np.sin(theta),color=TEAL)
        arrow(ax,(0,0),(-1,-1),BLUE,"∇c",(-24,0));arrow(ax,(0,0),(r*r,1),ROSE,"J = −D∇c",(12,20))
        plane(ax,[(-2,-1),(4,1)],title,(-2.7,5,-2,2))
    fig.text(.09,.035,"At the same time, concentration contours have axis ratio √(Dₓ/Dᵧ).",color=BLUE,fontsize=10);save(fig,"ch11-diffusion")
    panel_arrows("ch11-inertia","Anisotropic inertia can turn angular momentum",[("xy-plane sketch; I = diag(2,3,4)",[
        a((1,1),"ω = (1,1,0)",TEAL,(-48,12)),a((2,3),"L = (2,3,0)",BLUE,(38,0))])])
    fig,(ax,)=canvas("Every data index answers a different question")
    table(ax,[["batch","frame","row","column","channel"],["b","t","r","c","k"]],["index 1","index 2","index 3","index 4","index 5"])
    fig.text(.09,.035,"X[b,t,r,c,k] is one brightness value in a batch of colour videos.",color=BLUE,fontsize=10);save(fig,"ch11-data")
    fig,axes=canvas("A metric changes which arrows have unit length",2)
    for ax,r,title in zip(axes,[1,.5],["g = I: x² + y² = 1","g = diag(4,1): 4x² + y² = 1"]):
        ax.plot(r*np.cos(theta),np.sin(theta),color=TEAL)
        plane(ax,[(-1,-1),(1,1)],title,(-1.5,1.5,-1.5,1.5))
    save(fig,"ch11-metric")
    fig,(ax,)=canvas("Principal directions disentangle a symmetric rule")
    ang=np.pi/6;R=np.array([[np.cos(ang),-np.sin(ang)],[np.sin(ang),np.cos(ang)]])
    xy=R@np.vstack([3*np.cos(theta),np.sin(theta)])
    ax.plot(xy[0],xy[1],color=TEAL)
    arrow(ax,(0,0),R@np.array([3,0]),BLUE,"λ₁ = 3",(0,23))
    arrow(ax,(0,0),R@np.array([0,1]),ROSE,"λ₂ = 1",(-35,0))
    plane(ax,xy.T)
    fig.text(.09,.035,"Ellipse: image of the unit circle under S = R diag(3,1) Rᵀ.",color=BLUE,fontsize=10);save(fig,"ch11-applications")

def ch12():
    fig,axes=canvas("Forms measure objects of the matching degree",4)
    for ax,k in zip(axes,range(4)):
        ax.set_axis_off();ax.set_xlim(0,3);ax.set_ylim(0,3);ax.set_aspect("equal")
        ax.set_title(["0: function","1: path","2: patch","3: volume"][k],color=TEAL,fontsize=11)
        if k==0:label(ax,(1.5,1.5),"f(p) = 2",offset=(0,0))
        elif k==1:arrow(ax,(.3,.6),(2.6,2.3),BLUE)
        elif k==2:polygon(ax,[[.3,.5],[2.4,.5],[2.8,2.3],[.7,2.3]])
        else:
            polygon(ax,[[.3,.5],[2,.5],[2,2],[.3,2]])
            polygon(ax,[[.3,2],[2,2],[2.7,2.7],[1,2.7]],TEAL)
            polygon(ax,[[2,.5],[2.7,1.2],[2.7,2.7],[2,2]],ROSE)
    save(fig,"ch12-forms")
    panel_arrows("ch12-one-form","At a point, a 1-form asks a linear question",[("α = 2 dx − dy",[
        a((1,0),"α(e₁) = 2",BLUE,(0,-22)),a((0,1),"α(e₂) = −1",TEAL,(-50,0)),
        a((1,1),"α(e₁+e₂) = 1",ROSE,(42,20))])],(-1.5,2,-.8,2))
    fig,axes=canvas("dx ∧ dy reads signed parallelogram area",2)
    for ax,u,v,title in zip(axes,[(1,0),(0,1)],[(0,1),(1,0)],["(e₁,e₂): +1","(e₂,e₁): −1"]):
        plane(ax,area(ax,u,v,True),title,(-1,2,-1,2))
    save(fig,"ch12-two-form")
    fig,(ax,)=canvas("df measures the change of a height function")
    x,y=np.meshgrid(np.linspace(-2,2,120),np.linspace(-2,2,120))
    cs=ax.contour(x,y,x*x+y*y,levels=[.5,1,2,3,4],colors=TEAL);ax.clabel(cs,fontsize=10)
    ax.scatter([1],[1],color=BLUE,zorder=5);arrow(ax,(1,1),(1.8,1),ROSE,"direction e₁",(10,22))
    plane(ax,[(-2,-2),(2,2)],limits=(-2.4,2.4,-2.4,2.4))
    fig.text(.09,.035,"At (1,1): df = 2 dx + 2 dy, so df(e₁) = 2.",color=BLUE,fontsize=10);save(fig,"ch12-df")
    fig,(ax,)=canvas("ω = x dy gives more upward weight on the right")
    polygon(ax,[[0,0],[1,0],[1,1],[0,1]])
    for x in [0,.5,1]:
        for y in [.2,.5,.8]:arrow(ax,(x,y),(x,y+.12*x),TEAL,width=1.2)
    label(ax,(-.65,.5),"left edge:\nx = 0",ROSE,(0,0));label(ax,(1.65,.5),"right edge:\n∫ dy = 1",offset=(0,0))
    plane(ax,[(-1,0),(2,1)],limits=(-1.3,2.3,-.6,1.6));save(fig,"ch12-circulation")
    fig,(ax,)=canvas("Interior edges cancel; the outside remains")
    for i in range(2):
        for j in range(2):
            x,y=i/2,j/2
            polygon(ax,[[x,y],[x+.5,y],[x+.5,y+.5],[x,y+.5]],TEAL)
            for p,q in [((x+.08,y+.025),(x+.42,y+.025)),((x+.475,y+.08),(x+.475,y+.42)),
                        ((x+.42,y+.475),(x+.08,y+.475)),((x+.025,y+.42),(x+.025,y+.08))]:
                arrow(ax,p,q,ROSE,width=1.1)
    label(ax,(1.9,.5),"∫∂M x dy = 1\n∫M dx ∧ dy = 1",offset=(0,0))
    plane(ax,[(0,0),(2.7,1)],limits=(-.3,3,-.3,1.3));save(fig,"ch12-stokes")

def story_map():
    fig,axes=plt.subplots(3,4,figsize=(10.2,6.3))
    fig.patch.set_facecolor(PAPER);fig.suptitle("Alice's twelve mathematical rooms",fontsize=18,color=BLUE,weight="bold",y=.98)
    fig.subplots_adjust(top=.86,bottom=.10,left=.04,right=.96,hspace=.35,wspace=.22)
    names=["Arrows","Keyring","Tea machine","Measuring","Card area","Still paths","Two inputs","Area tickets","Pairing table","Costumes","Instruments","Dream map"]
    for i,(ax,name) in enumerate(zip(axes.flat,names),1):
        ax.set_axis_off();ax.set_xlim(0,1);ax.set_ylim(0,1)
        polygon(ax,[[.03,.03],[.97,.03],[.97,.95],[.03,.95]],TEAL)
        label(ax,(.5,.52),f"{i}\n{name}",offset=(0,0))
    fig.text(.5,.025,"Each room introduces an idea by play before naming it.",ha="center",color=BLUE)
    save(fig,"story-map")

def generate_all():
    SAVED.clear()
    for draw in [ch01,ch02,ch03,ch04,ch05,ch06,ch07,ch08,ch09,ch10,ch11,ch12,story_map]:
        draw()
    expected={name for names in FIGURE_NAMES.values() for name in names}|{"story-map"}
    if SAVED!=expected:raise RuntimeError(f"Figure registry mismatch: {SAVED ^ expected}")
    print(f"Generated {len(SAVED)-1} chapter illustrations and the story map.")

if __name__ == "__main__":
    generate_all()
