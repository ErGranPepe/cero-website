document.addEventListener('DOMContentLoaded', () => {
    // ============================================
    // GLOBAL: reduced-motion detection
    // ============================================
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // Shared scroll reader (hoisted so the scroll bundle at the bottom can update it
    // and the bg terrain render loop can read it).
    let bgScrollY = 0;

    // ============================================
    // DATA: DEPARTMENTS (the CERO org chart — all roles are open)
    // ============================================
    const departmentsData = [
        {
            code: 'ING', name: 'Ingeniería & Hardware', icon: 'fa-solid fa-cogs',
            vacancyType: 'urgent', vacancyLabel: 'Buscamos 5 — URGENTE: FEA',
            subDepartments: [
                { name: 'Chasis y Estructura', roles: ['Diseñador/a de Chasis Tubular', 'Analista de Fatiga y FEA'] },
                { name: 'Suspensiones, Dirección y Frenos', roles: ['Ingeniero/a de Dinámica', 'Especialista en Frenado'] },
                { name: 'Powertrain', roles: ['Ingeniero/a de Motores Eléctricos', 'Diseñador/a de Transmisión'] },
                { name: 'Sistemas Eléctricos y Baterías', roles: ['Especialista en BMS', 'Ingeniero/a Térmico', 'Diseño de Arnés'] }
            ]
        },
        {
            code: 'DIS', name: 'Diseño & 3D', icon: 'fa-solid fa-cube',
            vacancyType: 'open', vacancyLabel: 'Buscando equipo',
            subDepartments: [
                { name: 'Modelado CAD / Exterior', roles: ['Modelador/a Clase A', 'Concept Artist Auto'] },
                { name: 'Interiores y Ergonomía', roles: ['Ingeniero/a de Packaging', 'Diseñador/a de Habitáculo'] },
                { name: 'Aerodinámica y CFD', roles: ['Especialista en CFD', 'Ingeniero/a Aerodinámico'] },
                { name: 'Color & Materiales (CMF)', roles: ['Diseñador/a CMF'] }
            ]
        },
        {
            code: 'FAB', name: 'Fabricación & Makers', icon: 'fa-solid fa-hammer',
            vacancyType: 'open', vacancyLabel: 'Talleres y makers',
            subDepartments: [
                { name: 'Impresión 3D y Prototipado', roles: ['Operador/a FDM/SLA', 'Especialista en Materiales'] },
                { name: 'Soldadura y Chasis', roles: ['Soldador/a TIG/MIG Senior', 'Metrología'] },
                { name: 'Mecanizado CNC', roles: ['Programador/a CAM', 'Operador/a Fresa 5 ejes'] },
                { name: 'Montaje y QA', roles: ['Técnico/a de Ensamblaje', 'Inspector/a de Calidad'] }
            ]
        },
        {
            code: 'SW', name: 'Software & Telemetría', icon: 'fa-solid fa-code',
            vacancyType: 'urgent', vacancyLabel: 'Buscamos 2 — URGENTE: C++',
            subDepartments: [
                { name: 'Firmware y ECUs', roles: ['Dev Bare-metal/RTOS', 'Protocolo CAN/LIN'] },
                { name: 'HMI / Dashboard', roles: ['Frontend Qt/React Native', 'Gráficos 2D/3D'] },
                { name: 'Telemetría y Data', roles: ['Ingeniero/a de Datos', 'Dev Cloud'] },
                { name: 'Simulación y Gemelo Digital', roles: ['Dev ROS2', 'Modelado de Sistemas'] }
            ]
        },
        {
            code: 'UX', name: 'Diseño Industrial & UX', icon: 'fa-solid fa-user-astronaut',
            vacancyType: 'open', vacancyLabel: 'Buscando equipo',
            subDepartments: [
                { name: 'Investigación de Usuario', roles: ['UX Researcher Auto', 'Analista de Ergonomía'] },
                { name: 'UX de Conducción', roles: ['Diseñador/a de HMI', 'Acústica y Feedbacks'] },
                { name: 'Branding', roles: ['Diseñador/a Gráfico/a', 'Director/a de Identidad'] }
            ]
        },
        {
            code: 'MKT', name: 'Contenido & Marketing', icon: 'fa-solid fa-bullhorn',
            vacancyType: 'open', vacancyLabel: 'Buscamos 3 personas',
            subDepartments: [
                { name: 'Redes Sociales y Community', roles: ['Community Manager', 'Moderador/a Discord'] },
                { name: 'Producción Audiovisual', roles: ['Videógrafo/a Prototipado', 'Editor/a Documental'] },
                { name: 'Patrocinios', roles: ['Partnerships', 'Relaciones Públicas'] }
            ]
        },
        {
            code: 'FIN', name: 'Finanzas & Legal', icon: 'fa-solid fa-file-invoice-dollar',
            vacancyType: 'open', vacancyLabel: 'Buscamos 1 — Legal Open-Source',
            subDepartments: [
                { name: 'Tesorería y Presupuesto', roles: ['Controlador/a de Fondos', 'Crowdfunding'] },
                { name: 'Legal y Propiedad Intelectual', roles: ['Abogado/a Hardware Abierto', 'Licencias CERN OHL/GPL'] }
            ]
        },
        {
            code: 'COM', name: 'Compras & Logística', icon: 'fa-solid fa-boxes-stacked',
            vacancyType: 'forming', vacancyLabel: 'Buscando equipo',
            subDepartments: [
                { name: 'Proveedores de Componentes', roles: ['Scout COTS', 'Gestor/a de Compras'] },
                { name: 'Almacén y Envíos', roles: ['Logística Internacional', 'Inventariado'] }
            ]
        },
        {
            code: 'HR', name: 'Recursos Humanos & Cultura', icon: 'fa-solid fa-users',
            vacancyType: 'forming', vacancyLabel: 'Buscando coordinación',
            subDepartments: [
                { name: 'Onboarding', roles: ['Sherpa de Nuevos', 'Documentador/a'] },
                { name: 'Cultura y Equipos', roles: ['Eventos/Hackathons', 'Mediador/a'] }
            ]
        },
        {
            code: 'IDP', name: 'I+D y Pruebas', icon: 'fa-solid fa-flag-checkered',
            vacancyType: 'open', vacancyLabel: 'Buscamos 2 personas',
            subDepartments: [
                { name: 'Banco de Pruebas', roles: ['Op. Banco de Potencia', 'Analista NVH'] },
                { name: 'Testing en Pista', roles: ['Piloto de Pruebas', 'Ing. de Pista'] }
            ]
        }
    ];

    // (Removed: fabricated movidas/timeline data — the project hasn't started yet)

    // ============================================
    // RENDER: DEPARTMENTS GRID
    // ============================================
    const renderDepartments = () => {
        const grid = document.getElementById('departments-grid');
        if (!grid) return;
        grid.innerHTML = '';
        departmentsData.forEach((dept, idx) => {
            const card = document.createElement('article');
            card.className = 'dept-card';
            card.setAttribute('data-tilt', '');
            card.setAttribute('data-reveal', 'fade-up');
            card.style.setProperty('--reveal-delay', (idx * 70) + 'ms');

            const subs = dept.subDepartments.map(sub => `
                <div class="dept-subitem">
                    <div class="dept-subitem-name">${sub.name}</div>
                    <div class="dept-subitem-roles">${sub.roles.join(' · ')}</div>
                </div>
            `).join('');

            card.innerHTML = `
                <div class="dept-head">
                    <div class="dept-head-left">
                        <div class="dept-icon"><i class="${dept.icon}"></i></div>
                        <div class="dept-title-block">
                            <span class="dept-code">${dept.code}</span>
                            <h3>${dept.name}</h3>
                        </div>
                    </div>
                    <span class="dept-vacancy-badge vacancy-${dept.vacancyType}">
                        <span class="dot"></span>${dept.vacancyLabel}
                    </span>
                </div>
                <div class="dept-sublist">${subs}</div>
                <div class="dept-actions-row">
                    <a href="#recruitment" class="btn btn-secondary btn-apply-dept" data-dept="${dept.code.toLowerCase()}">
                        Sumarme al ${dept.code}
                    </a>
                </div>
            `;
            grid.appendChild(card);
        });

        // Re-attach tilt to the new cards
        if (!isTouchDeviceRef && grid.querySelectorAll('[data-tilt]').length > 0) {
            grid.querySelectorAll('[data-tilt]').forEach(el => {
                el.addEventListener('mousemove', (e) => {
                    const rect = el.getBoundingClientRect();
                    const x = (e.clientX - rect.left) / rect.width;
                    const y = (e.clientY - rect.top) / rect.height;
                    const maxTilt = 6;
                    const rotateY = (x - 0.5) * 2 * maxTilt;
                    const rotateX = -(y - 0.5) * 2 * maxTilt;
                    el.style.transform = `perspective(900px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(0)`;
                });
                el.addEventListener('mouseleave', () => { el.style.transform = ''; });
            });
        }

        // Re-attach the apply-dept click handlers
        grid.querySelectorAll('.btn-apply-dept').forEach(button => {
            button.addEventListener('click', () => {
                const dept = button.getAttribute('data-dept');
                const matchingBox = document.querySelector(`.select-box[data-value="${dept}"]`);
                if (matchingBox) matchingBox.click();
            });
        });

        // Re-observe new cards with the dynamic reveal observer
        grid.querySelectorAll('[data-reveal]').forEach(el => {
            if (dynamicRevealObserverRef) {
                dynamicRevealObserverRef.observe(el);
            } else {
                el.classList.add('is-visible');
            }
        });
    };

    // ============================================
    // RENDER: WIZARD STEP 1 SELECT BOXES
    // ============================================
    const renderWizardSelectBoxes = () => {
        const container = document.getElementById('wizard-grid-select');
        if (!container) return;
        container.innerHTML = '';
        departmentsData.forEach(dept => {
            const box = document.createElement('div');
            box.className = 'select-box';
            box.setAttribute('data-value', dept.code.toLowerCase());
            box.innerHTML = `
                <i class="${dept.icon}"></i>
                <span>${dept.code}</span>
            `;
            box.setAttribute('title', dept.name);
            container.appendChild(box);
        });
    };

    // Forward refs (the functions above need to call into refs that are defined later)
    let isTouchDeviceRef = false;
    let dynamicRevealObserverRef = null;

    // ============================================
    // 0. PAGE LOADER
    // ============================================
    const pageLoader = document.getElementById('page-loader');
    if (pageLoader) {
        const minDelay = new Promise(res => setTimeout(res, 1100));
        const winLoaded = new Promise(res => {
            if (document.readyState === 'complete') res();
            else window.addEventListener('load', res, { once: true });
        });
        Promise.all([minDelay, winLoaded]).then(() => {
            pageLoader.classList.add('hidden');
            setTimeout(() => pageLoader.remove(), 800);
        });
    }

    // ============================================
    // 1. SCROLL PROGRESS BAR
    // ============================================
    const scrollProgress = document.getElementById('scroll-progress');
    const updateScrollProgress = () => {
        if (!scrollProgress) return;
        const maxScroll = document.body.scrollHeight - window.innerHeight;
        const frac = maxScroll > 0 ? (window.scrollY / maxScroll) * 100 : 0;
        scrollProgress.style.width = frac + '%';
    };

    // ============================================
    // 2. NAVBAR SCROLL EFFECT
    // ============================================
    const navbar = document.querySelector('.navbar');
    const updateNavbar = () => {
        if (!navbar) return;
        if (window.scrollY > 24) navbar.classList.add('scrolled');
        else navbar.classList.remove('scrolled');
    };

    // ============================================
    // 3. REVEAL ON SCROLL (IntersectionObserver)
    // ============================================
    const revealEls = document.querySelectorAll('[data-reveal]');
    if (revealEls.length > 0 && 'IntersectionObserver' in window) {
        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const el = entry.target;
                    const delay = el.getAttribute('data-reveal-delay') || '0';
                    el.style.setProperty('--reveal-delay', delay + 'ms');
                    el.classList.add('is-visible');
                    revealObserver.unobserve(el);
                }
            });
        }, { threshold: 0.12, rootMargin: '0px 0px -50px 0px' });

        revealEls.forEach(el => revealObserver.observe(el));
    } else {
        // Fallback: reveal everything
        revealEls.forEach(el => el.classList.add('is-visible'));
    }

    // ============================================
    // 4. FLOATING PARTICLES (ambient, with variety)
    // ============================================
    const particleContainer = document.getElementById('bg-particles');
    if (particleContainer) {
        const isMobile = window.matchMedia('(max-width: 768px)').matches;
        const particleCount = isMobile ? 40 : 90;
        // Size variants and their weights (most are small, few are large/glowing)
        const sizeVariants = [
            { cls: 'p-sm',   weight: 0.55 },
            { cls: 'p-md',   weight: 0.30 },
            { cls: 'p-lg',   weight: 0.10 },
            { cls: 'p-glow', weight: 0.05 }
        ];
        const cumulative = [];
        let acc = 0;
        for (const v of sizeVariants) { acc += v.weight; cumulative.push({ cls: v.cls, until: acc }); }
        const pickVariant = () => {
            const r = Math.random() * acc;
            for (const c of cumulative) if (r <= c.until) return c.cls;
            return 'p-sm';
        };
        for (let i = 0; i < particleCount; i++) {
            const p = document.createElement('span');
            p.className = 'particle ' + pickVariant();
            p.style.left = (Math.random() * 100) + '%';
            p.style.top = '100%';
            const dur = 14 + Math.random() * 26;
            p.style.animationDuration = dur + 's';
            p.style.animationDelay = (Math.random() * -dur) + 's';
            const opacity = 0.25 + Math.random() * 0.55;
            p.style.setProperty('--p-opacity', opacity.toFixed(2));
            const drift = (Math.random() - 0.5) * 120;
            p.style.setProperty('--p-drift', drift + 'px');
            particleContainer.appendChild(p);
        }
    }

    // ============================================
    // 5. MOBILE MENU TOGGLE
    // ============================================
    const mobileNavToggle = document.querySelector('.mobile-nav-toggle');
    const navMenu = document.querySelector('.nav-menu');

    if (mobileNavToggle && navMenu && navbar) {
        const closeMenu = () => {
            navMenu.classList.remove('active');
            navbar.classList.remove('menu-open');
            document.body.style.overflow = '';
        };

        mobileNavToggle.addEventListener('click', () => {
            const isOpen = navMenu.classList.toggle('active');
            navbar.classList.toggle('menu-open', isOpen);
            document.body.style.overflow = isOpen ? 'hidden' : '';
        });

        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => closeMenu());
        });

        // Close on resize back to desktop
        window.addEventListener('resize', () => {
            if (window.innerWidth > 768 && navMenu.classList.contains('active')) {
                closeMenu();
            }
        });
    }

    // ============================================
    // 6. ACTIVE NAV LINK ON SCROLL
    // ============================================
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');

    const updateActiveLink = () => {
        let current = '';
        const scrollPos = window.pageYOffset + 140;
        sections.forEach(section => {
            const top = section.offsetTop;
            const h = section.offsetHeight;
            if (scrollPos >= top && scrollPos < top + h) {
                current = section.getAttribute('id');
            }
        });
        navLinks.forEach(link => {
            link.classList.remove('active');
            const href = link.getAttribute('href');
            if (href === '#' + current) link.classList.add('active');
        });
    };

    // ============================================
    // 7. 3D TILT EFFECT (mouse-driven on cards)
    // ============================================
    const tiltEls = document.querySelectorAll('[data-tilt]');
    const isTouchDevice = ('ontouchstart' in window) || (navigator.maxTouchPoints > 0);
    isTouchDeviceRef = isTouchDevice; // expose to renderDepartments()

    if (!isTouchDevice && tiltEls.length > 0) {
        tiltEls.forEach(el => {
            el.addEventListener('mousemove', (e) => {
                const rect = el.getBoundingClientRect();
                const x = (e.clientX - rect.left) / rect.width;
                const y = (e.clientY - rect.top) / rect.height;
                const maxTilt = el.classList.contains('dept-card') ? 8 : 6;
                const rotateY = (x - 0.5) * 2 * maxTilt;
                const rotateX = -(y - 0.5) * 2 * maxTilt;
                el.style.transform = `perspective(900px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(0)`;
            });

            el.addEventListener('mouseleave', () => {
                el.style.transform = '';
            });
        });
    }

    // ============================================
    // 8. MAGNETIC BUTTONS
    // ============================================
    const magneticBtns = document.querySelectorAll('[data-magnetic]');
    if (!isTouchDevice && magneticBtns.length > 0) {
        magneticBtns.forEach(btn => {
            btn.addEventListener('mousemove', (e) => {
                const rect = btn.getBoundingClientRect();
                const x = e.clientX - rect.left - rect.width / 2;
                const y = e.clientY - rect.top - rect.height / 2;
                btn.style.transform = `translate(${x * 0.25}px, ${y * 0.25}px)`;
            });
            btn.addEventListener('mouseleave', () => {
                btn.style.transform = '';
            });
        });
    }

    // ============================================
    // 9. 3D TERRAIN BACKGROUND
    // ============================================
    const bgCanvas = document.getElementById('bg-canvas');
    if (bgCanvas && !prefersReducedMotion) {
        const ctx = bgCanvas.getContext('2d');
        let width = bgCanvas.width = window.innerWidth;
        let height = bgCanvas.height = window.innerHeight;
        const dpr = Math.min(window.devicePixelRatio || 1, 2);

        const setSize = () => {
            width = window.innerWidth;
            height = window.innerHeight;
            bgCanvas.width = width * dpr;
            bgCanvas.height = height * dpr;
            bgCanvas.style.width = width + 'px';
            bgCanvas.style.height = height + 'px';
            ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        };
        setSize();
        window.addEventListener('resize', setSize);

        const isMobileBg = window.matchMedia('(max-width: 768px)').matches;
        const cols = isMobileBg ? 14 : 22;
        const rows = isMobileBg ? 14 : 22;
        const spacing = isMobileBg ? 80 : 70;

        const heights = [];
        for (let i = 0; i < cols; i++) {
            heights[i] = [];
            for (let j = 0; j < rows; j++) {
                const nx = (i - cols / 2) * 0.3;
                const ny = (j - rows / 2) * 0.3;
                const d = Math.sqrt(nx*nx + ny*ny);
                heights[i][j] = (Math.sin(nx) * Math.cos(ny) * 80) + (Math.cos(d * 0.8) * 40);
            }
        }

        const project = (x, y, z, rotX, rotY, zoom) => {
            const cx = x - (cols * spacing) / 2;
            const cy = y - (rows * spacing) / 2;
            const y1 = cy * Math.cos(rotX) - z * Math.sin(rotX);
            const z1 = cy * Math.sin(rotX) + z * Math.cos(rotX);
            const x2 = cx * Math.cos(rotY) - z1 * Math.sin(rotY);
            const z2 = cx * Math.sin(rotY) + z1 * Math.cos(rotY);
            const camDist = 600;
            const scale = zoom / (z2 + camDist);
            return {
                x: width / 2 + x2 * scale,
                y: height / 2 + y1 * scale
            };
        };

        const renderTerrain = () => {
            ctx.clearRect(0, 0, width, height);
            const maxScroll = document.body.scrollHeight - window.innerHeight;
            const scrollFrac = maxScroll > 0 ? bgScrollY / maxScroll : 0;

            const rotX = 0.85 + scrollFrac * 0.35 + Math.sin(Date.now() / 4000) * 0.03;
            const rotY = scrollFrac * Math.PI * 0.45 + (Date.now() / 15000);
            const zoom = 550 + scrollFrac * 150;

            ctx.strokeStyle = 'rgba(255, 255, 255, 0.035)';
            ctx.lineWidth = 1;

            const projected = [];
            for (let i = 0; i < cols; i++) {
                projected[i] = [];
                for (let j = 0; j < rows; j++) {
                    const x = i * spacing;
                    const y = j * spacing;
                    const z = heights[i][j];
                    projected[i][j] = project(x, y, z, rotX, rotY, zoom);
                }
            }
            for (let i = 0; i < cols; i++) {
                for (let j = 0; j < rows; j++) {
                    const pt = projected[i][j];
                    if (i < cols - 1) {
                        const ptR = projected[i + 1][j];
                        ctx.beginPath();
                        ctx.moveTo(pt.x, pt.y);
                        ctx.lineTo(ptR.x, ptR.y);
                        ctx.stroke();
                    }
                    if (j < rows - 1) {
                        const ptB = projected[i][j + 1];
                        ctx.beginPath();
                        ctx.moveTo(pt.x, pt.y);
                        ctx.lineTo(ptB.x, ptB.y);
                        ctx.stroke();
                    }
                }
            }
            requestAnimationFrame(renderTerrain);
        };
        renderTerrain();
    }

    // ============================================
    // 10. HERO LOGO GLOW ON SCROLL (consolidated into onScroll bundle below)
    // ============================================
    const heroLogoSymbol = document.querySelector('.hero-logo-large .cero-logo-symbol');
    let lastGlowValue = -1;
    const updateHeroGlow = () => {
        if (!heroLogoSymbol) return;
        const glow = Math.min(32, 6 + window.scrollY / 8);
        // Round to whole pixels and only write when the value actually changes
        const rounded = Math.round(glow);
        if (rounded === lastGlowValue) return;
        lastGlowValue = rounded;
        heroLogoSymbol.style.filter = `drop-shadow(0 0 ${rounded}px rgba(255,255,255,0.95))`;
    };

    // ============================================
    // 11. HERO COORDINATE CANVAS
    // ============================================
    const coordinateCanvas = document.getElementById('coordinate-canvas');
    if (coordinateCanvas) {
        const ctx = coordinateCanvas.getContext('2d');
        const targetX = 270, targetY = 90, startX = 140, startY = 300;
        let progress = 0;

        const getPathPoint = (t) => {
            const x = startX + (targetX - startX) * t + Math.sin(t * Math.PI * 4) * 35;
            const y = startY + (targetY - startY) * t;
            return { x, y };
        };

        const drawGrid = () => {
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.02)';
            ctx.lineWidth = 1;
            for (let i = 0; i < coordinateCanvas.width; i += 30) {
                ctx.beginPath();
                ctx.moveTo(i, 0);
                ctx.lineTo(i, coordinateCanvas.height);
                ctx.stroke();
            }
            for (let j = 0; j < coordinateCanvas.height; j += 30) {
                ctx.beginPath();
                ctx.moveTo(0, j);
                ctx.lineTo(coordinateCanvas.width, j);
                ctx.stroke();
            }
        };

        const drawRadarCircles = () => {
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.04)';
            ctx.lineWidth = 1;
            [30, 70, 120].forEach(r => {
                ctx.beginPath();
                ctx.arc(targetX, targetY, r, 0, Math.PI * 2);
                ctx.stroke();
            });
        };

        const animateRadar = () => {
            ctx.clearRect(0, 0, coordinateCanvas.width, coordinateCanvas.height);
            drawGrid();
            drawRadarCircles();

            ctx.strokeStyle = 'rgba(255, 59, 48, 0.75)';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(startX, startY);
            const currentSteps = Math.floor(progress * 200);
            for (let i = 0; i <= currentSteps; i++) {
                const t = i / 200;
                const pt = getPathPoint(t);
                ctx.lineTo(pt.x, pt.y);
            }
            ctx.stroke();

            if (progress >= 1) {
                const pulseRadius = 6 + Math.sin(Date.now() / 150) * 3;
                ctx.fillStyle = 'rgba(255, 59, 48, 0.2)';
                ctx.beginPath();
                ctx.arc(targetX, targetY, pulseRadius, 0, Math.PI * 2);
                ctx.fill();
                ctx.strokeStyle = 'rgba(255, 59, 48, 0.8)';
                ctx.beginPath();
                ctx.arc(targetX, targetY, pulseRadius, 0, Math.PI * 2);
                ctx.stroke();
                ctx.fillStyle = '#ffffff';
                ctx.beginPath();
                ctx.arc(targetX, targetY, 3, 0, Math.PI * 2);
                ctx.fill();
            } else {
                const pt = getPathPoint(progress);
                ctx.fillStyle = '#ffffff';
                ctx.beginPath();
                ctx.arc(pt.x, pt.y, 3, 0, Math.PI * 2);
                ctx.fill();
                progress += 0.005;
            }
            requestAnimationFrame(animateRadar);
        };
        animateRadar();
    }

    // ============================================
    // 12. WIZARD SKILLS DATA + LOGIC
    // ============================================
    const wizardSkillsData = {
        ing: [
            "Diseño de Chasis Tubular (CAD)",
            "Análisis de Fatiga y FEA",
            "Cálculo de Suspensiones y Dinámica",
            "Sistemas de Frenado y Dirección",
            "BMS y Gestión Térmica de Baterías",
            "Diseño de Powertrain Eléctrico"
        ],
        dis: [
            "Modelado de Superficies Clase A (Alias/Blender)",
            "Diseño de Interiores y Packaging",
            "Simulación CFD / Aerodinámica",
            "Color & Materiales (CMF)",
            "Renderizado Fotorrealista"
        ],
        fab: [
            "Impresión 3D FDM/SLA Industrial",
            "Soldadura TIG/MIG de Chasis",
            "Programación CAM y CNC 5 ejes",
            "Composite (Fibra de Carbono)",
            "Montaje Físico y QA"
        ],
        sw: [
            "Firmware Bare-metal / RTOS (C/C++)",
            "Protocolos CAN/LIN Bus",
            "Frontend HMI (Qt / React Native)",
            "ROS2 y Gemelo Digital",
            "Infraestructura Cloud y Data"
        ],
        ux: [
            "UX Research Automotriz",
            "Diseño de Interacciones HMI",
            "Acústica y Feedbacks de Conducción",
            "Branding e Identidad Visual",
            "Manual de Usuario Interactivo"
        ],
        mkt: [
            "Edición de Vídeo Vertical (Reels/TikTok)",
            "Community Management",
            "Producción Audiovisual / Documental",
            "Búsqueda de Patrocinios / PR",
            "Guion y Storytelling"
        ],
        fin: [
            "Control Financiero y Tesorería",
            "Hardware Abierto / Licencias (CERN OHL, GPL)",
            "Crowdfunding y Patreon",
            "Asesoría Legal Open-Source"
        ],
        com: [
            "Scout de Componentes COTS",
            "Gestión de Compras y Proveedores",
            "Logística Internacional y Aduanas",
            "Inventariado y Almacén"
        ],
        hr: [
            "Onboarding de Nuevos Miembros",
            "Documentación de Procesos",
            "Organización de Hackathones",
            "Cultura de Equipos Distribuidos"
        ],
        idp: [
            "Operación de Banco de Potencia",
            "Análisis NVH (Ruido y Vibración)",
            "Pilotaje de Pruebas en Pista",
            "Ingeniería de Dinámica de Pista"
        ]
    };

    let wizardState = {
        currentStep: 1,
        selectedDept: null,
        selectedSkills: [],
        email: '',
        instagram: '',
        colabId: '',
        roleTitle: ''
    };

    const stepPanes = {
        1: document.getElementById('pane-step-1'),
        2: document.getElementById('pane-step-2'),
        3: document.getElementById('pane-step-3'),
        success: document.getElementById('pane-success')
    };
    const stepIndicators = document.querySelectorAll('.w-step');
    const skillsCheckboxesContainer = document.getElementById('skills-checkboxes');

    // Render the wizard step 1 select-boxes from departmentsData, then re-query them
    renderWizardSelectBoxes();
    let selectBoxes = document.querySelectorAll('.select-box');
    const wizardRegisterForm = document.getElementById('wizard-register-form');
    const btnResetWizard = document.querySelector('.btn-reset-wizard');
    const assignedColabId = document.getElementById('assigned-colab-id');
    const assignedRoleTitle = document.getElementById('assigned-role-title');
    const assignedInstagram = document.getElementById('assigned-instagram');
    const progressFill = document.getElementById('wizard-progress-fill');

    const updateProgressBar = (step) => {
        if (!progressFill) return;
        const widths = { 1: '33.33%', 2: '66.66%', 3: '100%', success: '100%' };
        progressFill.style.width = widths[step] || '33.33%';
    };

    const goToStep = (step) => {
        wizardState.currentStep = step;
        Object.keys(stepPanes).forEach(key => {
            if (stepPanes[key]) {
                stepPanes[key].classList.toggle('active', key == step);
            }
        });
        stepIndicators.forEach(indicator => {
            const n = parseInt(indicator.getAttribute('data-step'));
            indicator.classList.toggle('active', n <= step && step !== 'success');
        });
        updateProgressBar(step);
    };

    selectBoxes.forEach(box => {
        box.addEventListener('click', () => {
            selectBoxes.forEach(b => b.classList.remove('selected'));
            box.classList.add('selected');
            wizardState.selectedDept = box.getAttribute('data-value');
            const nextBtn = stepPanes[1] && stepPanes[1].querySelector('.btn-next-step');
            if (nextBtn) nextBtn.disabled = false;
        });
    });

    // Apply buttons are attached after renderDepartments() runs (see below)

    const setupSkillsPane = () => {
        if (!wizardState.selectedDept) return;
        skillsCheckboxesContainer.innerHTML = '';
        const skillsList = wizardSkillsData[wizardState.selectedDept];
        wizardState.selectedSkills = [];

        skillsList.forEach((skill) => {
            const label = document.createElement('label');
            label.className = 'skill-checkbox-label';
            label.innerHTML = `
                <input type="checkbox" value="${skill}">
                <span>${skill}</span>
            `;
            const checkbox = label.querySelector('input');
            checkbox.addEventListener('change', () => {
                if (checkbox.checked) {
                    label.classList.add('checked');
                    wizardState.selectedSkills.push(skill);
                } else {
                    label.classList.remove('checked');
                    wizardState.selectedSkills = wizardState.selectedSkills.filter(s => s !== skill);
                }
            });
            skillsCheckboxesContainer.appendChild(label);
        });
    };

    document.querySelectorAll('.btn-next-step').forEach(btn => {
        btn.addEventListener('click', () => {
            if (wizardState.currentStep === 1) {
                setupSkillsPane();
                goToStep(2);
            } else if (wizardState.currentStep === 2) {
                goToStep(3);
            }
        });
    });

    document.querySelectorAll('.btn-prev-step').forEach(btn => {
        btn.addEventListener('click', () => {
            if (wizardState.currentStep === 2) goToStep(1);
            else if (wizardState.currentStep === 3) goToStep(2);
        });
    });

    // ============================================
    // 13. CONFETTI BURST (on success)
    // ============================================
    const confettiCanvas = document.getElementById('confetti-canvas');
    const fireConfetti = () => {
        if (!confettiCanvas) return;
        if (prefersReducedMotion) {
            // Static visual cue: a brief pulse on the card instead of a moving burst
            const card = document.getElementById('confetti-target');
            if (card) {
                card.style.transition = 'transform 0.3s ease';
                card.style.transform = 'scale(1.04)';
                setTimeout(() => { card.style.transform = ''; }, 320);
            }
            return;
        }
        const ctx = confettiCanvas.getContext('2d');
        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        const w = confettiCanvas.width = confettiCanvas.offsetWidth * dpr;
        const h = confettiCanvas.height = confettiCanvas.offsetHeight * dpr;
        ctx.scale(dpr, dpr);
        const W = confettiCanvas.offsetWidth;
        const H = confettiCanvas.offsetHeight;

        const colors = ['#ffffff', '#88888b', '#ff3b30', '#34c759'];
        const pieces = [];
        const N = 80;
        for (let i = 0; i < N; i++) {
            pieces.push({
                x: W * 0.5 + (Math.random() - 0.5) * 30,
                y: H * 0.3,
                vx: (Math.random() - 0.5) * 9,
                vy: -Math.random() * 12 - 4,
                g: 0.3,
                size: 2 + Math.random() * 4,
                color: colors[Math.floor(Math.random() * colors.length)],
                rot: Math.random() * Math.PI * 2,
                vr: (Math.random() - 0.5) * 0.3,
                life: 1
            });
        }
        let start = null;
        const duration = 2200;
        const tick = (ts) => {
            if (!start) start = ts;
            const elapsed = ts - start;
            ctx.clearRect(0, 0, W, H);
            pieces.forEach(p => {
                p.vy += p.g;
                p.x += p.vx;
                p.y += p.vy;
                p.rot += p.vr;
                p.life = Math.max(0, 1 - elapsed / duration);
                ctx.save();
                ctx.translate(p.x, p.y);
                ctx.rotate(p.rot);
                ctx.globalAlpha = p.life;
                ctx.fillStyle = p.color;
                ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 0.5);
                ctx.restore();
            });
            if (elapsed < duration) requestAnimationFrame(tick);
            else ctx.clearRect(0, 0, W, H);
        };
        requestAnimationFrame(tick);
    };

    if (wizardRegisterForm) {
        wizardRegisterForm.addEventListener('submit', (e) => {
            e.preventDefault();
            wizardState.email = document.getElementById('wiz-email').value;
            wizardState.instagram = document.getElementById('wiz-instagram').value;
            if (!wizardState.instagram.startsWith('@')) {
                wizardState.instagram = '@' + wizardState.instagram;
            }
            const randomIdNum = String(Math.floor(Math.random() * 180) + 20).padStart(3, '0');
            wizardState.colabId = `#${randomIdNum}`;

            // Build the role title from the live departmentsData so new departments are picked up
            const deptInfo = departmentsData.find(d => d.code.toLowerCase() === wizardState.selectedDept);
            const baseTitle = deptInfo ? `${deptInfo.name.split('&')[0].trim()} CERO` : 'Colaborador CERO';
            const skillSuf = wizardState.selectedSkills[0] ? ` (${wizardState.selectedSkills[0].split(' ').slice(0, 2).join(' ')})` : '';
            wizardState.roleTitle = baseTitle + skillSuf;

            localStorage.setItem('cero_profile', JSON.stringify(wizardState));

            if (assignedColabId) assignedColabId.innerText = wizardState.colabId;
            if (assignedRoleTitle) assignedRoleTitle.innerText = wizardState.roleTitle;
            if (assignedInstagram) assignedInstagram.innerText = wizardState.instagram;

            const newColab = {
                id: wizardState.colabId,
                name: wizardState.email.split('@')[0],
                email: wizardState.email,
                dept: wizardState.selectedDept,
                role: wizardState.roleTitle,
                insta: wizardState.instagram,
                skills: wizardState.selectedSkills.join(', ') || 'Colaboración General',
                approved: false
            };

            const collaborators = loadCollaborators();
            if (!collaborators.some(c => c.id === newColab.id)) {
                collaborators.push(newColab);
                localStorage.setItem('cero_collaborators', JSON.stringify(collaborators));
            }

            const webhookUrl = localStorage.getItem('cero_webhook_url');
            if (webhookUrl) {
                fetch(webhookUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(newColab)
                }).catch(err => console.error("Webhook POST failed:", err));
            }

            renderCollaborators();
            renderCEOCandidateTable();

            goToStep('success');
            fireConfetti();
        });
    }

    if (btnResetWizard) {
        btnResetWizard.addEventListener('click', () => {
            localStorage.removeItem('cero_profile');
            wizardState = {
                currentStep: 1,
                selectedDept: null,
                selectedSkills: [],
                email: '',
                instagram: '',
                colabId: '',
                roleTitle: ''
            };
            document.getElementById('wiz-email').value = '';
            document.getElementById('wiz-instagram').value = '';
            document.querySelectorAll('.select-box').forEach(b => b.classList.remove('selected'));
            const nextBtn = stepPanes[1].querySelector('.btn-next-step');
            if (nextBtn) nextBtn.disabled = true;
            goToStep(1);
        });
    }

    // ============================================
    // 14. COLLABORATOR DIRECTORY
    // ============================================
    const initialCollaborators = [];

    // Module-level reveal observer reused for dynamically rendered cards
    const dynamicRevealObserver = ('IntersectionObserver' in window)
        ? new IntersectionObserver((entries) => {
            entries.forEach(en => {
                if (en.isIntersecting) {
                    en.target.classList.add('is-visible');
                    dynamicRevealObserver.unobserve(en.target);
                }
            });
        }, { threshold: 0.1 })
        : null;
    dynamicRevealObserverRef = dynamicRevealObserver; // expose to renderers

    const loadCollaborators = () => {
        const stored = localStorage.getItem('cero_collaborators');
        if (!stored) {
            localStorage.setItem('cero_collaborators', JSON.stringify(initialCollaborators));
            return initialCollaborators;
        }
        return JSON.parse(stored);
    };

    const renderCollaborators = () => {
        const colabs = loadCollaborators();
        const gridContainer = document.getElementById('community-grid');
        if (!gridContainer) return;

        gridContainer.innerHTML = '';
        const approved = colabs.filter(c => c.approved === true);

        if (approved.length === 0) {
            gridContainer.innerHTML = `
                <div class="colab-empty" style="grid-column: 1 / -1; text-align: center; color: #88888b; font-family: monospace; font-size: 0.85rem; padding: 40px 0;">
                    SISTEMA DE PLANTILLA PÚBLICA ACTIVA. No hay colaboradores públicos dados de alta aún. Postúlate en el Asistente e ingresa a la Consola del CEO para aprobar tu perfil.
                </div>
            `;
            return;
        }

        approved.forEach((colab, idx) => {
            const card = document.createElement('div');
            card.className = 'colab-card';
            card.setAttribute('data-reveal', 'fade-up');
            card.style.setProperty('--reveal-delay', (idx * 80) + 'ms');
            card.innerHTML = `
                <div class="colab-card-header">
                    <span class="colab-name">${colab.name}</span>
                    <span class="colab-id">${colab.id}</span>
                </div>
                <div class="colab-role">${colab.role}</div>
                <div class="colab-skills">${colab.skills}</div>
                <a href="https://instagram.com/${colab.insta.replace('@', '')}" target="_blank" class="colab-insta">
                    <i class="fab fa-instagram"></i> ${colab.insta}
                </a>
            `;
            gridContainer.appendChild(card);
            if (dynamicRevealObserver) {
                dynamicRevealObserver.observe(card);
            } else {
                card.classList.add('is-visible');
            }
        });
    };

    renderCollaborators();
    renderDepartments();

    const checkExistingProfile = () => {
        const stored = localStorage.getItem('cero_profile');
        if (stored) {
            const data = JSON.parse(stored);
            wizardState = data;
            if (assignedColabId) assignedColabId.innerText = data.colabId;
            if (assignedRoleTitle) assignedRoleTitle.innerText = data.roleTitle;
            if (assignedInstagram) assignedInstagram.innerText = data.instagram;
            goToStep('success');
        }
    };
    checkExistingProfile();

    // ============================================
    // 15. CEO CONSOLE
    // ============================================
    const btnOpenCEO = document.getElementById('btn-open-ceo');
    const btnCloseCEO = document.getElementById('btn-close-ceo-modal');
    const ceoModal = document.getElementById('ceo-modal');
    const ceoLoginForm = document.getElementById('ceo-login-form');
    const ceoPasswordInput = document.getElementById('ceo-password');
    const ceoLoginError = document.getElementById('ceo-login-error');
    const ceoLoginView = document.getElementById('ceo-login-view');
    const ceoDashboardView = document.getElementById('ceo-dashboard-view');
    const btnLogoutCEO = document.getElementById('btn-logout-ceo');
    const candidateDetailContent = document.getElementById('candidate-detail-content');

    const interviewQuestionsMap = {
        ing: [
            { q: "¿Cómo plantearías el análisis de rigidez torsional del chasis tubular y qué factor de seguridad aplicarías?", hint: "Comprobar FEA, mallado, condiciones de contorno" },
            { q: "Para dimensionar el pack de baterías, ¿cómo calculas el pico de descarga continuo y la gestión térmica?", hint: "BMS, refrigeración líquida vs aire" },
            { q: "¿Qué MCU prefieres y cómo programarías el control de tracción vectorial?", hint: "C/C++ embebido, RTOS, lazo cerrado" }
        ],
        dis: [
            { q: "¿Qué experiencia tienes en modelado Clase A con Alias o Blender y cómo entregas superficies listas para estampación?", hint: "Continuidad de superficies, tolerancias de tooling" },
            { q: "En CFD aerodinámico, ¿qué modelos de turbulencia y refinamiento de capa límite usas?", hint: "k-ω SST, y+ objetivo, mallado poliédrico" },
            { q: "¿Cómo planteas la ergonomía del puesto de conducción y el packaging del HMI?", hint: "Percentiles 5/95, reach zones, visión" }
        ],
        fab: [
            { q: "Para el chasis tubular, ¿TIG o MIG? ¿Cómo minimizas la distorsión por calor?", hint: "Secuencia de soldadura, plantillas, baño" },
            { q: "¿Cómo parametrizarías la impresión FDM/SLA para piezas estructurales de exterior?", hint: "ASA, PETG-CF, fibra continua, orientación" }
        ],
        sw: [
            { q: "¿Qué RTOS has usado y cómo gestionarías multitarea en una ECU de control de motor?", hint: "FreeRTOS, Zephyr, scheduling, prioridades" },
            { q: "Si el coche pierde el bus CAN en plena conducción, ¿cuál es tu estrategia de fallback?", hint: "Watchdog, degradación segura, DTC" }
        ],
        ux: [
            { q: "¿Cómo testearías la usabilidad del HMI con conductores reales sin gastar en prototipos?", hint: "Wizard of Oz, eye-tracking, simuladores" },
            { q: "Define una librería de sonidos de alerta que no sea irritante en un viaje de 3 horas.", hint: "Acústica automotriz, umbrales adaptativos" }
        ],
        mkt: [
            { q: "¿Cómo estructurarías un guión vertical de 'Día a Día' que enganche en 3 segundos?", hint: "Hook, ritmo de corte, payoff emocional" },
            { q: "Sin presupuesto, ¿cómo consigues patrocinadores de componentes?", hint: "Dossier de impacto, visibilidad en créditos" }
        ],
        fin: [
            { q: "Modelos de monetización para hardware abierto: ¿CERN OHL, dual-license o patrocinios?", hint: "Trade-offs, mantenimiento a largo plazo" },
            { q: "Cómo presentarías un balance a la comunidad sin violar privacidad de colaboradores", hint: "Transparencia agregada, KPIs públicos" }
        ],
        com: [
            { q: "Scout de proveedores COTS para un pack de baterías de 60 kWh. ¿Qué criterios usas?", hint: "Datasheet, MOQ, plazos, lead time crítico" },
            { q: "Si una aduana retiene 3 semanas un envío crítico, ¿qué haces?", hint: "Plan B, courier alternativo, re-routing" }
        ],
        hr: [
            { q: "Onboarding remoto de un maker en LATAM. ¿Qué documentos compartes primero?", hint: "Manifiesto, repo, Discord, manifiesto de cultura" },
            { q: "Dos colaboradores discuten por una decisión técnica. ¿Cómo mediarías?", hint: "Decisión por datos, code review pública" }
        ],
        idp: [
            { q: "Diseña un test de frenado desde 100 km/h con telemetría. ¿Qué sensores y qué métrica defines?", hint: "Distancia, decel media/pico, fade, temperatura" },
            { q: "NVH en un monoplaza eléctrico. ¿Qué fuentes de ruido dominan y cómo las atacas?", hint: "Inverter, motor, vibración estructural" }
        ]
    };

    if (btnOpenCEO && ceoModal) {
        btnOpenCEO.addEventListener('click', (e) => {
            e.preventDefault();
            ceoModal.style.display = 'flex';
            if (ceoLoginError) ceoLoginError.style.display = 'none';
            if (ceoPasswordInput) {
                ceoPasswordInput.value = '';
                ceoPasswordInput.focus();
            }
            if (sessionStorage.getItem('ceo_logged_in') === 'true') {
                ceoLoginView.style.display = 'none';
                ceoDashboardView.style.display = 'flex';
                renderCEOCandidateTable();
            } else {
                ceoLoginView.style.display = 'flex';
                ceoDashboardView.style.display = 'none';
            }
        });
    }

    if (btnCloseCEO && ceoModal) {
        btnCloseCEO.addEventListener('click', () => { ceoModal.style.display = 'none'; });
    }

    // Google Sign-In Simulation Popup
    const btnGoogleLogin = document.getElementById('btn-google-login');
    if (btnGoogleLogin) {
        btnGoogleLogin.addEventListener('click', () => {
            const width = 500;
            const height = 600;
            const left = (window.innerWidth - width) / 2;
            const top = (window.innerHeight - height) / 2;

            const popup = window.open('', 'GoogleLogin', `width=${width},height=${height},top=${top},left=${left}`);
            if (popup) {
                popup.document.write(`
                    <html>
                    <head>
                        <title>Iniciar sesión: Cuentas de Google</title>
                        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap" rel="stylesheet">
                        <style>
                            body { font-family: 'Roboto', sans-serif; background: #fff; color: #202124; display: flex; flex-direction: column; align-items: center; padding: 40px 30px; margin: 0; }
                            .logo-container { margin-bottom: 24px; }
                            .header { text-align: center; margin-bottom: 30px; }
                            .header h1 { font-size: 24px; font-weight: 400; margin: 0 0 8px 0; }
                            .header p { font-size: 16px; margin: 0; color: #5f6368; }
                            .account-box { width: 100%; border: 1px solid #dadce0; border-radius: 8px; overflow: hidden; margin-bottom: 20px; }
                            .account-item { display: flex; align-items: center; padding: 16px; cursor: pointer; border-bottom: 1px solid #dadce0; transition: background-color 0.2s; }
                            .account-item:last-child { border-bottom: none; }
                            .account-item:hover { background-color: #f8f9fa; }
                            .avatar { width: 40px; height: 40px; background-color: #000; color: #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px; font-weight: bold; margin-right: 12px; }
                            .details { display: flex; flex-direction: column; }
                            .details .name { font-weight: 500; font-size: 14px; }
                            .details .email { font-size: 12px; color: #5f6368; }
                            .footer-text { font-size: 12px; color: #5f6368; text-align: center; line-height: 1.5; margin-top: 20px; }
                        </style>
                    </head>
                    <body>
                        <div class="logo-container">
                            <img src="https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg" width="74" alt="Google">
                        </div>
                        <div class="header">
                            <h1>Elige una cuenta</h1>
                            <p>para ir a <strong>CERO Workspace</strong></p>
                        </div>
                        <div class="account-box">
                            <div class="account-item" onclick="selectAccount('CEO CERO', 'ceo@cero.com')">
                                <div class="avatar">Ø</div>
                                <div class="details">
                                    <span class="name">CEO CERO (Fundador)</span>
                                    <span class="email">ceo@cero.com</span>
                                </div>
                            </div>
                            <div class="account-item" onclick="selectAccount('mario', 'mario@cero.com')">
                                <div class="avatar" style="background-color: #1a73e8;">M</div>
                                <div class="details">
                                    <span class="name">mario (Administrador)</span>
                                    <span class="email">mario@cero.com</span>
                                </div>
                            </div>
                        </div>
                        <p class="footer-text">
                            Para continuar, Google compartirá tu nombre, dirección de correo electrónico, foto de perfil y preferencia de idioma con CERO.
                        </p>
                        <script>
                            function selectAccount(name, email) {
                                window.opener.postMessage({ type: 'GOOGLE_AUTH_SUCCESS', name: name, email: email }, '*');
                                window.close();
                            }
                        <\/script>
                    </body>
                    </html>
                `);
            }
        });
    }

    window.addEventListener('message', (event) => {
        if (event.data && event.data.type === 'GOOGLE_AUTH_SUCCESS') {
            sessionStorage.setItem('ceo_logged_in', 'true');
            sessionStorage.setItem('ceo_auth_provider', 'google');
            sessionStorage.setItem('ceo_user_email', event.data.email);
            if (ceoLoginError) ceoLoginError.style.display = 'none';
            ceoLoginView.style.display = 'none';
            ceoDashboardView.style.display = 'flex';
            renderCEOCandidateTable();
        }
    });

    if (ceoLoginForm) {
        ceoLoginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const password = ceoPasswordInput.value;
            if (password === 'cero2026') {
                sessionStorage.setItem('ceo_logged_in', 'true');
                sessionStorage.setItem('ceo_auth_provider', 'local');
                if (ceoLoginError) ceoLoginError.style.display = 'none';
                ceoLoginView.style.display = 'none';
                ceoDashboardView.style.display = 'flex';
                renderCEOCandidateTable();
            } else {
                if (ceoLoginError) {
                    ceoLoginError.style.display = 'block';
                    ceoLoginError.style.animation = 'none';
                    void ceoLoginError.offsetWidth;
                    ceoLoginError.style.animation = '';
                }
                ceoPasswordInput.value = '';
                ceoPasswordInput.focus();
            }
        });
    }

    if (btnLogoutCEO) {
        btnLogoutCEO.addEventListener('click', () => {
            sessionStorage.removeItem('ceo_logged_in');
            sessionStorage.removeItem('ceo_auth_provider');
            sessionStorage.removeItem('ceo_user_email');
            ceoLoginView.style.display = 'flex';
            ceoDashboardView.style.display = 'none';
            if (candidateDetailContent) {
                candidateDetailContent.innerHTML = `<p class="empty-detail-msg">Seleccione un candidato para iniciar el asistente de entrevista y generar preguntas personalizadas.</p>`;
            }
        });
    }

    const renderCEOCandidateTable = () => {
        const colabs = loadCollaborators();
        const tableBody = document.getElementById('ceo-candidates-list');
        if (!tableBody) return;

        tableBody.innerHTML = '';
        colabs.forEach((colab, index) => {
            const tr = document.createElement('tr');
            tr.setAttribute('data-id', colab.id);

            const statusBadgeHTML = colab.approved
                ? `<span class="status-badge status-approved">Aprobado</span>`
                : `<span class="status-badge status-pending">Privado</span>`;
            const actionButtonHTML = colab.approved
                ? `<button class="btn btn-reject btn-toggle-public" data-index="${index}">Ocultar</button>`
                : `<button class="btn btn-approve btn-toggle-public" data-index="${index}">Aprobar</button>`;

            tr.innerHTML = `
                <td><code style="font-family:monospace; color:#ffffff;">${colab.id}</code></td>
                <td>
                    <div style="font-weight:600;">${colab.name}</div>
                    <div style="font-size:0.7rem; color:#88888b;">${colab.email}</div>
                </td>
                <td><span style="text-transform:capitalize;">${colab.dept}</span></td>
                <td>${statusBadgeHTML}</td>
                <td class="ceo-actions-cell">${actionButtonHTML}</td>
            `;
            tr.addEventListener('click', (e) => {
                if (e.target.classList.contains('btn-toggle-public')) return;
                document.querySelectorAll('#ceo-candidates-list tr').forEach(r => r.classList.remove('active-row'));
                tr.classList.add('active-row');
                showCandidateDetails(colab);
            });
            tableBody.appendChild(tr);
        });

        document.querySelectorAll('.btn-toggle-public').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const index = parseInt(btn.getAttribute('data-index'));
                toggleCandidatePublicStatus(index);
            });
        });
    };

    const toggleCandidatePublicStatus = (index) => {
        const colabs = loadCollaborators();
        if (colabs[index]) {
            colabs[index].approved = !colabs[index].approved;
            localStorage.setItem('cero_collaborators', JSON.stringify(colabs));
            renderCollaborators();
            renderCEOCandidateTable();
            const activeRow = document.querySelector('#ceo-candidates-list tr.active-row');
            if (activeRow) {
                const activeId = activeRow.getAttribute('data-id');
                if (activeId === colabs[index].id) {
                    showCandidateDetails(colabs[index]);
                }
            }
        }
    };

    const showCandidateDetails = (candidate) => {
        if (!candidateDetailContent) return;
        const questionsList = interviewQuestionsMap[candidate.dept] || [];
        let questionsHTML = '';
        if (questionsList.length > 0) {
            questionsList.forEach((qObj, i) => {
                questionsHTML += `
                    <div class="question-item">
                        <p>${i + 1}. ${qObj.q}</p>
                        <span><strong style="color:#ffffff;">Objetivo:</strong> ${qObj.hint}</span>
                    </div>
                `;
            });
        } else {
            questionsHTML = `<p style="font-size:0.8rem; color:#88888b; font-family:monospace;">Sin preguntas recomendadas.</p>`;
        }
        candidateDetailContent.innerHTML = `
            <div class="candidate-profile">
                <div class="profile-header">
                    <div class="profile-name">${candidate.name}</div>
                    <div class="profile-meta">${candidate.id} | ${candidate.email}</div>
                    <div class="profile-meta" style="margin-top: 4px;">
                        <i class="fab fa-instagram"></i> <strong>${candidate.insta}</strong>
                    </div>
                </div>
                <div>
                    <div class="profile-section-title">Habilidades Declaradas</div>
                    <div class="profile-skills-box">${candidate.skills}</div>
                </div>
                <div>
                    <div class="profile-section-title">Guía de Preguntas Técnicas Recomendadas</div>
                    <div class="interview-questions">${questionsHTML}</div>
                </div>
            </div>
        `;
    };

    // ============================================
    // 16. EXCEL (CSV) EXPORT
    // ============================================
    const btnExportExcel = document.getElementById('btn-export-excel');
    if (btnExportExcel) {
        btnExportExcel.addEventListener('click', () => {
            const colabs = loadCollaborators();
            let csvContent = "\uFEFF";
            csvContent += "ID,Nombre,Email,Departamento,Rol,Instagram,Habilidades,Estado\n";
            colabs.forEach(c => {
                const row = [
                    c.id, c.name, c.email, c.dept,
                    `"${c.role.replace(/"/g, '""')}"`,
                    c.insta,
                    `"${c.skills.replace(/"/g, '""')}"`,
                    c.approved ? "APROBADO" : "PRIVADO"
                ].join(",");
                csvContent += row + "\n";
            });
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const url = URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.setAttribute("href", url);
            link.setAttribute("download", `cero_candidatos_${Date.now()}.csv`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        });
    }

    // ============================================
    // 17. WEBHOOK SETTINGS
    // ============================================
    const btnToggleSettings = document.getElementById('btn-toggle-settings');
    const settingsPanel = document.getElementById('dashboard-settings-panel');
    const webhookUrlInput = document.getElementById('settings-webhook-url');
    const btnSaveSettings = document.getElementById('btn-save-settings');
    const settingsStatusMsg = document.getElementById('settings-status-msg');

    if (btnToggleSettings && settingsPanel) {
        btnToggleSettings.addEventListener('click', () => {
            const isHidden = settingsPanel.style.display === 'none';
            settingsPanel.style.display = isHidden ? 'block' : 'none';
            if (isHidden && webhookUrlInput) {
                webhookUrlInput.value = localStorage.getItem('cero_webhook_url') || '';
            }
        });
    }

    if (btnSaveSettings && webhookUrlInput && settingsStatusMsg) {
        btnSaveSettings.addEventListener('click', () => {
            const url = webhookUrlInput.value;
            localStorage.setItem('cero_webhook_url', url);
            settingsStatusMsg.style.display = 'block';
            setTimeout(() => { settingsStatusMsg.style.display = 'none'; }, 3000);
        });
    }

    // ============================================
    // 18. LEGAL MODALS
    // ============================================
    const openPolicyBtns = document.querySelectorAll('.btn-open-policy');
    const closePolicyBtns = document.querySelectorAll('.legal-modal-close');

    openPolicyBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const modalId = btn.getAttribute('data-modal');
            const targetModal = document.getElementById(modalId);
            if (targetModal) targetModal.style.display = 'flex';
        });
    });

    closePolicyBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const modalId = btn.getAttribute('data-close');
            const targetModal = document.getElementById(modalId);
            if (targetModal) targetModal.style.display = 'none';
        });
    });

    window.addEventListener('click', (e) => {
        if (e.target.classList.contains('legal-modal')) {
            e.target.style.display = 'none';
        }
        if (e.target === ceoModal) {
            ceoModal.style.display = 'none';
        }
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            document.querySelectorAll('.legal-modal, .ceo-modal').forEach(m => {
                if (m.style.display === 'flex' || m.style.display === 'block') m.style.display = 'none';
            });
            if (navMenu && navMenu.classList.contains('active')) {
                navMenu.classList.remove('active');
                navbar.classList.remove('menu-open');
                document.body.style.overflow = '';
            }
        }
    });

    // ============================================
    // 19. COOKIE CONSENT
    // ============================================
    const cookieBanner = document.getElementById('cookie-banner');
    const btnAcceptCookies = document.getElementById('btn-accept-cookies');

    if (cookieBanner && btnAcceptCookies) {
        if (localStorage.getItem('cero_cookies_accepted') !== 'true') {
            setTimeout(() => cookieBanner.classList.add('visible'), 2200);
        }
        btnAcceptCookies.addEventListener('click', () => {
            localStorage.setItem('cero_cookies_accepted', 'true');
            cookieBanner.classList.remove('visible');
            setTimeout(() => { cookieBanner.style.display = 'none'; }, 600);
        });
    }

    // ============================================
    // 23. PARALLAX BANNERS (scroll-driven bg offset)
    // ============================================
    const parallaxBgs = Array.from(document.querySelectorAll('.parallax-bg'));
    const updateParallax = () => {
        if (prefersReducedMotion) return;
        const viewportH = window.innerHeight;
        parallaxBgs.forEach(bg => {
            const wrapper = bg.parentElement;
            if (!wrapper) return;
            const rect = wrapper.getBoundingClientRect();
            if (rect.bottom < -200 || rect.top > viewportH + 200) return;
            const speed = parseFloat(bg.getAttribute('data-parallax')) || 0.4;
            const bannerCenter = rect.top + rect.height / 2;
            const viewportCenter = viewportH / 2;
            const offset = (bannerCenter - viewportCenter) * -speed;
            bg.style.transform = `translate3d(0, ${offset.toFixed(2)}px, 0)`;
        });
    };

    // ============================================
    // 25. DAY COUNTER ANIMATION (auto-counts from 0 to the real day)
    // ============================================
    const statusDayEl = document.getElementById('status-day');
    if (statusDayEl) {
        // Project start date: 07.07.2026 (local time, to avoid off-by-one near midnight in LATAM)
        const startDate = new Date(2026, 6, 7);
        const today = new Date();
        const dayDiff = Math.floor((today - startDate) / (1000 * 60 * 60 * 24)) + 1;
        const targetDay = Math.max(1, dayDiff);

        // Respect reduced motion: just set the final value, no counting animation
        if (prefersReducedMotion) {
            statusDayEl.textContent = String(targetDay).padStart(3, '0');
        } else {
            const duration = 1800;
            const startTs = performance.now();
            const tick = (now) => {
                const elapsed = now - startTs;
                const t = Math.min(elapsed / duration, 1);
                // easeOutExpo
                const eased = t === 1 ? 1 : 1 - Math.pow(2, -10 * t);
                const current = Math.max(1, Math.floor(eased * targetDay));
                statusDayEl.textContent = String(current).padStart(3, '0');
                if (t < 1) requestAnimationFrame(tick);
            };
            // Delay the counter start so the page loader has a moment to fade out
            setTimeout(() => requestAnimationFrame(tick), 600);
        }
    }

    // ============================================
    // 24. SCROLL EVENT BUNDLING (perf)
    // ============================================
    let ticking = false;
    const onScroll = () => {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(() => {
            updateScrollProgress();
            updateNavbar();
            updateActiveLink();
            updateHeroGlow();
            bgScrollY = window.scrollY;
            if (parallaxBgs.length > 0) updateParallax();
            ticking = false;
        });
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
});
