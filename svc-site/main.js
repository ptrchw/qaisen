/* ==========================================================
   Site settings — change these once and every page updates.
   ========================================================== */
var SITE = {
  calendly: 'https://calendly.com/your-handle/20min',   // TODO: your Calendly event link
  whatsapp: '6500000000',                                // TODO: business WhatsApp number, digits only with country code
  whatsappText: 'Hi, I found your site and would like to talk about a UX project.',
  email: 'hello@qaisen.com',                             // business email
  linkedin: 'https://www.linkedin.com/in/ptrchw/',
  portfolio: 'https://example.com/portfolio'             // TODO: portfolio URL once it is on GitHub Pages
};

(function () {
  'use strict';

  var doc = document.documentElement;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Always open a new page at the top ----------
     Browsers, and viewers that show the site inside a frame, can keep the
     previous page's scroll position. Reset it unless the link targets a
     section (#anchor). */
  try { if ('scrollRestoration' in history) history.scrollRestoration = 'manual'; } catch (e) {}
  var NAV_FLAG = 'svc-internal-nav';
  function cameFromThisSite() {
    var flag = false;
    try { flag = sessionStorage.getItem(NAV_FLAG) === '1'; sessionStorage.removeItem(NAV_FLAG); } catch (e) {}
    if (flag) return true;
    try { return !!document.referrer && new URL(document.referrer).origin === location.origin; } catch (e) { return false; }
  }
  var internalNav = cameFromThisSite();
  function toTop() {
    if (location.hash && location.hash.length > 1) return;
    window.scrollTo(0, 0);
    if (internalNav) {
      // Also scrolls any outer frame or viewer container back to this page's top
      var pad = doc.style.scrollPaddingTop;
      doc.style.scrollPaddingTop = '0px';
      try { doc.scrollIntoView({ block: 'start', inline: 'nearest' }); } catch (e) { doc.scrollIntoView(true); }
      doc.style.scrollPaddingTop = pad;
    }
  }
  toTop();
  window.addEventListener('load', toTop);
  window.addEventListener('pageshow', function (e) { if (e.persisted) toTop(); });
  // Mark clicks on links to other pages of this site
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a) return;
    var href = a.getAttribute('href');
    if (!href || href.charAt(0) === '#' || a.target === '_blank' || /^(https?:|mailto:|tel:)/i.test(href)) return;
    try { sessionStorage.setItem(NAV_FLAG, '1'); } catch (err) {}
  }, true);

  /* ---------- Fill links from SITE settings ---------- */
  function waLink() {
    return 'https://wa.me/' + SITE.whatsapp + '?text=' + encodeURIComponent(SITE.whatsappText);
  }
  var linkMap = {
    calendly: SITE.calendly,
    whatsapp: waLink(),
    linkedin: SITE.linkedin,
    portfolio: SITE.portfolio,
    email: 'mailto:' + SITE.email
  };
  document.querySelectorAll('[data-link]').forEach(function (a) {
    var key = a.getAttribute('data-link');
    if (linkMap[key]) {
      a.setAttribute('href', linkMap[key]);
      if (key !== 'email') {
        a.setAttribute('target', '_blank');
        a.setAttribute('rel', 'noopener');
      }
    }
  });
  document.querySelectorAll('[data-fill="email"]').forEach(function (el) { el.textContent = SITE.email; });
  document.querySelectorAll('[data-fill="whatsapp"]').forEach(function (el) {
    var n = SITE.whatsapp;
    el.textContent = '+' + n.slice(0, 2) + ' ' + n.slice(2, 6) + ' ' + n.slice(6);
  });
  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* ---------- Mobile navigation ---------- */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  var desktop = window.matchMedia('(min-width: 1080px)');

  function setNav(open) {
    if (!toggle || !nav) return;
    toggle.setAttribute('aria-expanded', String(open));
    toggle.querySelector('.nav-toggle-label').textContent = open ? 'Close' : 'Menu';
    nav.hidden = !open;
  }
  if (toggle && nav) {
    setNav(desktop.matches);
    toggle.addEventListener('click', function () {
      setNav(toggle.getAttribute('aria-expanded') !== 'true');
    });
    // Close the menu when a link in it is chosen
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a') && !desktop.matches) setNav(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true' && !desktop.matches) {
        setNav(false);
        toggle.focus();
      }
    });
    var onChange = function (e) { setNav(e.matches); };
    if (desktop.addEventListener) desktop.addEventListener('change', onChange);
    else if (desktop.addListener) desktop.addListener(onChange);
  }

  /* ---------- Header border on scroll ---------- */
  var header = document.querySelector('.site-header');
  function onScroll() {
    if (header) header.classList.toggle('is-scrolled', window.scrollY > 8);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Copy buttons ---------- */
  document.querySelectorAll('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var target = document.getElementById(btn.getAttribute('data-copy'));
      var status = document.getElementById(btn.getAttribute('data-copy') + '-status');
      if (!target) return;
      var text = target.textContent.trim();
      function selectFallback() {
        var range = document.createRange();
        range.selectNodeContents(target);
        var sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
        if (status) status.textContent = 'Selected. Press Ctrl+C or Cmd+C to copy.';
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () {
          if (status) status.textContent = 'Copied to clipboard.';
        }, selectFallback);
      } else {
        selectFallback();
      }
    });
  });

  /* ---------- Smooth scrolling (desktop, motion allowed) ---------- */
  var lenis = null;
  var finePointer = window.matchMedia('(pointer: fine) and (min-width: 1024px)').matches;
  if (!reduceMotion && finePointer && typeof window.Lenis === 'function') {
    try {
      lenis = new window.Lenis({ duration: 1.05, smoothWheel: true });
      if (window.gsap && window.ScrollTrigger) {
        lenis.on('scroll', window.ScrollTrigger.update);
        window.gsap.ticker.add(function (time) { lenis.raf(time * 1000); });
        window.gsap.ticker.lagSmoothing(0);
      } else {
        var raf = function (t) { lenis.raf(t); requestAnimationFrame(raf); };
        requestAnimationFrame(raf);
      }
      // In-page anchors (skip link, #privacy, etc.)
      document.querySelectorAll('a[href^="#"]').forEach(function (a) {
        a.addEventListener('click', function (e) {
          var id = a.getAttribute('href');
          if (id.length < 2) return;
          var el = document.querySelector(id);
          if (!el) return;
          e.preventDefault();
          lenis.scrollTo(el, { offset: -90 });
          if (a.classList.contains('skip-link')) el.focus({ preventScroll: true });
        });
      });
    } catch (err) { lenis = null; }
  }

  /* ---------- Motion (GSAP) ----------
     Content is fully visible without JS. Animations only run when GSAP
     loads and the visitor has not asked for reduced motion. */
  if (reduceMotion || !window.gsap) return;
  var gsap = window.gsap;
  if (window.ScrollTrigger) gsap.registerPlugin(window.ScrollTrigger);

  var heroItems = document.querySelectorAll('[data-hero]');
  if (heroItems.length) {
    gsap.from(heroItems, { y: 18, opacity: 0, duration: 0.7, ease: 'power2.out', stagger: 0.08, clearProps: 'transform,opacity' });
  }

  if (!window.ScrollTrigger) return;
  var vh = window.innerHeight;

  document.querySelectorAll('[data-reveal]').forEach(function (el) {
    // Skip anything already on screen so first paint never flickers
    if (el.getBoundingClientRect().top < vh * 0.9) return;
    var kids = el.hasAttribute('data-reveal-stagger') ? el.children : el;
    gsap.from(kids, {
      y: 22, opacity: 0, duration: 0.65, ease: 'power2.out', stagger: 0.07,
      clearProps: 'transform,opacity',
      scrollTrigger: { trigger: el, start: 'top 90%', once: true }
    });
  });

})();

