/**
 * ==========================================================================
 * CERO PLM DASHBOARD & REELS GENERATOR ENGINE
 * Multi-tab control, Three.js 3D Physics engine, and 60FPS Video Encoder
 * ==========================================================================
 */

document.addEventListener('DOMContentLoaded', () => {
    // ==========================================
    // 1. STATE MANAGEMENT & DATA BASE STRUCTURE
    // ==========================================
    let bomData = [];
    let selectedPartIdx = null;
    let bgImageFile = null; // Custom uploaded background for video
    let currentTab = 'tab-telemetry';

    // Base database: 25 components for a collaborative formula-style electric car
    const defaultBOM = [
        { code: "ING-CHA-01", name: "Chasis Spaceframe Tubular", dept: "chassis", status: "fea", material: "Acero 4130 Chromoly", mfg: "Soldadura TIG / Curvadora", mass: 26500, cost: 0, x: 1100, y: 0, z: 280, feaStatus: "Aprobado", sponsor: "Metales Industriales S.A.", cadUrl: "https://github.com/buildcero/cad/blob/main/chassis.step", notes: "Tubos principales de 1.0 inch OD, espesor 2.4mm y 1.6mm." },
        { code: "ING-CHA-02", name: "Aro de Seguridad Principal (Roll Hoop)", dept: "chassis", status: "fabricacion", material: "Acero 4130 Chromoly", mfg: "Soldadura TIG / Doblado CNC", mass: 8500, cost: 0, x: 1450, y: 0, z: 620, feaStatus: "Aprobado", sponsor: "Curvados CERO", cadUrl: "", notes: "Arqueado principal detrás de la cabeza del piloto." },
        { code: "ING-SUS-01", name: "Mangueta Delantera Derecha", dept: "suspension", status: "comprado", material: "Aluminio 7075-T6", mfg: "Mecanizado CNC 5 Ejes", mass: 1250, cost: 0, x: 400, y: 600, z: 220, feaStatus: "Aprobado", sponsor: "Taller Mecanizado Gomez", cadUrl: "", notes: "Geometría optimizada para reducir masa no suspendida." },
        { code: "ING-SUS-02", name: "Mangueta Delantera Izquierda", dept: "suspension", status: "comprado", material: "Aluminio 7075-T6", mfg: "Mecanizado CNC 5 Ejes", mass: 1250, cost: 0, x: 400, y: -600, z: 220, feaStatus: "Aprobado", sponsor: "Taller Mecanizado Gomez", cadUrl: "", notes: "Simétrica a la derecha." },
        { code: "ING-SUS-03", name: "Trapecio Superior Delantero (x2)", dept: "suspension", status: "terminado", material: "Acero 4130 / Insertos Al", mfg: "Soldadura / Corte Láser", mass: 1100, cost: 0, x: 400, y: 350, z: 310, feaStatus: "Aprobado", sponsor: "Sponsor Tubos", cadUrl: "", notes: "Doble trapecio de suspensión con terminales de rótula." },
        { code: "ING-SUS-04", name: "Trapecio Inferior Delantero (x2)", dept: "suspension", status: "terminado", material: "Acero 4130 / Insertos Al", mfg: "Soldadura / Corte Láser", mass: 1450, cost: 0, x: 400, y: 350, z: 120, feaStatus: "Aprobado", sponsor: "Sponsor Tubos", cadUrl: "", notes: "Soporte para el anclaje del pushrod." },
        { code: "ING-POW-01", name: "Motor Eléctrico Emrax 228", dept: "powertrain", status: "comprado", material: "Imán Permanente/Cobre/Al", mfg: "COTS Comercial", mass: 12300, cost: 3500, x: 1850, y: 0, z: 250, feaStatus: "Aprobado", sponsor: "Donación Particular", cadUrl: "", notes: "Motor axial, refrigerado por líquido. Pico de 100 kW." },
        { code: "ING-POW-02", name: "Inversor Bamocar D3", dept: "powertrain", status: "comprado", material: "Componentes Electrónicos/Al", mfg: "COTS Comercial", mass: 6400, cost: 2400, x: 1720, y: 0, z: 380, feaStatus: "Aprobado", sponsor: "Adquirido", cadUrl: "", notes: "Controlador de motor trifásico de alta tensión." },
        { code: "ING-POW-03", name: "Diferencial de Deslizamiento Limitado Drexler", dept: "powertrain", status: "diseño", material: "Acero Nitrurado", mfg: "Mecanizado CNC / Tallado", mass: 4500, cost: 1200, x: 1950, y: 0, z: 220, feaStatus: "Pendiente", sponsor: "Drexler Autosport", cadUrl: "", notes: "Diferencial autoblocante tarado para Formula Student." },
        { code: "ING-BAT-01", name: "Celdas de Iones de Litio 18650 (Pack)", dept: "battery", status: "fabricacion", material: "Litio / Cátodo Níquel", mfg: "Soldadura por Puntos CNC", mass: 25500, cost: 0, x: 1150, y: 0, z: 180, feaStatus: "Aprobado", sponsor: "Sponsor Energía", cadUrl: "", notes: "Configuración 80S6P. Total de 480 celdas, 350V nominales." },
        { code: "ING-BAT-02", name: "Contenedor de Batería (Accumulator)", dept: "battery", status: "fea", material: "Fibra de Carbono / Nomex", mfg: "Laminado al Vacío / Autoclave", mass: 8200, cost: 0, x: 1150, y: 0, z: 180, feaStatus: "Aprobado", sponsor: "Laminados del Sur", cadUrl: "", notes: "Carcasa ignífuga de seguridad estructural contra impactos." },
        { code: "ING-BAT-03", name: "BMS (Battery Management System) Orion", dept: "battery", status: "comprado", material: "Placa PCB / Carcasa Al", mfg: "Comercial", mass: 800, cost: 950, x: 1150, y: 150, z: 300, feaStatus: "Aprobado", sponsor: "Adquirido", cadUrl: "", notes: "Monitoreo de voltaje de celda y temperaturas." },
        { code: "ING-ELE-01", name: "ECU Principal y Adquisición de Datos", dept: "electronics", status: "terminado", material: "Placa PCB / ABS 3D", mfg: "Diseño Propio Kicad / SMT", mass: 350, cost: 0, x: 800, y: 220, z: 280, feaStatus: "Aprobado", sponsor: "PCBWay Sponsor", cadUrl: "", notes: "Procesador Teensy 4.1 con transceptor CAN integrado." },
        { code: "ING-ELE-02", name: "Mazo de Cables de Baja Tensión", dept: "electronics", status: "diseño", material: "Cobre / Tefzel / Raychem", mfg: "Montaje a Mano / Concentrador", mass: 2800, cost: 0, x: 1100, y: 0, z: 250, feaStatus: "Pendiente", sponsor: "Raychem Donante", cadUrl: "", notes: "Cableado de sensores, ECU, HMI y seguridad." },
        { code: "ING-STE-01", name: "Volante de Fibra de Carbono con Pantalla", dept: "electronics", status: "fabricacion", material: "Carbono Prepreg / Resina / PLA", mfg: "Impresión 3D + Laminación", mass: 980, cost: 0, x: 920, y: 0, z: 460, feaStatus: "Aprobado", sponsor: "Makers Comunidad", cadUrl: "", notes: "Pantalla Nextion 4.3 pulgadas y LEDs de RPM reactivos." },
        { code: "ING-STE-02", name: "Cremallera de Dirección Rápida", dept: "suspension", status: "comprado", material: "Acero / Aluminio", mfg: "Mecanizado Comercial", mass: 2200, cost: 0, x: 550, y: 0, z: 200, feaStatus: "Aprobado", sponsor: "Desguaces CERO", notes: "Relación de giro rápida para circuito cerrado." },
        { code: "ING-BRA-01", name: "Pinzas de Freno Wilwood (x4)", dept: "suspension", status: "comprado", material: "Aluminio Forjado", mfg: "Comercial", mass: 3100, cost: 0, x: 1200, y: 550, z: 220, feaStatus: "Aprobado", sponsor: "Wilwood Iberia", notes: "Pinzas de 2 pistones ligeras." },
        { code: "ING-BRA-02", name: "Discos de Freno Ventilados (x4)", dept: "suspension", status: "fabricacion", material: "Acero Inoxidable 420", mfg: "Corte Láser CNC / Rectificado", mass: 3800, cost: 0, x: 1200, y: 550, z: 220, feaStatus: "Aprobado", sponsor: "Corte Láser Metal", notes: "Discos con patrón de taladrado para disipación térmica." },
        { code: "ING-PED-01", name: "Pedalera Ajustable (Acelerador/Freno)", dept: "ergonomics", status: "terminado", material: "Aluminio 6082-T6", mfg: "Mecanizado / Impresión 3D metal", mass: 1900, cost: 0, x: 580, y: 0, z: 120, feaStatus: "Aprobado", sponsor: "Taller CNC", notes: "Sensor Hall doble en acelerador y barra de equilibrio mecánica." },
        { code: "ING-AER-01", name: "Alerón Delantero y Endplates", dept: "aerodynamics", status: "diseño", material: "Fibra de Carbono / Core Divinycell", mfg: "Laminación al Vacío", mass: 4300, cost: 0, x: -150, y: 0, z: 140, feaStatus: "Pendiente", sponsor: "Aero Carbono", notes: "Perfil de alta carga aerodinámica validado en CFD." },
        { code: "ING-AER-02", name: "Alerón Trasero con DRS Activo", dept: "aerodynamics", status: "concepto", material: "Carbono Prepreg / Actuador 12V", mfg: "Autoclave / CNC", mass: 5600, cost: 0, x: 2350, y: 0, z: 780, feaStatus: "Pendiente", sponsor: "Aero Carbono", notes: "Mecanismo DRS con servomotores para rectas." },
        { code: "ING-ERG-01", name: "Asiento a Medida de Fibra de Carbono", dept: "ergonomics", status: "terminado", material: "Fibra de Carbono / Espuma EPS", mfg: "Moldeado a mano del piloto", mass: 2100, cost: 0, x: 1220, y: 0, z: 210, feaStatus: "Aprobado", sponsor: "Fibras de Toledo", notes: "Asiento ergonómico con ranuras para arnés de 6 puntos." },
        { code: "ING-WHE-01", name: "Llantas OZ Racing 13 pulgadas (x4)", dept: "suspension", status: "comprado", material: "Magnesio Forjado", mfg: "Comercial", mass: 12000, cost: 0, x: 1200, y: 600, z: 220, feaStatus: "Aprobado", sponsor: "OZ Wheels Donación", notes: "Llantas super ligeras monobloque." },
        { code: "ING-WHE-02", name: "Neumáticos Hoosier Slick (x4)", dept: "suspension", status: "comprado", material: "Caucho de Competición", mfg: "Comercial", mass: 14000, cost: 800, x: 1200, y: 600, z: 220, feaStatus: "Aprobado", sponsor: "Comprados", notes: "Neumáticos de compuesto blando C2000 para seco." },
        { code: "ING-POW-04", name: "Semiejes de Transmisión (Driveshafts)", dept: "powertrain", status: "diseño", material: "Acero Grado Aeroespacial 300M", mfg: "Torneado CNC / Rallado", mass: 3200, cost: 0, x: 1950, y: 350, z: 220, feaStatus: "Pendiente", sponsor: "Mecanizados de Precisión", notes: "Semiejes con juntas homocinéticas ligeras." }
    ];

    // ==========================================
    // 2. INITIALIZATION AND LOCALSTORAGE
    // ==========================================
    const initBOM = () => {
        const localData = localStorage.getItem('cero_bom');
        if (localData) {
            try {
                bomData = JSON.parse(localData);
            } catch (e) {
                console.error("Error al cargar BOM, cargando base por defecto", e);
                bomData = [...defaultBOM];
                saveBOMToLocal();
            }
        } else {
            bomData = [...defaultBOM];
            saveBOMToLocal();
        }
    };

    const saveBOMToLocal = () => {
        localStorage.setItem('cero_bom', JSON.stringify(bomData));
        updateDashboardKPIs();
        renderBOMTable();
        updateReelPartDropdown();
        updateThreeJSScene();
    };

    // ==========================================
    // 3. TAB NAVIGATION CONTROLLER
    // ==========================================
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');
            
            tabButtons.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            const targetPane = document.getElementById(targetTab);
            if (targetPane) targetPane.classList.add('active');

            currentTab = targetTab;
            
            // Resize handler for Three.js when tab shifts to render properly
            if (currentTab === 'tab-telemetry') {
                onThreejsResize();
            }
            
            // Start or stop canvas loop depending on active tab to save CPU
            if (currentTab === 'tab-reels') {
                startReelPreview();
            } else {
                stopReelPreview();
            }
        });
    });

    // ==========================================
    // 4. PHYSICS ENGINE: CENTER OF GRAVITY (CoG)
    // ==========================================
    const updateDashboardKPIs = () => {
        let totalMassGrams = 0;
        let totalCost = 0;
        let totalMomentX = 0;
        let totalMomentY = 0;
        let totalMomentZ = 0;

        let totalCADCount = 0;
        let totalFabCount = 0;

        bomData.forEach(part => {
            const mass = parseFloat(part.mass) || 0;
            totalMassGrams += mass;
            totalCost += parseFloat(part.cost) || 0;

            // Moments: mass * distance
            totalMomentX += mass * (parseFloat(part.x) || 0);
            totalMomentY += mass * (parseFloat(part.y) || 0);
            totalMomentZ += mass * (parseFloat(part.z) || 0);

            // Lifecycle stats
            if (['diseño', 'fea', 'fabricacion', 'terminado', 'comprado'].includes(part.status)) {
                totalCADCount++;
            }
            if (['terminado', 'comprado'].includes(part.status)) {
                totalFabCount++;
            }
        });

        const totalMassKg = totalMassGrams / 1000;
        
        // CoG coordinates
        const cogX = totalMassGrams > 0 ? (totalMomentX / totalMassGrams) : 0;
        const cogY = totalMassGrams > 0 ? (totalMomentY / totalMassGrams) : 0;
        const cogZ = totalMassGrams > 0 ? (totalMomentZ / totalMassGrams) : 0;

        // Write KPIs in UI
        document.getElementById('kpi-mass').textContent = totalMassKg.toFixed(2) + " kg";
        document.getElementById('kpi-cost').textContent = totalCost.toLocaleString('es-ES') + " €";
        document.getElementById('kpi-cog-z').textContent = cogZ.toFixed(0) + " mm";

        // Weight distribution calculation: Wheelbase 1600mm, front axle at X=400, rear at X=2000
        // Wheel base = 1600. Y=0 is center. Left wheels at Y=-600, right at Y=600.
        let distFrontPercent = 50;
        let distRearPercent = 50;

        if (totalMassGrams > 0) {
            // Force percentage rear = (cogX - 400) / 1600
            // Since Front is X=400, Rear is X=2000.
            const df = cogX - 400;
            const wRear = (df / 1600) * 100;
            const wFront = 100 - wRear;

            distFrontPercent = Math.max(0, Math.min(100, wFront));
            distRearPercent = Math.max(0, Math.min(100, wRear));
        }
        
        document.getElementById('kpi-weight-dist').textContent = `${distFrontPercent.toFixed(0)}% / ${distRearPercent.toFixed(0)}%`;

        // Percentages progress
        const partCount = bomData.length;
        const cadPercent = partCount > 0 ? (totalCADCount / partCount) * 100 : 0;
        const fabPercent = partCount > 0 ? (totalFabCount / partCount) * 100 : 0;

        document.getElementById('kpi-cad-prog').textContent = cadPercent.toFixed(0) + "%";
        document.getElementById('kpi-cad-count').textContent = `${totalCADCount} de ${partCount} piezas`;

        document.getElementById('kpi-fab-prog').textContent = fabPercent.toFixed(0) + "%";
        document.getElementById('kpi-fab-count').textContent = `${totalFabCount} de ${partCount} piezas`;

        // CoG Coordinates displays
        document.getElementById('cog-coord-x').textContent = cogX.toFixed(1) + " mm";
        document.getElementById('cog-coord-y').textContent = cogY.toFixed(1) + " mm";
        document.getElementById('cog-coord-z').textContent = cogZ.toFixed(1) + " mm";

        // Warning alerts based on engineering checks
        const warningEl = document.getElementById('cog-warning-text');
        if (totalMassKg > 280) {
            warningEl.innerHTML = `<i class="fas fa-exclamation-triangle" style="color:var(--color-neon-pink);"></i> EXCESO DE PESO: Monoplaza excede los 280kg límite.`;
        } else if (distFrontPercent < 40 || distFrontPercent > 50) {
            warningEl.innerHTML = `<i class="fas fa-exclamation-triangle" style="color:var(--color-neon-yellow);"></i> REPARTO INESTABLE: Centro de masas demasiado alejado de la cabina (Del: ${distFrontPercent.toFixed(0)}%).`;
        } else if (Math.abs(cogY) > 25) {
            warningEl.innerHTML = `<i class="fas fa-exclamation-triangle" style="color:var(--color-neon-pink);"></i> DESEQUILIBRIO LATERAL: Centro de gravedad desviado a los lados (${cogY.toFixed(0)}mm).`;
        } else {
            warningEl.innerHTML = `<i class="fas fa-circle-check" style="color:var(--color-neon-green);"></i> REPARTO INTEGRAL CORRECTO: Parámetros del chasis validados para trazado dinámico.`;
        }

        // Store CoG values for 3D update
        window.currentCoG = { x: cogX, y: cogY, z: cogZ };
    };

    // ==========================================
    // 5. THREE.JS 3D GRAPHICS CONSTRUCTOR
    // ==========================================
    let scene3d, camera3d, renderer3d, controls3d;
    let partsGroup3d; // Node groups for parts
    let cogMesh3d; // Mass indicator
    let chassisLines3d; // Spaceframe structural representation

    const initThreeJS = () => {
        const container = document.getElementById('threejs-canvas-wrapper');
        if (!container) return;

        // Scene setup
        scene3d = new THREE.Scene();
        scene3d.background = new THREE.Color(0x08090d);
        scene3d.fog = new THREE.FogExp2(0x08090d, 0.0003);

        // Camera setup: Automotive scale. X is length, Y is side width, Z is height.
        // Formula Student coordinates: origin is ground at front bulkhead center.
        camera3d = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 8000);
        camera3d.position.set(-2500, 2000, 1500); // Isometric review starting angle

        // Renderer
        renderer3d = new THREE.WebGLRenderer({ antialias: true });
        renderer3d.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
        renderer3d.setSize(container.clientWidth, container.clientHeight);
        container.appendChild(renderer3d.domElement);

        // Mouse Controls
        controls3d = new THREE.OrbitControls(camera3d, renderer3d.domElement);
        controls3d.enableDamping = true;
        controls3d.dampingFactor = 0.05;
        controls3d.maxPolarAngle = Math.PI / 2 - 0.02; // Prevents camera sinking under ground
        controls3d.minDistance = 300;
        controls3d.maxDistance = 5000;

        // Lights
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.2);
        scene3d.add(ambientLight);

        const dirLight1 = new THREE.DirectionalLight(0xffffff, 0.5);
        dirLight1.position.set(2000, 3000, 2000);
        scene3d.add(dirLight1);

        const dirLight2 = new THREE.DirectionalLight(0x00e5ff, 0.6); // Tech blue secondary backlight
        dirLight2.position.set(-2000, -1000, 1000);
        scene3d.add(dirLight2);

        // Ground Grid
        const gridHelper = new THREE.GridHelper(6000, 60, 0x1f242d, 0x13161a);
        gridHelper.position.y = 0;
        gridHelper.rotation.x = Math.PI / 2; // Orient grid on XY floor plane (automotive coordinate layout)
        scene3d.add(gridHelper);

        // Chassis Structural Line Node Layout
        // Nodes array [X, Y, Z] (dimensions matching real spaceframe layout)
        const nodes = {
            f_bulk_tl: [400, 180, 250],
            f_bulk_tr: [400, -180, 250],
            f_bulk_bl: [400, 180, 50],
            f_bulk_br: [400, -180, 50],
            
            f_hoop_tl: [800, 220, 480],
            f_hoop_tr: [800, -220, 480],
            f_hoop_bl: [800, 250, 50],
            f_hoop_br: [800, -250, 50],

            m_hoop_t: [1450, 0, 950],
            m_hoop_ml: [1450, 260, 580],
            m_hoop_mr: [1450, -260, 580],
            m_hoop_bl: [1450, 280, 50],
            m_hoop_br: [1450, -280, 50],

            r_bulk_tl: [2100, 150, 350],
            r_bulk_tr: [2100, -150, 350],
            r_bulk_bl: [2100, 150, 80],
            r_bulk_br: [2100, -150, 80]
        };

        const chassisMaterial = new THREE.LineBasicMaterial({ color: 0x555c68, transparent: true, opacity: 0.5 });
        const chassisGeometry = new THREE.BufferGeometry();
        const positions = [];

        const addTubeLink = (n1, n2) => {
            positions.push(...nodes[n1], ...nodes[n2]);
        };

        // Connect Front Bulkhead
        addTubeLink('f_bulk_tl', 'f_bulk_tr'); addTubeLink('f_bulk_tr', 'f_bulk_br');
        addTubeLink('f_bulk_br', 'f_bulk_bl'); addTubeLink('f_bulk_bl', 'f_bulk_tl');
        // Connect Front Hoop
        addTubeLink('f_hoop_tl', 'f_hoop_tr'); addTubeLink('f_hoop_tr', 'f_hoop_br');
        addTubeLink('f_hoop_br', 'f_hoop_bl'); addTubeLink('f_hoop_bl', 'f_hoop_tl');
        // Connect Main Hoop
        addTubeLink('m_hoop_bl', 'm_hoop_ml'); addTubeLink('m_hoop_ml', 'm_hoop_t');
        addTubeLink('m_hoop_t', 'm_hoop_mr'); addTubeLink('m_hoop_mr', 'm_hoop_br');
        addTubeLink('m_hoop_br', 'm_hoop_bl');
        // Connect Rear Bulkhead
        addTubeLink('r_bulk_tl', 'r_bulk_tr'); addTubeLink('r_bulk_tr', 'r_bulk_br');
        addTubeLink('r_bulk_br', 'r_bulk_bl'); addTubeLink('r_bulk_bl', 'r_bulk_tl');

        // Connect longitudinal structures
        addTubeLink('f_bulk_tl', 'f_hoop_tl'); addTubeLink('f_bulk_tr', 'f_hoop_tr');
        addTubeLink('f_bulk_bl', 'f_hoop_bl'); addTubeLink('f_bulk_br', 'f_hoop_br');
        
        addTubeLink('f_hoop_tl', 'm_hoop_ml'); addTubeLink('f_hoop_tr', 'm_hoop_mr');
        addTubeLink('f_hoop_bl', 'm_hoop_bl'); addTubeLink('f_hoop_br', 'm_hoop_br');

        addTubeLink('m_hoop_ml', 'r_bulk_tl'); addTubeLink('m_hoop_mr', 'r_bulk_tr');
        addTubeLink('m_hoop_bl', 'r_bulk_bl'); addTubeLink('m_hoop_br', 'r_bulk_br');

        // Diagonal bracing members
        addTubeLink('f_bulk_bl', 'f_hoop_tl'); addTubeLink('f_bulk_br', 'f_hoop_tr');
        addTubeLink('f_hoop_bl', 'm_hoop_ml'); addTubeLink('f_hoop_br', 'm_hoop_mr');
        addTubeLink('m_hoop_t', 'r_bulk_bl'); addTubeLink('m_hoop_t', 'r_bulk_br');

        chassisGeometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
        chassisLines3d = new THREE.LineSegments(chassisGeometry, chassisMaterial);
        scene3d.add(chassisLines3d);

        // Group for BOM Parts
        partsGroup3d = new THREE.Group();
        scene3d.add(partsGroup3d);

        // Center of Gravity Sphere indicator
        const cogGeo = new THREE.SphereGeometry(32, 16, 16);
        const cogMat = new THREE.MeshBasicMaterial({ color: 0xff007f, transparent: true, opacity: 0.95 });
        cogMesh3d = new THREE.Mesh(cogGeo, cogMat);
        
        // Add glowing ring around CoG
        const ringGeo = new THREE.RingGeometry(45, 50, 32);
        const ringMat = new THREE.MeshBasicMaterial({ color: 0xff007f, side: THREE.DoubleSide });
        const ringMesh = new THREE.Mesh(ringGeo, ringMat);
        ringMesh.rotation.x = Math.PI / 2; // Flat on horizontal ground projection
        cogMesh3d.add(ringMesh);

        // Axis projection lines from CoG down to floor grid
        const lineMat = new THREE.LineDashedMaterial({ color: 0xff007f, dashSize: 40, gapSize: 20 });
        const lineGeo = new THREE.BufferGeometry().setAttribute('position', new THREE.Float32BufferAttribute([0, 0, 0, 0, 0, -2000], 3));
        const projLine = new THREE.Line(lineGeo, lineMat);
        projLine.computeLineDistances();
        cogMesh3d.add(projLine);

        scene3d.add(cogMesh3d);

        // Animate Frame Loop
        const animate = () => {
            requestAnimationFrame(animate);
            if (controls3d) controls3d.update();
            if (renderer3d && scene3d && camera3d) {
                renderer3d.render(scene3d, camera3d);
            }
        };
        animate();

        window.addEventListener('resize', onThreejsResize);
        onThreejsResize();
    };

    const onThreejsResize = () => {
        const container = document.getElementById('threejs-canvas-wrapper');
        if (!container || !renderer3d || !camera3d) return;

        camera3d.aspect = container.clientWidth / container.clientHeight;
        camera3d.updateProjectionMatrix();
        renderer3d.setSize(container.clientWidth, container.clientHeight);
    };

    // Rebuild meshes on the 3D canvas based on updated BOM list
    const updateThreeJSScene = () => {
        if (!scene3d || !partsGroup3d) return;

        // Clear existing parts
        while (partsGroup3d.children.length > 0) {
            const child = partsGroup3d.children[0];
            partsGroup3d.remove(child);
        }

        // Draw parts
        bomData.forEach((part, index) => {
            // Scale geometry representation size by its relative mass
            const mass = parseFloat(part.mass) || 100;
            const size = Math.max(25, Math.min(180, Math.pow(mass, 0.33) * 3));
            
            let geometry;
            let materialColor = 0x39ff14; // Default neon green

            // Color parts by Department for visual distinction
            if (part.dept === 'chassis') materialColor = 0x71717a;
            else if (part.dept === 'suspension') materialColor = 0x00e5ff;
            else if (part.dept === 'powertrain') materialColor = 0xffff00;
            else if (part.dept === 'battery') materialColor = 0xffa500;
            else if (part.dept === 'electronics') materialColor = 0xda70d6;
            else if (part.dept === 'aerodynamics') materialColor = 0x4682b4;

            // Geometry shapes based on name keywords
            const partNameLower = part.name.toLowerCase();
            if (partNameLower.includes("llanta") || partNameLower.includes("neumático") || partNameLower.includes("rueda")) {
                geometry = new THREE.CylinderGeometry(size * 1.5, size * 1.5, size * 1.0, 16);
            } else if (partNameLower.includes("motor") || partNameLower.includes("inversor")) {
                geometry = new THREE.CylinderGeometry(size, size, size * 1.6, 16);
            } else if (partNameLower.includes("chasis") || partNameLower.includes("aro")) {
                // Skips placing boxes for chassis (already line spaceframe drawn)
                return;
            } else {
                geometry = new THREE.BoxGeometry(size, size, size);
            }

            // Highlighting style if part is selected
            const isSelected = (selectedPartIdx === index);
            const material = new THREE.MeshPhongMaterial({
                color: materialColor,
                wireframe: true,
                transparent: true,
                opacity: isSelected ? 0.9 : 0.45,
                shininess: 100
            });

            const mesh = new THREE.Mesh(geometry, material);
            
            // Coordinates translation: Automotive coordinates in THREE:
            // FS system: X (length, front -> back), Y (side, center -> left/right), Z (height, ground -> up)
            // ThreeJS default coordinate frame: X (lateral), Y (height), Z (depth)
            // Mapping: ThreeJS X = part.y (width), ThreeJS Y = part.z (height), ThreeJS Z = -part.x (depth)
            mesh.position.set(part.y, part.z, -part.x);
            mesh.userData = { index: index };
            
            // Add a text code placard in 3D (visual indicator wire box)
            if (isSelected) {
                const boxHelper = new THREE.BoxHelper(mesh, 0xff007f);
                partsGroup3d.add(boxHelper);
            }

            partsGroup3d.add(mesh);
        });

        // Update Center of Gravity sphere mesh position
        if (window.currentCoG) {
            const cog = window.currentCoG;
            // Map coordinates frame
            cogMesh3d.position.set(cog.y, cog.z, -cog.x);
            
            // Adjust the floor line dash heights
            const projLine = cogMesh3d.children[1];
            if (projLine) {
                cogMesh3d.remove(projLine);
                const lineMat = new THREE.LineDashedMaterial({ color: 0xff007f, dashSize: 20, gapSize: 10 });
                const lineGeo = new THREE.BufferGeometry().setAttribute('position', new THREE.Float32BufferAttribute([0, 0, 0, 0, -cog.z, 0], 3));
                const newProjLine = new THREE.Line(lineGeo, lineMat);
                newProjLine.computeLineDistances();
                cogMesh3d.add(newProjLine);
            }
        }
    };

    // ==========================================
    // 6. BILL OF MATERIALS (BOM) RENDER LOGIC
    // ==========================================
    const renderBOMTable = () => {
        const body = document.getElementById('bom-table-body');
        if (!body) return;
        body.innerHTML = '';

        const deptFilter = document.getElementById('filter-dept').value;
        const statusFilter = document.getElementById('filter-status').value;
        const searchQuery = document.getElementById('search-bom').value.toLowerCase();

        bomData.forEach((part, index) => {
            // Apply filtering logic
            if (deptFilter !== 'all' && part.dept !== deptFilter) return;
            if (statusFilter !== 'all' && part.status !== statusFilter) return;
            if (searchQuery) {
                const queryMatch = part.name.toLowerCase().includes(searchQuery) ||
                                   part.code.toLowerCase().includes(searchQuery) ||
                                   part.material.toLowerCase().includes(searchQuery);
                if (!queryMatch) return;
            }

            const tr = document.createElement('tr');
            if (selectedPartIdx === index) tr.style.background = 'rgba(0, 229, 255, 0.05)';

            tr.innerHTML = `
                <td class="bom-code">${part.code}</td>
                <td class="bom-part-name">${part.name}</td>
                <td>${translateDept(part.dept)}</td>
                <td><span class="bom-status-badge status-${part.status}">${part.status}</span></td>
                <td>${part.material}</td>
                <td class="bom-mass">${(parseFloat(part.mass) || 0).toLocaleString('es-ES')} g</td>
                <td class="bom-pos">${part.x}, ${part.y}, ${part.z}</td>
                <td class="bom-cost">${(parseFloat(part.cost) || 0).toLocaleString('es-ES')} €</td>
                <td class="fea-status-${part.feaStatus ? part.feaStatus.toLowerCase() : 'pendiente'}"><span class="fea-${part.feaStatus === 'Aprobado' ? 'aprobado' : (part.feaStatus === 'Corregir' ? 'corregir' : 'pendiente')}">${part.feaStatus || 'Pendiente'}</span></td>
                <td>${part.sponsor || '—'}</td>
                <td>
                    <div class="table-row-actions">
                        <button class="btn-icon-sm edit-btn" data-idx="${index}" title="Editar Pieza"><i class="fas fa-edit"></i></button>
                        <button class="btn-icon-sm delete delete-btn" data-idx="${index}" title="Eliminar Pieza"><i class="fas fa-trash"></i></button>
                    </div>
                </td>
            `;

            // Event Listeners for actions
            tr.querySelector('.edit-btn').addEventListener('click', (e) => {
                e.stopPropagation();
                openPartModal(index);
            });

            tr.querySelector('.delete-btn').addEventListener('click', (e) => {
                e.stopPropagation();
                if (confirm(`¿Estás seguro de eliminar el componente "${part.name}"? Esto afectará los cálculos del Centro de Gravedad.`)) {
                    bomData.splice(index, 1);
                    saveBOMToLocal();
                }
            });

            // Click table row to highlight on 3D viewport
            tr.addEventListener('click', () => {
                selectedPartIdx = (selectedPartIdx === index) ? null : index;
                renderBOMTable();
                updateThreeJSScene();
                if (selectedPartIdx !== null) {
                    focusCameraOnPart(bomData[selectedPartIdx]);
                }
            });

            body.appendChild(tr);
        });
    };

    const translateDept = (dept) => {
        const mapping = {
            chassis: "Chasis",
            suspension: "Suspensión/Frenos",
            powertrain: "Powertrain",
            battery: "Batería Pack",
            electronics: "Electrónica",
            aerodynamics: "Aerodinámica",
            ergonomics: "Ergonomía"
        };
        return mapping[dept] || dept;
    };

    // Camera autofocus on chosen node coordinates
    const focusCameraOnPart = (part) => {
        if (!camera3d || !controls3d) return;

        // Animate camera target movement
        const targetX = part.y;
        const targetY = part.z;
        const targetZ = -part.x;

        // Smooth translation
        let step = 0;
        const originTarget = controls3d.target.clone();
        
        const smoothCamMove = () => {
            if (step < 20) {
                controls3d.target.lerp(new THREE.Vector3(targetX, targetY, targetZ), 0.15);
                step++;
                requestAnimationFrame(smoothCamMove);
            }
        };
        smoothCamMove();
    };

    // Search and Filters triggering table render
    document.getElementById('filter-dept').addEventListener('change', renderBOMTable);
    document.getElementById('filter-status').addEventListener('change', renderBOMTable);
    document.getElementById('search-bom').addEventListener('input', renderBOMTable);

    // BOM Modal controls
    const partModal = document.getElementById('part-modal');
    const formPartEditor = document.getElementById('form-part-editor');

    const openPartModal = (index = null) => {
        formPartEditor.reset();
        document.getElementById('edit-part-idx').value = index !== null ? index : '';
        
        if (index !== null) {
            document.getElementById('modal-title-text').innerHTML = `<i class="fas fa-edit"></i> Editar Componente`;
            const part = bomData[index];
            document.getElementById('part-code').value = part.code;
            document.getElementById('part-name').value = part.name;
            document.getElementById('part-dept').value = part.dept;
            document.getElementById('part-status').value = part.status;
            document.getElementById('part-material').value = part.material;
            document.getElementById('part-mfg').value = part.mfg;
            document.getElementById('part-mass').value = part.mass;
            document.getElementById('part-cost').value = part.cost;
            document.getElementById('part-x').value = part.x;
            document.getElementById('part-y').value = part.y;
            document.getElementById('part-z').value = part.z;
            document.getElementById('part-fea-status').value = part.feaStatus || "Pendiente";
            document.getElementById('part-sponsor').value = part.sponsor || "";
            document.getElementById('part-cad-url').value = part.cadUrl || "";
            document.getElementById('part-notes').value = part.notes || "";
        } else {
            document.getElementById('modal-title-text').innerHTML = `<i class="fas fa-plus-circle"></i> Añadir Nueva Pieza al Monoplaza`;
            // Suggest clean incremental code
            const nextIdx = bomData.length + 1;
            document.getElementById('part-code').value = `ING-PIEZA-${nextIdx < 10 ? '0' + nextIdx : nextIdx}`;
        }
        partModal.style.display = 'flex';
    };

    document.getElementById('btn-add-part').addEventListener('click', () => openPartModal(null));
    document.getElementById('btn-cancel-modal').addEventListener('click', () => partModal.style.display = 'none');
    document.getElementById('btn-close-part-modal').addEventListener('click', () => partModal.style.display = 'none');

    formPartEditor.addEventListener('submit', (e) => {
        e.preventDefault();
        const indexVal = document.getElementById('edit-part-idx').value;
        
        const partInfo = {
            code: document.getElementById('part-code').value,
            name: document.getElementById('part-name').value,
            dept: document.getElementById('part-dept').value,
            status: document.getElementById('part-status').value,
            material: document.getElementById('part-material').value,
            mfg: document.getElementById('part-mfg').value,
            mass: parseFloat(document.getElementById('part-mass').value) || 0,
            cost: parseFloat(document.getElementById('part-cost').value) || 0,
            x: parseFloat(document.getElementById('part-x').value) || 0,
            y: parseFloat(document.getElementById('part-y').value) || 0,
            z: parseFloat(document.getElementById('part-z').value) || 0,
            feaStatus: document.getElementById('part-fea-status').value,
            sponsor: document.getElementById('part-sponsor').value,
            cadUrl: document.getElementById('part-cad-url').value,
            notes: document.getElementById('part-notes').value
        };

        if (indexVal !== '') {
            // Update
            bomData[parseInt(indexVal)] = partInfo;
        } else {
            // Create
            bomData.push(partInfo);
        }

        saveBOMToLocal();
        partModal.style.display = 'none';
    });

    // Populate standard car components from CERO template database
    document.getElementById('btn-load-base').addEventListener('click', () => {
        if (confirm("¿Quieres recargar el listado base homologado de CERO? Esto reemplazará los datos que hayas modificado.")) {
            bomData = [...defaultBOM];
            saveBOMToLocal();
        }
    });

    // Export/Import JSON database files
    document.getElementById('btn-export-bom').addEventListener('click', () => {
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(bomData, null, 2));
        const downloadAnchor = document.createElement('a');
        downloadAnchor.setAttribute("href", dataStr);
        downloadAnchor.setAttribute("download", `BOM_CERO_PROYECTO_${Date.now()}.json`);
        document.body.appendChild(downloadAnchor);
        downloadAnchor.click();
        downloadAnchor.remove();
    });

    const importTrigger = document.getElementById('btn-import-bom-trigger');
    const importInput = document.getElementById('input-import-bom');
    
    importTrigger.addEventListener('click', () => importInput.click());
    
    importInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (evt) => {
            try {
                const parsed = JSON.parse(evt.target.result);
                if (Array.isArray(parsed)) {
                    bomData = parsed;
                    saveBOMToLocal();
                    alert("Base de datos BOM importada correctamente con " + parsed.length + " piezas.");
                } else {
                    alert("El archivo no contiene un formato de inventario compatible.");
                }
            } catch (err) {
                alert("Error al leer el archivo JSON.");
            }
        };
        reader.readAsText(file);
    });

    // ==========================================
    // 7. TECHNICAL CALCULATORS FORMULAS
    // ==========================================
    
    // Calculator 1: Battery accumulator
    document.getElementById('btn-calc-battery').addEventListener('click', () => {
        const cellV = parseFloat(document.getElementById('cell-v').value) || 0;
        const cellCap = parseFloat(document.getElementById('cell-cap').value) || 0;
        const cellsS = parseInt(document.getElementById('cells-s').value) || 0;
        const cellsP = parseInt(document.getElementById('cells-p').value) || 0;
        const cellDis = parseFloat(document.getElementById('cell-dis').value) || 0;
        const cellW = parseFloat(document.getElementById('cell-w').value) || 0;

        const packVolt = cellsS * cellV;
        const packCap = cellsP * cellCap;
        const packEnergy = (packVolt * packCap) / 1000; // kWh
        const packCurr = cellsP * cellDis; // Max peak current
        const packPower = (packVolt * packCurr) / 1000; // kW
        const packMass = (cellsS * cellsP * cellW) / 1000; // kg of cells

        document.getElementById('res-bat-volt').textContent = packVolt.toFixed(1) + " V";
        document.getElementById('res-bat-cap').textContent = packCap.toFixed(1) + " Ah";
        document.getElementById('res-bat-energy').textContent = packEnergy.toFixed(2) + " kWh";
        document.getElementById('res-bat-curr').textContent = packCurr.toFixed(0) + " A";
        document.getElementById('res-bat-power').textContent = packPower.toFixed(1) + " kW (pico)";
        document.getElementById('res-bat-mass').textContent = packMass.toFixed(2) + " kg";

        document.getElementById('results-battery').style.display = 'block';
    });

    // Calculator 2: Transmission and Speed
    document.getElementById('btn-calc-transmission').addEventListener('click', () => {
        const rpm = parseFloat(document.getElementById('motor-rpm').value) || 0;
        const torque = parseFloat(document.getElementById('motor-torque').value) || 0;
        const ratio = parseFloat(document.getElementById('gear-ratio').value) || 1;
        const diamInches = parseFloat(document.getElementById('tire-diam').value) || 0;

        const wheelTorque = torque * ratio;
        const wheelRpm = rpm / ratio;
        const tireDiamMeters = diamInches * 0.0254; // inch to meter conversion
        
        // Speed formula: V (m/s) = RPM_wheel * PI * Diam / 60
        // Speed (km/h) = V(m/s) * 3.6
        const speed = (wheelRpm * Math.PI * tireDiamMeters / 60) * 3.6;

        document.getElementById('res-trans-torque').textContent = wheelTorque.toFixed(0) + " Nm";
        document.getElementById('res-trans-speed').textContent = speed.toFixed(1) + " km/h";
        document.getElementById('res-trans-wheelrpm').textContent = wheelRpm.toFixed(0) + " RPM";

        document.getElementById('results-transmission').style.display = 'block';
    });

    // Calculator 3: Structural beam calculations (Euler-Bernoulli beam theory)
    document.getElementById('btn-calc-beam').addEventListener('click', () => {
        const material = document.getElementById('beam-material').value;
        const od = parseFloat(document.getElementById('beam-od').value) || 0;
        const t = parseFloat(document.getElementById('beam-t').value) || 0;
        const l = parseFloat(document.getElementById('beam-length').value) || 0;

        // Constants based on material choices
        let E = 205000; // MPa (N/mm^2)
        let Sy = 460; // MPa
        let rho = 7.85e-6; // kg/mm^3 (Steel density)

        if (material === '1020') {
            E = 200000; Sy = 295; rho = 7.85e-6;
        } else if (material === '6082') {
            E = 70000; Sy = 250; rho = 2.7e-6;
        }

        const id = od - (2 * t); // Inner diameter
        if (id <= 0) {
            alert("El espesor de pared excede el radio del tubo.");
            return;
        }

        // Moment of Inertia for circular tube: I = PI/64 * (OD^4 - ID^4)
        const I = (Math.PI / 64) * (Math.pow(od, 4) - Math.pow(id, 4));
        
        // Cross-section area: A = PI/4 * (OD^2 - ID^2)
        const A = (Math.PI / 4) * (Math.pow(od, 2) - Math.pow(id, 2));
        const mass = rho * l * A; // kg

        // Flexural Stiffness: E * I (converted to N*m^2)
        // E (N/mm^2) * I (mm^4) = E * I (N*mm^2). Divide by 1e6 to get N*m^2.
        const EI = (E * I) / 1000000;

        // Maximum central load force before yield under simply supported conditions:
        // Max bending stress: sigma = M * c / I where c = OD/2.
        // For central point load F, M_max = F * L / 4.
        // Therefore, Sy = (F * L / 4) * (OD/2) / I ==> F_max = (8 * Sy * I) / (L * OD)
        const maxForce = (8 * Sy * I) / (l * od);

        document.getElementById('res-beam-i').textContent = I.toFixed(1) + " mm⁴";
        document.getElementById('res-beam-mass').textContent = mass.toFixed(3) + " kg";
        document.getElementById('res-beam-ei').textContent = EI.toFixed(1) + " N·m²";
        document.getElementById('res-beam-load').textContent = maxForce.toFixed(0) + " N (" + (maxForce / 9.81).toFixed(0) + " kgf)";

        document.getElementById('results-beam').style.display = 'block';
    });


    // ==========================================
    // 8. MOTION GRAPHICS & REELS VIDEO EXPORTER
    // ==========================================
    const reelPartSelect = document.getElementById('reel-part-select');
    const updateReelPartDropdown = () => {
        if (!reelPartSelect) return;
        reelPartSelect.innerHTML = '';
        bomData.forEach((part, index) => {
            const opt = document.createElement('option');
            opt.value = index;
            opt.textContent = `[${part.code}] ${part.name}`;
            reelPartSelect.appendChild(opt);
        });
    };

    // Canvas drawing contexts for video generator
    const reelCanvas = document.getElementById('reel-canvas');
    let ctxReel = null;
    let previewLoopActive = false;
    let frameCount = 0;
    
    // Sound wave simulation frequencies
    let audioWaveFreq = 1;
    let audioGenre = 'techno';

    const startReelPreview = () => {
        if (!reelCanvas) return;
        ctxReel = reelCanvas.getContext('2d');
        previewLoopActive = true;
        
        // Handle dropdown music rhythm changes
        const musicSelect = document.getElementById('reel-music-beat');
        const updateBeatSpeed = () => {
            const val = musicSelect.value;
            audioGenre = val;
            if (val === 'techno') audioWaveFreq = 2.4;
            else if (val === 'synthwave') audioWaveFreq = 1.6;
            else if (val === 'lofi') audioWaveFreq = 0.8;
        };
        musicSelect.addEventListener('change', updateBeatSpeed);
        updateBeatSpeed();

        drawReelFrameLoop();
    };

    const stopReelPreview = () => {
        previewLoopActive = false;
    };

    // Subida de imagen propia
    const bgImageInput = document.getElementById('reel-bg-image');
    const clearBgImageBtn = document.getElementById('btn-clear-bg-image');
    let loadedBgImage = null;

    bgImageInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (evt) => {
                const img = new Image();
                img.onload = () => {
                    loadedBgImage = img;
                    clearBgImageBtn.style.display = 'inline-block';
                };
                img.src = evt.target.result;
            };
            reader.readAsDataURL(file);
        }
    });

    clearBgImageBtn.addEventListener('click', () => {
        loadedBgImage = null;
        bgImageInput.value = '';
        clearBgImageBtn.style.display = 'none';
    });

    // Draw frame on canvas (shared by preview and recorder export)
    const drawSingleFrame = (ctx, canvasWidth, canvasHeight, time, frameIdx) => {
        // Clear background
        ctx.fillStyle = "#040508";
        ctx.fillRect(0, 0, canvasWidth, canvasHeight);

        // Fetch inputs dynamically
        const partIdx = parseInt(reelPartSelect.value) || 0;
        const part = bomData[partIdx] || { code: "CERO-00", name: "Monoplaza Colaborativo", mass: 230000, cost: 0, material: "Chromoly", status: "Concepto", x:0, y:0, z:0 };
        const template = document.getElementById('reel-template').value;
        const neonColor = document.getElementById('reel-neon-color').value;
        const dayNumber = document.getElementById('reel-day').value;
        const watermark = document.getElementById('reel-watermark').value;
        const titleText = document.getElementById('reel-title').value.toUpperCase();
        const subtitleText = document.getElementById('reel-subtitle').value;

        // Pulse scale factor (reactive to simulated audio beats)
        const bpmFrequency = (audioGenre === 'techno') ? 132 : (audioGenre === 'synthwave' ? 110 : 80);
        const beatInterval = 60 / bpmFrequency; // seconds per beat
        const pulseVal = Math.pow(Math.sin((time / 1000) * Math.PI * (bpmFrequency / 60)), 4);
        
        // Background layer: loaded user photo vs wireframe/matrix graphics
        if (loadedBgImage) {
            // Draw image with Ken Burns slow panning zoom effect
            const aspect = loadedBgImage.width / loadedBgImage.height;
            const zoomScale = 1.05 + 0.05 * Math.sin(time / 4000);
            const w = canvasHeight * aspect * zoomScale;
            const h = canvasHeight * zoomScale;
            const x = (canvasWidth - w) / 2 + 15 * Math.cos(time / 3000);
            const y = (canvasHeight - h) / 2;
            ctx.drawImage(loadedBgImage, x, y, w, h);

            // Dark tech gradient overlay
            const grad = ctx.createLinearGradient(0, 0, 0, canvasHeight);
            grad.addColorStop(0, "rgba(4, 5, 8, 0.9)");
            grad.addColorStop(0.3, "rgba(4, 5, 8, 0.4)");
            grad.addColorStop(0.7, "rgba(4, 5, 8, 0.4)");
            grad.addColorStop(1, "rgba(4, 5, 8, 0.95)");
            ctx.fillStyle = grad;
            ctx.fillRect(0, 0, canvasWidth, canvasHeight);
        } else {
            // Procedural neon grid background (scrolling down)
            ctx.strokeStyle = "rgba(255, 255, 255, 0.015)";
            ctx.lineWidth = 1;
            
            const gridSpacing = 40;
            const yScroll = (time * 0.06) % gridSpacing;
            for (let x = 0; x < canvasWidth; x += gridSpacing) {
                ctx.beginPath();
                ctx.moveTo(x, 0);
                ctx.lineTo(x, canvasHeight);
                ctx.stroke();
            }
            for (let y = yScroll; y < canvasHeight; y += gridSpacing) {
                ctx.beginPath();
                ctx.moveTo(0, y);
                ctx.lineTo(canvasWidth, y);
                ctx.stroke();
            }

            // Draw a futuristic rotating 3D wireframe representing the part
            // Draw wireframe in the center of the video screen
            const centerY = canvasHeight * 0.42;
            const centerX = canvasWidth / 2;
            const orbitRotX = time * 0.0006;
            const orbitRotY = time * 0.001;

            ctx.strokeStyle = neonColor;
            ctx.lineWidth = 2.0;
            
            // Draw custom wireframe geometries based on part dimensions
            // A wheel cylindrical profile vs chassis tubular wirecube
            const partNameLower = part.name.toLowerCase();
            const geometryType = (partNameLower.includes("llanta") || partNameLower.includes("neumático") || partNameLower.includes("rueda")) ? 'wheel' : 
                                 (partNameLower.includes("chasis") || partNameLower.includes("aro") ? 'spaceframe' : 'box');

            drawProcedural3DOn2D(ctx, centerX, centerY, 150 + 8 * pulseVal, orbitRotX, orbitRotY, geometryType, neonColor);
        }

        // --- HUD HUD HUD OVERLAY ELEMENTS ---
        // Top URL Bar (cero branding)
        ctx.fillStyle = "rgba(255,255,255,0.05)";
        ctx.fillRect(30, 40, canvasWidth - 60, 40);
        ctx.strokeStyle = "rgba(255,255,255,0.1)";
        ctx.strokeRect(30, 40, canvasWidth - 60, 40);
        
        ctx.fillStyle = "#fff";
        ctx.font = "bold 14px " + getFontSans();
        ctx.fillText("BUILDCERO.COM", 50, 65);

        // Day tag neon badge
        ctx.fillStyle = neonColor;
        ctx.fillRect(canvasWidth - 110, 48, 70, 24);
        ctx.fillStyle = "#000";
        ctx.font = "bold 11px " + getFontMono();
        ctx.textAlign = "center";
        ctx.fillText(`DÍA ${dayNumber}`, canvasWidth - 75, 64);
        ctx.textAlign = "left"; // reset

        // Draw lateral scrolling logs (matrix HUD style)
        ctx.fillStyle = "rgba(255,255,255,0.25)";
        ctx.font = "9px " + getFontMono();
        const logs = [
            `SYS_TELEMETRY_CLOCK: ${(time/1000).toFixed(3)}s`,
            `ACTIVE_NODE: ${part.code}`,
            `PART_MAPPED_COORDS: X=${part.x} Y=${part.y} Z=${part.z}`,
            `MATERIAL_STRENGTH_YIELD: ${part.material}`,
            `WEIGHT_COG_INFLUENCE: ${((part.mass/230000)*100).toFixed(2)}%`,
            `CAD_STATUS_REVISION: Approved`
        ];
        logs.forEach((log, idx) => {
            ctx.fillText(log, 40, 140 + (idx * 16));
        });

        // Bottom HUD Panel with borders
        const infoPanelY = canvasHeight * 0.68;
        ctx.fillStyle = "rgba(12, 14, 18, 0.9)";
        ctx.fillRect(35, infoPanelY, canvasWidth - 70, canvasHeight - infoPanelY - 90);
        ctx.strokeStyle = "rgba(255, 255, 255, 0.08)";
        ctx.lineWidth = 1;
        ctx.strokeRect(35, infoPanelY, canvasWidth - 70, canvasHeight - infoPanelY - 90);

        // Glowing border accents based on style selection
        ctx.strokeStyle = neonColor;
        ctx.beginPath();
        ctx.moveTo(35, infoPanelY + 30);
        ctx.lineTo(35, infoPanelY);
        ctx.lineTo(75, infoPanelY);
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(canvasWidth - 35, infoPanelY + 30);
        ctx.lineTo(canvasWidth - 35, infoPanelY);
        ctx.lineTo(canvasWidth - 75, infoPanelY);
        ctx.stroke();

        // Technical descriptions texts inside panel
        ctx.fillStyle = "#fff";
        ctx.font = "bold 14px " + getFontMono();
        ctx.fillText(part.code, 55, infoPanelY + 30);

        // Status pill
        ctx.fillStyle = "rgba(255,255,255,0.06)";
        ctx.fillRect(canvasWidth - 170, infoPanelY + 16, 120, 20);
        ctx.fillStyle = neonColor;
        ctx.font = "bold 10px " + getFontMono();
        ctx.fillText("ESTADO: " + part.status.toUpperCase(), canvasWidth - 160, infoPanelY + 30);

        // Draw Big Title and Subtitle
        ctx.fillStyle = "#fff";
        ctx.font = "bold 24px " + getFontDisplay();
        ctx.fillText(titleText, 55, infoPanelY + 68);

        ctx.fillStyle = "rgba(255,255,255,0.7)";
        ctx.font = "12px " + getFontSans();
        ctx.fillText(subtitleText, 55, infoPanelY + 88);

        // Render parameters grid depending on selected Template style
        const gridY = infoPanelY + 115;
        ctx.strokeStyle = "rgba(255,255,255,0.05)";
        ctx.beginPath();
        ctx.moveTo(55, gridY);
        ctx.lineTo(canvasWidth - 55, gridY);
        ctx.stroke();

        if (template === 'telemetry-hud') {
            // Template 1: Technical specs
            drawSpecItem(ctx, "Masa Est.", (part.mass / 1000).toFixed(2) + " kg", 55, gridY + 25);
            drawSpecItem(ctx, "Material", part.material, 175, gridY + 25);
            drawSpecItem(ctx, "Fabricación", part.mfg, 55, gridY + 55);
            drawSpecItem(ctx, "Posición", `[${part.x},${part.y},${part.z}]`, 175, gridY + 55);
        } else if (template === 'fea-stress') {
            // Template 2: FEA Stress indicators
            drawSpecItem(ctx, "FEA Status", part.feaStatus || "Aprobado", 55, gridY + 25, neonColor);
            drawSpecItem(ctx, "Material", part.material, 175, gridY + 25);
            drawSpecItem(ctx, "Corte", part.mfg, 55, gridY + 55);
            drawSpecItem(ctx, "Seguridad", "Fs: 2.1 (Min)", 175, gridY + 55);
        } else if (template === 'budget-ticker') {
            // Template 3: Cost and Sponsor reveals
            drawSpecItem(ctx, "Coste Real", part.cost + " €", 55, gridY + 25, "#39ff14");
            drawSpecItem(ctx, "Presupuesto", "Meta €0", 175, gridY + 25);
            drawSpecItem(ctx, "Patrocinador", part.sponsor || "Patrocinio Pendiente", 55, gridY + 55, neonColor);
            drawSpecItem(ctx, "Ahorro", part.cost === 0 ? "100% patrocinado" : "—", 175, gridY + 55);
        } else {
            // Minimalist profile specs
            drawSpecItem(ctx, "Peso de la pieza", part.mass + " g", 55, gridY + 25);
            drawSpecItem(ctx, "Centro de Masas", `Z: ${part.z}mm`, 175, gridY + 25);
            drawSpecItem(ctx, "Homologado", "F.S. T-12", 55, gridY + 55);
            drawSpecItem(ctx, "Sponsor", part.sponsor || "Makers CERO", 175, gridY + 55);
        }

        // Draw reactively pulsing audio waveform line at the bottom
        ctx.strokeStyle = "rgba(255,255,255,0.06)";
        ctx.lineWidth = 1;
        ctx.beginPath();
        const waveY = canvasHeight - 75;
        ctx.moveTo(35, waveY);
        ctx.lineTo(canvasWidth - 35, waveY);
        ctx.stroke();

        ctx.strokeStyle = neonColor;
        ctx.lineWidth = 2;
        ctx.beginPath();
        for (let x = 40; x < canvasWidth - 40; x += 4) {
            const distFromCenter = Math.abs(x - (canvasWidth / 2)) / (canvasWidth / 2);
            // Wave height decays towards edges
            const amplitude = 35 * (1 - distFromCenter) * (0.2 + 0.8 * pulseVal);
            const freqFactor = audioWaveFreq;
            const yOffset = Math.sin((x * 0.08) - (time * 0.015) * freqFactor) * amplitude;
            
            if (x === 40) ctx.moveTo(x, waveY + yOffset);
            else ctx.lineTo(x, waveY + yOffset);
        }
        ctx.stroke();

        // Footer copyright watermark
        ctx.fillStyle = "rgba(255,255,255,0.3)";
        ctx.font = "bold 12px " + getFontSans();
        ctx.fillText("PROYECTO CERO", 40, canvasHeight - 35);

        ctx.fillStyle = neonColor;
        ctx.font = "bold 12px " + getFontMono();
        ctx.textAlign = "right";
        ctx.fillText(watermark, canvasWidth - 40, canvasHeight - 35);
        ctx.textAlign = "left"; // reset
    };

    // Helper functions for fonts
    const getFontSans = () => "'Outfit', sans-serif";
    const getFontDisplay = () => "'Space Grotesk', sans-serif";
    const getFontMono = () => "'JetBrains Mono', monospace";

    const drawSpecItem = (ctx, label, val, x, y, valColor = "#fff") => {
        ctx.fillStyle = "rgba(255,255,255,0.4)";
        ctx.font = "10px " + getFontSans();
        ctx.fillText(label.toUpperCase(), x, y);

        ctx.fillStyle = valColor;
        ctx.font = "bold 12px " + getFontMono();
        ctx.fillText(val, x, y + 15);
    };

    // Fast 3D wireframe render projected on 2D Canvas context
    // This allows us to avoid running a second WebGL session which crashes during video export
    const drawProcedural3DOn2D = (ctx, cx, cy, scale, rotX, rotY, type, color) => {
        let vertices = [];
        let edges = [];

        if (type === 'wheel') {
            // Draw cylinder representing Formula tyre
            const steps = 12;
            const radius = 0.9;
            const height = 0.8;
            
            // Build vertices
            for (let i = 0; i < steps; i++) {
                const ang = (i / steps) * Math.PI * 2;
                const x = Math.cos(ang) * radius;
                const y = Math.sin(ang) * radius;
                // Front and back face loops
                vertices.push({ x: x, y: y, z: height/2 });
                vertices.push({ x: x, y: y, z: -height/2 });
                
                // Outer circle loops connections
                const idx = i * 2;
                edges.push([idx, (idx + 2) % (steps * 2)]);
                edges.push([idx + 1, (idx + 3) % (steps * 2)]);
                edges.push([idx, idx + 1]); // connecting cylinder depths
            }
        } else if (type === 'spaceframe') {
            // Complex spaceframe layout
            vertices = [
                {x: -0.8, y: -0.4, z: -0.4}, {x: -0.8, y: 0.4, z: -0.4}, {x: -0.8, y: -0.4, z: 0.4}, {x: -0.8, y: 0.4, z: 0.4},
                {x: -0.2, y: -0.5, z: -0.5}, {x: -0.2, y: 0.5, z: -0.5}, {x: -0.2, y: -0.5, z: 0.5}, {x: -0.2, y: 0.5, z: 0.5},
                {x: 0.5, y: -0.6, z: -0.6}, {x: 0.5, y: 0.6, z: -0.6}, {x: 0.5, y: -0.6, z: 0.8}, {x: 0.5, y: 0.6, z: 0.8},
                {x: 1.2, y: -0.4, z: -0.4}, {x: 1.2, y: 0.4, z: -0.4}, {x: 1.2, y: -0.4, z: 0.4}, {x: 1.2, y: 0.4, z: 0.4}
            ];
            edges = [
                [0,1], [1,3], [3,2], [2,0], [4,5], [5,7], [7,6], [6,4],
                [8,9], [9,11], [11,10], [10,8], [12,13], [13,15], [15,14], [14,12],
                [0,4], [1,5], [2,6], [3,7], [4,8], [5,9], [6,10], [7,11],
                [8,12], [9,13], [10,14], [11,15], [0,7], [1,6], [10,13], [11,12]
            ];
        } else {
            // Solid cuboid box
            vertices = [
                {x: -0.6, y: -0.6, z: -0.6}, {x: 0.6, y: -0.6, z: -0.6},
                {x: 0.6, y: 0.6, z: -0.6}, {x: -0.6, y: 0.6, z: -0.6},
                {x: -0.6, y: -0.6, z: 0.6}, {x: 0.6, y: -0.6, z: 0.6},
                {x: 0.6, y: 0.6, z: 0.6}, {x: -0.6, y: 0.6, z: 0.6}
            ];
            edges = [
                [0,1], [1,2], [2,3], [3,0], [4,5], [5,6], [6,7], [7,4],
                [0,4], [1,5], [2,6], [3,7], [0,5], [2,7] // braces
            ];
        }

        // Project and Draw 3D
        const projected = [];
        vertices.forEach(v => {
            // Apply rotations
            // Y rotation
            let x1 = v.x * Math.cos(rotY) - v.z * Math.sin(rotY);
            let z1 = v.x * Math.sin(rotY) + v.z * Math.cos(rotY);
            let y1 = v.y;

            // X rotation
            let y2 = y1 * Math.cos(rotX) - z1 * Math.sin(rotX);
            let z2 = y1 * Math.sin(rotX) + z1 * Math.cos(rotX);
            let x2 = x1;

            // Simple isometric projection
            const camDistance = 3.0;
            const factor = scale / (z2 + camDistance);
            
            projected.push({
                x: cx + x2 * factor,
                y: cy + y2 * factor
            });
        });

        // Draw wireframe links
        edges.forEach(edge => {
            const p1 = projected[edge[0]];
            const p2 = projected[edge[1]];
            
            ctx.beginPath();
            ctx.moveTo(p1.x, p1.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.stroke();
        });

        // Draw vertex nodes
        ctx.fillStyle = "#fff";
        projected.forEach(p => {
            ctx.beginPath();
            ctx.arc(p.x, p.y, 3, 0, Math.PI * 2);
            ctx.fill();
        });
    };

    // Live preview frame loops
    const drawReelFrameLoop = () => {
        if (!previewLoopActive) return;
        
        const now = Date.now();
        frameCount++;
        
        // Render 540x960 inside UI preview
        drawSingleFrame(ctxReel, reelCanvas.width, reelCanvas.height, now, frameCount);
        
        // Calculate and show active preview FPS count
        if (frameCount % 30 === 0) {
            const fpsText = document.getElementById('fps-display');
            if (fpsText) fpsText.textContent = "60 FPS Preview";
        }

        requestAnimationFrame(drawReelFrameLoop);
    };

    // Export Reels engine using high bitrate stream encoder
    const btnReelExport = document.getElementById('btn-reel-export');
    const exportProgressWrap = document.getElementById('export-progress-wrap');
    const exportProgressFill = document.getElementById('export-progress-fill');
    const exportProgressPercent = document.getElementById('export-progress-percent');

    btnReelExport.addEventListener('click', async () => {
        if (bomData.length === 0) {
            alert("Carga o añade componentes al inventario antes de exportar.");
            return;
        }

        // Disable UI actions during processing
        btnReelExport.disabled = true;
        exportProgressWrap.style.display = 'block';
        
        // Setup a dedicated high-res Canvas offscreen (1080x1920 Full HD)
        const exportCanvas = document.createElement('canvas');
        exportCanvas.width = 1080;
        exportCanvas.height = 1920;
        const ctxExport = exportCanvas.getContext('2d');

        // Grab canvas video stream
        // High quality setting: 60 FPS, Bitrate: 10Mbps (10000000)
        let stream;
        try {
            stream = exportCanvas.captureStream(60);
        } catch (e) {
            // Safari / Older browser fallback
            stream = exportCanvas.captureStream(30);
        }

        const options = { mimeType: 'video/webm;codecs=vp9,opus', videoBitsPerSecond: 10000000 };
        let mediaRecorder;
        
        try {
            mediaRecorder = new MediaRecorder(stream, options);
        } catch (e) {
            // Fallback if VP9 codec not supported on machine
            try {
                mediaRecorder = new MediaRecorder(stream, { mimeType: 'video/webm;codecs=vp8', videoBitsPerSecond: 8000000 });
            } catch (err) {
                // Hard fallback
                mediaRecorder = new MediaRecorder(stream, { videoBitsPerSecond: 6000000 });
            }
        }

        const recordedChunks = [];
        mediaRecorder.ondataavailable = (e) => {
            if (e.data && e.data.size > 0) recordedChunks.push(e.data);
        };

        // Complete compilation and download triggers
        mediaRecorder.onstop = () => {
            const videoBlob = new Blob(recordedChunks, { type: 'video/webm' });
            const videoUrl = URL.createObjectURL(videoBlob);
            
            const downloadAnchor = document.createElement('a');
            downloadAnchor.href = videoUrl;
            downloadAnchor.download = `REEL_CERO_DAY_${document.getElementById('reel-day').value}_${Date.now()}.webm`;
            document.body.appendChild(downloadAnchor);
            downloadAnchor.click();
            downloadAnchor.remove();
            
            // Re-enable interface
            btnReelExport.disabled = false;
            exportProgressWrap.style.display = 'none';
        };

        // Start recording
        mediaRecorder.start();

        // High precision frame-by-frame rendering loop
        const totalDurationMs = 5000; // 5-second dynamic reel
        const targetFps = 60;
        const totalFrames = (totalDurationMs / 1000) * targetFps;
        const frameIntervalMs = 1000 / targetFps;

        let curFrame = 0;
        
        const renderExportFrame = () => {
            if (curFrame >= totalFrames) {
                // Finished
                mediaRecorder.stop();
                return;
            }

            const simulatedTime = curFrame * frameIntervalMs;
            
            // Draw high resolution frame
            drawSingleFrame(ctxExport, exportCanvas.width, exportCanvas.height, simulatedTime, curFrame);
            
            // Update progress bars
            curFrame++;
            const pct = (curFrame / totalFrames) * 100;
            exportProgressFill.style.width = pct + '%';
            exportProgressPercent.textContent = pct.toFixed(0) + '%';
            
            // Run next block
            setTimeout(renderExportFrame, 5); // Speed up export rendering faster than realtime
        };

        renderExportFrame();
    });

    // ==========================================
    // 8.5 MARKETING CAMPAIGNS & COPYWRITING PRESETS (1000-DAY LIFECYCLE)
    // ==========================================
    const campaignPresets = [
        { day: 1, title: "BUSCANDO UN GARAJE", subtitle: "Llamando en frío a dueños de locales en Móstoles.", template: "budget-ticker", color: "#ffff00", music: "techno" },
        { day: 5, title: "EL ACUERDO DE PERMUTA", subtitle: "Trueque de publicidad en YouTube por espacio de taller.", template: "budget-ticker", color: "#39ff14", music: "synthwave" },
        { day: 12, title: "DISEÑO DE CHASSIS 3D", subtitle: "Modelado Onshape CAD tubular completo.", template: "telemetry-hud", color: "#00e5ff", music: "techno" },
        { day: 25, title: "EL MOCKUP DE MADERA", subtitle: "Prototipo escala 1:1 para validar ergonomía.", template: "minimal-orbit", color: "#ffffff", music: "lofi" },
        { day: 40, title: "ENERGÍA TALLER: 5.5 kW", subtitle: "Limitación de potencia contratada para soldadura.", template: "telemetry-hud", color: "#ff007f", music: "techno" },
        { day: 60, title: "COMPRANDO EL EMRAX 228", subtitle: "Firma de alianzas para el motor de flujo axial.", template: "budget-ticker", color: "#00e5ff", music: "synthwave" },
        { day: 90, title: "PREPARACIÓN MESA JIG", subtitle: "Nivelado láser micrométrico de perfiles de acero.", template: "minimal-orbit", color: "#ffffff", music: "lofi" },
        { day: 110, title: "CORTANDO CROMOLY 4130", subtitle: "Corte y biselado con notcher CNC en taller.", template: "fea-stress", color: "#ffff00", music: "techno" },
        { day: 130, title: "PURGA INTERNA DE ARGÓN", subtitle: "Llenado de tubos para evitar óxido interno.", template: "fea-stress", color: "#39ff14", music: "techno" },
        { day: 150, title: "SOLDADURA TIG INICIADA", subtitle: "Uniendo las juntas con varilla de aporte ER70S-6.", template: "fea-stress", color: "#ff007f", music: "techno" },
        { day: 180, title: "ENSAMBLANDO CELDAS 18650", subtitle: "Soldadura por puntos CNC de pack acumulador.", template: "telemetry-hud", color: "#39ff14", music: "synthwave" },
        { day: 200, title: "MONTAJE PUSH-ROD", subtitle: "Instalación de trapecios dobles y coilovers.", template: "minimal-orbit", color: "#00e5ff", music: "synthwave" },
        { day: 220, title: "CABLEADO DE CONTROL LV", subtitle: "Mazo de cables ECU y sistema redundante Hall.", template: "telemetry-hud", color: "#ffff00", music: "lofi" },
        { day: 240, title: "SHAKEDOWN EN PISTA", subtitle: "Pruebas de slalom dinámico en aeródromo privado.", template: "minimal-orbit", color: "#39ff14", music: "techno" },
        { day: 260, title: "ENSAYO DE RUIDO R51", subtitle: "Sonómetro a velocidad constante en circuito.", template: "fea-stress", color: "#ffffff", music: "lofi" },
        { day: 280, title: "PRUEBAS DE FRENO R13-H", subtitle: "Eficiencia Wilwood en mojado con IDIADA.", template: "fea-stress", color: "#ff007f", music: "techno" },
        { day: 300, title: "OBTENCIÓN PLACAS CALLE", subtitle: "Matriculación individual (HIV) en España.", template: "minimal-orbit", color: "#39ff14", music: "synthwave" },
        { day: 320, title: "VENTA DE FLAT-PACK KITS", subtitle: "Planos y tubos pre-cortados listos para soldar.", template: "budget-ticker", color: "#ffff00", music: "synthwave" },
        { day: 350, title: "PATREON REVENUE MODEL", subtitle: "MRR recurrente para financiar el desarrollo de EV.", template: "budget-ticker", color: "#00e5ff", music: "lofi" },
        { day: 365, title: "1 AÑO DE BUILDCERO", subtitle: "Resumen de operaciones, comunidad y vlogs.", template: "minimal-orbit", color: "#ff007f", music: "synthwave" }
    ];

    const campaignSelect = document.getElementById('reel-campaign-select');
    if (campaignSelect) {
        campaignPresets.forEach((preset, idx) => {
            const opt = document.createElement('option');
            opt.value = idx;
            opt.textContent = `Día ${preset.day}: ${preset.title}`;
            campaignSelect.appendChild(opt);
        });

        campaignSelect.addEventListener('change', () => {
            const selectedIdx = campaignSelect.value;
            if (selectedIdx !== "") {
                const preset = campaignPresets[selectedIdx];
                document.getElementById('reel-day').value = preset.day;
                document.getElementById('reel-title').value = preset.title;
                document.getElementById('reel-subtitle').value = preset.subtitle;
                document.getElementById('reel-template').value = preset.template;
                document.getElementById('reel-neon-color').value = preset.color;
                document.getElementById('reel-music-beat').value = preset.music;
                // Force dispatch change events
                const evTemplate = new Event('change');
                document.getElementById('reel-template').dispatchEvent(evTemplate);
            }
        });
    }

    // ==========================================
    // 9. ENGINE BOOTSTRAP
    // ==========================================
    initBOM();
    initThreeJS();
});
