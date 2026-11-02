/* marker-sketch : moteur du mode interactif.
 * Lit la config JSON (#scenes), anime les éléments de #sketch entre états successifs
 * (Maintenant / Ensuite / Plus tard...), garde les liens attachés aux éléments qui bougent,
 * permet de déplacer des éléments à la souris, d'éditer les textes et d'exporter l'état en SVG.
 * Aucune dépendance. Ne pas modifier: toute la chorégraphie vient de la config. */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var cfg = JSON.parse($('#scenes').textContent);
  var svg = $('#sketch');
  var states = cfg.states && cfg.states.length ? cfg.states : ['Vue'];
  var N = states.length;
  var DEF = { x: 0, y: 0, s: 1, r: 0, o: 1, draw: 1 };
  var NUM = /-?\d*\.?\d+(?:e[-+]?\d+)?/gi;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var SEG = reduce ? 0 : (cfg.duration || 1100);
  var HOLD = cfg.hold || 1700;

  var clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };
  var lerp = function (a, b, f) { return a + (b - a) * f; };
  var ease = function (u) { return u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2; };

  /* ---------- éléments et images clés ---------- */
  var E = {};
  var specs = cfg.elements || {};
  Object.keys(specs).forEach(function (id) { register(id, specs[id]); });
  Array.prototype.forEach.call(svg.querySelectorAll('[data-layer]'), function (el) {
    if (!el.id) el.id = 'auto-' + Math.random().toString(36).slice(2, 7);
    if (!E[el.id]) register(el.id, {});
  });

  function register(id, spec) {
    var el = svg.querySelector('[id="' + id + '"]');
    if (!el) { console.warn('marker-sketch: élément absent', id); return; }
    var frames = [], cur = Object.assign({}, DEF);
    var isPath = el.tagName.toLowerCase() === 'path';
    if (isPath && el.hasAttribute('d') && !el.hasAttribute('data-link')) cur.d = el.getAttribute('d');
    var k = spec.k || [];
    for (var i = 0; i < N; i++) { cur = Object.assign({}, cur, k[i] || {}); frames.push(cur); }
    E[id] = { id: id, el: el, frames: frames, lag: spec.lag || 0, drag: !!spec.drag, isPath: isPath,
      layer: el.getAttribute('data-layer'), len: null, cur: Object.assign({}, frames[0]), bb: null };
    if (E[id].drag) el.classList.add('drag');
  }

  /* ---------- liens attachés ---------- */
  var links = Array.prototype.map.call(svg.querySelectorAll('[data-link]'), function (p) {
    var ab = p.getAttribute('data-link').split('>');
    return { p: p, a: ab[0].trim(), b: ab[1].trim(), bend: parseFloat(p.getAttribute('data-bend') || '0') };
  });
  function bbox(e) {
    if (!e.bb) { try { e.bb = e.el.getBBox(); } catch (x) { e.bb = { x: 0, y: 0, width: 40, height: 40 }; } }
    return e.bb;
  }
  function centre(e) {
    var b = bbox(e), c = e.cur;
    return { x: c.x + c.s * (b.x + b.width / 2), y: c.y + c.s * (b.y + b.height / 2), hw: c.s * b.width / 2, hh: c.s * b.height / 2 };
  }
  function edge(c, to, gap) {
    var dx = to.x - c.x, dy = to.y - c.y;
    var k = 1 / Math.max(Math.abs(dx) / (c.hw + gap), Math.abs(dy) / (c.hh + gap), 1e-6);
    return { x: c.x + dx * k, y: c.y + dy * k };
  }
  function updateLinks() {
    links.forEach(function (l) {
      var A = E[l.a], B = E[l.b];
      if (!A || !B) return;
      var ca = centre(A), cb = centre(B);
      var p1 = edge(ca, cb, 12), p2 = edge(cb, ca, 16);
      var dx = p2.x - p1.x, dy = p2.y - p1.y, d;
      if (Math.abs(dx) >= Math.abs(dy) * 0.7) {
        var o = dy * l.bend;
        d = 'M' + p1.x.toFixed(1) + ' ' + p1.y.toFixed(1) + ' C' + (p1.x + dx * 0.5).toFixed(1) + ' ' + (p1.y + o).toFixed(1) + ' ' + (p2.x - dx * 0.5).toFixed(1) + ' ' + (p2.y - o).toFixed(1) + ' ' + p2.x.toFixed(1) + ' ' + p2.y.toFixed(1);
      } else {
        var o2 = dx * l.bend;
        d = 'M' + p1.x.toFixed(1) + ' ' + p1.y.toFixed(1) + ' C' + (p1.x + o2).toFixed(1) + ' ' + (p1.y + dy * 0.5).toFixed(1) + ' ' + (p2.x - o2).toFixed(1) + ' ' + (p2.y - dy * 0.5).toFixed(1) + ' ' + p2.x.toFixed(1) + ' ' + p2.y.toFixed(1);
      }
      l.p.setAttribute('d', d);
      var op = Math.min(A.cur.o, B.cur.o) * Math.min(layerAlpha(A), layerAlpha(B));
      var own = E[l.p.id];
      l.p.style.opacity = own ? Math.min(op, own.cur.o) : op;
    });
  }

  /* ---------- couches (afficher / masquer) ---------- */
  var layerOn = {}, layerA = {};
  (cfg.layers || []).forEach(function (L) { layerOn[L.id] = L.on !== false; layerA[L.id] = layerOn[L.id] ? 1 : 0; });
  function layerAlpha(e) { return e.layer && layerA[e.layer] !== undefined ? layerA[e.layer] : 1; }

  /* ---------- rendu d'un instant t (0 .. N-1) ---------- */
  var T = 0;
  function morph(d0, d1, f) {
    if (!d0 || !d1 || d0.replace(NUM, '#') !== d1.replace(NUM, '#')) return f < 0.5 ? d0 : d1;
    var a = d0.match(NUM), b = d1.match(NUM), i = 0;
    return d0.replace(NUM, function () { var v = lerp(+a[i], +b[i], f); i++; return v.toFixed(1); });
  }
  function render(t) {
    T = clamp(t, 0, N - 1);
    var i = Math.min(Math.floor(T), Math.max(N - 2, 0)), f = N > 1 ? T - i : 0;
    Object.keys(E).forEach(function (id) {
      var e = E[id], a = e.frames[i], b = e.frames[Math.min(i + 1, N - 1)];
      var u = e.lag ? clamp((f - e.lag) / (1 - e.lag), 0, 1) : f;
      u = ease(u);
      var c = e.cur;
      c.x = lerp(a.x, b.x, u); c.y = lerp(a.y, b.y, u); c.s = lerp(a.s, b.s, u);
      c.r = lerp(a.r, b.r, u); c.o = lerp(a.o, b.o, u); c.draw = lerp(a.draw, b.draw, u);
      e.el.setAttribute('transform', 'translate(' + c.x.toFixed(1) + ' ' + c.y.toFixed(1) + ')' + (c.r ? ' rotate(' + c.r.toFixed(1) + ')' : '') + (c.s !== 1 ? ' scale(' + c.s.toFixed(3) + ')' : ''));
      var tx = (f < 0.5 ? a : b).txt;
      if (tx !== undefined && e.el.textContent !== tx) e.el.textContent = tx;
      var op = c.o * layerAlpha(e);
      e.el.style.opacity = op.toFixed(3);
      e.el.style.pointerEvents = op < 0.05 ? 'none' : '';
      if (e.isPath) {
        if (a.d !== undefined) { c.d = morph(a.d, b.d, u); e.el.setAttribute('d', c.d); if (a.d !== b.d) e.bb = null; }
        if (a.draw !== 1 || b.draw !== 1) {
          if (e.len === null) { try { e.len = e.el.getTotalLength(); } catch (x) { e.len = 1000; } }
          e.el.style.strokeDasharray = e.len; e.el.style.strokeDashoffset = (e.len * (1 - c.draw)).toFixed(1);
        }
      }
    });
    updateLinks();
    syncUI();
  }

  /* ---------- animation ---------- */
  var anim = null, playing = false, holdTimer = null, frames = [], degraded = false;
  function stop() { if (anim) cancelAnimationFrame(anim.raf); anim = null; clearTimeout(holdTimer); }
  function to(target, done) {
    stop();
    target = clamp(target, 0, N - 1);
    var from = T, dist = Math.abs(target - from);
    if (!SEG || dist === 0) { render(target); if (done) done(); return; }
    var dur = SEG * Math.max(dist, 0.35), t0 = performance.now();
    anim = { raf: 0 };
    (function step(now) {
      var u = clamp((now - t0) / dur, 0, 1);
      render(lerp(from, target, u));
      monitor(now);
      if (u < 1) anim.raf = requestAnimationFrame(step); else { anim = null; if (done) done(); }
    })(t0);
  }
  function monitor(now) {
    frames.push(now);
    if (frames.length > 40) frames.shift();
    if (!degraded && frames.length === 40 && (frames[39] - frames[0]) / 39 > 45) {
      degraded = true; document.documentElement.setAttribute('data-q', 'low');
    }
  }
  function go(i) { setPlaying(false); to(clamp(i, 0, N - 1)); }
  function setPlaying(on) {
    playing = on; stop(); if (!on) { syncUI(); return; }
    if (T >= N - 1 - 1e-3) { render(0); }
    (function next() {
      var target = Math.floor(T + 1e-3) + 1;
      if (target > N - 1) { playing = false; syncUI(); return; }
      to(target, function () { holdTimer = setTimeout(function () { if (playing) next(); }, HOLD); });
    })();
    syncUI();
  }

  /* ---------- interface ---------- */
  var ui = {};
  function build() {
    $('#ttl').textContent = cfg.title || '';
    svg.setAttribute('aria-label', cfg.title || 'Croquis interactif');
    var bar = $('#bar');
    bar.innerHTML = '';
    var row1 = el('div', 'row');
    ui.prev = btn('‹', 'État précédent', function () { go(Math.round(T) - 1); });
    ui.next = btn('›', 'État suivant', function () { go(Math.round(T) + 1); });
    ui.steps = states.map(function (s, i) { var b = btn(s, s, function () { go(i); }); b.classList.add('chip'); return b; });
    row1.appendChild(ui.prev);
    ui.steps.forEach(function (b) { row1.appendChild(b); });
    row1.appendChild(ui.next);
    ui.play = btn('▶', 'Lecture', function () { setPlaying(!playing); });
    ui.play.classList.add('play');
    row1.appendChild(ui.play);
    bar.appendChild(row1);
    if (N > 1) {
      ui.scrub = el('input', 'scrub'); ui.scrub.type = 'range'; ui.scrub.min = 0; ui.scrub.max = N - 1; ui.scrub.step = 0.001; ui.scrub.value = 0;
      ui.scrub.setAttribute('aria-label', 'Faire défiler dans le temps');
      ui.scrub.addEventListener('input', function () { setPlaying(false); stop(); render(parseFloat(ui.scrub.value)); });
      bar.appendChild(ui.scrub);
    }
    var row2 = el('div', 'row small');
    (cfg.layers || []).forEach(function (L) {
      var b = btn(L.label, L.label, function () {
        layerOn[L.id] = !layerOn[L.id]; b.classList.toggle('on', layerOn[L.id]); fadeLayers();
      });
      b.classList.add('chip', 'layer'); b.classList.toggle('on', layerOn[L.id]); row2.appendChild(b);
    });
    var sp = el('span', 'sp'); row2.appendChild(sp);
    row2.appendChild(btn('Exporter SVG', 'Exporter l’état affiché en SVG', exportSVG));
    row2.appendChild(btn('Copier la disposition', 'Copier la disposition des éléments (JSON)', copyLayout));
    bar.appendChild(row2);
    ui.note = $('#note');
  }
  function el(tag, cls) { var n = document.createElement(tag); if (cls) n.className = cls; return n; }
  function btn(label, title, fn) { var b = el('button'); b.type = 'button'; b.textContent = label; b.title = title; b.setAttribute('aria-label', title); b.addEventListener('click', fn); return b; }
  function syncUI() {
    if (!ui.steps) return;
    var k = Math.round(T);
    ui.steps.forEach(function (b, i) { b.classList.toggle('on', i === k); b.setAttribute('aria-pressed', i === k); });
    if (ui.scrub && document.activeElement !== ui.scrub) ui.scrub.value = T;
    ui.play.textContent = playing ? '❚❚' : (T >= N - 1 - 1e-3 && N > 1 ? '↺' : '▶');
    ui.play.title = playing ? 'Pause' : 'Lecture';
    ui.prev.disabled = k <= 0; ui.next.disabled = k >= N - 1;
    var n = (cfg.notes && cfg.notes[k]) || '';
    if (ui.note && ui.note.textContent !== n) ui.note.textContent = n;
  }
  function fadeLayers() {
    var t0 = performance.now(), start = {};
    Object.keys(layerA).forEach(function (id) { start[id] = layerA[id]; });
    (function step(now) {
      var u = clamp((now - t0) / 350, 0, 1);
      Object.keys(layerA).forEach(function (id) { layerA[id] = lerp(start[id], layerOn[id] ? 1 : 0, u); });
      render(T);
      if (u < 1) requestAnimationFrame(step);
    })(t0);
  }

  /* ---------- glisser-déposer (modifie l'état affiché) ---------- */
  var dragging = null;
  function pt(ev) {
    var p = svg.createSVGPoint(); p.x = ev.clientX; p.y = ev.clientY;
    return p.matrixTransform(svg.getScreenCTM().inverse());
  }
  svg.addEventListener('pointerdown', function (ev) {
    var g = ev.target.closest && ev.target.closest('.drag');
    if (!g || !E[g.id]) return;
    setPlaying(false); stop();
    var k = Math.round(T); render(k);
    var e = E[g.id], p = pt(ev);
    dragging = { e: e, k: k, dx: p.x - e.frames[k].x, dy: p.y - e.frames[k].y };
    g.setPointerCapture(ev.pointerId); g.classList.add('grab'); ev.preventDefault();
  });
  svg.addEventListener('pointermove', function (ev) {
    if (!dragging) return;
    var p = pt(ev), f = dragging.e.frames[dragging.k];
    f.x = Math.round(p.x - dragging.dx); f.y = Math.round(p.y - dragging.dy);
    dragging.e.dirty = true;
    render(dragging.k);
  });
  function endDrag(ev) { if (dragging) { dragging.e.el.classList.remove('grab'); dragging = null; } }
  svg.addEventListener('pointerup', endDrag); svg.addEventListener('pointercancel', endDrag);

  /* ---------- édition des textes (double-clic) ---------- */
  svg.addEventListener('dblclick', function (ev) {
    var t = ev.target.closest && ev.target.closest('text');
    if (!t) return;
    var r = t.getBoundingClientRect(), box = $('#stage').getBoundingClientRect();
    var inp = el('input', 'edit'); inp.value = t.textContent;
    inp.style.left = (r.left - box.left - 8) + 'px'; inp.style.top = (r.top - box.top - 6) + 'px';
    inp.style.width = Math.max(r.width + 40, 120) + 'px'; inp.style.height = (r.height + 12) + 'px';
    $('#stage').appendChild(inp); inp.focus(); inp.select();
    var closed = false;
    var done = function (ok) { if (closed) return; closed = true; if (ok) t.textContent = inp.value; inp.remove(); };
    inp.addEventListener('keydown', function (e) { if (e.key === 'Enter') done(true); if (e.key === 'Escape') done(false); });
    inp.addEventListener('blur', function () { done(true); });
  });

  /* ---------- export ---------- */
  function exportSVG() {
    var c = svg.cloneNode(true);
    c.removeAttribute('id');
    Array.prototype.forEach.call(c.querySelectorAll('.drag'), function (n) { n.classList.remove('drag'); });
    var s = '<?xml version="1.0" encoding="UTF-8"?>\n' + new XMLSerializer().serializeToString(c);
    var name = 'croquis-' + (states[Math.round(T)] || 'etat').toLowerCase().replace(/[^a-z0-9]+/g, '-') + '.svg';
    try {
      var a = document.createElement('a');
      a.href = URL.createObjectURL(new Blob([s], { type: 'image/svg+xml' })); a.download = name;
      document.body.appendChild(a); a.click(); a.remove();
    } catch (x) { fallbackText(s); }
  }
  function layoutJSON() {
    var out = {};
    Object.keys(E).forEach(function (id) {
      var e = E[id];
      if (!e.drag && !e.dirty) return;
      out[id] = { k: e.frames.map(function (f) { return { x: f.x, y: f.y }; }) };
    });
    return JSON.stringify(out, null, 1);
  }
  function copyLayout() {
    var s = layoutJSON();
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(s).catch(function () { fallbackText(s); });
    else fallbackText(s);
  }
  function fallbackText(s) {
    var ta = el('textarea', 'fallback'); ta.value = s; ta.readOnly = true;
    $('#stage').appendChild(ta); ta.focus(); ta.select();
    ta.addEventListener('blur', function () { ta.remove(); });
  }

  /* ---------- clavier ---------- */
  document.addEventListener('keydown', function (ev) {
    if (/input|textarea/i.test((ev.target.tagName || ''))) return;
    if (ev.key === 'ArrowRight') go(Math.round(T) + 1);
    else if (ev.key === 'ArrowLeft') go(Math.round(T) - 1);
    else if (ev.key === ' ') { ev.preventDefault(); setPlaying(!playing); }
    else if (ev.key === 'Home') go(0);
    else if (ev.key === 'End') go(N - 1);
    else if (ev.key === 'f') { if (document.fullscreenElement) document.exitFullscreen(); else if (document.documentElement.requestFullscreen) document.documentElement.requestFullscreen(); }
  });

  /* ---------- démarrage ---------- */
  build();
  var start = parseFloat((location.hash.match(/state=([\d.]+)/) || [])[1]);
  render(isNaN(start) ? 0 : start);
  window.sketch = { jump: function (t) { stop(); render(t); }, go: go, play: function () { setPlaying(true); }, get t() { return T; }, layout: layoutJSON };
})();
