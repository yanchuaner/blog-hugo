// Particle background - minimal & elegant
(function() {
  const canvas = document.getElementById('particles');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  let particles = [];
  const PARTICLE_COUNT = 50;
  const CONNECT_DIST = 130;

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  window.addEventListener('resize', resize);
  resize();

  function isDark() {
    if (document.documentElement.classList.contains('dark')) return true;
    if (document.documentElement.getAttribute('data-theme') === 'dark') return true;
    return false;
  }

  function getColor(alpha) {
    return isDark()
      ? `rgba(255,255,255,${alpha})`
      : `rgba(0,0,0,${alpha})`;
  }

  class Particle {
    constructor() {
      this.reset(true);
    }
    reset(initial) {
      this.x = Math.random() * canvas.width;
      this.y = initial ? Math.random() * canvas.height : canvas.height + 10;
      this.vx = (Math.random() - 0.5) * 0.35;
      this.vy = (Math.random() - 0.5) * 0.35 - 0.05;
      this.size = Math.random() * 1.5 + 0.4;
      this.opacity = Math.random() * 0.6 + 0.2;
    }
    update() {
      this.x += this.vx;
      this.y += this.vy;
      // wrap around
      if (this.x < -20) this.x = canvas.width + 20;
      if (this.x > canvas.width + 20) this.x = -20;
      if (this.y < -20) this.y = canvas.height + 20;
      if (this.y > canvas.height + 20) this.y = -20;
    }
    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.fillStyle = getColor(this.opacity * 0.7);
      ctx.fill();
    }
  }

  for (let i = 0; i < PARTICLE_COUNT; i++) {
    particles.push(new Particle());
  }

  function drawLines() {
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < CONNECT_DIST) {
          const alpha = (1 - dist / CONNECT_DIST) * 0.08;
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = getColor(alpha);
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }
  }

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(p => { p.update(); p.draw(); });
    drawLines();
    requestAnimationFrame(animate);
  }

  animate();
})();

// Scroll reveal animations
(function() {
  function reveal() {
    const reveals = document.querySelectorAll('.spa-section, .spa-card, .spa-post-entry');
    reveals.forEach(el => {
      const top = el.getBoundingClientRect().top;
      const windowH = window.innerHeight;
      if (top < windowH * 0.88) {
        el.style.opacity = '1';
        el.style.transform = 'translateY(0)';
      }
    });
  }

  // Initialize: hide sections for reveal
  document.querySelectorAll('.spa-section').forEach(el => {
    if (!el.classList.contains('spa-hero')) {
      el.style.opacity = '0';
      el.style.transform = 'translateY(30px)';
      el.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
    }
  });

  window.addEventListener('scroll', reveal);
  window.addEventListener('load', reveal);
  reveal();
})();

// Smooth nav highlighting
(function() {
  const sections = document.querySelectorAll('.spa-section[id], .spa-hero[id]');
  const navLinks = document.querySelectorAll('.spa-nav a[href^="#"]');

  function setActive() {
    let current = 'hero';
    sections.forEach(section => {
      const rect = section.getBoundingClientRect();
      if (rect.top <= window.innerHeight * 0.4) {
        current = section.id;
      }
    });
    navLinks.forEach(link => {
      const href = link.getAttribute('href');
      link.classList.toggle('active', href === '#' + current);
    });
  }

  window.addEventListener('scroll', setActive, { passive: true });
  setActive();

  navLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
})();

// Dark mode sync: PaperMod [data-theme] ↔ .dark class
(function() {
  function syncDark() {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    document.documentElement.classList.toggle('dark', isDark);
  }
  syncDark();
  const observer = new MutationObserver(syncDark);
  observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
})();

// Back-to-top button
(function() {
  const btn = document.createElement('button');
  btn.innerHTML = '↑';
  btn.className = 'spa-back-top';
  btn.setAttribute('aria-label', '回到顶部');
  document.body.appendChild(btn);

  const style = document.createElement('style');
  style.textContent = '.spa-back-top{position:fixed;bottom:2rem;right:2rem;z-index:99;width:40px;height:40px;border-radius:50%;border:1px solid var(--spa-border);background:var(--spa-surface);color:var(--spa-text-secondary);font-size:1.1rem;cursor:pointer;opacity:0;transform:translateY(10px);transition:all 0.3s;box-shadow:var(--spa-shadow);pointer-events:none}.spa-back-top.visible{opacity:1;transform:translateY(0);pointer-events:auto}.spa-back-top:hover{background:var(--spa-accent);color:#fff;border-color:var(--spa-accent)}';
  document.head.appendChild(style);

  function toggle() {
    btn.classList.toggle('visible', window.scrollY > 600);
  }
  window.addEventListener('scroll', toggle, { passive: true });
  btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  toggle();
})();
