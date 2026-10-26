(function () {
  // Dropdown menus
  document.querySelectorAll('.nav-item > button').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      var item = btn.parentElement;
      var open = item.classList.contains('open');
      document.querySelectorAll('.nav-item.open').forEach(function (n) { n.classList.remove('open'); n.querySelector('button').setAttribute('aria-expanded', 'false'); });
      if (!open) { item.classList.add('open'); btn.setAttribute('aria-expanded', 'true'); }
      e.stopPropagation();
    });
  });
  document.addEventListener('click', function () {
    document.querySelectorAll('.nav-item.open').forEach(function (n) { n.classList.remove('open'); });
  });

  // Mobile menu
  var burger = document.querySelector('.burger');
  if (burger) burger.addEventListener('click', function () {
    var h = document.querySelector('.site-header');
    var open = h.classList.toggle('menu-open');
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  // Region switcher (staging: SG only)
  var region = document.querySelector('.region');
  if (region) region.addEventListener('change', function () {
    var note = document.querySelector('.region-note');
    if (note) note.hidden = region.value === 'sg';
  });

  // Reveal on scroll
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (entries) {
    entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('seen'); io.unobserve(en.target); } });
  }, { threshold: 0.12 }) : null;
  document.querySelectorAll('.reveal').forEach(function (el) { io ? io.observe(el) : el.classList.add('seen'); });

  // Step-through demos: elements with data-step="n" appear in order, then loop.
  function runDemo(root) {
    var steps = Array.prototype.slice.call(root.querySelectorAll('[data-step]'));
    var max = steps.reduce(function (m, el) { return Math.max(m, +el.dataset.step); }, 0);
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    function show(n) {
      steps.forEach(function (el) {
        var on = +el.dataset.step <= n;
        el.classList.toggle(el.dataset.cls || 'in', on);
      });
    }
    if (reduce) { show(max); return; }
    var n = 0;
    function tick() {
      n += 1;
      if (n > max + 2) { n = 0; }
      show(n);
      setTimeout(tick, n === 0 ? 700 : (n > max ? 2600 : 1100));
    }
    setTimeout(tick, 600);
  }
  document.querySelectorAll('[data-demo]').forEach(runDemo);

  // Waitlist / form placeholders
  document.querySelectorAll('form[data-staging]').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var msg = f.querySelector('.form-note');
      if (msg) msg.textContent = 'Thanks. This staging form is not connected yet, so nothing was sent.';
    });
  });
})();
