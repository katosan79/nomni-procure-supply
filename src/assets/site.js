(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var header = document.querySelector('.site-header');

  // Header state on scroll
  function onScroll() { if (header) header.classList.toggle('scrolled', window.scrollY > 40); }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // Dropdown menus
  document.querySelectorAll('.nav-item > button').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      var item = btn.parentElement, open = item.classList.contains('open');
      document.querySelectorAll('.nav-item.open').forEach(function (n) { n.classList.remove('open'); n.firstElementChild.setAttribute('aria-expanded', 'false'); });
      if (!open) { item.classList.add('open'); btn.setAttribute('aria-expanded', 'true'); }
      e.stopPropagation();
    });
  });
  document.addEventListener('click', function () { document.querySelectorAll('.nav-item.open').forEach(function (n) { n.classList.remove('open'); }); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') document.querySelectorAll('.nav-item.open').forEach(function (n) { n.classList.remove('open'); }); });

  // Mobile menu
  var burger = document.querySelector('.burger');
  if (burger) burger.addEventListener('click', function () {
    var open = header.classList.toggle('menu-open');
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  // Region (staging: SG only)
  var region = document.querySelector('.region');
  if (region) region.addEventListener('change', function () {
    var note = document.querySelector('.region-note'); if (note) note.hidden = region.value === 'sg';
  });

  // Reveal on scroll
  var els = document.querySelectorAll('.rv');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('seen'); io.unobserve(en.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    els.forEach(function (el) { io.observe(el); });
  } else { els.forEach(function (el) { el.classList.add('seen'); }); }

  // Statement: words light up as you scroll
  var st = document.querySelector('.statement');
  if (st && !reduce) {
    var dims = st.querySelectorAll('.dim');
    window.addEventListener('scroll', function () {
      var r = st.getBoundingClientRect(), vh = window.innerHeight;
      var p = Math.min(1, Math.max(0, (vh * 0.85 - r.top) / (r.height + vh * 0.35)));
      var n = Math.round(p * dims.length);
      dims.forEach(function (d, i) { d.style.color = i < n ? 'inherit' : ''; });
    }, { passive: true });
  } else if (st) { st.querySelectorAll('.dim').forEach(function (d) { d.style.color = 'inherit'; }); }

  // Sequenced demos: [data-seq] containers, children with data-at="n" gain .in in order, then loop
  document.querySelectorAll('[data-seq]').forEach(function (root) {
    var items = Array.prototype.slice.call(root.querySelectorAll('[data-at]'));
    var max = items.reduce(function (m, el) { return Math.max(m, +el.dataset.at); }, 0);
    var step = +(root.dataset.seq || 1100);
    function show(n) { items.forEach(function (el) { el.classList.toggle('in', +el.dataset.at <= n); }); }
    if (reduce) { show(max); return; }
    var n = 0, started = false;
    function tick() { n = n > max + 2 ? 0 : n + 1; show(n); setTimeout(tick, n === 0 ? 600 : (n > max ? 3200 : step)); }
    var start = function () { if (!started) { started = true; setTimeout(tick, 400); } };
    if ('IntersectionObserver' in window) {
      var o = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { start(); o.disconnect(); } }, { threshold: 0.2 });
      o.observe(root);
    } else start();
  });

  // Agent console
  var EVENTS = {
    invoice: [
      ['Invoice Agent', 'Matched INV-20418 from Fresh Produce Co. to the PO and delivery. 12 of 13 lines are clean and posted to Xero.', ['View', 'Undo']],
      ['Invoice Agent', 'Romaine is 12% above the PO price. Holding 1 line for your review.', ['Accept price', 'Ask supplier']],
      ['Invoice Agent', 'PEPPOL invoice from Dairy Supplier received. Matched in full and posted.', ['View']]
    ],
    ordering: [
      ['Ordering Agent', "Drafted tomorrow's order for Outlet A: 14 lines from 3 suppliers, based on par levels and recent sales.", ['Approve', 'Edit']],
      ['Ordering Agent', 'Seafood Supplier cuts off at 4pm. Order is ready for your approval.', ['Approve']]
    ],
    margin: [
      ['Margin Agent', 'Chicken thigh is up 9% this week. Chicken rice drops to 61% margin against a 65% target.', ['Reprice', 'Re-source']],
      ['Margin Agent', 'Two dishes use romaine. Caesar salad is now below target.', ['See options']]
    ],
    variance: [
      ['Variance Agent', 'Outlet B used 6 kg more salmon than sales explain. 4 kg is logged waste; 2 kg is unexplained.', ['Review count']],
      ['Variance Agent', 'Transfers between Outlet A and C did not match on 2 items.', ['Reconcile']]
    ],
    governance: [
      ['Governance Agent', 'Dairy price file received. Drafted updates to 42 items across 3 outlet groups.', ['Approve all', 'Review']]
    ],
    inbox: [
      ['Supply · Order inbox', 'WhatsApp from Demo Bistro: "same as usual but chicken 8kg ah". Drafted 6 lines, within credit limit.', ['Approve', 'Edit']],
      ['Supply · Order inbox', 'Voice note transcribed and matched: 2 kg peeled shallots added to the draft.', ['Approve']]
    ]
  };
  var con = document.querySelector('[data-console]');
  if (con) {
    var feed = con.querySelector('.feed'), btns = document.querySelectorAll('.agent-btn'), active = 'all', idx = 0, timer;
    function pool() {
      if (active !== 'all') return EVENTS[active];
      var all = []; Object.keys(EVENTS).forEach(function (k) { all = all.concat(EVENTS[k]); }); return all;
    }
    var clock = 7 * 60 + 12;
    function stamp() { clock += 3 + Math.floor(Math.random() * 6); var h = Math.floor(clock / 60) % 24, m = clock % 60; return (h < 10 ? '0' : '') + h + ':' + (m < 10 ? '0' : '') + m; }
    function push() {
      var p = pool(), e = p[idx % p.length]; idx++;
      var li = document.createElement('li'); li.className = 'ev';
      var acts = e[2].map(function (a, i) { return '<span' + (i === 0 ? ' class="p"' : '') + '>' + a + '</span>'; }).join('');
      li.innerHTML = '<time>' + stamp() + '</time><div><div class="who">' + e[0] + '</div><p>' + e[1] + '</p><div class="acts">' + acts + '</div></div>';
      feed.appendChild(li);
      while (feed.children.length > 4) feed.removeChild(feed.firstElementChild);
    }
    function run() { clearInterval(timer); feed.innerHTML = ''; idx = 0; push(); push(); push(); if (!reduce) timer = setInterval(push, 2600); }
    btns.forEach(function (b) {
      b.addEventListener('click', function () {
        var same = b.getAttribute('aria-selected') === 'true';
        btns.forEach(function (x) { x.setAttribute('aria-selected', 'false'); });
        active = same ? 'all' : b.dataset.agent;
        if (!same) b.setAttribute('aria-selected', 'true');
        run();
      });
    });
    run();
  }

  // Count-up numbers
  document.querySelectorAll('[data-count]').forEach(function (el) {
    var target = +el.dataset.count, suffix = el.dataset.suffix || '';
    if (reduce || !('IntersectionObserver' in window)) { el.firstChild.nodeValue = target + suffix; return; }
    var o = new IntersectionObserver(function (es) {
      if (!es[0].isIntersecting) return; o.disconnect();
      var t0 = performance.now();
      (function f(t) { var p = Math.min(1, (t - t0) / 1400), v = Math.round(target * (1 - Math.pow(1 - p, 3))); el.firstChild.nodeValue = v + suffix; if (p < 1) requestAnimationFrame(f); })(t0);
    }, { threshold: 0.4 });
    o.observe(el);
  });

  // Staging forms
  document.querySelectorAll('form[data-staging]').forEach(function (f) {
    f.addEventListener('submit', function (e) { e.preventDefault(); var m = f.querySelector('.form-note'); if (m) m.textContent = 'Thanks. This staging form isn’t connected yet, so nothing was sent.'; });
  });
})();
