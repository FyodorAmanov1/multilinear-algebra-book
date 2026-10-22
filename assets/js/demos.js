(function () {
  "use strict";

  const OXFORD = "#002147";
  const TEAL = "#0f766e";
  const GOLD = "#c9a227";
  const ROSE = "#b3375f";
  const INK = "#151515";
  const PAPER = "#fbfbf8";
  const LINE = "#d9d2c4";

  const canvasCenter = { x: 360, y: 260 };
  const unit = 76;

  function getCanvas(id) {
    return document.getElementById(id);
  }

  function ctxOf(canvas) {
    if (!canvas) return null;
    const ctx = canvas.getContext("2d");
    if (!ctx) return null;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    return ctx;
  }

  function toCanvas(v) {
    return {
      x: canvasCenter.x + v.x * unit,
      y: canvasCenter.y - v.y * unit
    };
  }

  function line(ctx, a, b, color, width) {
    const p = toCanvas(a);
    const q = toCanvas(b);
    ctx.beginPath();
    ctx.moveTo(p.x, p.y);
    ctx.lineTo(q.x, q.y);
    ctx.strokeStyle = color || INK;
    ctx.lineWidth = width || 1.5;
    ctx.stroke();
  }

  function arrow(ctx, from, to, color, width, label) {
    const p = toCanvas(from);
    const q = toCanvas(to);
    const dx = q.x - p.x;
    const dy = q.y - p.y;
    const len = Math.hypot(dx, dy);
    if (len < 1) return;
    const head = Math.min(14, len * .22);
    const ux = dx / len;
    const uy = dy / len;

    ctx.beginPath();
    ctx.moveTo(p.x, p.y);
    ctx.lineTo(q.x - ux * head, q.y - uy * head);
    ctx.strokeStyle = color || OXFORD;
    ctx.lineWidth = width || 3;
    ctx.lineCap = "round";
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(q.x, q.y);
    ctx.lineTo(q.x - ux * head - uy * head * .45, q.y - uy * head + ux * head * .45);
    ctx.lineTo(q.x - ux * head + uy * head * .45, q.y - uy * head - ux * head * .45);
    ctx.closePath();
    ctx.fillStyle = color || OXFORD;
    ctx.fill();

    if (label) {
      ctx.fillStyle = color || OXFORD;
      ctx.font = "700 14px system-ui, sans-serif";
      ctx.fillText(label, q.x + 8, q.y - 8);
    }
  }

  function grid(ctx, opts) {
    const options = opts || {};
    const width = 720;
    const height = 520;
    ctx.fillStyle = options.background || PAPER;
    ctx.fillRect(0, 0, width, height);

    ctx.strokeStyle = options.gridColor || LINE;
    ctx.lineWidth = 1;
    const step = unit / 2;
    for (let x = 0; x <= width; x += step) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.stroke();
    }
    for (let y = 0; y <= height; y += step) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(width, y);
      ctx.stroke();
    }

    ctx.strokeStyle = options.axisColor || "rgba(21,21,21,.30)";
    ctx.lineWidth = 2;
    line(ctx, { x: -5, y: 0 }, { x: 5, y: 0 }, options.axisColor || "rgba(21,21,21,.30)", 2);
    line(ctx, { x: 0, y: -3.5 }, { x: 0, y: 3.5 }, options.axisColor || "rgba(21,21,21,.30)", 2);
  }

  function label(ctx, text, x, y, color, size) {
    ctx.fillStyle = color || INK;
    ctx.font = `${size || 14}px Georgia, serif`;
    ctx.fillText(text, x, y);
  }

  function polygon(ctx, points, fill, stroke) {
    if (!points.length) return;
    ctx.beginPath();
    const first = toCanvas(points[0]);
    ctx.moveTo(first.x, first.y);
    for (let i = 1; i < points.length; i++) {
      const p = toCanvas(points[i]);
      ctx.lineTo(p.x, p.y);
    }
    ctx.closePath();
    if (fill) {
      ctx.fillStyle = fill;
      ctx.fill();
    }
    if (stroke) {
      ctx.strokeStyle = stroke;
      ctx.lineWidth = 2;
      ctx.stroke();
    }
  }

  function dot(ctx, v, color, radius) {
    const p = toCanvas(v);
    ctx.beginPath();
    ctx.arc(p.x, p.y, radius || 6, 0, Math.PI * 2);
    ctx.fillStyle = color;
    ctx.fill();
  }

  function value(id, fallback) {
    const el = document.getElementById(id);
    if (!el) return fallback;
    const n = Number(el.value);
    return Number.isFinite(n) ? n : fallback;
  }

  function checked(id) {
    const el = document.getElementById(id);
    return !!(el && el.checked);
  }

  function textOf(id, fallback) {
    const el = document.getElementById(id);
    return el ? el.value : fallback;
  }

  function wave(time, speed) {
    return .5 + .5 * Math.sin(time * (speed || 1));
  }

  function lerp(a, b, t) {
    return a + (b - a) * t;
  }

  function drawVectorPlayground(ctx, time) {
    grid(ctx);
    const ax = value("vector-a-x", 1);
    const ay = value("vector-a-y", 2);
    const bx = value("vector-b-x", 3);
    const by = value("vector-b-y", -1);
    const scale = value("scale", 1);
    const a = { x: ax, y: ay };
    const b = { x: bx, y: by };
    const sum = { x: ax + bx, y: ay + by };
    const diff = { x: ax - bx, y: ay - by };

    arrow(ctx, { x: 0, y: 0 }, a, OXFORD, 4, "u");
    arrow(ctx, a, sum, TEAL, 4, "v");
    arrow(ctx, { x: 0, y: 0 }, sum, GOLD, 5, "u + v");
    arrow(ctx, { x: 0, y: 0 }, diff, ROSE, 4, "u - v");

    const scaled = { x: scale * ax, y: scale * ay };
    arrow(ctx, { x: 0, y: 0 }, scaled, "rgba(15,118,110,.55)", 3, "c u");

    const phase = wave(time, 1.5);
    const leg1 = Math.min(1, phase * 2);
    const leg2 = Math.max(0, Math.min(1, phase * 2 - 1));
    const walker = {
      x: lerp(0, ax, leg1) + lerp(0, bx, leg2),
      y: lerp(0, ay, leg1) + lerp(0, by, leg2)
    };
    dot(ctx, walker, ROSE, 7);

    label(ctx, `u = (${ax.toFixed(1)}, ${ay.toFixed(1)})`, 20, 34, OXFORD, 15);
    label(ctx, `v = (${bx.toFixed(1)}, ${by.toFixed(1)})`, 20, 58, TEAL, 15);
    label(ctx, `u + v = (${sum.x.toFixed(1)}, ${sum.y.toFixed(1)})`, 20, 82, "#8a6d00", 15);
    label(ctx, `c = ${scale.toFixed(1)}`, 20, 106, INK, 14);
  }

  function drawBasisExplorer(ctx, time) {
    grid(ctx);
    const angleA = value("basis-a-angle", 15);
    const lenA = value("basis-a-length", 1);
    const angleB = value("basis-b-angle", 105);
    const lenB = value("basis-b-length", 1);
    const px = value("point-x", 2);
    const py = value("point-y", 1);

    const a = {
      x: lenA * Math.cos(angleA * Math.PI / 180),
      y: lenA * Math.sin(angleA * Math.PI / 180)
    };
    const b = {
      x: lenB * Math.cos(angleB * Math.PI / 180),
      y: lenB * Math.sin(angleB * Math.PI / 180)
    };
    const det = a.x * b.y - a.y * b.x;
    const c1 = (px * b.y - py * b.x) / det;
    const c2 = (a.x * py - a.y * px) / det;
    const p = { x: px, y: py };

    arrow(ctx, { x: 0, y: 0 }, a, OXFORD, 4, "b1");
    arrow(ctx, { x: 0, y: 0 }, b, TEAL, 4, "b2");
    arrow(ctx, { x: 0, y: 0 }, p, GOLD, 5, "p");

    const phase = wave(time, 1.2);
    const first = { x: c1 * a.x * phase, y: c1 * a.y * phase };
    const second = {
      x: first.x + c2 * b.x * phase,
      y: first.y + c2 * b.y * phase
    };
    arrow(ctx, { x: 0, y: 0 }, first, "rgba(0,33,71,.35)", 3);
    arrow(ctx, first, second, "rgba(15,118,110,.35)", 3);
    dot(ctx, second, "#8a6d00", 6);

    label(ctx, `coordinates of p in basis {b1,b2}`, 20, 34, OXFORD, 15);
    label(ctx, `(${c1.toFixed(2)}, ${c2.toFixed(2)})`, 20, 58, TEAL, 15);
    label(ctx, `det = ${det.toFixed(2)}`, 20, 82, INK, 14);
  }

  function drawLinearMapTheater(ctx, time) {
    grid(ctx);
    const target = {
      a: value("matrix-a", 1),
      b: value("matrix-b", 0),
      c: value("matrix-c", 0),
      d: value("matrix-d", 1)
    };
    const phase = wave(time, .8);
    const a = lerp(1, target.a, phase);
    const b = lerp(0, target.b, phase);
    const c = lerp(0, target.c, phase);
    const d = lerp(1, target.d, phase);
    const map = v => ({ x: a * v.x + b * v.y, y: c * v.x + d * v.y });

    const corners = [
      { x: 0, y: 0 },
      { x: 1, y: 0 },
      { x: 1, y: 1 },
      { x: 0, y: 1 }
    ].map(map);
    polygon(ctx, corners, "rgba(201,162,39,.22)", GOLD);

    arrow(ctx, { x: 0, y: 0 }, map({ x: 1, y: 0 }), OXFORD, 4, "T(e1)");
    arrow(ctx, { x: 0, y: 0 }, map({ x: 0, y: 1 }), TEAL, 4, "T(e2)");

    ctx.strokeStyle = "rgba(21,21,21,.18)";
    for (let i = -4; i <= 4; i++) {
      for (let j = -3; j <= 3; j++) {
        const p = map({ x: i, y: j });
        const pUp = map({ x: i, y: j + 1 });
        line(ctx, p, pUp, "rgba(21,21,21,.12)", 1);
      }
    }
    for (let j = -3; j <= 3; j++) {
      for (let i = -4; i < 4; i++) {
        const p = map({ x: i, y: j });
        const pRight = map({ x: i + 1, y: j });
        line(ctx, p, pRight, "rgba(21,21,21,.12)", 1);
      }
    }

    label(ctx, `target A = [${target.a.toFixed(1)} ${target.b.toFixed(1)}; ${target.c.toFixed(1)} ${target.d.toFixed(1)}]`, 20, 34, OXFORD, 15);
    label(ctx, `det A = ${(target.a * target.d - target.b * target.c).toFixed(2)}`, 20, 58, TEAL, 15);
    label(ctx, phase < .05 ? "starting square" : "mapped square", 20, 82, INK, 14);
  }

  function drawInnerProductLab(ctx, time) {
    grid(ctx);
    const uAngle = value("u-angle", 25) * Math.PI / 180;
    const uLen = value("u-length", 3);
    const vAngle = value("v-angle", 95) * Math.PI / 180;
    const vLen = value("v-length", 2);
    const u = { x: uLen * Math.cos(uAngle), y: uLen * Math.sin(uAngle) };
    const v = { x: vLen * Math.cos(vAngle), y: vLen * Math.sin(vAngle) };
    const dot = u.x * v.x + u.y * v.y;
    const normV = Math.hypot(v.x, v.y) || 1;
    const projScale = dot / (normV * normV);
    const proj = { x: projScale * v.x, y: projScale * v.y };

    arrow(ctx, { x: 0, y: 0 }, u, OXFORD, 4, "u");
    arrow(ctx, { x: 0, y: 0 }, v, TEAL, 4, "v");
    arrow(ctx, { x: 0, y: 0 }, proj, GOLD, 4, "proj");
    line(ctx, u, proj, ROSE, 2);

    const phase = wave(time, 1.4);
    const shadow = {
      x: lerp(u.x, proj.x, phase),
      y: lerp(u.y, proj.y, phase)
    };
    dot(ctx, shadow, ROSE, 6);

    label(ctx, `⟨u,v⟩ = ${dot.toFixed(2)}`, 20, 34, OXFORD, 15);
    const angle = Math.acos(Math.max(-1, Math.min(1, dot / (uLen * vLen)))) * 180 / Math.PI;
    label(ctx, `angle = ${angle.toFixed(1)}°`, 20, 58, TEAL, 15);
    if (Math.abs(dot) < .02) label(ctx, "orthogonal!", 20, 82, ROSE, 15);
    else label(ctx, "the gold arrow is u's shadow on v", 20, 82, "#8a6d00", 14);
  }

  function drawDeterminantVolume(ctx, time) {
    grid(ctx);
    const targetA = value("matrix-a", 1.5);
    const targetB = value("matrix-b", .5);
    const targetC = value("matrix-c", .5);
    const targetD = value("matrix-d", 1.2);
    const phase = wave(time, .9);
    const a = lerp(1, targetA, phase);
    const b = lerp(0, targetB, phase);
    const c = lerp(0, targetC, phase);
    const d = lerp(1, targetD, phase);
    const det = a * d - b * c;
    const targetDet = targetA * targetD - targetB * targetC;
    const u = { x: a, y: c };
    const v = { x: b, y: d };

    polygon(ctx, [
      { x: 0, y: 0 },
      { x: 1, y: 0 },
      { x: 1, y: 1 },
      { x: 0, y: 1 }
    ], "rgba(15,118,110,.10)", "rgba(15,118,110,.5)");
    polygon(ctx, [
      { x: 0, y: 0 },
      u,
      { x: a + b, y: c + d },
      v
    ], det >= 0 ? "rgba(201,162,39,.25)" : "rgba(179,55,95,.25)", det >= 0 ? GOLD : ROSE);
    arrow(ctx, { x: 0, y: 0 }, u, OXFORD, 4, "col 1");
    arrow(ctx, { x: 0, y: 0 }, v, TEAL, 4, "col 2");
    label(ctx, `det A = ${det.toFixed(2)}`, 20, 34, OXFORD, 15);
    label(ctx, det < 0 ? "orientation reversed" : "orientation preserved", 20, 58, TEAL, 15);
    label(ctx, `target det = ${targetDet.toFixed(2)}`, 20, 82, INK, 14);
  }

  function drawEigenvectorDance(ctx, time) {
    grid(ctx);
    const a = value("matrix-a", 1.4);
    const d = value("matrix-d", .8);
    const iterations = value("iterations", 4);
    const speed = value("speed", 1);
    const A = [
      [a, .4],
      [.3, d]
    ];
    const phase = wave(time, speed);
    const animatedIterations = 1 + (iterations - 1) * phase;

    for (let i = 0; i < 18; i++) {
      const angle = i * Math.PI / 9;
      let v = { x: Math.cos(angle), y: Math.sin(angle) };
      const steps = Math.min(iterations, Math.ceil(animatedIterations));
      for (let k = 0; k < steps; k++) {
        const next = {
          x: A[0][0] * v.x + A[0][1] * v.y,
          y: A[1][0] * v.x + A[1][1] * v.y
        };
        const partial = k === steps - 1 ? animatedIterations - Math.floor(animatedIterations) : 1;
        const shown = k < Math.floor(animatedIterations) ? next : {
          x: lerp(v.x, next.x, partial),
          y: lerp(v.y, next.y, partial)
        };
        arrow(ctx, v, shown, "rgba(15,118,110,.22)", 2);
        if (partial >= 1 || k < Math.floor(animatedIterations)) v = next;
      }
    }

    const tr = a + d;
    const disc = tr * tr - 4 * (a * d - .12);
    if (disc >= 0) {
      const root = Math.sqrt(disc);
      const l1 = (tr + root) / 2;
      const l2 = (tr - root) / 2;
      [l1, l2].forEach((lambda, index) => {
        const y = (lambda - A[0][0]) / A[0][1];
        const norm = Math.hypot(1, y) || 1;
        arrow(ctx, { x: 0, y: 0 }, { x: 2.5 / norm, y: 2.5 * y / norm }, index === 0 ? GOLD : ROSE, 5, `λ=${lambda.toFixed(2)}`);
      });
      label(ctx, `A = [${a.toFixed(1)} 0.4; 0.3 ${d.toFixed(1)}]`, 20, 34, OXFORD, 15);
      label(ctx, `iterations = ${animatedIterations.toFixed(1)}`, 20, 58, TEAL, 15);
    } else {
      label(ctx, `A = [${a.toFixed(1)} 0.4; 0.3 ${d.toFixed(1)}]`, 20, 34, OXFORD, 15);
      label(ctx, "complex eigenvalues: a whirl, not a fixed line", 20, 58, ROSE, 14);
    }
  }

  function drawBilinearFormLab(ctx, time) {
    grid(ctx);
    const a = value("form-a", 1);
    const b = value("form-b", .5);
    const c = value("form-c", 1);
    const det = a * c - b * b;

    const cell = .22;
    for (let x = -4.4; x <= 4.4; x += cell) {
      for (let y = -3.2; y <= 3.2; y += cell) {
        const q = a * x * x + 2 * b * x * y + c * y * y;
        const intensity = Math.min(.28, Math.abs(q) * .04 + .03);
        ctx.fillStyle = q >= 0 ? `rgba(15,118,110,${intensity})` : `rgba(179,55,95,${intensity})`;
        const p = toCanvas({ x: x, y: y });
        const q2 = toCanvas({ x: x + cell, y: y + cell });
        ctx.fillRect(p.x, q2.y, q2.x - p.x, p.y - q2.y);
      }
    }

    const angle = time * .7;
    const v = { x: Math.cos(angle), y: Math.sin(angle) };
    const q = a * v.x * v.x + 2 * b * v.x * v.y + c * v.y * v.y;
    arrow(ctx, { x: 0, y: 0 }, v, q >= 0 ? TEAL : ROSE, 4, "v");
    arrow(ctx, { x: 0, y: 0 }, { x: q * v.x, y: q * v.y }, GOLD, 4, "B(v,v)v");

    label(ctx, `A = [${a.toFixed(1)} ${b.toFixed(1)}; ${b.toFixed(1)} ${c.toFixed(1)}]`, 20, 34, OXFORD, 15);
    label(ctx, `B(v,v) = ${q.toFixed(2)}`, 20, 58, q >= 0 ? TEAL : ROSE, 15);
    label(ctx, det > 0 ? "same-sign bowl" : "saddle-like form", 20, 82, INK, 14);
  }

  function drawWedgeAreas(ctx, time) {
    grid(ctx);
    const uAngle = value("u-angle", 25) * Math.PI / 180;
    const uLen = value("u-length", 3);
    const vAngle = value("v-angle", 110) * Math.PI / 180;
    const vLen = value("v-length", 2);
    const u = { x: uLen * Math.cos(uAngle), y: uLen * Math.sin(uAngle) };
    const v = { x: vLen * Math.cos(vAngle), y: vLen * Math.sin(vAngle) };
    const area = u.x * v.y - u.y * v.x;
    const phase = wave(time, .9);

    polygon(ctx, [
      { x: 0, y: 0 },
      u,
      { x: u.x + v.x, y: u.y + v.y },
      v
    ], "none", area >= 0 ? GOLD : ROSE);
    polygon(ctx, [
      { x: 0, y: 0 },
      u,
      { x: u.x + phase * v.x, y: u.y + phase * v.y },
      { x: phase * v.x, y: phase * v.y }
    ], area >= 0 ? "rgba(201,162,39,.30)" : "rgba(179,55,95,.30)");
    arrow(ctx, { x: 0, y: 0 }, u, OXFORD, 4, "u");
    arrow(ctx, { x: 0, y: 0 }, v, TEAL, 4, "v");
    label(ctx, `u ∧ v = ${area.toFixed(2)}`, 20, 34, OXFORD, 15);
    label(ctx, `area = ${Math.abs(area).toFixed(2)}`, 20, 58, TEAL, 15);
    label(ctx, area >= 0 ? "counterclockwise ticket" : "clockwise ticket", 20, 82, INK, 14);
  }

  function drawTensorProductBuilder(ctx, time) {
    grid(ctx);
    const ux = value("u-x", 2);
    const uy = value("u-y", 1);
    const vx = value("v-x", 1);
    const vy = value("v-y", 3);
    const size = value("basis-size", 3);

    arrow(ctx, { x: 0, y: 0 }, { x: ux, y: uy }, OXFORD, 4, "u");
    arrow(ctx, { x: 0, y: 0 }, { x: vx, y: vy }, TEAL, 4, "v");

    const origin = toCanvas({ x: -3.2, y: -2.4 });
    const active = Math.floor(wave(time, 1.2) * size * size);
    for (let i = 0; i < size; i++) {
      for (let j = 0; j < size; j++) {
        const intensity = (i + j) / (2 * size - 2 || 1);
        const isCurrent = i * size + j === active;
        ctx.fillStyle = isCurrent
          ? "rgba(201,162,39,.55)"
          : `rgba(0,33,71,${.08 + intensity * .22})`;
        ctx.fillRect(origin.x + i * 46, origin.y + j * 46, 40, 40);
        if (isCurrent) {
          ctx.strokeStyle = GOLD;
          ctx.lineWidth = 3;
          ctx.strokeRect(origin.x + i * 46, origin.y + j * 46, 40, 40);
        }
      }
    }

    label(ctx, `u ⊗ v has ${size * size} basis products`, 20, 34, OXFORD, 15);
    label(ctx, `u = (${ux.toFixed(1)}, ${uy.toFixed(1)})`, 20, 58, TEAL, 14);
    label(ctx, `v = (${vx.toFixed(1)}, ${vy.toFixed(1)})`, 20, 82, INK, 14);
    label(ctx, "one lamp lights each product slot", 20, 106, "#8a6d00", 14);
  }

  function drawComponentTransformer(ctx, time) {
    grid(ctx);
    const angle = value("angle", 30) * Math.PI / 180;
    const kind = textOf("tensor-type", "vector");
    const cov = textOf("covariance", "upper");
    const phase = wave(time, .7);
    const shownAngle = angle * phase;
    const cos = Math.cos(shownAngle);
    const sin = Math.sin(shownAngle);

    const b1 = { x: cos, y: sin };
    const b2 = { x: -sin, y: cos };
    arrow(ctx, { x: 0, y: 0 }, b1, OXFORD, 4, "b1");
    arrow(ctx, { x: 0, y: 0 }, b2, TEAL, 4, "b2");

    const fixed = { x: 2, y: 1 };
    arrow(ctx, { x: 0, y: 0 }, fixed, GOLD, 5, "object");

    const c1 = fixed.x * cos + fixed.y * sin;
    const c2 = -fixed.x * sin + fixed.y * cos;
    label(ctx, `basis angle = ${(shownAngle * 180 / Math.PI).toFixed(0)}°`, 20, 34, OXFORD, 15);
    label(ctx, `type = ${kind}`, 20, 58, TEAL, 15);
    label(ctx, cov === "upper" ? "contravariant components" : "covariant components", 20, 82, INK, 14);
    label(ctx, `components ≈ (${c1.toFixed(2)}, ${c2.toFixed(2)})`, 20, 106, "#8a6d00", 15);
  }

  function drawTensorApplications(ctx, time) {
    grid(ctx);
    const a = value("stress-a", 1.5);
    const b = value("stress-b", .7);
    const ratio = value("diffusion-ratio", 1);
    const lambda1 = Math.max(.1, a + Math.abs(b));
    const lambda2 = Math.max(.1, a - Math.abs(b));

    ctx.strokeStyle = OXFORD;
    ctx.lineWidth = 3;
    const center = toCanvas({ x: 0, y: 0 });
    const pulse = .94 + .06 * Math.sin(time * 1.4);
    ctx.beginPath();
    ctx.ellipse(center.x, center.y, lambda1 * unit * pulse, lambda2 * unit * pulse, Math.atan2(b, a), 0, Math.PI * 2);
    ctx.stroke();

    for (let i = 0; i < 12; i++) {
      const angle = i * Math.PI / 6;
      const dir = { x: Math.cos(angle), y: Math.sin(angle) };
      const stretch = ratio * (1 + .25 * Math.cos(2 * (angle - Math.atan2(b, a))));
      const breath = .75 + .25 * Math.sin(time * 1.4 - angle * 2);
      arrow(ctx, dir, {
        x: dir.x * stretch * breath,
        y: dir.y * stretch * breath
      }, "rgba(15,118,110,.60)", 2);
    }

    label(ctx, `stress eigenvalues ≈ (${lambda1.toFixed(2)}, ${lambda2.toFixed(2)})`, 20, 34, OXFORD, 15);
    label(ctx, `diffusion ratio = ${ratio.toFixed(2)}`, 20, 58, TEAL, 15);
    label(ctx, "the field breathes with the tensor", 20, 82, INK, 14);
  }

  function drawFormsAndFields(ctx, time) {
    grid(ctx);
    const a = value("form-a", 1);
    const b = value("form-b", .5);
    const showArea = checked("show-area");
    const norm = Math.hypot(a, b);
    const normal = norm > .001 ? { x: a / norm, y: b / norm } : { x: 1, y: 0 };
    const tangent = { x: -normal.y, y: normal.x };

    if (norm > .001) {
      for (let level = -3; level <= 3; level++) {
        const center = { x: level * .55 * normal.x, y: level * .55 * normal.y };
        line(
          ctx,
          { x: center.x - 3.4 * tangent.x, y: center.y - 3.4 * tangent.y },
          { x: center.x + 3.4 * tangent.x, y: center.y + 3.4 * tangent.y },
          level === 0 ? "rgba(21,21,21,.35)" : "rgba(15,118,110,.24)",
          level === 0 ? 2 : 1
        );
      }
    }

    const angle = time * .8;
    const test = { x: Math.cos(angle), y: Math.sin(angle) };
    const measured = a * test.x + b * test.y;
    arrow(ctx, { x: 0, y: 0 }, test, measured >= 0 ? TEAL : ROSE, 4, "v");
    label(ctx, `α(v) = ${measured.toFixed(2)}`, 360, 486, measured >= 0 ? TEAL : ROSE, 15);

    if (showArea) {
      const pulse = .35 + .12 * Math.sin(time * 1.3);
      polygon(ctx, [
        { x: .5, y: .5 },
        { x: 1.5, y: .5 },
        { x: 1.5, y: 1.5 },
        { x: .5, y: 1.5 }
      ], `rgba(201,162,39,${pulse})`, GOLD);
    }

    arrow(ctx, { x: 0, y: 0 }, { x: a, y: b }, OXFORD, 5, "α");
    label(ctx, `α = ${a.toFixed(1)} dx + ${b.toFixed(1)} dy`, 20, 34, OXFORD, 15);
    label(ctx, `area form = ${a.toFixed(1)} dx ∧ dy`, 20, 58, TEAL, 15);
    label(ctx, "stacked lines are level sets of α", 20, 82, INK, 14);
  }

  const renderers = {
    "vector-playground": drawVectorPlayground,
    "basis-explorer": drawBasisExplorer,
    "linear-map-theater": drawLinearMapTheater,
    "inner-product-lab": drawInnerProductLab,
    "determinant-volume": drawDeterminantVolume,
    "eigenvector-dance": drawEigenvectorDance,
    "bilinear-form-lab": drawBilinearFormLab,
    "wedge-areas": drawWedgeAreas,
    "tensor-product-builder": drawTensorProductBuilder,
    "component-transformer": drawComponentTransformer,
    "tensor-applications": drawTensorApplications,
    "forms-and-fields": drawFormsAndFields
  };

  function setupDemo(id) {
    const canvas = getCanvas(id);
    if (!canvas) return;
    const render = renderer => {
      const ctx = ctxOf(canvas);
      if (ctx) renderers[id](ctx, renderer.time);
    };

    const state = {
      playing: false,
      rafId: null,
      last: null,
      time: 0
    };

    const button = canvas.closest(".demo-shell")?.querySelector(".demo-play");
    const status = canvas.closest(".demo-shell")?.querySelector(".demo-state");
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    const updateControls = () => {
      if (!button) return;
      button.textContent = state.playing ? "Pause animation" : "Play animation";
      button.setAttribute("aria-pressed", state.playing ? "true" : "false");
      button.classList.toggle("is-playing", state.playing);
      if (status) {
        status.textContent = state.playing
          ? "Animation playing"
          : (reducedMotion ? "Paused (reduced motion)" : "Paused");
      }
    };

    const frame = now => {
      if (!state.playing) return;
      if (state.last !== null) {
        state.time += Math.min(.05, (now - state.last) / 1000);
      }
      state.last = now;
      render(state);
      state.rafId = window.requestAnimationFrame(frame);
    };

    const play = () => {
      if (state.playing) return;
      state.playing = true;
      state.last = null;
      updateControls();
      state.rafId = window.requestAnimationFrame(frame);
    };

    const pause = () => {
      if (!state.playing) return;
      state.playing = false;
      if (state.rafId !== null) window.cancelAnimationFrame(state.rafId);
      state.rafId = null;
      state.last = null;
      updateControls();
    };

    if (button) {
      button.addEventListener("click", () => {
        if (state.playing) pause();
        else play();
      });
    }

    canvas.closest("main")?.querySelectorAll("input, select").forEach(control => {
      control.addEventListener("input", () => render(state));
      control.addEventListener("change", () => render(state));
    });

    document.addEventListener("visibilitychange", () => {
      if (document.hidden) pause();
    });

    render(state);
    updateControls();
  }

  document.addEventListener("DOMContentLoaded", () => {
    Object.keys(renderers).forEach(setupDemo);
  });
})();
