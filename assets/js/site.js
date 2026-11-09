/* Ganor site behaviour. No dependencies. */
(() => {
  'use strict';

  const root = document.documentElement;
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const LAUNCH = '30 November';

  /* ---------- Waitlist destination ----------
     Set data-endpoint on the join form (e.g. a Formspree or Google Apps Script URL)
     to collect sign-ups in a sheet. Until then, sign-ups open WhatsApp with the
     details filled in, sent to the Ganor number. */
  const WHATSAPP = '2348103301999';

  /* ---------- Intro (first visit per session) ---------- */
  function runIntro(done) {
    const intro = $('[data-intro]');
    if (!intro || root.classList.contains('no-intro')) { done(); return; }
    const pct = $('[data-intro-pct]', intro);
    const bar = $('[data-intro-bar]', intro);
    const start = performance.now();
    const DURATION = 950;
    const fonts = document.fonts ? document.fonts.ready : Promise.resolve();
    let fontsReady = false;
    fonts.then(() => { fontsReady = true; });
    const ease = t => 1 - Math.pow(1 - t, 3);

    function tick(now) {
      const t = Math.min(1, (now - start) / DURATION);
      const v = Math.round(ease(t) * 100);
      pct.textContent = String(v).padStart(2, '0');
      bar.style.setProperty('--p', ease(t));
      if (t < 1 || (!fontsReady && now - start < 2500)) { requestAnimationFrame(tick); return; }
      intro.classList.add('is-out');
      try { sessionStorage.setItem('ganor-intro', '1'); } catch (e) {}
      setTimeout(done, 260);
      setTimeout(() => intro.classList.add('is-gone'), 900);
    }
    requestAnimationFrame(tick);
  }

  /* ---------- Hero entrance ---------- */
  function startHero() {
    const hero = $('.hero');
    if (!hero) return;
    $$('[data-rise]', hero).forEach((el, i) => el.style.setProperty('--d', i));
    $$('[data-tag]', hero).forEach((el, i) => el.style.setProperty('--d', i));
    const title = $('[data-lines]', hero);
    requestAnimationFrame(() => {
      hero.classList.add('is-ready');
      if (title) title.classList.add('is-in');
    });
  }

  /* ---------- Reveal on scroll ---------- */
  function setupReveal() {
    $$('[data-lines]').forEach(el => $$('.line > span', el).forEach((s, i) => s.style.setProperty('--i', i)));
    const groups = new Map();
    $$('[data-reveal]').forEach(el => {
      const p = el.parentElement;
      const n = groups.get(p) || 0;
      el.style.setProperty('--i', Math.min(n, 6));
      groups.set(p, n + 1);
    });
    const targets = [...$$('[data-reveal]'), ...$$('[data-lines]').filter(el => !el.closest('.hero'))];
    if (!('IntersectionObserver' in window)) { targets.forEach(el => el.classList.add('is-in')); return; }
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (!e.isIntersecting) return;
        e.target.classList.add('is-in');
        e.target.dispatchEvent(new CustomEvent('reveal'));
        io.unobserve(e.target);
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.12 });
    targets.forEach(el => io.observe(el));
  }

  /* ---------- Nav: solid after the hero, theme colour follows ---------- */
  function setupNav() {
    const nav = $('[data-nav]');
    const hero = $('.hero');
    const meta = $('meta[name="theme-color"]');
    if (!nav) return;
    if (!hero) { nav.classList.add('is-solid'); if (meta) meta.content = '#F6F1E7'; return; }
    let solid = null;
    const update = () => {
      const s = hero.getBoundingClientRect().bottom <= nav.offsetHeight;
      if (s === solid) return;
      solid = s;
      nav.classList.toggle('is-solid', s);
      if (meta) meta.content = s ? '#F6F1E7' : '#3730B8';
    };
    update();
    addEventListener('scroll', () => requestAnimationFrame(update), { passive: true });
    addEventListener('resize', update);
  }

  /* ---------- Mobile menu ---------- */
  function setupMenu() {
    const sheet = $('[data-menu]');
    const open = $('[data-menu-open]');
    if (!sheet || !open || typeof sheet.showModal !== 'function') return;
    open.addEventListener('click', () => sheet.showModal());
    $('[data-menu-close]', sheet).addEventListener('click', () => sheet.close());
    sheet.addEventListener('click', e => {
      if (e.target === sheet || e.target.closest('a')) sheet.close();
    });
  }

  /* ---------- Hero search (pre-launch) ---------- */
  function setupSearch() {
    const form = $('[data-search]');
    const msg = $('[data-search-msg]');
    if (!form || !msg) return;
    const say = () => {
      const type = form.type.value;
      const area = form.area.value;
      const what = type ? type.toLowerCase() : 'events';
      const where = area ? ` in ${area}` : ' in Kano';
      msg.innerHTML = '';
      msg.append(`Ganor opens on ${LAUNCH}. `);
      const a = document.createElement('a');
      a.href = '#join';
      a.textContent = 'Join the list';
      a.addEventListener('click', () => prefill({ role: 'guest', interest: type }));
      msg.append(a, ` and we’ll tell you when ${what}${where} go live.`);
      msg.hidden = false;
    };
    form.addEventListener('submit', e => { e.preventDefault(); say(); });
    $$('[data-chip]').forEach(chip => chip.addEventListener('click', () => {
      form.type.value = chip.dataset.chip;
      say();
    }));
  }

  /* ---------- Prefill the join form from anywhere ---------- */
  function prefill({ role, interest }) {
    const form = $('[data-join]');
    if (!form) return;
    if (role) { const r = form.querySelector(`input[name="role"][value="${role}"]`); if (r) r.checked = true; }
    if (interest !== undefined && interest !== null) {
      const opt = [...form.interest.options].find(o => o.text === interest);
      if (opt) form.interest.value = opt.value || opt.text;
    }
  }
  function setupPrefill() {
    $$('[data-interest]').forEach(a => a.addEventListener('click', () => prefill({ role: 'guest', interest: a.dataset.interest })));
    $$('[data-interest-role]').forEach(a => a.addEventListener('click', () => prefill({ role: a.dataset.interestRole })));
  }

  /* ---------- Scroll timeline (how it works) ---------- */
  function setupSteps() {
    const list = $('[data-steps]');
    if (!list) return;
    const fill = $('[data-steps-fill]', list);
    const steps = $$('[data-step]', list);
    const update = () => {
      const vh = innerHeight;
      const r = list.getBoundingClientRect();
      const line = vh * 0.62;
      const p = Math.max(0, Math.min(1, (line - r.top) / r.height));
      fill.style.setProperty('--p', p.toFixed(4));
      steps.forEach(step => {
        const active = step.getBoundingClientRect().top + 40 < line;
        if (active !== step.classList.contains('is-active')) {
          step.classList.toggle('is-active', active);
          if (active) { const img = $('[data-replay]', step); if (img) replay(img); }
        }
      });
    };
    let raf = 0;
    addEventListener('scroll', () => { if (!raf) raf = requestAnimationFrame(() => { raf = 0; update(); }); }, { passive: true });
    addEventListener('resize', update);
    update();
  }
  function replay(img) {
    const src = img.getAttribute('src').split('?')[0];
    img.setAttribute('src', `${src}?r=${Date.now()}`);
  }

  /* ---------- Rolling digits ---------- */
  function digitEl() {
    const d = document.createElement('span');
    d.className = 'digit';
    const col = document.createElement('span');
    col.className = 'digit__col';
    for (let n = 0; n < 10; n++) { const s = document.createElement('span'); s.textContent = n; col.append(s); }
    d.append(col);
    return d;
  }
  function setDigits(el, value, minLen = 2) {
    const str = String(value).padStart(minLen, '0');
    while (el.children.length < str.length) el.prepend(digitEl());
    while (el.children.length > str.length) el.firstElementChild.remove();
    [...el.children].forEach((d, i) => d.firstElementChild.style.setProperty('--n', str[i]));
    el.setAttribute('aria-label', str);
  }

  /* ---------- Countdown to launch ---------- */
  function setupCountdown() {
    const box = $('[data-countdown]');
    if (!box) return;
    const target = new Date(box.dataset.countdown).getTime();
    const units = { d: $('[data-unit="d"]', box), h: $('[data-unit="h"]', box), m: $('[data-unit="m"]', box) };
    Object.values(units).forEach(u => u.setAttribute('role', 'text'));
    const render = () => {
      let s = Math.max(0, Math.floor((target - Date.now()) / 1000));
      const d = Math.floor(s / 86400); s -= d * 86400;
      const h = Math.floor(s / 3600); s -= h * 3600;
      const m = Math.floor(s / 60);
      setDigits(units.d, d); setDigits(units.h, h); setDigits(units.m, m);
      box.setAttribute('aria-label', `${d} days, ${h} hours and ${m} minutes until Ganor opens in Kano`);
      if (target - Date.now() <= 0) { box.closest('.join__copy').querySelector('.label').lastChild.textContent = 'Ganor is open in Kano'; }
    };
    // start from zero so the digits roll in when the section appears
    Object.values(units).forEach(u => setDigits(u, 0));
    const go = () => { render(); setInterval(render, 15000); };
    if ('IntersectionObserver' in window) {
      const io = new IntersectionObserver(([e]) => { if (e.isIntersecting) { io.disconnect(); setTimeout(go, 150); } }, { threshold: 0.4 });
      io.observe(box);
    } else go();
  }

  /* ---------- Counters in the bento ---------- */
  function setupCounters() {
    $$('[data-count]').forEach(el => {
      const value = +el.dataset.count;
      el.textContent = '';
      setDigits(el, 0, String(value).length);
      const card = el.closest('[data-reveal]') || el;
      const run = () => setTimeout(() => setDigits(el, value, String(value).length), 200);
      if (card.classList.contains('is-in')) run(); else card.addEventListener('reveal', run, { once: true });
    });
  }

  /* ---------- Switches ---------- */
  function setupSwitches() {
    $$('.switch').forEach(sw => sw.addEventListener('click', () => {
      sw.setAttribute('aria-checked', sw.getAttribute('aria-checked') === 'true' ? 'false' : 'true');
    }));
  }

  /* ---------- Gate check-in demo ---------- */
  function setupGate() {
    const gate = $('[data-gate]');
    if (!gate) return;
    const img = $('[data-gate-icon]', gate);
    const title = $('[data-gate-title]', gate);
    const sub = $('[data-gate-sub]', gate);
    const STATES = {
      ok: { icon: 'admitted', title: 'Admitted', sub: 'A. Musa · Regular · Admit one' },
      warn: { icon: 'already-checked-in', title: 'Already checked in', sub: 'First scanned 10:12 · Gate 1' },
      bad: { icon: 'not-valid', title: 'Not a valid ticket', sub: 'Send the guest to the help desk' }
    };
    let timer = 0;
    $$('[data-scan]').forEach(btn => btn.addEventListener('click', () => {
      clearTimeout(timer);
      const k = btn.dataset.scan;
      const s = STATES[k];
      gate.classList.remove('is-shown');
      const show = () => {
        img.src = `assets/gate/ganor-status-${s.icon}.svg?r=${Date.now()}`;
        title.textContent = s.title;
        sub.textContent = s.sub;
        gate.dataset.state = k;
        requestAnimationFrame(() => gate.classList.add('is-shown'));
        timer = setTimeout(() => { gate.dataset.state = 'ready'; gate.classList.remove('is-shown'); }, 4200);
      };
      if (reduced.matches) { show(); return; }
      gate.dataset.state = 'checking';
      timer = setTimeout(show, 900);
    }));
  }

  /* ---------- FAQ accordion ---------- */
  function setupAccordion() {
    $$('[data-acc] .acc__btn').forEach(btn => {
      const panel = document.getElementById(btn.getAttribute('aria-controls'));
      panel.hidden = false;
      panel.classList.toggle('is-open', btn.getAttribute('aria-expanded') === 'true');
      btn.addEventListener('click', () => {
        const open = btn.getAttribute('aria-expanded') !== 'true';
        btn.setAttribute('aria-expanded', String(open));
        panel.classList.toggle('is-open', open);
      });
    });
  }

  /* ---------- Join form ---------- */
  function setupJoin() {
    const form = $('[data-join]');
    if (!form) return;
    const done = $('[data-join-done]', form);
    const label = $('[data-join-label]', form);
    const normalise = v => v.replace(/[^\d+]/g, '').replace(/^\+/, '');
    const validPhone = v => /^(0[789][01]\d{8}|234[789][01]\d{8})$/.test(normalise(v));
    const fieldOf = name => form.elements[name].closest('.field');

    const check = name => {
      const el = form.elements[name];
      const ok = name === 'phone' ? validPhone(el.value) : el.value.trim().length > 1;
      fieldOf(name).classList.toggle('is-invalid', !ok);
      el.setAttribute('aria-invalid', String(!ok));
      return ok;
    };
    ['name', 'phone'].forEach(n => {
      const el = form.elements[n];
      const err = form.querySelector(`[data-err="${n}"]`);
      err.id = `err-${n}`;
      el.setAttribute('aria-describedby', err.id);
      el.addEventListener('blur', () => { if (el.value) check(n); });
      el.addEventListener('input', () => { if (fieldOf(n).classList.contains('is-invalid')) check(n); });
    });

    form.addEventListener('submit', async e => {
      e.preventDefault();
      const okName = check('name');
      const okPhone = check('phone');
      if (!okName || !okPhone) { form.querySelector('.is-invalid input').focus(); return; }
      const role = form.role.value;
      const roleText = { host: 'hosting an event', guest: 'looking for events', business: 'a local business' }[role];
      const data = {
        name: form.elements.name.value.trim(),
        phone: form.elements.phone.value.trim(),
        role,
        interest: form.interest.value || '',
        source: 'ganor.ng'
      };
      const endpoint = form.dataset.endpoint;
      label.textContent = 'Sending…';
      if (endpoint) {
        try {
          const res = await fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(data) });
          if (!res.ok) throw new Error(res.status);
        } catch (err) {
          label.textContent = 'Try again';
          return;
        }
      } else {
        const text = `Hi Ganor, please add me to the list.\nName: ${data.name}\nI'm ${roleText}.` + (data.interest ? `\nInterested in: ${data.interest}` : '');
        window.open(`https://wa.me/${WHATSAPP}?text=${encodeURIComponent(text)}`, '_blank', 'noopener');
      }
      label.textContent = 'Join the list';
      done.hidden = false;
      form.reset();
    });
  }

  /* ---------- Boot ---------- */
  setupNav();
  setupMenu();
  setupSearch();
  setupPrefill();
  setupSteps();
  setupSwitches();
  setupGate();
  setupAccordion();
  setupJoin();
  setupReveal();
  setupCounters();
  setupCountdown();
  runIntro(startHero);
})();
