// ===========================================
// 黄湘林 Blog v2.0 — Performance Optimized
// ===========================================

// --- Particle background with cached dark state ---
(function() {
  const canvas = document.getElementById('particles');
  if (!canvas || window.innerWidth < 768) return; // disable on mobile
  const ctx = canvas.getContext('2d');

  let particles = [];
  const COUNT = 45;
  const CONNECT = 130;

  // Cached dark state — updated via MutationObserver only
  let isDarkMode = document.documentElement.classList.contains('dark');

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  window.addEventListener('resize', resize);
  resize();

  function getColor(alpha) {
    return isDarkMode
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
      this.vx = (Math.random() - 0.5) * 0.3;
      this.vy = (Math.random() - 0.5) * 0.3 - 0.04;
      this.size = Math.random() * 1.2 + 0.4;
      this.opacity = Math.random() * 0.5 + 0.15;
    }
    update() {
      this.x += this.vx;
      this.y += this.vy;
      if (this.x < -20) this.x = canvas.width + 20;
      if (this.x > canvas.width + 20) this.x = -20;
      if (this.y < -20) this.y = canvas.height + 20;
      if (this.y > canvas.height + 20) this.y = -20;
    }
    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.fillStyle = getColor(this.opacity * 0.6);
      ctx.fill();
    }
  }

  for (let i = 0; i < COUNT; i++) particles.push(new Particle());

  function drawLines() {
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < CONNECT) {
          const alpha = (1 - dist / CONNECT) * 0.06;
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = getColor(alpha);
          ctx.lineWidth = 0.4;
          ctx.stroke();
        }
      }
    }
  }

  let animating = true;
  let inView = true;

  function animate() {
    if (!animating || !inView) return;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(p => { p.update(); p.draw(); });
    drawLines();
    requestAnimationFrame(animate);
  }

  document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
      animating = false;
    } else {
      animating = true;
      animate();
    }
  });

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(function(entries) {
      entries.forEach(entry => {
        inView = entry.isIntersecting;
        if (inView && animating) {
          animate();
        }
      });
    }, { threshold: 0 });
    observer.observe(canvas);
  }

  animate();

  // Watch theme changes instead of polling DOM every frame
  new MutationObserver(function() {
    isDarkMode = document.documentElement.classList.contains('dark');
  }).observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
})();

// --- Scroll reveal (sections & cards) ---
(function() {
  function reveal() {
    var els = document.querySelectorAll('.spa-section[id], .spa-project-card, .spa-skill-category');
    for (var i = 0; i < els.length; i++) {
      var top = els[i].getBoundingClientRect().top;
      if (top < window.innerHeight * 0.9) {
        els[i].style.opacity = '1';
        els[i].style.transform = 'translateY(0)';
      }
    }
  }

  // Init
  var sections = document.querySelectorAll('.spa-section[id]');
  for (var i = 0; i < sections.length; i++) {
    sections[i].style.opacity = '0';
    sections[i].style.transform = 'translateY(24px)';
    sections[i].style.transition = 'opacity 0.5s ease-out, transform 0.5s ease-out';
  }

  window.addEventListener('scroll', reveal, { passive: true });
  window.addEventListener('load', reveal);
  reveal();
})();

// --- Smooth nav anchor scrolling ---
(function() {
  var links = document.querySelectorAll('a[href^="#"]');
  for (var i = 0; i < links.length; i++) {
    links[i].addEventListener('click', function(e) {
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  }
})();


// --- Back-to-top button ---
(function() {
  var btn = document.createElement('button');
  btn.innerHTML = '\u2191';
  btn.className = 'spa-back-top';
  btn.setAttribute('aria-label', '\u56de\u5230\u9876\u90e8');
  document.body.appendChild(btn);

  function toggle() {
    btn.classList.toggle('visible', window.scrollY > 500);
  }
  window.addEventListener('scroll', toggle, { passive: true });
  btn.addEventListener('click', function() { window.scrollTo({ top: 0, behavior: 'smooth' }); });
  toggle();
})();
