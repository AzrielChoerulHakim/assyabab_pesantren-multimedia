'use strict';
// Progressive enhancements; main content and links work without JavaScript.
(() => {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const fine = matchMedia('(hover: hover) and (pointer: fine)');
  const toggle = document.querySelector('.menu-toggle');
  const menu = document.querySelector('#mobile-menu');
  const closeMenu = (focus = false) => {
    if (!menu || !toggle) return;
    menu.hidden = true; toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Buka navigasi');
    document.body.classList.remove('menu-open');
    if (focus) toggle.focus();
  };
  toggle?.addEventListener('click', () => {
    if (!menu) return;
    const open = menu.hidden; menu.hidden = !open;
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Tutup navigasi' : 'Buka navigasi');
    document.body.classList.toggle('menu-open', open);
    if (open) menu.querySelector('a')?.focus();
  });
  menu?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => closeMenu()));
  addEventListener('resize', () => { if (innerWidth > 700) closeMenu(); }, { passive: true });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu && !menu.hidden) closeMenu(true);
    if (event.key !== 'Tab' || !menu || menu.hidden) return;
    const items = [toggle, ...menu.querySelectorAll('a')].filter(Boolean);
    if (event.shiftKey && document.activeElement === items[0]) {
      event.preventDefault(); items.at(-1).focus();
    } else if (!event.shiftKey && document.activeElement === items.at(-1)) {
      event.preventDefault(); items[0].focus();
    }
  });
  const targets = [...document.querySelectorAll('[data-reveal]')];
  if (!reduced.matches && 'IntersectionObserver' in window) {
    document.documentElement.classList.add('has-motion');
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); }
      });
    }, { threshold: 0.06, rootMargin: '0px 0px 20px 0px' });
    targets.forEach(target => observer.observe(target));
  }
  reduced.addEventListener?.('change', event => {
    if (event.matches) document.documentElement.classList.remove('has-motion');
  });
  const progress = document.querySelector('.scroll-progress');
  let scrollFrame = 0;
  const paintProgress = () => {
    const range = document.documentElement.scrollHeight - innerHeight;
    const value = range > 0 ? Math.max(0, Math.min(1, scrollY / range)) : 0;
    if (progress) progress.style.transform = `scaleX(${value})`;
    scrollFrame = 0;
  };
  addEventListener('scroll', () => {
    if (!scrollFrame) scrollFrame = requestAnimationFrame(paintProgress);
  }, { passive: true });
  paintProgress();
  // Small desktop-only CSS book tilt; no WebGL, canvas, or continuous render loop.
  const stage = document.querySelector('.hero-art');
  const book = document.querySelector('.quran-book');
  let tiltFrame = 0, x = 0, y = 0;
  stage?.addEventListener('pointermove', event => {
    if (!book || reduced.matches || !fine.matches) return;
    const rect = stage.getBoundingClientRect();
    x = (event.clientX - rect.left) / rect.width - 0.5;
    y = (event.clientY - rect.top) / rect.height - 0.5;
    if (tiltFrame) return;
    tiltFrame = requestAnimationFrame(() => {
      book.style.transform = `rotateX(${12-y*7}deg) rotateY(${-23+x*12}deg) rotateZ(${11+x*3}deg)`;
      tiltFrame = 0;
    });
  }, { passive: true });
  stage?.addEventListener('pointerleave', () => {
    cancelAnimationFrame(tiltFrame); tiltFrame = 0;
    if (book) book.style.transform = '';
  });
  const courses = [...document.querySelectorAll('.four-t-list details')];
  courses.forEach(course => course.addEventListener('toggle', () => {
    if (course.open) courses.forEach(other => { if (other !== course) other.open = false; });
  }));
  const dayButtons = [...document.querySelectorAll('[data-day]')];
  const dayPanels = [...document.querySelectorAll('[data-day-panel]')];
  function selectDay(key) {
    dayButtons.forEach(button => {
      const active = button.dataset.day === key;
      button.classList.toggle('active', active); button.setAttribute('aria-pressed', String(active));
    });
    dayPanels.forEach(panel => { panel.hidden = panel.dataset.dayPanel !== key; });
  }
  dayButtons.forEach((button, index) => {
    button.addEventListener('click', () => selectDay(button.dataset.day));
    button.addEventListener('keydown', event => {
      let target = null;
      if (event.key === 'ArrowRight') target = (index+1) % dayButtons.length;
      if (event.key === 'ArrowLeft') target = (index-1+dayButtons.length) % dayButtons.length;
      if (event.key === 'Home') target = 0;
      if (event.key === 'End') target = dayButtons.length-1;
      if (target === null) return;
      event.preventDefault(); dayButtons[target].focus(); selectDay(dayButtons[target].dataset.day);
    });
  });
  selectDay('pagi');
  const gallery = document.querySelector('.gallery-track');
  const prev = document.querySelector('[data-gallery-prev]');
  const next = document.querySelector('[data-gallery-next]');
  const updateGallery = () => {
    if (!gallery) return;
    if (prev) prev.disabled = gallery.scrollLeft < 3;
    if (next) next.disabled = gallery.scrollLeft + gallery.clientWidth >= gallery.scrollWidth - 3;
  };
  function moveGallery(direction) {
    if (!gallery) return;
    const inset = parseFloat(getComputedStyle(gallery).paddingLeft) || 0;
    const positions = [...gallery.querySelectorAll('.gallery-item')].map(item => item.offsetLeft - gallery.offsetLeft - inset);
    const current = gallery.scrollLeft;
    const destination = direction > 0
      ? positions.find(position => position > current+8) ?? gallery.scrollWidth
      : [...positions].reverse().find(position => position < current-8) ?? 0;
    gallery.scrollTo({ left: destination, behavior: reduced.matches ? 'instant' : 'smooth' });
  }
  prev?.addEventListener('click', () => moveGallery(-1)); next?.addEventListener('click', () => moveGallery(1));
  gallery?.addEventListener('scroll', updateGallery, { passive: true });
  gallery?.addEventListener('keydown', event => {
    if (event.target === gallery && (event.key === 'ArrowLeft' || event.key === 'ArrowRight')) {
      event.preventDefault(); moveGallery(event.key === 'ArrowRight' ? 1 : -1);
    }
  });
  addEventListener('resize', updateGallery, { passive: true }); updateGallery();
  const lightbox = document.querySelector('.lightbox');
  let lastPhoto = null;
  if (lightbox && typeof lightbox.showModal === 'function') {
    document.querySelectorAll('[data-lightbox]').forEach(link => link.addEventListener('click', event => {
      event.preventDefault();
      const image = lightbox.querySelector('img');
      image.src = link.href; image.alt = link.querySelector('img')?.alt || 'Dokumentasi Pesantren Assyabab';
      lightbox.querySelector('figcaption').textContent = link.dataset.caption || '';
      lastPhoto = link; lightbox.showModal();
    }));
    lightbox.querySelector('.lightbox-close')?.addEventListener('click', () => lightbox.close());
    lightbox.addEventListener('click', event => {
      if (event.target !== lightbox) return;
      const rect = lightbox.getBoundingClientRect();
      if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) lightbox.close();
    });
    lightbox.addEventListener('close', () => lastPhoto?.focus({ preventScroll: true }));
  }
})();