/* ==========================================================
   Home pilot interactions (run without GSAP)
   ========================================================== */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Count-up stats */
  var nums = document.querySelectorAll('[data-count]');
  if (nums.length && !reduce && 'IntersectionObserver' in window) {
    var run = function (el) {
      var target = parseFloat(el.getAttribute('data-count'));
      var pre = el.getAttribute('data-prefix') || '';
      var suf = el.getAttribute('data-suffix') || '';
      var start = null, dur = 1400;
      function step(t) {
        if (!start) start = t;
        var p = Math.min(1, (t - start) / dur);
        var eased = 1 - Math.pow(1 - p, 3);
        el.textContent = pre + Math.round(target * eased) + suf;
        if (p < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    };
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { run(e.target); io.unobserve(e.target); }
      });
    }, { threshold: 0.6 });
    nums.forEach(function (el) { io.observe(el); });
  }

  /* Three-lens showcase: auto-advancing accordion with progress bars.
     Self-contained, so it works the same in any browser or viewer frame. */
  document.querySelectorAll('[data-lens]').forEach(function (root) {
    var items = Array.prototype.slice.call(root.querySelectorAll('.lens-item'));
    var frames = root.querySelectorAll('.lens-frame');
    var pauseBtn = root.querySelector('.lens-pause');
    var current = 0, userPaused = false, hoverPaused = false;
    var auto = !reduce;
    if (!auto && pauseBtn) pauseBtn.hidden = true;

    function show(i, moveFocus) {
      current = i;
      items.forEach(function (it, k) {
        var on = k === i;
        it.classList.toggle('is-active', on);
        var btn = it.querySelector('.lens-btn');
        var panel = it.querySelector('.lens-panel');
        btn.setAttribute('aria-expanded', String(on));
        panel.hidden = !on;
        var bar = it.querySelector('.lens-bar span');
        // restart the progress animation on the newly active item
        bar.style.animation = 'none'; void bar.offsetWidth; bar.style.animation = '';
      });
      frames.forEach(function (f, k) { f.classList.toggle('is-active', k === i); });
      if (moveFocus) items[i].querySelector('.lens-btn').focus();
      syncPause();
    }
    function syncPause() {
      var paused = !auto || userPaused || hoverPaused;
      root.classList.toggle('is-paused', paused);
    }
    items.forEach(function (it, i) {
      it.querySelector('.lens-btn').addEventListener('click', function () { if (!root.classList.contains('is-static')) show(i, false); });
      it.querySelector('.lens-bar span').addEventListener('animationend', function () {
        if (auto && !userPaused && !hoverPaused && i === current && !root.classList.contains('is-static')) show((current + 1) % items.length, false);
      });
    });
    if (pauseBtn) {
      pauseBtn.addEventListener('click', function () {
        userPaused = !userPaused;
        pauseBtn.setAttribute('aria-pressed', String(userPaused));
        pauseBtn.querySelector('.lens-pause-label').textContent = userPaused ? 'Play' : 'Pause';
        syncPause();
      });
    }
    // Pause while the visitor is reading or using the keyboard inside it
    root.addEventListener('mouseenter', function () { hoverPaused = true; syncPause(); });
    root.addEventListener('mouseleave', function () { hoverPaused = false; syncPause(); });
    root.addEventListener('focusin', function () { hoverPaused = true; syncPause(); });
    root.addEventListener('focusout', function (e) { if (!root.contains(e.relatedTarget)) { hoverPaused = false; syncPause(); } });
    // Phones: show every lens as a stacked card (picture, then its text), no auto-advance
    var mq = window.matchMedia('(max-width: 699px)');
    function applyMode() {
      if (mq.matches) {
        root.classList.add('is-static');
        items.forEach(function (it) {
          it.classList.add('is-active');
          it.querySelector('.lens-btn').setAttribute('aria-expanded', 'true');
          it.querySelector('.lens-panel').hidden = false;
        });
      } else {
        root.classList.remove('is-static');
        show(current, false);
      }
    }
    if (mq.addEventListener) mq.addEventListener('change', applyMode); else if (mq.addListener) mq.addListener(applyMode);
    root.classList.add('is-ready');
    show(0, false);
    applyMode();
  });

  /* Accessible tabs */
  document.querySelectorAll('[data-tabs]').forEach(function (root) {
    var tabs = Array.prototype.slice.call(root.querySelectorAll('[role="tab"]'));
    function select(i, focus) {
      tabs.forEach(function (t, k) {
        var on = k === i;
        t.setAttribute('aria-selected', String(on));
        t.tabIndex = on ? 0 : -1;
        var panel = document.getElementById(t.getAttribute('aria-controls'));
        if (panel) panel.hidden = !on;
      });
      if (focus) tabs[i].focus();
      try { tabs[i].scrollIntoView({ block: 'nearest', inline: 'nearest' }); } catch (e) {}
    }
    var bar = root.querySelector('.sprint-tabbar');
    function keepInView(i) {
      // Sprints page: after switching, start the visitor at the top of the new panel
      if (!bar) return;
      var panel = document.getElementById(tabs[i].getAttribute('aria-controls'));
      if (!panel) return;
      var barBox = bar.getBoundingClientRect();
      var top = panel.getBoundingClientRect().top;
      if (top < barBox.bottom) {
        var y = window.scrollY + top - barBox.bottom - 8;
        try { window.scrollTo({ top: y, behavior: 'auto' }); } catch (e) { window.scrollTo(0, y); }
      }
    }
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(i, false); keepInView(i); });
      t.addEventListener('keydown', function (e) {
        var n = null;
        if (e.key === 'ArrowRight') n = (i + 1) % tabs.length;
        else if (e.key === 'ArrowLeft') n = (i - 1 + tabs.length) % tabs.length;
        else if (e.key === 'Home') n = 0;
        else if (e.key === 'End') n = tabs.length - 1;
        if (n !== null) { e.preventDefault(); select(n, true); keepInView(n); }
      });
    });
  });
})();
