(function() {
    'use strict';

    // ——————————————————————————————————
    // LOADER
    // ——————————————————————————————————
    window.addEventListener('load', () => {
        setTimeout(() => {
        const loader = document.getElementById('loader');
        if (loader) loader.classList.add('loaded');
        }, 2400);
    });

    // ——————————————————————————————————
    // CUSTOM CURSOR
    // ——————————————————————————————————
    const cursorDot  = document.getElementById('cursor-dot');
    const cursorRing = document.getElementById('cursor-ring');
    let mouseX = 0, mouseY = 0, ringX = 0, ringY = 0;

    document.addEventListener('mousemove', e => {
        mouseX = e.clientX; mouseY = e.clientY;
        cursorDot.style.left = mouseX + 'px';
        cursorDot.style.top  = mouseY + 'px';
    });

    // Cursor trail
    const TRAIL_COUNT = 8;
    const trails = [];
    for (let i = 0; i < TRAIL_COUNT; i++) {
        const el = document.createElement('div');
        el.className = 'cursor-trail';
        el.style.opacity = (1 - i / TRAIL_COUNT) * 0.5;
        el.style.width = el.style.height = (4 - i * 0.3) + 'px';
        document.body.appendChild(el);
        trails.push({ el, x: 0, y: 0 });
    }

    function animateCursor() {
        ringX += (mouseX - ringX) * 0.14;
        ringY += (mouseY - ringY) * 0.14;
        cursorRing.style.left = ringX + 'px';
        cursorRing.style.top  = ringY + 'px';

        let prevX = mouseX, prevY = mouseY;
        trails.forEach((t, i) => {
        t.x += (prevX - t.x) * (0.25 - i * 0.02);
        t.y += (prevY - t.y) * (0.25 - i * 0.02);
        t.el.style.left = t.x + 'px';
        t.el.style.top  = t.y + 'px';
        t.el.style.opacity = mouseX ? (0.35 - i * 0.04) : 0;
        prevX = t.x; prevY = t.y;
        });
        requestAnimationFrame(animateCursor);
    }
    animateCursor();

    // ——————————————————————————————————
    // STAR CANVAS
    // ——————————————————————————————————
    const starCanvas = document.getElementById('canvas-stars');
    const starCtx = starCanvas.getContext('2d');

    function resizeStars() {
        starCanvas.width  = window.innerWidth;
        starCanvas.height = window.innerHeight;
    }
    resizeStars();
    window.addEventListener('resize', resizeStars);

    const STAR_COUNT = 320;
    const stars = Array.from({ length: STAR_COUNT }, () => ({
        x: Math.random(), y: Math.random(),
        r: Math.random() * 1.6 + 0.2,
        a: Math.random(),
        s: Math.random() * 0.4 + 0.1,
        twinkleOffset: Math.random() * Math.PI * 2
    }));

    // Galaxy blobs
    const galaxies = [
        { x: 0.78, y: 0.12, r: 110, color: 'rgba(26,79,196,0.09)' },
        { x: 0.12, y: 0.65, r: 80,  color: 'rgba(124,58,237,0.07)' },
        { x: 0.55, y: 0.82, r: 95,  color: 'rgba(0,212,255,0.06)'  }
    ];

    let starT = 0;
    function drawStars() {
        const W = starCanvas.width, H = starCanvas.height;
        starCtx.clearRect(0, 0, W, H);

        // Galaxy blobs
        galaxies.forEach(g => {
        const grd = starCtx.createRadialGradient(g.x*W, g.y*H, 0, g.x*W, g.y*H, g.r);
        grd.addColorStop(0, g.color);
        grd.addColorStop(1, 'transparent');
        starCtx.fillStyle = grd;
        starCtx.beginPath();
        starCtx.arc(g.x*W, g.y*H, g.r, 0, Math.PI*2);
        starCtx.fill();
        });

        // Stars
        stars.forEach(s => {
        const twinkle = 0.4 + 0.6 * Math.sin(starT * s.s + s.twinkleOffset);
        starCtx.globalAlpha = s.a * twinkle;
        starCtx.fillStyle = '#e8f4ff';
        starCtx.beginPath();
        starCtx.arc(s.x * W, s.y * H, s.r, 0, Math.PI * 2);
        starCtx.fill();
        });
        starCtx.globalAlpha = 1;
        starT += 0.02;
        requestAnimationFrame(drawStars);
    }
    drawStars();

    // ——————————————————————————————————
    // HERO PARTICLES
    // ——————————————————————————————————
    const pCanvas = document.getElementById('particles-canvas');
    const pCtx = pCanvas.getContext('2d');

    function resizeParticles() {
        pCanvas.width  = pCanvas.offsetWidth;
        pCanvas.height = pCanvas.offsetHeight;
    }
    resizeParticles();
    window.addEventListener('resize', resizeParticles);

    const PARTICLE_COUNT = 60;
    const particles = Array.from({ length: PARTICLE_COUNT }, () => ({
        x: Math.random(),
        y: Math.random(),
        vx: (Math.random() - 0.5) * 0.0003,
        vy: (Math.random() - 0.5) * 0.0003,
        r: Math.random() * 2 + 0.5,
        a: Math.random() * 0.5 + 0.1,
        color: Math.random() > 0.6 ? '#00d4ff' : Math.random() > 0.5 ? '#00ffe0' : '#1a4fc4'
    }));

    let pT = 0;
    function animateParticles() {
        const W = pCanvas.width, H = pCanvas.height;
        pCtx.clearRect(0, 0, W, H);

        particles.forEach(p => {
        p.x += p.vx;
        p.y += p.vy;
        if (p.x < 0) p.x = 1;
        if (p.x > 1) p.x = 0;
        if (p.y < 0) p.y = 1;
        if (p.y > 1) p.y = 0;

        const pulse = 0.5 + 0.5 * Math.sin(pT * 0.5 + p.x * 10);
        pCtx.globalAlpha = p.a * pulse;
        pCtx.fillStyle = p.color;
        pCtx.shadowBlur = 6;
        pCtx.shadowColor = p.color;
        pCtx.beginPath();
        pCtx.arc(p.x * W, p.y * H, p.r, 0, Math.PI * 2);
        pCtx.fill();

        // Connect nearby particles
        particles.forEach(p2 => {
            const dx = (p.x - p2.x) * W, dy = (p.y - p2.y) * H;
            const dist = Math.sqrt(dx*dx + dy*dy);
            if (dist < 80 && dist > 0) {
            pCtx.globalAlpha = (1 - dist / 80) * 0.12;
            pCtx.strokeStyle = '#00d4ff';
            pCtx.shadowBlur = 0;
            pCtx.lineWidth = 0.5;
            pCtx.beginPath();
            pCtx.moveTo(p.x * W, p.y * H);
            pCtx.lineTo(p2.x * W, p2.y * H);
            pCtx.stroke();
            }
        });
        });
        pCtx.globalAlpha = 1;
        pCtx.shadowBlur = 0;
        pT += 0.016;
        requestAnimationFrame(animateParticles);
    }
    animateParticles();

    // ——————————————————————————————————
    // NAVBAR SCROLL
    // ——————————————————————————————————
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
        navbar.classList.toggle('scrolled', window.scrollY > 60);
    }, { passive: true });

    // ——————————————————————————————————
    // MOBILE NAV TOGGLE
    // ——————————————————————————————————
    const navToggle = document.querySelector('.nav-toggle');
    const mainNav   = document.getElementById('main-nav');
    navToggle?.addEventListener('click', () => {
        const expanded = navToggle.getAttribute('aria-expanded') === 'true';
        navToggle.setAttribute('aria-expanded', !expanded);
        mainNav.classList.toggle('open');
    });
    // Close on link click
    mainNav?.querySelectorAll('a').forEach(a => {
        a.addEventListener('click', () => {
        navToggle.setAttribute('aria-expanded', 'false');
        mainNav.classList.remove('open');
        });
    });

    // ——————————————————————————————————
    // SCROLL ANIMATIONS (Intersection Observer)
    // ——————————————————————————————————
    const fadeEls = document.querySelectorAll('.fade-in, .fade-in-left, .timeline-item, .eco-card');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(e => {
        if (e.isIntersecting) {
            e.target.classList.add('visible');
            observer.unobserve(e.target);
        }
        });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    fadeEls.forEach(el => observer.observe(el));

    // ——————————————————————————————————
    // STAT BARS (animate on visibility)
    // ——————————————————————————————————
    const statBars = document.querySelectorAll('.stat-bar-fill');
    const barObserver = new IntersectionObserver(entries => {
        entries.forEach(e => {
        if (e.isIntersecting) {
            const w = e.target.dataset.width;
            setTimeout(() => { e.target.style.width = w + '%'; }, 200);
            barObserver.unobserve(e.target);
        }
        });
    }, { threshold: 0.5 });
    statBars.forEach(b => barObserver.observe(b));

    // ——————————————————————————————————
    // ECOSYSTEM FILTER
    // ——————————————————————————————————
    const ecoButtons = document.querySelectorAll('.eco-nav button');
    const ecoCards   = document.querySelectorAll('.eco-card');
    ecoButtons.forEach(btn => {
        btn.addEventListener('click', () => {
        ecoButtons.forEach(b => { b.classList.remove('active'); b.setAttribute('aria-selected', 'false'); });
        btn.classList.add('active');
        btn.setAttribute('aria-selected', 'true');
        const filter = btn.dataset.filter;
        ecoCards.forEach(card => {
            const match = filter === 'all' || card.dataset.category === filter;
            card.style.display = match ? '' : 'none';
        });
        });
    });

    // ——————————————————————————————————
    // RIPPLE EFFECT
    // ——————————————————————————————————
    document.querySelectorAll('.ripple-container').forEach(el => {
        el.addEventListener('click', function(e) {
        const rect = this.getBoundingClientRect();
        const ripple = document.createElement('span');
        ripple.className = 'ripple';
        const size = Math.max(rect.width, rect.height);
        ripple.style.cssText = `
            width: ${size}px; height: ${size}px;
            left: ${e.clientX - rect.left - size/2}px;
            top:  ${e.clientY - rect.top  - size/2}px;
        `;
        this.appendChild(ripple);
        ripple.addEventListener('animationend', () => ripple.remove());
        });
    });

    // Add ripple to all cards
    document.querySelectorAll('.company-card, .eco-card, .page-card').forEach(el => {
        el.classList.add('ripple-container');
        el.addEventListener('click', function(e) {
        const rect = this.getBoundingClientRect();
        const ripple = document.createElement('span');
        ripple.className = 'ripple';
        const size = Math.max(rect.width, rect.height);
        ripple.style.cssText = `
            width: ${size}px; height: ${size}px;
            left: ${e.clientX - rect.left - size/2}px;
            top:  ${e.clientY - rect.top  - size/2}px;
        `;
        this.appendChild(ripple);
        ripple.addEventListener('animationend', () => ripple.remove());
        });
    });

    // ——————————————————————————————————
    // PARALLAX ON MOUSE MOVE
    // ——————————————————————————————————
    document.addEventListener('mousemove', e => {
        const x = (e.clientX / window.innerWidth  - 0.5);
        const y = (e.clientY / window.innerHeight - 0.5);
        document.querySelector('.nebula-1').style.transform = `translate(${x*18}px, ${y*12}px)`;
        document.querySelector('.nebula-2').style.transform = `translate(${x*-12}px, ${y*18}px)`;
        document.querySelector('.nebula-3').style.transform = `translate(${x*20}px, ${y*-14}px)`;
    });

    // ——————————————————————————————————
    // PARALLAX SCROLL
    // ——————————————————————————————————
    let ticking = false;
    window.addEventListener('scroll', () => {
        if (!ticking) {
        requestAnimationFrame(() => {
            const scrollY = window.scrollY;
            const heroContent = document.querySelector('.hero-content');
            if (heroContent) {
                heroContent.style.transform = `translateY(${scrollY * 0.35}px)`;
                heroContent.style.opacity = Math.max(0, 1 - scrollY / 750);
            }
            ticking = false;
        });
        ticking = true;
        }
    }, { passive: true });

    // ——————————————————————————————————
    // HERO COUNTER ANIMATION
    // ——————————————————————————————————
    function animateCounter(el, target, suffix, duration) {
        let start = 0;
        const step = target / (duration / 16);
        const timer = setInterval(() => {
        start = Math.min(start + step, target);
        el.textContent = Math.floor(start) + suffix;
        if (start >= target) clearInterval(timer);
        }, 16);
    }

    // Animate hero stats on load
    const heroObserver = new IntersectionObserver(entries => {
        if (entries[0].isIntersecting) {
        document.querySelectorAll('.hero-stat-num').forEach(el => {
            const text = el.textContent;
            if (text.includes('75K+')) animateCounter(el, 75, 'K+', 1500);
            else if (text.includes('1M+')) animateCounter(el, 1, 'M+', 1200);
        });
        heroObserver.disconnect();
        }
    }, { threshold: 0.5 });
    const heroStats = document.querySelector('.hero-stats');
    if (heroStats) heroObserver.observe(heroStats);

    // ——————————————————————————————————
    // STAGGER DELAYS
    // ——————————————————————————————————
    document.querySelectorAll('.stagger-children > *').forEach((el, i) => {
        el.style.setProperty('--i', i);
    });

    // ——————————————————————————————————
    // KEYBOARD NAVIGATION (eco filter)
    // ——————————————————————————————————
    document.querySelector('.eco-nav')?.addEventListener('keydown', e => {
        const btns = [...document.querySelectorAll('.eco-nav button')];
        const idx  = btns.indexOf(document.activeElement);
        if (e.key === 'ArrowRight' && idx < btns.length - 1) { btns[idx + 1].focus(); btns[idx + 1].click(); }
        if (e.key === 'ArrowLeft'  && idx > 0)               { btns[idx - 1].focus(); btns[idx - 1].click(); }
    });

    // ——————————————————————————————————
    // SMOOTH ACTIVE NAV INDICATOR
    // ——————————————————————————————————
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('nav a[href^="#"]');
    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(s => {
        if (window.scrollY >= s.offsetTop - 200) current = s.id;
        });
        navLinks.forEach(a => {
        a.style.color = a.getAttribute('href') === '#' + current
            ? 'var(--cyan)' : '';
        });
    }, { passive: true });
})();