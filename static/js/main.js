// OVPA Website - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Mobile Menu Toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            const expanded = menuToggle.getAttribute('aria-expanded') === 'true' || false;
            menuToggle.setAttribute('aria-expanded', !expanded);
        });
    }
    
    // Smooth Scroll for Anchor Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#' && href !== '#!') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
    
    // Auto-hide Messages
    const messages = document.querySelectorAll('.message');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.transition = 'opacity 0.5s ease';
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 500);
        }, 5000);
    });
    
// Form Validation Enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('error');
                } else {
                    field.classList.remove('error');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });

    // --- GOV.PH Feature 1: PST Live Digital Clock ---
    function updatePSTClock() {
        const clockElem = document.getElementById('pst-live-clock');
        if (!clockElem) return;

        // Create date formatted in Asia/Manila (PST)
        const now = new Date();
        const options = {
            timeZone: 'Asia/Manila',
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: true
        };

        const formatter = new Intl.DateTimeFormat('en-US', options);
        clockElem.textContent = formatter.format(now);
    }
    
    updatePSTClock();
    setInterval(updatePSTClock, 1000);

    // --- GOV.PH Feature 2: Font Size Adjuster ---
    let currentFontSizeOffset = 0;
    const bodyElem = document.body;

    const btnDecrease = document.getElementById('btn-font-decrease');
    const btnReset = document.getElementById('btn-font-reset');
    const btnIncrease = document.getElementById('btn-font-increase');

    if (btnDecrease && btnReset && btnIncrease) {
        btnDecrease.addEventListener('click', function() {
            if (currentFontSizeOffset > -2) {
                currentFontSizeOffset--;
                applyFontSize();
            }
        });

        btnReset.addEventListener('click', function() {
            currentFontSizeOffset = 0;
            applyFontSize();
        });

        btnIncrease.addEventListener('click', function() {
            if (currentFontSizeOffset < 4) {
                currentFontSizeOffset++;
                applyFontSize();
            }
        });

        function applyFontSize() {
            bodyElem.style.fontSize = (100 + currentFontSizeOffset * 8) + '%';
        }
    }

    // --- GOV.PH Feature 3: High Contrast Mode Toggle ---
    const btnContrast = document.getElementById('btn-high-contrast');
    if (btnContrast) {
        // Load saved state
        if (localStorage.getItem('govph_high_contrast') === 'enabled') {
            bodyElem.classList.add('high-contrast');
        }

        btnContrast.addEventListener('click', function() {
            bodyElem.classList.toggle('high-contrast');
            if (bodyElem.classList.contains('high-contrast')) {
                localStorage.setItem('govph_high_contrast', 'enabled');
            } else {
                localStorage.setItem('govph_high_contrast', 'disabled');
            }
        });
    }

    // --- GOV.PH Feature 4: Accessibility Popout Panel Toggle ---
    const btnAccToggle = document.getElementById('btn-accessibility-toggle');
    const accPanel = document.getElementById('accessibility-popout-panel');
    const btnClosePopout = document.getElementById('btn-close-popout');

    if (btnAccToggle && accPanel) {
        btnAccToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            const isOpen = accPanel.style.display === 'block';
            accPanel.style.display = isOpen ? 'none' : 'block';
        });

        if (btnClosePopout) {
            btnClosePopout.addEventListener('click', function(e) {
                e.stopPropagation();
                accPanel.style.display = 'none';
            });
        }

        // Close popout on click outside
        document.addEventListener('click', function(e) {
            if (accPanel.style.display === 'block' && !accPanel.contains(e.target) && e.target !== btnAccToggle) {
                accPanel.style.display = 'none';
            }
        });
    }

    // --- ISO Certificate Popout Modal Handlers ---
    const btnOpenIsoModal = document.getElementById('btn-open-iso-modal');
    const btnCloseIsoModal = document.getElementById('btn-close-iso-modal');
    const isoModal = document.getElementById('iso-certificate-modal');

    if (btnOpenIsoModal && isoModal) {
        btnOpenIsoModal.addEventListener('click', function(e) {
            e.preventDefault();
            isoModal.style.display = 'flex';
            document.body.style.overflow = 'hidden'; // Prevent background scrolling
        });

        if (btnCloseIsoModal) {
            btnCloseIsoModal.addEventListener('click', function() {
                isoModal.style.display = 'none';
                document.body.style.overflow = '';
            });
        }

        // Close on clicking backdrop
        isoModal.addEventListener('click', function(e) {
            if (e.target === isoModal) {
                isoModal.style.display = 'none';
                document.body.style.overflow = '';
            }
        });

        // Close on ESC key press
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && isoModal.style.display === 'flex') {
                isoModal.style.display = 'none';
                document.body.style.overflow = '';
            }
        });
    }

    // --- Urgent Announcements & Advisories Continuous Marquee Text ---
    const tickerSlider = document.getElementById('ticker-slider');
    const btnTickerPause = document.getElementById('btn-ticker-pause');

    if (tickerSlider) {
        // Duplicate items to ensure seamless infinite looping marquee
        tickerSlider.innerHTML += tickerSlider.innerHTML;

        let posX = 0;
        const speed = 1.2; // Pixels per frame
        let animationFrameId = null;
        let isTickerPaused = false;

        function animateMarquee() {
            posX -= speed;
            const halfWidth = tickerSlider.scrollWidth / 2;
            if (Math.abs(posX) >= halfWidth) {
                posX = 0;
            }
            tickerSlider.style.transform = `translateX(${posX}px)`;
            if (!isTickerPaused) {
                animationFrameId = requestAnimationFrame(animateMarquee);
            }
        }

        animationFrameId = requestAnimationFrame(animateMarquee);

        // Pause on mouse hover over marquee area
        const marqueeWrapper = document.getElementById('marquee-wrapper');
        if (marqueeWrapper) {
            marqueeWrapper.addEventListener('mouseenter', function() {
                isTickerPaused = true;
                if (animationFrameId) cancelAnimationFrame(animationFrameId);
            });
            marqueeWrapper.addEventListener('mouseleave', function() {
                if (!btnTickerPause || !btnTickerPause.classList.contains('user-paused')) {
                    isTickerPaused = false;
                    animationFrameId = requestAnimationFrame(animateMarquee);
                }
            });
        }

        // Toggle via Pause/Play Button
        if (btnTickerPause) {
            btnTickerPause.addEventListener('click', function() {
                if (isTickerPaused) {
                    btnTickerPause.classList.remove('user-paused');
                    isTickerPaused = false;
                    animationFrameId = requestAnimationFrame(animateMarquee);
                    btnTickerPause.innerHTML = '<i class="fas fa-pause"></i>';
                } else {
                    btnTickerPause.classList.add('user-paused');
                    isTickerPaused = true;
                    if (animationFrameId) cancelAnimationFrame(animationFrameId);
                    btnTickerPause.innerHTML = '<i class="fas fa-play"></i>';
                }
            });
        }
    }

    // Cash Office Offcanvas Drawer Handler
    const btnOpenDrawer = document.getElementById('btn-open-drawer');
    const btnCloseDrawer = document.getElementById('btn-close-drawer');
    const drawer = document.getElementById('check-offcanvas-drawer');
    const drawerOverlay = document.getElementById('drawer-overlay');

    function openDrawer() {
        if (drawerOverlay && drawer) {
            drawerOverlay.style.display = 'block';
            setTimeout(() => {
                drawerOverlay.style.opacity = '1';
                drawer.style.right = '0';
            }, 10);
        }
    }

    function closeDrawer() {
        if (drawerOverlay && drawer) {
            drawer.style.right = '-550px';
            drawerOverlay.style.opacity = '0';
            setTimeout(() => {
                drawerOverlay.style.display = 'none';
            }, 350);
        }
    }

    if (btnOpenDrawer) btnOpenDrawer.addEventListener('click', openDrawer);
    if (btnCloseDrawer) btnCloseDrawer.addEventListener('click', closeDrawer);
    if (drawerOverlay) drawerOverlay.addEventListener('click', closeDrawer);

    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('q') || urlParams.has('status')) {
        openDrawer();
    }

    // Dynamic Section TOC for Structured Pages
    const contentContainer = document.getElementById("page-main-content");
    const sidebar = document.getElementById("page-sidebar");
    const navContainer = document.getElementById("nav-tabs-container");

    if (contentContainer && sidebar && navContainer) {
        const headings = contentContainer.querySelectorAll("h3");
        if (headings.length > 0) {
            sidebar.style.display = "block";
            headings.forEach((heading, index) => {
                if (!heading.id) {
                    heading.id = "section-" + (index + 1);
                }
                const link = document.createElement("a");
                link.href = "#" + heading.id;
                link.className = "nav-tab";
                link.innerHTML = `<span class="nav-tab-dot"></span><span>${heading.innerText}</span>`;
                if (index === 0) link.classList.add("active");
                navContainer.appendChild(link);
            });
        }
    }
});

