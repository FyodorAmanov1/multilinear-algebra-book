(function () {
  "use strict";

  const BLUE = "#002147", TEAL = "#0f766e", GOLD = "#946900", ROSE = "#b3375f";
  const INK = "#151515", PAPER = "#fbfbf8", LINE = "#ded9cf";
  const ZERO = { x: 0, y: 0 };
  const WIDTH = 720, HEIGHT = 520;
  let drawingView = { x: 360, y: 260, unit: 58 };
  let metrics = null;

  const point = (x, y) => ({ x, y });
  const plus = (a, b) => point(a.x + b.x, a.y + b.y);
  const times = (a, n) => point(a.x * n, a.y * n);
  const norm = a => Math.hypot(a.x, a.y);
  const finite = p => Number.isFinite(p.x) && Number.isFinite(p.y);
  const clamp = (n, lo, hi) => Math.max(lo, Math.min(hi, n));
  const radians = a => a * Math.PI / 180;
  const degrees = a => (a * 180 / Math.PI + 360) % 360;
  const wave = (time, speed = 1) => .5 + .5 * Math.sin(time * speed);
  const progress = (state, speed) => state.playing ? wave(state.time, speed) : 1;
  const lerp = (a, b, t) => a + (b - a) * t;
  const polar = (angle, length) => point(length * Math.cos(radians(angle)), length * Math.sin(radians(angle)));
  const viewFor = id => id === "tensor-product-builder" ? { x: 220, y: 280, unit: 50 } : { x: 360, y: 260, unit: 58 };
  const toCanvas = v => point(drawingView.x + v.x * drawingView.unit, drawingView.y - v.y * drawingView.unit);
  const number = n => Math.abs(n) < .00005 ? "0" : Math.abs(n) >= 10000 ? n.toExponential(2) : Number(n.toFixed(2)).toString();
  const coordinates = v => `(${number(v.x)}, ${number(v.y)})`;

  function value(id, fallback = 0) {
    const field = document.getElementById(id);
    return field && Number.isFinite(Number(field.value)) ? Number(field.value) : fallback;
  }
  const textValue = (id, fallback) => document.getElementById(id)?.value || fallback;
  const checked = id => Boolean(document.getElementById(id)?.checked);
  const xy = (x, y) => point(value(x), value(y));
  const polarFields = (angle, length) => polar(value(angle), value(length));

  function put(id, n) {
    const field = document.getElementById(id);
    if (!field || !Number.isFinite(n)) return;
    const lo = field.min === "" ? -Infinity : Number(field.min);
    const hi = field.max === "" ? Infinity : Number(field.max);
    const step = Number(field.step) || .1;
    const base = Number.isFinite(lo) ? lo : 0;
    field.value = String(Number(clamp(base + Math.round((clamp(n, lo, hi) - base) / step) * step, lo, hi).toFixed(6)));
  }
  function putXY(x, y, p) { put(x, p.x); put(y, p.y); }
  function putPolar(angle, length, p) {
    if (norm(p) > .00001) put(angle, degrees(Math.atan2(p.y, p.x)));
    put(length, norm(p));
  }

  function line(ctx, a, b, color = INK, width = 1.5, dashed = false) {
    if (!finite(a) || !finite(b)) return;
    const p = toCanvas(a), q = toCanvas(b);
    ctx.beginPath(); ctx.setLineDash(dashed ? [5, 5] : []);
    ctx.moveTo(p.x, p.y); ctx.lineTo(q.x, q.y);
    ctx.strokeStyle = color; ctx.lineWidth = width; ctx.stroke(); ctx.setLineDash([]);
  }
  function arrow(ctx, a, b, color = BLUE, width = 3, label = "") {
    if (!finite(a) || !finite(b)) return;
    const p = toCanvas(a), q = toCanvas(b);
    const len = Math.hypot(q.x - p.x, q.y - p.y);
    if (len < .5) return;
    const ux = (q.x - p.x) / len, uy = (q.y - p.y) / len, head = Math.min(12, len * .25);
    ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(q.x - ux * head, q.y - uy * head);
    ctx.strokeStyle = color; ctx.lineWidth = width; ctx.lineCap = "round"; ctx.stroke();
    ctx.beginPath(); ctx.moveTo(q.x, q.y);
    ctx.lineTo(q.x - ux * head - uy * head * .45, q.y - uy * head + ux * head * .45);
    ctx.lineTo(q.x - ux * head + uy * head * .45, q.y - uy * head - ux * head * .45);
    ctx.closePath(); ctx.fillStyle = color; ctx.fill();
    if (label) { ctx.font = "600 13px system-ui, sans-serif"; ctx.fillText(label, q.x + 12, q.y - 12); }
  }
  function dot(ctx, v, color, radius = 5) {
    if (!finite(v)) return;
    const p = toCanvas(v);
    ctx.beginPath(); ctx.arc(p.x, p.y, radius, 0, Math.PI * 2); ctx.fillStyle = color; ctx.fill();
  }
  function polygon(ctx, points, fill, stroke) {
    if (!points.every(finite)) return;
    const first = toCanvas(points[0]);
    ctx.beginPath(); ctx.moveTo(first.x, first.y);
    points.slice(1).forEach(v => { const p = toCanvas(v); ctx.lineTo(p.x, p.y); });
    ctx.closePath();
    if (fill) { ctx.fillStyle = fill; ctx.fill(); }
    if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = 2; ctx.stroke(); }
  }
  function metric(text, color = INK) { metrics.push({ text, color }); }
  function grid(ctx) {
    ctx.fillStyle = PAPER; ctx.fillRect(0, 0, WIDTH, HEIGHT);
    const { x: cx, y: cy, unit } = drawingView, step = unit / 2;
    ctx.strokeStyle = LINE; ctx.lineWidth = .7;
    for (let x = cx % step; x < WIDTH; x += step) {
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, HEIGHT); ctx.stroke();
    }
    for (let y = cy % step; y < HEIGHT; y += step) {
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(WIDTH, y); ctx.stroke();
    }
    ctx.strokeStyle = "#99958b"; ctx.lineWidth = 1.4;
    ctx.beginPath(); ctx.moveTo(0, cy); ctx.lineTo(WIDTH, cy); ctx.moveTo(cx, 0); ctx.lineTo(cx, HEIGHT); ctx.stroke();
    ctx.fillStyle = "#777269"; ctx.font = "11px system-ui, sans-serif";
    for (let n = -7; n <= 7; n++) {
      const x = cx + n * unit, y = cy - n * unit;
      if (n && x > 12 && x < WIDTH - 15) ctx.fillText(String(n), x - 4, cy + 17);
      if (n && y > 15 && y < HEIGHT - 10) ctx.fillText(String(n), cx + 7, y + 4);
    }
    ctx.fillText("0", cx + 7, cy + 17);
    ctx.fillText("x", WIDTH - 16, cy - 9); ctx.fillText("y", cx + 10, 16);
  }
  const matrix = () => ({ a: value("matrix-a"), b: value("matrix-b"), c: value("matrix-c"), d: value("matrix-d") });
  const applyMatrix = (m, v) => point(m.a * v.x + m.b * v.y, m.c * v.x + m.d * v.y);
  const unitVector = p => norm(p) < 1e-10 ? ZERO : times(p, 1 / norm(p));
  const shortVector = (p, radius = 3.4) => norm(p) > radius ? times(p, radius / norm(p)) : p;

  function drawVectors(ctx, state) {
    grid(ctx);
    const u = xy("vector-a-x", "vector-a-y"), v = xy("vector-b-x", "vector-b-y");
    const sum = plus(u, v), diff = plus(u, times(v, -1)), scale = value("scale", 1);
    polygon(ctx, [ZERO, u, sum, v], "rgba(15,118,110,.07)", "rgba(15,118,110,.28)");
    arrow(ctx, u, sum, "rgba(15,118,110,.45)", 2);
    arrow(ctx, ZERO, sum, GOLD, 4, "u + v");
    arrow(ctx, ZERO, diff, "rgba(179,55,95,.65)", 2, "u - v");
    line(ctx, ZERO, times(u, scale), "rgba(15,118,110,.45)", 5, true);
    arrow(ctx, ZERO, u, BLUE, 4); arrow(ctx, ZERO, v, TEAL, 4);
    if (state.playing) {
      const t = wave(state.time, 1.3) * 2;
      dot(ctx, t < 1 ? times(u, t) : plus(u, times(v, t - 1)), ROSE, 7);
    }
    metric(`u = ${coordinates(u)}`, BLUE); metric(`v = ${coordinates(v)}`, TEAL);
    metric(`u + v = ${coordinates(sum)}`, GOLD); metric(`${number(scale)}u = ${coordinates(times(u, scale))}`);
  }

  function drawBasis(ctx, state) {
    grid(ctx);
    const u = polarFields("basis-a-angle", "basis-a-length"), v = polarFields("basis-b-angle", "basis-b-length");
    const p = xy("point-x", "point-y"), det = u.x * v.y - u.y * v.x;
    arrow(ctx, ZERO, u, BLUE, 4); arrow(ctx, ZERO, v, TEAL, 4); arrow(ctx, ZERO, p, GOLD, 4);
    metric(`b1 = ${coordinates(u)}`, BLUE); metric(`b2 = ${coordinates(v)}`, TEAL);
    metric(`p = ${coordinates(p)}`, GOLD);
    if (Math.abs(det) < 1e-4 * Math.max(1, norm(u) * norm(v))) {
      metric("Dependent directions: this pair is not a basis.", ROSE);
      metric("Coordinates in this pair are not uniquely defined.", ROSE);
      return;
    }
    const c1 = (p.x * v.y - p.y * v.x) / det, c2 = (u.x * p.y - u.y * p.x) / det;
    if (Math.max(Math.abs(c1), Math.abs(c2)) < 40) {
      const first = times(u, c1), t = progress(state, 1.1);
      line(ctx, ZERO, first, "rgba(0,33,71,.4)", 3, true);
      line(ctx, first, p, "rgba(15,118,110,.5)", 3, true);
      if (state.playing) dot(ctx, times(p, t), ROSE, 6);
    }
    metric(`p = ${number(c1)} b1 ${c2 < 0 ? "-" : "+"} ${number(Math.abs(c2))} b2`);
    metric(`det = ${number(det)}${Math.abs(det) < .1 ? " (nearly dependent)" : ""}`, Math.abs(det) < .1 ? ROSE : TEAL);
  }

  function drawMatrix(ctx, state, determinantOnly = false) {
    grid(ctx);
    const target = matrix(), t = progress(state, .8);
    const shown = { a: lerp(1, target.a, t), b: target.b * t, c: target.c * t, d: lerp(1, target.d, t) };
    const map = p => applyMatrix(shown, p), det = shown.a * shown.d - shown.b * shown.c;
    if (!determinantOnly) {
      for (let i = -6; i <= 6; i++) {
        line(ctx, map(point(i, -5)), map(point(i, 5)), "rgba(15,118,110,.25)");
        line(ctx, map(point(-6, i)), map(point(6, i)), "rgba(15,118,110,.25)");
      }
    }
    polygon(ctx, [ZERO, point(1, 0), point(1, 1), point(0, 1)], "rgba(15,118,110,.06)", "rgba(15,118,110,.45)");
    polygon(ctx, [ZERO, map(point(1, 0)), map(point(1, 1)), map(point(0, 1))], det >= 0 ? "rgba(201,162,39,.23)" : "rgba(179,55,95,.2)", det >= 0 ? GOLD : ROSE);
    arrow(ctx, ZERO, map(point(1, 0)), BLUE, 4); arrow(ctx, ZERO, map(point(0, 1)), TEAL, 4);
    if (!determinantOnly) {
      const p = xy("point-x", "point-y"), mapped = map(p);
      dot(ctx, mapped, ROSE, 6); line(ctx, p, mapped, "rgba(179,55,95,.4)", 1.5, true);
      arrow(ctx, ZERO, p, GOLD, 2);
      metric(`p = ${coordinates(p)}; ${state.playing ? "target " : ""}A p = ${coordinates(applyMatrix(target, p))}`, ROSE);
    }
    metric(`A = [${number(target.a)}, ${number(target.b)}; ${number(target.c)}, ${number(target.d)}]`, BLUE);
    metric(`det A = ${number(target.a * target.d - target.b * target.c)}`, TEAL);
    metric(Math.abs(det) < 1e-8 ? "Collapsed: the two columns enclose no area." : det > 0 ? "Current square: positive orientation" : "Current square: orientation reversed", Math.abs(det) < 1e-8 ? ROSE : GOLD);
    if (state.playing) metric(`Animated area scale = ${number(det)}`);
  }

  function drawInnerProduct(ctx, state) {
    grid(ctx);
    const u = polarFields("u-angle", "u-length"), v = polarFields("v-angle", "v-length");
    const product = u.x * v.x + u.y * v.y, squared = v.x * v.x + v.y * v.y;
    arrow(ctx, ZERO, u, BLUE, 4); arrow(ctx, ZERO, v, TEAL, 4);
    metric(`u = ${coordinates(u)}`, BLUE); metric(`v = ${coordinates(v)}`, TEAL);
    metric(`u dot v = ${number(product)}`, GOLD);
    if (squared < 1e-10) {
      metric("Projection onto the zero vector is undefined.", ROSE);
    } else {
      const projection = times(v, product / squared);
      arrow(ctx, ZERO, projection, GOLD, 4, "projection"); line(ctx, u, projection, ROSE, 2, true);
      if (state.playing) { const t = wave(state.time, 1.2); dot(ctx, point(lerp(u.x, projection.x, t), lerp(u.y, projection.y, t)), ROSE, 6); }
      metric(`Projection = ${coordinates(projection)}`, GOLD);
    }
    if (norm(u) < 1e-8 || norm(v) < 1e-8) metric("An angle needs two nonzero vectors.", ROSE);
    else metric(`Angle = ${number(Math.acos(clamp(product / (norm(u) * norm(v)), -1, 1)) * 180 / Math.PI)} degrees${Math.abs(product) < .01 ? " (orthogonal!)" : ""}`);
  }

  function realEigenpairs(m) {
    const trace = m.a + m.d, disc = (m.a - m.d) ** 2 + 4 * m.b * m.c;
    if (disc < -1e-9) return [];
    const root = Math.sqrt(Math.max(0, disc));
    return [(trace + root) / 2, (trace - root) / 2].map((lambda, i) => {
      let v = point(m.b, lambda - m.a), alternative = point(lambda - m.d, m.c);
      if (norm(alternative) > norm(v)) v = alternative;
      if (norm(v) < 1e-9) v = i ? point(0, 1) : point(1, 0);
      return { lambda, v: unitVector(v) };
    });
  }
  function drawEigenvectors(ctx, state) {
    grid(ctx);
    const m = matrix(), count = Math.round(value("iterations", 4));
    arrow(ctx, ZERO, point(m.a, m.c), "rgba(0,33,71,.35)", 2);
    arrow(ctx, ZERO, point(m.b, m.d), "rgba(15,118,110,.35)", 2);
    const steps = state.playing ? Math.max(1, Math.ceil(count * wave(state.time, value("speed", 1)))) : count;
    for (let j = 0; j < 16; j++) {
      let p = polar(j * 22.5, 1);
      for (let k = 0; k < steps; k++) {
        const next = times(unitVector(applyMatrix(m, p)), 1 + (k + 1) * .15);
        line(ctx, p, next, "rgba(15,118,110,.15)", 1.5); p = next;
      }
    }
    const pairs = realEigenpairs(m);
    pairs.forEach((pair, index) => {
      const color = index ? ROSE : GOLD;
      line(ctx, times(pair.v, -4), times(pair.v, 4), color, 2, true);
      metric(`Eigenvalue ${index + 1} = ${number(pair.lambda)}`, color);
    });
    if (!pairs.length) metric("Complex eigenvalues: no real eigenvector direction.", ROSE);
    const v = xy("probe-x", "probe-y"), mapped = applyMatrix(m, v);
    arrow(ctx, ZERO, v, GOLD, 4); arrow(ctx, ZERO, shortVector(mapped), TEAL, 4, norm(mapped) > 3.4 ? "A v (shortened)" : "A v");
    let repeated = v;
    for (let k = 0; k < count; k++) repeated = applyMatrix(m, repeated);
    arrow(ctx, ZERO, times(unitVector(repeated), 2.8), "rgba(179,55,95,.6)", 2, `direction of A^${count}v`);
    metric(`A v = ${coordinates(mapped)}`, TEAL); metric(`A^${count} v = ${coordinates(repeated)}`);
    metric("Faint trails show normalized directions; columns set the matrix.");
  }

  function drawBilinear(ctx, state) {
    grid(ctx);
    const a = value("form-a", 1), b = value("form-b", .5), c = value("form-c", 1), cell = .22;
    for (let x = -6.3; x < 6.3; x += cell) for (let y = -4.6; y < 4.6; y += cell) {
      const q = a * x * x + 2 * b * x * y + c * y * y;
      const p = toCanvas(point(x, y + cell));
      ctx.fillStyle = q >= 0 ? `rgba(15,118,110,${Math.min(.25, Math.abs(q) * .025)})` : `rgba(179,55,95,${Math.min(.25, Math.abs(q) * .025)})`;
      ctx.fillRect(p.x, p.y, cell * drawingView.unit + 1, cell * drawingView.unit + 1);
    }
    const v = xy("probe-x", "probe-y"), bv = point(a * v.x + b * v.y, b * v.x + c * v.y), q = v.x * bv.x + v.y * bv.y;
    arrow(ctx, ZERO, point(a, b), "rgba(15,118,110,.4)", 2);
    arrow(ctx, ZERO, point(b, c), "rgba(179,55,95,.4)", 2);
    arrow(ctx, ZERO, shortVector(bv), GOLD, 3, norm(bv) > 3.4 ? "Bv (shortened)" : "Bv");
    arrow(ctx, ZERO, v, BLUE, 4);
    if (state.playing) dot(ctx, v, q >= 0 ? TEAL : ROSE, 5 + 4 * wave(state.time, 2));
    const det = a * c - b * b;
    metric(`B = [${number(a)}, ${number(b)}; ${number(b)}, ${number(c)}]`, BLUE);
    metric(`B(v,v) = ${number(q)}`, q >= 0 ? TEAL : ROSE);
    metric(Math.abs(det) < 1e-8 ? "Degenerate form" : det < 0 ? "Indefinite: positive and negative directions" : a > 0 ? "Positive definite" : "Negative definite");
    metric("The two coefficient handles stay symmetric: changing b moves both.");
  }

  function drawWedge(ctx, state) {
    grid(ctx);
    const u = polarFields("u-angle", "u-length"), v = polarFields("v-angle", "v-length");
    const area = u.x * v.y - u.y * v.x, t = progress(state, .9), color = area < 0 ? ROSE : GOLD;
    polygon(ctx, [ZERO, u, plus(u, v), v], null, color);
    polygon(ctx, [ZERO, u, plus(u, times(v, t)), times(v, t)], area < 0 ? "rgba(179,55,95,.24)" : "rgba(201,162,39,.25)");
    arrow(ctx, ZERO, u, BLUE, 4); arrow(ctx, ZERO, v, TEAL, 4);
    metric(`u wedge v = ${number(area)} (e1 wedge e2)`, BLUE);
    metric(`Area = ${number(Math.abs(area))}`, GOLD);
    metric(Math.abs(area) < 1e-8 ? "Parallel or zero vectors: the area has collapsed." : area > 0 ? "Counterclockwise orientation" : "Clockwise orientation", color);
  }

  const tensorLayout = { x: 464, y: 140, cell: 44 };
  function productSize() { return Math.round(value("basis-size", 3)); }
  function productValue(row, col) {
    const u = [value("u-x"), value("u-y")], v = [value("v-x"), value("v-y")];
    return (u[row] || 0) * (v[col] || 0);
  }
  function drawTensorProduct(ctx, state) {
    grid(ctx);
    const u = xy("u-x", "u-y"), v = xy("v-x", "v-y"), size = productSize();
    arrow(ctx, ZERO, u, BLUE, 4); arrow(ctx, ZERO, v, TEAL, 4);
    ctx.fillStyle = "#f8f5ee"; ctx.fillRect(430, 0, 290, HEIGHT);
    ctx.strokeStyle = LINE; ctx.beginPath(); ctx.moveTo(430, 0); ctx.lineTo(430, HEIGHT); ctx.stroke();
    ctx.fillStyle = BLUE; ctx.font = "700 18px system-ui, sans-serif"; ctx.fillText("The product table", 450, 39);
    ctx.font = "13px system-ui, sans-serif"; ctx.fillText("Click a cell to inspect its coefficient.", 450, 66);
    const { x, y, cell } = tensorLayout;
    const active = state.playing ? Math.min(size * size - 1, Math.floor(wave(state.time, 1.1) * size * size)) : state.selectedProduct;
    for (let row = 0; row < size; row++) for (let col = 0; col < size; col++) {
      const coefficient = productValue(row, col), selected = row * size + col === active;
      const px = x + col * cell, py = y + row * cell;
      ctx.fillStyle = selected ? "#f1db91" : coefficient > 0 ? "#d8eee7" : coefficient < 0 ? "#f2dce3" : "#eae7df";
      ctx.fillRect(px, py, cell - 4, cell - 4);
      if (selected) { ctx.strokeStyle = GOLD; ctx.lineWidth = 2.5; ctx.strokeRect(px, py, cell - 4, cell - 4); }
      ctx.fillStyle = BLUE; ctx.font = "600 12px system-ui, sans-serif"; ctx.textAlign = "center";
      ctx.fillText(number(coefficient), px + 20, py + 25);
    }
    ctx.font = "12px system-ui, sans-serif";
    for (let i = 0; i < size; i++) {
      ctx.fillText(`v${i + 1}`, x + i * cell + 20, y - 12);
      ctx.fillText(`u${i + 1}`, x - 18, y + i * cell + 25);
    }
    ctx.textAlign = "start";
    const row = Math.floor(active / size), col = active % size;
    metric(`u = ${coordinates(u)}; v = ${coordinates(v)}`, BLUE);
    metric(`Coefficient of e${row + 1} tensor e${col + 1}: ${number(productValue(row, col))}`, GOLD);
    metric(`${size} x ${size} = ${size * size} basis products`);
    if (size > 2) metric("Only the first two vector components are nonzero; the extra components are zero.");
  }

  function drawComponents(ctx, state) {
    grid(ctx);
    const targetAngle = value("angle", 30), angle = radians(targetAngle * progress(state, .7));
    const c = Math.cos(angle), s = Math.sin(angle), kind = textValue("tensor-type", "vector"), lower = textValue("covariance", "upper") === "lower";
    const b1 = point(c, s), b2 = point(-s, c), object = xy("object-x", "object-y");
    line(ctx, times(b1, -5), times(b1, 5), "rgba(0,33,71,.25)", 2, true);
    line(ctx, times(b2, -5), times(b2, 5), "rgba(15,118,110,.25)", 2, true);
    arrow(ctx, ZERO, b1, BLUE, 3); arrow(ctx, ZERO, b2, TEAL, 3);
    metric(`Frame angle = ${number(targetAngle)} degrees`, BLUE);
    if (kind === "bilinear form") {
      const a = object.x, d = object.y;
      for (let x = -5.8; x < 5.8; x += .3) for (let y = -4.3; y < 4.3; y += .3) {
        const q = a * x * x + d * y * y, p = toCanvas(point(x, y + .3));
        ctx.fillStyle = q >= 0 ? "rgba(15,118,110,.08)" : "rgba(179,55,95,.1)";
        ctx.fillRect(p.x, p.y, .3 * drawingView.unit, .3 * drawingView.unit);
      }
      arrow(ctx, ZERO, point(a, 0), GOLD, 4); arrow(ctx, ZERO, point(0, d), ROSE, 4);
      metric(`Fixed form = diag(${number(a)}, ${number(d)})`, GOLD);
      metric(`In this frame: [${number(a * c * c + d * s * s)}, ${number((d - a) * c * s)}; ${number((d - a) * c * s)}, ${number(a * s * s + d * c * c)}]`);
    } else {
      arrow(ctx, ZERO, object, GOLD, 4);
      const first = object.x * c + object.y * s, second = -object.x * s + object.y * c;
      line(ctx, object, times(b1, first), "rgba(201,162,39,.6)", 2, true);
      metric(`${kind === "covector" ? "Covector" : "Vector"} in the fixed frame = ${coordinates(object)}`, GOLD);
      metric(`${lower ? "Lower" : "Upper"} components in the rotated frame = (${number(first)}, ${number(second)})`);
    }
    metric("This frame is orthonormal: upper and lower components have the same numerical rotation rule.");
  }

  function drawApplications(ctx, state) {
    grid(ctx);
    const a = value("stress-a", 1.5), b = value("stress-b", .7), ratio = value("diffusion-ratio", 1);
    const S = { a, b, c: b, d: a };
    ctx.beginPath();
    for (let i = 0; i <= 180; i++) {
      const p = toCanvas(applyMatrix(S, polar(i * 2, 1)));
      if (!i) ctx.moveTo(p.x, p.y); else ctx.lineTo(p.x, p.y);
    }
    ctx.strokeStyle = BLUE; ctx.lineWidth = 3; ctx.stroke();
    const axis1 = times(point(1, 1), (a + b) / Math.SQRT2), axis2 = times(point(-1, 1), (a - b) / Math.SQRT2);
    line(ctx, ZERO, axis1, BLUE, 2); line(ctx, ZERO, axis2, TEAL, 2);
    for (let i = 0; i < 16; i++) {
      const angle = i * 22.5, dir = polar(angle, 1);
      const D = { a: ratio, b: .25 * ratio, c: .25 * ratio, d: ratio };
      const breath = state.playing ? .75 + .25 * Math.sin(state.time * 1.4 - radians(angle) * 2) : 1;
      arrow(ctx, dir, plus(dir, times(applyMatrix(D, dir), .55 * breath)), "rgba(15,118,110,.65)", 2);
    }
    line(ctx, point(.15, -3), point(4.5, -3), "rgba(179,55,95,.35)", 3);
    metric(`Stress S = [${number(a)}, ${number(b)}; ${number(b)}, ${number(a)}]`, BLUE);
    metric(`Principal stresses = ${number(a + b)}, ${number(a - b)}`, TEAL);
    metric(`Diffusion scale = ${number(ratio)}`, ROSE);
    metric("Drag the two principal-axis handles; the bottom handle changes diffusion.");
  }

  function drawForms(ctx, state) {
    grid(ctx);
    const a = value("form-a", 1), b = value("form-b", .5), length = Math.hypot(a, b);
    if (length > 1e-8) {
      const normal = point(a / length, b / length), tangent = point(-normal.y, normal.x);
      for (let k = -10; k <= 10; k++) {
        const center = times(normal, k / length);
        line(ctx, plus(center, times(tangent, -9)), plus(center, times(tangent, 9)), k ? "rgba(15,118,110,.3)" : "rgba(21,21,21,.4)", k ? 1 : 2);
      }
    }
    const v = xy("probe-x", "probe-y"), measured = a * v.x + b * v.y;
    if (checked("show-area")) {
      const anchor = point(-2, -1), corner = xy("area-x", "area-y");
      const measuredArea = a * (corner.x - anchor.x) * (corner.y - anchor.y);
      polygon(ctx, [anchor, point(corner.x, anchor.y), corner, point(anchor.x, corner.y)], measuredArea < 0 ? "rgba(179,55,95,.2)" : "rgba(201,162,39,.23)", GOLD);
      dot(ctx, anchor, GOLD, 4);
      metric(`Area form on the patch = ${number(measuredArea)}`, GOLD);
    }
    arrow(ctx, ZERO, point(a, b), BLUE, 4); arrow(ctx, ZERO, v, TEAL, 4);
    if (state.playing) dot(ctx, v, measured < 0 ? ROSE : TEAL, 5 + 4 * wave(state.time, 2));
    metric(`alpha = ${number(a)} dx ${b < 0 ? "-" : "+"} ${number(Math.abs(b))} dy`, BLUE);
    metric(`alpha(v) = ${number(measured)}`, measured < 0 ? ROSE : TEAL);
    metric(`Area form = ${number(a)} dx wedge dy`);
    metric(length < 1e-8 ? "The zero 1-form measures every vector as zero." : "Each parallel line is an integer level of alpha(x,y).");
  }

  function xyHandle(id, name, x, y, color, short = name) {
    return { id, name, color, short, get: () => xy(x, y), set: p => putXY(x, y, p) };
  }
  function polarHandle(id, name, angle, length, color, short = name) {
    return { id, name, color, short, get: () => polarFields(angle, length), set: p => putPolar(angle, length, p) };
  }
  function matrixHandles() {
    return [xyHandle("col1", "First matrix column", "matrix-a", "matrix-c", BLUE, "A e1"), xyHandle("col2", "Second matrix column", "matrix-b", "matrix-d", TEAL, "A e2")];
  }
  function getHandles(id) {
    switch (id) {
      case "vector-playground": return [xyHandle("u", "Vector u", "vector-a-x", "vector-a-y", BLUE, "u"), xyHandle("v", "Vector v", "vector-b-x", "vector-b-y", TEAL, "v")];
      case "basis-explorer": return [polarHandle("b1", "Basis vector b1", "basis-a-angle", "basis-a-length", BLUE, "b1"), polarHandle("b2", "Basis vector b2", "basis-b-angle", "basis-b-length", TEAL, "b2"), xyHandle("point", "Point p", "point-x", "point-y", GOLD, "p")];
      case "linear-map-theater": return [...matrixHandles(), xyHandle("point", "Input point p", "point-x", "point-y", GOLD, "p")];
      case "determinant-volume": return matrixHandles();
      case "inner-product-lab":
      case "wedge-areas": return [polarHandle("u", "Vector u", "u-angle", "u-length", BLUE, "u"), polarHandle("v", "Vector v", "v-angle", "v-length", TEAL, "v")];
      case "eigenvector-dance": return [...matrixHandles(), xyHandle("probe", "Starting vector v", "probe-x", "probe-y", GOLD, "v")];
      case "bilinear-form-lab": return [xyHandle("col1", "First form column", "form-a", "form-b", TEAL, "B e1"), xyHandle("col2", "Second form column", "form-b", "form-c", ROSE, "B e2"), xyHandle("probe", "Test vector v", "probe-x", "probe-y", BLUE, "v")];
      case "tensor-product-builder": return [xyHandle("u", "Vector u", "u-x", "u-y", BLUE, "u"), xyHandle("v", "Vector v", "v-x", "v-y", TEAL, "v")];
      case "component-transformer": {
        const bases = [
          { id: "b1", name: "Rotate basis b1", short: "b1", color: BLUE, get: () => polar(value("angle"), 1), set: p => { if (norm(p) > 1e-8) put("angle", degrees(Math.atan2(p.y, p.x))); } },
          { id: "b2", name: "Rotate basis b2", short: "b2", color: TEAL, get: () => polar(value("angle") + 90, 1), set: p => { if (norm(p) > 1e-8) put("angle", degrees(Math.atan2(p.y, p.x) - Math.PI / 2)); } }
        ];
        if (textValue("tensor-type", "vector") !== "bilinear form") return [...bases, xyHandle("object", "Fixed object", "object-x", "object-y", GOLD, "object")];
        return [...bases,
          { id: "coefficient1", name: "First form coefficient", short: "a", color: GOLD, get: () => point(value("object-x"), 0), set: p => put("object-x", p.x) },
          { id: "coefficient2", name: "Second form coefficient", short: "c", color: ROSE, get: () => point(0, value("object-y")), set: p => put("object-y", p.y) }
        ];
      }
      case "tensor-applications": return [
        { id: "stress1", name: "First principal stress", short: "stress 1", color: BLUE, get: () => times(point(1, 1), (value("stress-a") + value("stress-b")) / Math.SQRT2), set: p => {
          const next = (p.x + p.y) / Math.SQRT2, other = value("stress-a") - value("stress-b");
          put("stress-a", (next + other) / 2); put("stress-b", (next - other) / 2);
        } },
        { id: "stress2", name: "Second principal stress", short: "stress 2", color: TEAL, get: () => times(point(-1, 1), (value("stress-a") - value("stress-b")) / Math.SQRT2), set: p => {
          const next = (-p.x + p.y) / Math.SQRT2, other = value("stress-a") + value("stress-b");
          put("stress-a", (next + other) / 2); put("stress-b", (other - next) / 2);
        } },
        { id: "diffusion", name: "Diffusion scale", short: "diffusion", color: ROSE, get: () => point(value("diffusion-ratio") * 1.5, -3), set: p => put("diffusion-ratio", p.x / 1.5) }
      ];
      case "forms-and-fields": return [xyHandle("form", "1-form coefficients", "form-a", "form-b", BLUE, "alpha"), xyHandle("probe", "Test vector v", "probe-x", "probe-y", TEAL, "v"), ...(checked("show-area") ? [xyHandle("patch", "Area patch corner", "area-x", "area-y", GOLD, "patch")] : [])];
      default: return [];
    }
  }

  const instructions = {
    "vector-playground": "Drag the blue u or teal v arrow tip. Click an empty place on the grid to move the selected vector; the sum and difference update immediately.",
    "basis-explorer": "Drag either basis arrow or the gold point. Try lining up the two basis directions and watch what happens to the coordinates.",
    "linear-map-theater": "Drag the two matrix-column tips to reshape the entire grid. Move the gold input point to see where the transformation sends it.",
    "inner-product-lab": "Drag the u and v arrow tips to change their lengths and angle. Watch the gold projection and the dot product.",
    "determinant-volume": "Drag either column tip to stretch, reverse, or collapse the parallelogram. The signed area changes as you move.",
    "eigenvector-dance": "Drag the matrix columns or the starting vector. Try aligning v with a dashed eigenvector line; A v then stays on that line.",
    "bilinear-form-lab": "Drag the test vector through the colored field, or drag the form-column handles to reshape it. The two form columns share the coefficient b.",
    "wedge-areas": "Drag u and v around the origin. Swap their orientation or bring them into line to explore signed area.",
    "tensor-product-builder": "Drag u and v on the left grid. Click a cell in the product table to see which pair of components produces its value.",
    "component-transformer": "Drag b1 or b2 around the origin to rotate the frame. Move the gold object, or edit the form coefficients when that type is selected.",
    "tensor-applications": "Drag the stress handles along their diagonal axes. Drag the rose handle along the bottom rail to change the diffusion scale.",
    "forms-and-fields": "Drag the blue 1-form tip or the teal test vector. With the area form visible, drag the gold patch corner to change its signed measurement."
  };
  const renderers = {
    "vector-playground": drawVectors, "basis-explorer": drawBasis,
    "linear-map-theater": (ctx, state) => drawMatrix(ctx, state), "inner-product-lab": drawInnerProduct,
    "determinant-volume": (ctx, state) => drawMatrix(ctx, state, true), "eigenvector-dance": drawEigenvectors,
    "bilinear-form-lab": drawBilinear, "wedge-areas": drawWedge, "tensor-product-builder": drawTensorProduct,
    "component-transformer": drawComponents, "tensor-applications": drawApplications, "forms-and-fields": drawForms
  };

  function drawHandles(ctx, handles, state) {
    handles.forEach(handle => {
      const p = toCanvas(handle.get());
      if (!finite(p)) return;
      const active = state.active === handle.id, hovered = state.hover === handle.id;
      ctx.beginPath(); ctx.arc(p.x, p.y, active ? 15 : hovered ? 13 : 10, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(255,255,255,.88)"; ctx.fill();
      ctx.strokeStyle = handle.color; ctx.lineWidth = active || hovered ? 2.5 : 1.5; ctx.stroke();
      ctx.beginPath(); ctx.arc(p.x, p.y, 5, 0, Math.PI * 2); ctx.fillStyle = handle.color; ctx.fill();
      ctx.font = `${active ? 700 : 600} 13px system-ui, sans-serif`;
      const w = ctx.measureText(handle.short).width;
      const left = p.x > WIDTH - w - 35 ? p.x - w - 20 : p.x + 17;
      const top = p.y < 30 ? p.y + 27 : p.y - 13;
      ctx.fillStyle = "rgba(255,255,255,.9)"; ctx.fillRect(left - 3, top - 13, w + 6, 18);
      ctx.fillStyle = handle.color; ctx.fillText(handle.short, left, top);
    });
  }

  function setupDemo(id) {
    const canvas = document.getElementById(id);
    if (!canvas) return;
    const ctx = canvas.getContext("2d"), shell = canvas.closest(".demo-shell");
    if (!ctx || !shell) return;
    const state = { playing: false, time: 0, last: null, raf: null, active: getHandles(id)[0]?.id, hover: null, pointer: null, offset: ZERO, selectedProduct: 0 };
    const choices = shell.querySelector(".demo-objects"), liveValues = shell.querySelector(".demo-values");
    const instruction = shell.querySelector(".demo-instructions"), selection = shell.querySelector(".demo-selection");
    const playButton = shell.querySelector(".demo-play"), status = shell.querySelector(".demo-state"), announcer = shell.querySelector(".demo-announcer");
    const controls = Array.from(shell.querySelectorAll(".demo-controls input, .demo-controls select"));
    const initial = controls.map(field => ({ field, value: field.value, checked: field.checked }));
    const view = viewFor(id);
    let handles = getHandles(id), choiceKey = "", productSelect, productCount = 0;
    if (instruction) instruction.textContent = instructions[id];
    const announce = text => { if (announcer) announcer.textContent = text; };
    const activeHandle = () => handles.find(handle => handle.id === state.active) || handles[0];

    function syncFields() {
      controls.forEach(field => {
        const output = shell.querySelector(`output[for="${field.id}"]`);
        if (output) output.value = field.type === "range" ? number(Number(field.value)) : field.value;
      });
    }
    function syncChoices() {
      const key = handles.map(handle => handle.id).join("|");
      if (choices && key !== choiceKey) {
        choices.replaceChildren(); choiceKey = key;
        handles.forEach(handle => {
          const button = document.createElement("button");
          button.type = "button"; button.className = "demo-object"; button.dataset.handle = handle.id;
          button.style.setProperty("--handle-color", handle.color);
          button.textContent = handle.name;
          button.addEventListener("click", () => { finishPointer(); pause(); state.active = handle.id; render(); announce(`${handle.name} selected. Click on the grid or use its arrow keys.`); });
          choices.append(button);
        });
      }
      choices?.querySelectorAll("button").forEach(button => button.setAttribute("aria-pressed", String(button.dataset.handle === state.active)));
      const handle = activeHandle();
      if (selection && handle) selection.textContent = `${handle.name}: ${coordinates(handle.get())}`;
    }
    function syncMetrics() {
      if (!liveValues) return;
      while (liveValues.children.length > metrics.length) liveValues.lastElementChild.remove();
      metrics.forEach((entry, i) => {
        let node = liveValues.children[i];
        if (!node) { node = document.createElement("p"); node.className = "demo-value"; liveValues.append(node); }
        if (node.textContent !== entry.text) node.textContent = entry.text;
        node.style.setProperty("--metric-color", entry.color);
      });
    }
    function syncProducts() {
      if (!productSelect) return;
      const size = productSize();
      state.selectedProduct = clamp(state.selectedProduct, 0, size * size - 1);
      if (productCount !== size) {
        productSelect.replaceChildren(); productCount = size;
        for (let i = 0; i < size * size; i++) { const option = document.createElement("option"); option.value = String(i); productSelect.append(option); }
      }
      Array.from(productSelect.options).forEach((option, i) => { option.textContent = `u${Math.floor(i / size) + 1} x v${i % size + 1} = ${number(productValue(Math.floor(i / size), i % size))}`; });
      productSelect.value = String(state.selectedProduct);
    }
    if (id === "tensor-product-builder") {
      const extra = shell.querySelector(".demo-extra"), label = document.createElement("label");
      label.className = "demo-product-inspector"; label.textContent = "Inspect a product coefficient ";
      productSelect = document.createElement("select"); productSelect.setAttribute("aria-label", "Product coefficient");
      productSelect.addEventListener("change", () => { pause(); state.selectedProduct = Number(productSelect.value); render(); announce(productSelect.selectedOptions[0].textContent); });
      label.append(productSelect); extra?.append(label);
    }
    function render() {
      drawingView = view; metrics = [];
      handles = getHandles(id);
      if (!handles.some(handle => handle.id === state.active)) state.active = handles[0]?.id;
      state.selectedProduct = clamp(state.selectedProduct, 0, productSize() ** 2 - 1);
      ctx.clearRect(0, 0, WIDTH, HEIGHT);
      renderers[id](ctx, state); drawHandles(ctx, handles, state);
      syncFields(); syncChoices(); syncMetrics(); syncProducts();
    }
    function animationUI() {
      if (playButton) {
        playButton.textContent = state.playing ? "Pause animation" : "Play animation";
        playButton.setAttribute("aria-pressed", String(state.playing));
        playButton.classList.toggle("is-playing", state.playing);
      }
      if (status) status.textContent = state.playing ? "Animation playing" : "Paused - ready to explore";
    }
    function pause() {
      state.playing = false;
      if (state.raf !== null) window.cancelAnimationFrame(state.raf);
      state.raf = null; state.last = null; animationUI();
    }
    function frame(now) {
      if (!state.playing) return;
      if (state.last !== null) state.time += Math.min(.05, (now - state.last) / 1000);
      state.last = now; render(); state.raf = window.requestAnimationFrame(frame);
    }
    playButton?.addEventListener("click", () => {
      finishPointer();
      if (state.playing) { pause(); render(); }
      else { state.playing = true; state.last = null; animationUI(); state.raf = window.requestAnimationFrame(frame); }
    });
    function finishPointer() {
      const pointer = state.pointer;
      state.pointer = null; canvas.classList.remove("is-dragging");
      if (pointer !== null && canvas.hasPointerCapture(pointer)) canvas.releasePointerCapture(pointer);
      canvas.style.cursor = "crosshair";
    }
    function reset() {
      finishPointer(); pause();
      initial.forEach(entry => { entry.field.value = entry.value; entry.field.checked = entry.checked; });
      state.time = 0; state.selectedProduct = 0; state.active = getHandles(id)[0]?.id;
      render(); announce("The original example has been restored.");
    }
    shell.querySelector(".demo-reset")?.addEventListener("click", reset);
    controls.forEach(field => {
      const onChange = () => { finishPointer(); pause(); render(); };
      field.addEventListener("input", onChange); field.addEventListener("change", onChange);
    });
    function position(event) {
      const rect = canvas.getBoundingClientRect();
      const pixel = point((event.clientX - rect.left) * WIDTH / rect.width, (event.clientY - rect.top) * HEIGHT / rect.height);
      return { pixel, world: point((pixel.x - view.x) / view.unit, (view.y - pixel.y) / view.unit), rect };
    }
    function hitHandle(event) {
      const { pixel, rect } = position(event), radius = event.pointerType === "touch" ? 30 : 22;
      drawingView = view;
      return handles.map(handle => {
        const p = toCanvas(handle.get());
        const distance = Math.hypot((p.x - pixel.x) * rect.width / WIDTH, (p.y - pixel.y) * rect.height / HEIGHT);
        return { handle, distance };
      }).filter(hit => hit.distance <= radius).sort((a, b) => Math.abs(a.distance - b.distance) < 3 ? (a.handle.id === state.active ? -1 : b.handle.id === state.active ? 1 : a.distance - b.distance) : a.distance - b.distance)[0]?.handle;
    }
    function productAt(pixel) {
      if (id !== "tensor-product-builder") return null;
      const { x, y, cell } = tensorLayout, size = productSize();
      const col = Math.floor((pixel.x - x) / cell), row = Math.floor((pixel.y - y) / cell);
      if (col < 0 || row < 0 || col >= size || row >= size) return null;
      return row * size + col;
    }
    canvas.addEventListener("pointerdown", event => {
      if (!event.isPrimary || event.button !== 0 || state.pointer !== null) return;
      const { world, pixel } = position(event), hit = hitHandle(event), product = productAt(pixel);
      if (!hit && product !== null) {
        event.preventDefault(); pause(); state.selectedProduct = product; render(); announce(productSelect?.selectedOptions[0].textContent || "Product selected."); return;
      }
      if (id === "tensor-product-builder" && pixel.x >= 430 && !hit) return;
      event.preventDefault(); pause(); canvas.focus({ preventScroll: true });
      if (hit) {
        state.active = hit.id; const p = hit.get(); state.offset = point(p.x - world.x, p.y - world.y);
      } else {
        state.offset = ZERO; activeHandle()?.set(world);
      }
      state.pointer = event.pointerId; canvas.setPointerCapture(event.pointerId); canvas.classList.add("is-dragging");
      render();
    });
    canvas.addEventListener("pointermove", event => {
      if (state.pointer !== null) {
        if (state.pointer !== event.pointerId) return;
        event.preventDefault(); activeHandle()?.set(plus(position(event).world, state.offset)); render();
      } else {
        const hit = hitHandle(event), product = productAt(position(event).pixel);
        state.hover = hit?.id || null; canvas.style.cursor = hit ? "grab" : product !== null ? "pointer" : "crosshair";
        render();
      }
    });
    canvas.addEventListener("pointerup", event => {
      if (event.pointerId !== state.pointer) return;
      const handle = activeHandle(); finishPointer(); render();
      if (handle) announce(`${handle.name}: ${coordinates(handle.get())}`);
    });
    canvas.addEventListener("pointercancel", event => { if (event.pointerId === state.pointer) { finishPointer(); render(); announce("Drag stopped. Your current values are kept."); } });
    canvas.addEventListener("lostpointercapture", () => { if (state.pointer !== null) { state.pointer = null; canvas.classList.remove("is-dragging"); render(); } });
    canvas.addEventListener("pointerleave", () => { if (state.pointer === null) { state.hover = null; render(); } });
    canvas.addEventListener("keydown", event => {
      if (event.key === "Escape") { finishPointer(); return; }
      if (event.key === "Home") { event.preventDefault(); reset(); return; }
      const direction = { ArrowLeft: point(-1, 0), ArrowRight: point(1, 0), ArrowUp: point(0, 1), ArrowDown: point(0, -1) }[event.key];
      if (!direction) return;
      event.preventDefault(); pause(); const handle = activeHandle();
      if (handle) { handle.set(plus(handle.get(), times(direction, event.shiftKey ? .5 : .1))); render(); announce(`${handle.name}: ${coordinates(handle.get())}`); }
    });
    document.addEventListener("visibilitychange", () => { if (document.hidden) { finishPointer(); pause(); render(); } });
    window.addEventListener("blur", () => { finishPointer(); pause(); render(); });
    render(); animationUI();
  }

  document.addEventListener("DOMContentLoaded", () => Object.keys(renderers).forEach(setupDemo));
})();
