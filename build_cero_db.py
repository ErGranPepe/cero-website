import os
import json

def get_db():
    db = {}
    
    # ----------------------------------------------------
    # CARPETA 00: GOBERNANZA Y ESTRATEGIA (OPERATIVO & COMUNIDAD)
    # ----------------------------------------------------
    
    db["DOC-001"] = {
        "category": "00_Gobernanza_y_Estrategia",
        "title": "Foundational Manifest",
        "subtitle": "Declaración de Principios, Visión y Reglas de Coordinación",
        "author": "Fundadores de CERO",
        "status": "APROBADO",
        "version": "v16.0",
        "date": "15.07.2026",
        "sections": [
            ["1. La Misión Fundamental de CERO", 
             "CERO es el primer coche de calle del mundo desarrollado 100% en abierto por internet. Sin fábrica física de nuestra propiedad, sin capital de partida, y coordinando colaboradores de forma de comunidad descentralizada. El coche de CERO se concibe como un diseño abierto y homologable en Europa, permitiendo que cualquiera descargue sus planos y los replique de manera local. Queremos romper las barreras de entrada de la industria de automoción tradicional.\n\n"
             "Tradicionalmente, diseñar un coche exige millones de euros, laboratorios privados y equipos cerrados. CERO demuestra que la inteligencia colectiva y la transparencia radical pueden coordinar talento de manera descentralizada para fabricar un vehículo real, homologable y de alto rendimiento. No aspiramos solo a construir un coche rápido, sino a crear el plano de libertad definitivo para que cualquier aficionado al motor pueda replicar la construcción física en su entorno local con recursos modestos. El proyecto no tiene fines puramente lucrativos en su fase inicial. Nace como un grito de guerra tecnológico contra la sobre-regulación y el hermetismo industrial que ha destruido la figura del constructor aficionado (car builder) en Europa.\n\n"
             "Queremos democratizar la ingeniería automotriz, permitiendo que estudiantes de universidades de todo el mundo, soldadores experimentados de talleres locales y entusiastas de internet colaboren hombro con hombro en una plataforma compartida. CERO es la prueba de que un grupo de desconocidos en internet, coordinados mediante herramientas gratuitas y principios claros, puede fabricar una máquina física que cumpla con los estándares de seguridad vial europeos más exigentes. La meta es demostrar que el código abierto es tan aplicable a la ingeniería física pesada como al desarrollo de sistemas de software."],
            ["2. Principios de Bootstrapping y Apertura",
             "• Transparencia Radical: Todo el trabajo se realiza en público. Las simulaciones, el software, las actas de reuniones y las finanzas son de acceso libre en el repositorio. No existen secretos industriales ni patentes ocultas; cada render, cada fallo en las soldaduras y cada céntimo gastado se publican de forma inmediata en GitHub, garantizando la confianza de mecenas e ingenieros colaboradores.\n\n"
             "• Acción Verificable: Una idea teórica no tiene valor si no está acompañada de una simulación matemática, un modelo CAD o un prototipo físico probado. Los debates en Discord se resuelven mostrando datos objetivos y resultados numéricos, no opiniones subjetivas o rangos de antigüedad.\n\n"
             "• Colaboración Desinteresada Inicial: Priorizamos a los ingenieros que buscan crear un portfolio real o que participan por entusiasmo técnico. Compensamos su tiempo mediante un reparto de equity (stock options) en la futura S.L. una vez constituida de forma oficial, permitiendo una alineación de intereses a largo plazo.\n\n"
             "• Financiación Comunitaria ex-ante: No gastamos dinero propio de los fundadores. Los gastos de caja (compra de materiales, sensores, consumibles o gestiones viales) se pagan exclusivamente con la caja acumulada del Patreon de la comunidad, lanzado en el Mes 4, asegurando que el proyecto dependa del interés social real para seguir avanzando. Si el público no valida la idea con su mecenazgo, el proyecto no consume recursos personales."],
            ["3. Criterios de Éxito a Largo Plazo",
             "Establecer la viabilidad del open-source en el sector automotriz físico. Demostrar que un coche diseñado colectivamente puede superar las pruebas de emisiones, ruido e impacto de la ITV individual en España, creando un precedente mundial para constructores aficionados. El éxito se medirá cuando el primer chasis soldado circule de forma legal con placas de matrícula ordinarias, con planos Onshape 100% validados por la comunidad.\n\n"
             "Además, el proyecto busca sentar cátedra en el desarrollo de hardware físico distribuido. Queremos que la metodología CERO (diseño CAD modular, validación FEA colaborativa, purga interna de argón en soldadura tubular y sourcing mediante barter comercial) sea replicada por otros equipos para fabricar motocicletas, tractores, maquinaria agrícola o incluso sistemas de movilidad urbana limpia, demostrando la madurez del código abierto en el mundo físico. El fin último es la creación de un ecosistema descentralizado de manufactura local bajo demanda."]
        ]
    }
    
    db["DOC-002"] = {
        "category": "00_Gobernanza_y_Estrategia",
        "title": "Strategic Plan",
        "subtitle": "Plan de Negocio a 28 Meses y Modelo Operativo",
        "author": "Dirección Estratégica CERO",
        "status": "APROBADO",
        "version": "v16.0",
        "date": "15.07.2026",
        "sections": [
            ["1. Horizonte y Fases de Ejecución", 
             "El proyecto se extiende a 28 meses para incorporar de forma segura la fase de homologación de calle en España (ITV individual):\n\n"
             "• Fase 1 (Mes 1-3): Lanzamiento, reclutamiento y captación de talento en LinkedIn y Discord. Fase puramente conceptual centrada en la narrativa, la estructura de la comunidad y la búsqueda del garaje físico local. Se congelan las dimensiones generales preliminares del monoplaza.\n"
             "• Fase 2 (Mes 4-6): Búsqueda activa de local o garaje y lanzamiento del Patreon oficial. Modelado CAD conceptual del chasis y cockpit en Onshape. Se inician las simulaciones de ergonomía y colocación de mandos.\n"
             "• Fase 3 (Mes 7-12): Fabricación del prototipo de madera (mockup) a escala 1:1 en el garaje para validar físicamente la ergonomía del piloto (percentil 95) en Onshape. Ingeniería de detalle y simulaciones FEA/CFD en abierto. Obtención final del garaje mediante canje o alquiler básico.\n"
             "• Fase 4 (Mes 13-18): Alianzas y soldadura del chasis tubular en el garaje o taller colaborador. Se adquieren los tubos de acero cromoly 4130 mediante patrocinio y se fabrica la mesa jig de soldadura.\n"
             "• Fase 5 (Mes 19-21): Montaje del tren motriz, cableado básico, suspensión, dirección y doble circuito de frenos Wilwood. Colaboración estrecha con los ingenieros para la integración del sistema.\n"
             "• Fase 6 (Mes 22-24): Fabricación de la carrocería final de composite y pruebas dinámicas de slalom y frenado en pista privada o aeródromo cerrado.\n"
             "• Fase 7 (Mes 25-28): Pruebas en laboratorios oficiales IDIADA/INTA y matriculación ordinaria para vías públicas de España."],
            ["2. Modelo de Financiación Mixto", 
             "Operación inicial con 0€ basándose en sponsors y canjes de publicidad. La compra de los componentes del coche se financia con la caja acumulada del Patreon de la comunidad, lanzado en el Mes 4. Todo incremento de costes imprevisto en los ensayos mecánicos se cubrirá mediante campañas especiales de merchandising o crowdfunding. El Core Team no realizará aportaciones de capital de su propio bolsillo, asegurando la sostenibilidad del bootstrapping puro durante toda la fase de desarrollo virtual. La estrategia comercial se centra en asociar marcas de componentes (frenos, amortiguadores, llantas, herramientas) que busquen visibilidad en la serie de vlogs y redes sociales del proyecto."],
            ["3. Plan de Contingencia y Rutas Alternativas", 
             "Si en el Mes 12 la recaudación es insuficiente para la compra de materiales, se retrasará el encargo del corte de tubos cromoly, extendiendo el diseño CAD virtual y lanzando retos adicionales de patrocinio en redes viales. El diseño virtual continuará optimizándose en Onshape, realizando más iteraciones en OpenFOAM.\n\n"
             "En caso de que un taller colaborador retire el espacio físico cedido para el montaje del chasis tubular, se activará el Plan B: trueque comercial con institutos de formación profesional mecánica en la zona sur de Madrid, ofreciéndoles acceso directo a los planos de ingeniería para sus asignaturas prácticas de soldadura y automoción a cambio del uso de sus instalaciones durante los fines de semana. Si el motor seleccionado inicialmente resulta muy costoso, se estudiará la pivotación a un motor síncrono de imanes comerciales alternativo, rediseñando la placa adaptadora del diferencial con el equipo técnico."]
        ]
    }
    
    db["DOC-003"] = {
        "category": "00_Gobernanza_y_Estrategia",
        "title": "Master Roadmap",
        "subtitle": "Hitos, Entregables y Dependencias Críticas",
        "author": "Gestión de Proyectos CERO",
        "status": "APROBADO",
        "version": "v16.0",
        "date": "15.07.2026",
        "sections": [
            ["1. Cronograma de Hitos (Master Gantt)", 
             "El desarrollo del vehículo se organiza en un cronograma lineal de 28 meses. Las dependencias críticas son el escaneo 3D del motor y del inversor elegidos por los ingenieros antes de cerrar el CAD trasero del chasis, y el diseño de aristas según normativa peatonal para el dossier IDIADA/INTA. Cada retraso en una fase de diseño afectará directamente al inicio del ensamblaje físico en el taller colaborador. La planificación se ha estructurado con amortiguadores temporales (buffers) de 15 días entre fases críticas para mitigar demoras en el suministro de metalurgia. La ruta crítica pasa obligatoriamente por el congelado del diseño de suspensión y dirección, ya que sus anclajes dictan la triangulación del chasis delantero."],
            ["2. Gráfico del Gantt de Desarrollo", "A continuación se ilustra gráficamente la planificación temporal y fases del proyecto:"],
            ["3. Tabla de Puertas de Control (Gates)", "A continuación se dejan indicadas las fases y entregables clave del roadmap:"]
        ],
        "image": "project_timeline_gantt.png",
        "table": {
            "cols": [50, 60, 200, 80, 114],
            "data": [
                ["Hito", "Fase", "Entregable Clave", "Límite", "Estado"],
                ["MS-0", "Fase 1", "Freeze de Requerimientos Técnicos Básicos y Búsqueda de Garaje", "Mes 3", "Completado"],
                ["MS-1", "Fase 2", "Diseño Conceptual CAD en Onshape y Lanzamiento Patreon", "Mes 6", "En Progreso"],
                ["MS-2", "Fase 3", "Prototipo de Madera 1:1 (Mockup) y Cierre de Alianzas", "Mes 12", "Planificado"],
                ["MS-3", "Fase 4", "Adquisición y Ensamblaje de Chasis Tubular en Garaje", "Mes 18", "Planificado"],
                ["MS-4", "Fase 5", "Integración Tren Motriz y Cableado de Control V1", "Mes 21", "Planificado"],
                ["MS-5", "Fase 6", "Lanzamiento de Prototipo y Pruebas en Pista", "Mes 24", "Planificado"],
                ["MS-6", "Fase 7", "Dossier IDIADA / INTA y Obtención de Placas de Calle", "Mes 28", "Planificado"]
            ]
        }
    }
    
    db["DOC-004"] = {
        "category": "00_Gobernanza_y_Estrategia",
        "title": "Operating System",
        "subtitle": "Estructura de la Organización de Internet y Canales de Comunicación",
        "author": "Operaciones CERO",
        "status": "APROBADO",
        "version": "v16.0",
        "date": "15.07.2026",
        "sections": [
            ["1. Estructura de Trabajo Abierta", 
             "El proyecto opera mediante un núcleo (Core Team) y comisiones de voluntarios coordinadas en Discord y GitHub. No existen rangos jerárquicos corporativos clásicos; las aportaciones técnicas registradas en el repositorio otorgan el estatus de colaborador activo. Esto fomenta una meritocracia técnica pura donde las mejores ideas se validan en CAD de forma colegiada y transparente, evitando atascos burocráticos. La gobernanza busca descentralizar el desarrollo de ingeniería mientras mantiene un núcleo fuerte responsable de las operaciones de taller físico y marketing."],
            ["2. Canales Oficiales y Protocolos de Comunicación", 
             "• Discord: Debates rápidos y reuniones de voz dominicales. Canales específicos para cada subsistema del coche (chasis, suspensión, aero, baterías, contenido).\n"
             "• GitHub: Control de versiones de planos Onshape (enlaces y archivos CAD) e informes técnicos. Todos los documentos Markdown oficiales residen en la raíz del proyecto.\n"
             "• Web (buildcero.com): Landing de captación y data room. Acceso rápido a renders en 3D para patrocinadores e inversores.\n"
             "• Frecuencia de Reuniones: Asamblea general los domingos a las 20:00 CEST en Discord. Reuniones técnicas ad-hoc los miércoles. Todo el progreso se documenta mediante actas semanales publicadas en abierto."],
            ["3. Embudo de Crecimiento y Conversión Comunitaria", "A continuación se muestra gráficamente cómo convertimos espectadores casuales en colaboradores del proyecto:"],
            ["4. Diagrama de Roles y Organización del Discord", "A continuación se ilustra la hierarquía de roles y responsabilidades en Discord:"],
            ["5. Matriz RACI Básica", "A continuación se presenta la matriz RACI del equipo CERO:"]
        ],
        "image": "growth_funnel.png",
        "table": {
            "cols": [150, 70, 70, 70, 70, 70],
            "data": [
                ["Actividad / Hito", "ENG (Ing.)", "MED (Medios)", "PART (Alian.)", "LEG (Legal)", "GOV (Gob.)"],
                ["Requerimientos", "A", "C", "I", "C", "R"],
                ["Diseño CAD", "R", "I", "C", "I", "A"],
                ["Vídeos YouTube", "I", "R", "C", "I", "A"],
                ["Contratos IP", "I", "I", "C", "R", "A"]
            ]
        }
    }
    
    db["DOC-017"] = {
        "category": "00_Gobernanza_y_Estrategia",
        "title": "Weekly Review System",
        "subtitle": "Metodología de Reunión y Plantilla de Estado de Operaciones",
        "author": "Operaciones CERO",
        "status": "APROBADO",
        "version": "v16.0",
        "date": "15.07.2026",
        "sections": [
            ["1. Metodología Semanal de Sincronización", 
             "Las reuniones del equipo Core y colaboradores clave se celebran todos los domingos a las 20:00 CEST en el canal de voz de Discord. La asamblea está limitada estrictamente a 45 minutos. Cada coordinador dispone de un máximo de 3 minutos para reportar sus avances, bloqueos y planes. Las notas se suben a GitHub de forma inmediata para mantener el historial del proyecto accesible de forma transparente.\n\n"
             "El objetivo es evitar discusiones de diseño prolongadas durante la reunión de estado. Si surge una discrepancia técnica sobre un nudo de suspensión o un soporte de freno, se agenda una reunión específica (breakout room) entre los ingenieros de esa comisión para el miércoles por la tarde, manteniendo la asamblea dominical enfocada puramente en operaciones, marketing y hitos del Gantt."],
            ["2. Plantilla de Reporte y Semáforo de Riesgo", 
             "• KPIs de Tracción (Cuentas de Discord, followers en Instagram, suscriptores en Patreon, visualizaciones del vlog de YouTube).\n"
             "• Hitos del CAD (Avances en suspensiones, ergonomía del cockpit, triangulación del chasis en Onshape).\n"
             "• Bloqueos Críticos (Sponsors silenciados, retraso en sourcing de piezas, dudas de diseño de cara a la ITV, estado de búsqueda de garaje).\n"
             "• Semáforo de Hito: Verde (En tiempo), Amarillo (Con riesgo de retraso menor de 7 días), Rojo (Bloqueado, requiere intervención de soldadores/ingenieros de forma urgente)."],
            ["3. Planificación de Tareas Semanales y Asignación", 
             "Cada tarea abierta en Discord recibe un responsable único y un deadline de 7 días. Si la tarea no se completa o no se reporta en la asamblea dominical sin causa justificada, se reasigna a otro voluntario técnico para evitar atascos en la ruta crítica del desarrollo conceptual del monoplaza. El historial de cumplimiento se almacena en el Data Room para evaluar la participación de cara a la asignación de stock options de la futura S.L."]
        ]
    }
    
    db["DOC-018"] = {
        "category": "00_Gobernanza_y_Estrategia",
        "title": "Decision Register",
        "subtitle": "Protocolo de Registro y Aprobación de Decisiones Críticas",
        "author": "Comité de Gobernanza CERO",
        "status": "APROBADO",
        "version": "v16.0",
        "date": "15.07.2026",
        "sections": [
            ["1. Protocolo de Registro de Decisiones de Arquitectura (ADR)", 
             "Toda decisión que altere de forma permanente las dimensiones físicas, especificaciones mecánicas o distribución de costes de CERO debe documentarse formalmente como un Architecture Decision Record (ADR) en el repositorio GitHub. Esto previene la pérdida de contexto cuando se incorporen nuevos colaboradores técnicos. Cada archivo ADR debe detallar el contexto del problema, las alternativas analizadas (con sus ventajas e inconvenientes) y la decisión final adoptada junto con la firma de los ingenieros involucrados."],
            ["2. Proceso de Votación y Desbloqueo de Discrepancias", 
             "El debate técnico se abre durante 72 horas en el canal de Discord correspondiente. Cada propuesta debe estar sustentada en simulaciones FEA, datos de coste o requerimientos de ITV. Si no existe consenso al cabo del plazo, el Lead Engineer ostentará el voto de calidad para desbloquear el avance técnico del chasis. Esto garantiza que el diseño avance de forma ágil sin entrar en bucles de discusión interminables."],
            ["3. Criterios de Aprobación Financiera y Gestión de Caja", 
             "Las decisiones de gasto de caja superiores a 50€ requieren la aprobación por mayoría del Core Team de la asociación cultural. Queda prohibida la realización de compras individuales con fondos de la comunidad sin previa publicación del acuerdo y su respectivo registro en el archivo de decisiones críticas del proyecto, manteniendo un control contable estricto ante los mecenas de Patreon."]
        ]
    }
    
    db["DOC-025"] = {
        "category": "00_Gobernanza_y_Estrategia",
        "title": "Critical Project Audit and Risk Analysis",
        "subtitle": "Auditoría de Viabilidad y Análisis Crítico del Ecosistema de Proyecto",
        "author": "Dirección Estratégica CERO",
        "status": "APROBADO",
        "version": "v16.0",
        "date": "15.07.2026",
        "sections": [
            ["1. Bucle de Muerte de la Tracción de 0€", 
             "En el día 1, proponer canjes de branding con 0 seguidores es inviable. Debemos concentrar el Mes 1-3 en ganar visibilidad técnica compartiendo diseños y simulaciones impactantes antes de contactar con patrocinadores. Si intentamos conseguir tubos de acero cromoly o espacio en talleres sin un canal de YouTube con tracción, la tasa de rechazo será del 100%. La estrategia pasa por crear expectación compartiendo el proceso de diseño en redes antes de realizar llamadas de sourcing físico."],
            ["2. Riesgo de Falta de Espacio Físico (Garaje)", 
             "El montaje físico no puede iniciarse sin un local seguro. El riesgo de no encontrar un taller colaborador o garaje asequible se mitiga mediante un plan de trueque publicitario con escuelas de Formación Profesional o pequeños talleres locales en Móstoles que busquen visibilidad online. Si fallan las negociaciones, se retrasará la compra de materiales físicos y se extenderá la fase de diseño CAD virtual en Onshape, minimizando el burn-rate de caja."],
            ["3. Logística Oculta y Gastos Hormiga", 
             "Radial, gases TIG, discos, furgoneta de transporte y tornillería sumarán unos 300-600€ el primer año. Se financiarán con la caja de Patreon del Mes 4, prohibiendo compras grandes hasta cubrir consumibles. Es común que los proyectos amateur fracasen por subestimar estos gastos hormiga (discos de amoladora, varillas de aporte, gas argón, tornillería estructural grado 8.8), consumiendo el presupuesto antes de comprar las piezas principales del monoplaza."]
        ]
    }
    
    db["DOC-026"] = {
        "category": "00_Gobernanza_y_Estrategia",
        "title": "Competitor Analysis",
        "subtitle": "Benchmark del Mercado de Monoplazas y Proyectos de Internet",
        "author": "Dirección Estratégica CERO",
        "status": "APROBADO",
        "version": "v16.0",
        "date": "15.07.2026",
        "sections": [
            ["1. Precedentes Históricos y Lecciones", 
             "• Project Binky: Tardaron 10 años por no delegar en la comunidad. Su perfeccionismo artesanal retrasó el montaje. CERO usará Onshape público para diseño colaborativo y modular para acelerar el desarrollo.\n"
             "• Wesley Kagan: Demostró la viabilidad de coches F1 clásicos en 18 meses liberando el CAD. CERO aplicará este dinamismo de prototipado rápido pero adaptando el chasis a normativas de calle desde el día 1.\n"
             "• Wikispeed: Demostraron rapidez ágil pero fallaron en homologación. CERO integra el plan de ITV individual y asesores de laboratorios oficiales españoles desde el inicio. El diseño ágil debe ir de la mano con el cumplimiento legal."],
            ["2. Propuesta de Valor Única (USP)", 
             "CERO es el primer coche de calle del mundo desarrollado con código abierto e internet, permitiendo la co-creación real de su chasis y tren motriz por parte de aficionados e ingenieros. La combinación de una narrativa audiovisual atractiva en YouTube con un desarrollo de ingeniería transparente y de comunidad nos posiciona como un proyecto único en el sector automotriz global, abriendo un canal directo de conversión comunitaria."]
        ]
    }
    
    db["DOC-028"] = {
        "category": "00_Gobernanza_y_Estrategia",
        "title": "Technical Vision",
        "subtitle": "Especificación Técnica General del Chasis, Materiales y Soldadura",
        "author": "Ingeniería CERO",
        "status": "APROBADO",
        "version": "v16.0",
        "date": "15.07.2026",
        "sections": [
            ["1. Requerimientos del Chasis Tubular", 
             "Adopción de estándares FSAE (Formula Student):\n"
             "• Arco Principal (Main Hoop): Acero cromoly 4130, diámetro exterior de 25.4mm y espesor de pared de 2.0mm. Asegura la jaula de seguridad del piloto.\n"
             "• Diagonales y Tirantes: Acero 4130, 25.0mm x 1.2mm. Brindan rigidez estructural contra torsión torsional.\n"
             "• Dimensionamiento Ergonómico: El cockpit se diseñará en Onshape para alojar a pilotos de hasta el percentil 95 de estatura (1.90 m), asegurando espacio holgado para el casco y las piernas.\n"
             "• El chasis debe resistir fuerzas de torsión estática de hasta 1.800 Nm por grado de flexión angular, validados por simulaciones numéricas (FEA)."],
            ["2. Control de Soldadura y Homologación de Soldadores", 
             "Todos los soldadores voluntarios deben soldar un cupón de prueba de acero 4130. Este cupón se enviará a ensayos de tracción en laboratorio. Solo los soldadores aprobados podrán soldar la jaula de seguridad del chasis físico, garantizando la integridad de las juntas bajo cargas extremas. Se realizarán inspecciones con líquidos penetrantes en taller para validar la ausencia de poros en la raíz de la soldadura."],
            ["3. Comparativa de Resistencia Estructural", "A continuación se muestra la resistencia elástica (MPa) del acero cromoly 4130 seleccionado frente al acero dulce estándar:"],
            ["4. Mapa de Tensiones FEA de la Estructura de Chasis", "A continuación se presenta el mapa de tensiones estructurales en 3D del chasis obtenido mediante simulación estática por el resolvedor de elementos finitos de CERO, demostrando la deformación y áreas de distribución de carga Von Mises bajo impacto frontal de 5G:"]
        ],
        "image": "chassis_fea.png"
    }

    # ----------------------------------------------------
    # CARPETA 01: PRODUCTO E INGENIERÍA (CONCEPTUAL & PROCESOS)
    # ----------------------------------------------------
    
    db["DOC-005"] = {
        "category": "01_Producto_e_Ingenieria",
        "title": "Product Requirements Document",
        "subtitle": "Ficha de Requerimientos ITV de Calle, Ergonomía y Homologación",
        "author": "Ingeniería CERO",
        "status": "APROBADO",
        "version": "v16.0",
        "date": "15.07.2026",
        "sections": [
            ["1. Filosofía de Ingeniería y Sistemas Automotrices", 
             "El documento de requerimientos de producto (PRD) de CERO se ha estructurado bajo los estándares de ingeniería de sistemas de la NASA (NASA Systems Engineering Handbook, SP-2016-6105). El objetivo es diseñar, simular y fabricar un vehículo monoplaza de calle con un coste de adquisición inicial de 0€, optimizando al límite el peso estructural y la rigidez torsional.\n\n"
             "El monoplaza debe combinar la agilidad en curva de un kart de competición con el cumplimiento estricto de los requisitos legales del Reglamento General de Vehículos en España y las directivas de homologación individual de la Unión Europea (Reglamento UE 2018/858)."],
            ["2. Especificaciones de Sistemas Dinámicos y Mecánicos",
             "• Chasis Tubular: Estructura espacial triangulada (spaceframe) fabricada en tubos de acero aleado al cromo-molibdeno 4130. El arco principal de seguridad antivuelco (Main Hoop) tendrá un diámetro de 25.4 mm y un espesor de pared mínimo de 2.0 mm, dimensionado para alojar un piloto del percentil 95 (1.90 m de altura).\n"
             "• Suspensión Cinemática: Configuración de doble trapecio independiente (double wishbone) delantero y trasero. Brazos fabricados en tubo 4130, unidos mediante rótulas esféricas de competición (uniball) de rosca métrica fina grado automotriz. Amortiguación ajustable montada con sistema de bieletas push-rod para optimizar el ratio de movimiento y el control de balanceo.\n"
             "• Sistema de Frenado Independiente: Pinzas de doble pistón opuesto y discos ventilados. El pedalier de competición incluirá dos bombas de freno independientes conectadas mediante una barra de equilibrio (bias bar) mecánica ajustable en cabina. Esto garantiza el doble circuito independiente exigido por ley: si ocurre una fuga en el circuito delantero, el circuito trasero retiene capacidad de frenado estática superior al 45%."],
            ["3. Tren Motriz Eléctrico e Inversor de Tracción (Conceptual)",
             "El coche utilizará un motor eléctrico síncrono de imanes permanentes montado en el subchasis trasero en una zona protegida contra colisiones laterales. La especificación exacta del motor y del inversor de tracción será definida por el equipo de ingenieros y patrocinadores una vez completada la fase conceptual, basándose en la disponibilidad de canje o compra Patreon:\n"
             "• Tipo de Motor: Imanes permanentes de flujo axial, refrigeración líquida.\n"
             "• Par y Potencia de Diseño: Potencia máxima objetivo de 80-100 kW, par máximo de 240 Nm.\n"
             "• Inversor: Controlador trifásico de alta tensión controlado por bus CAN a 500 kbps.\n"
             "• Sistema de Batería: Acumulador de iones de litio encapsulado en un contenedor ignífugo de fibra de carbono y Nomex."],
            ["4. Curva de Potencia y Par del Motor Eléctrico (Conceptual)", "A continuación se ilustra la curva de potencia (hp) y par motor (Nm) en función de las revoluciones por minuto (RPM) proyectada para el bloque motor:"],
            ["5. Distribución de Fuerzas de Frenado Frontal y Trasera", "A continuación se muestra el análisis de distribución de fuerzas hidráulicas de frenado y la línea de adherencia óptima calculada para evitar el bloqueo del eje trasero:"],
            ["6. Requerimientos Legales para Homologación de Calle en España (ITV)",
             "Para la obtención de placas de matrícula ordinarias mediante el proceso de Homologación Individual de Vehículos (HIV):\n\n"
             "• Secuencia de Luces: Integración de luces de posición, cruce, carretera, intermitentes, emergencia, luz de marcha atrás, antiniebla trasera y luz de matrícula con código de homologación europeo 'E' grabado en las lentes.\n"
             "• Seguridad Peatonal (Radios de Curvatura): El exterior de la carrocería de composite (fibra de vidrio) debe ser completamente suave, sin salientes punzantes ni aristas. Todos los radios de curvatura exteriores en superficies expuestas deben ser superiores a 2.5 mm.\n"
             "• Retrovisores: Dos retrovisores exteriores con espejo convexo que permitan un campo de visión horizontal mínimo de 15 metros a una distancia de 10 metros detrás del coche.\n"
             "• Auditoría ex-ante: Se firmará un acuerdo con un laboratorio oficial (como IDIADA o el INTA) para realizar una revisión preliminar de los planos CAD antes de iniciar la fabricación física."]
        ],
        "image": "engine_power_torque_curve.png"
    }
    
    db["DOC-006"] = {
        "category": "01_Producto_e_Ingenieria",
        "title": "Bill of Materials",
        "subtitle": "Lista de Materiales Detallada (BOM) y Presupuesto de Sourcing",
        "author": "Alianzas y Sourcing CERO",
        "status": "APROBADO",
        "version": "v16.0",
        "date": "15.07.2026",
        "sections": [
            ["1. Arquitectura de Sourcing y Logística", 
             "Esta Lista de Materiales (BOM) detalla de manera conceptual cada elemento físico necesario para el montaje final de CERO. Para mantener el modelo estratégico de bootstrapping de 0€, el aprovisionamiento se gestiona mediante tres fuentes:\n\n"
             "• Sourcing por Sponsor (Canje de Branding): Metalúrgicas de acero 4130, talleres CNC de aluminio y marcas de neumáticos.\n"
             "• Caja Acumulada de Patreon (Compra Directa): Compra de motor de tracción, inversor, latiguillos de freno, BMS y celdas de batería.\n"
             "• Consumibles y Adecuación: Herramientas de taller, extintores de CO2 de seguridad para litio, gases de purga argón, varillas de soldadura TIG de aporte (ER70S-6 o ER80S-D2).\n"
             "Toda adquisición se registra de forma pública en el Data Room de inversores (DOC-022) para garantizar traza contable total."],
            ["2. Distribución Presupuestaria Comparativa", "A continuación se muestra de forma visual la distribución de costes y el presupuesto estimado del monoplaza:"],
            ["3. Lista Detallada de Componentes de Ingeniería", "A continuación se presenta la base de datos conceptual de piezas del monoplaza:"]
        ],
        "image": "financial_breakdown.png",
        "table": {
            "cols": [110, 160, 90, 144],
            "data": [
                ["Componente", "Especificación / Modelo", "Coste Caja", "Estrategia Adquisición"],
                ["Motor Eléctrico", "Flujo axial, síncrono, refrigerado por líquido", "3.500 €", "Compra Patreon / Donación"],
                ["Inversor de Tracción", "Controlador trifásico con bus CAN", "2.400 €", "Compra Patreon"],
                ["Tubos Acero 4130", "25.4mm x 2.0mm (50 metros)", "0 €", "Patrocinio de Metalúrgica"],
                ["Doble Pinza Freno", "Pinzas Wilwood / Brembo y discos", "900 €", "Compra Patreon / Sponsor"],
                ["Celdas Batería", "Celdas de iones de litio (pack acumulador)", "1.500 €", "Compra Patreon"],
                ["Sistema BMS", "Battery Management System, CAN", "950 €", "Compra Patreon"],
                ["Extintores y Fuerza", "Adecuación de seguridad e instalación garaje", "350 €", "Compra Patreon Consumibles"],
                ["Kit Luces / Espejos", "Kit luces e-marked calle", "800 €", "Compra Patreon / Sponsors"],
                ["Tasas Homologación", "IDIADA / INTA individual", "2.500 €", "Patrocinadores Corporativos"]
            ]
        }
    }
    
    db["DOC-007"] = {
        "category": "01_Producto_e_Ingenieria",
        "title": "Technical Architecture",
        "subtitle": "Arquitectura Mecánica y Eléctrica del Monoplaza Eléctrico",
        "author": "Ingeniería CERO",
        "status": "APROBADO",
        "version": "v16.0",
        "date": "15.07.2026",
        "sections": [
            ["1. Arquitectura de Sistemas de Tracción Eléctrica (General)", 
             "El tren motriz de CERO utiliza un motor síncrono de imanes permanentes montado en el subchasis trasero. Transmisión directa mediante acoplamiento hacia un diferencial autoblocante, transmitiendo el par a los palieres traseros de acero. El sistema de acumulador de alta tensión (HV) utiliza celdas de litio encapsuladas en un contenedor estructural ignífugo. Un sistema de gestión de baterías (BMS) monitorea constantemente el voltaje de cada celda y su temperatura, comunicándose por bus CAN con el inversor de tracción para limitar la corriente en caso de sobretemperatura. La especificación final de marcas comerciales se cerrará junto con los ingenieros y patrocinadores definitivos."],
            ["2. Geometría de Dirección y Comportamiento Dinámico Ackerman", "A continuación se muestra el análisis geométrico de la dirección Ackerman y su porcentaje de desviación (85% Ackerman) para el comportamiento óptimo de guiado en curva del eje delantero:"],
            ["3. Rigidez de Amortiguación y Ratio de Fuerza de Rueda", "A continuación se ilustra la curva de rigidez de los coilovers en función del recorrido de rueda (mm) y la fuerza aplicada (N):"],
            ["4. Arquitectura de Suspensión y Geometría de Dirección", 
             "Geometría de suspensión de doble trapecio independiente en las 4 ruedas. El diseño cinemático en Onshape optimiza el centro de balanceo (Roll Center) manteniéndolo a 45 mm del suelo en reposo. Manguetas (uprights) delanteras y traseras fresadas por control numérico (CNC) en aluminio aeronáutico para minimizar la masa no suspendida. Brazos de suspensión diseñados con perfiles elípticos aerodinámicos para reducir la resistencia al avance. Cremallera de dirección mecánica directa de kart modificada con 1.5 vueltas de tope a tope, garantizando una respuesta inmediata y precisa. El brazo de dirección incorpora un diseño de Ackerman al 85% para reducir el arrastre de neumáticos en curvas cerradas."],
            ["5. Arquitectura Eléctrica y Gestión Electrónica (ECU)", 
             "Mazo de cables de baja tensión (LV) aligerado de cables innecesarios. La ECU principal de diseño propio gestiona la adquisición de datos, lectura de aceleradores Hall duales redundantes y comunicación con el inversor. Se integra un dispositivo de monitoreo de aislamiento (IMD) que corta la línea de seguridad (Shutdown loop) si detecta una fuga de corriente entre el sistema de alta tensión (HV) y el chasis de baja tensión (LV)."]
        ],
        "image": "steering_geometry_ackermann.png"
    }
    
    db["DOC-008"] = {
        "category": "01_Producto_e_Ingenieria",
        "title": "Manufacturing Plan",
        "subtitle": "Plan de Corte, Soldadura e Integración en Taller Colaborador",
        "author": "Ingeniería CERO",
        "status": "APROBADO",
        "version": "v16.0",
        "date": "15.07.2026",
        "sections": [
            ["1. Construcción de la Bancada de Soldadura (Jig)", 
             "Para evitar cualquier distorsión térmica o desalineación milimétrica de la estructura del chasis durante la soldadura, es obligatorio fabricar una bancada de soldadura (jig) rígida de acero.\n\n"
             "La bancada se fabricará utilizando perfiles de acero dulce estructural de 80 mm x 40 mm x 4 mm, atornillados al suelo nivelado del taller. Se soldarán soportes ajustables para sujetar en su posición teórica exacta los nudos de suspensión delantera, soportes de motor y el arco antivuelco principal antes de realizar las soldaduras definitivas. La nivelación de la mesa jig se comprobará mediante nivel láser micrométrico, admitiéndose una desviación máxima de 0.2 mm por metro lineal."],
            ["2. Proceso de Soldadura TIG de Tubos de Cromoly 4130", 
             "El acero cromoly 4130 requiere soldadura TIG de alta precisión para evitar la formación de microfisuras debido al enfriamiento rápido:\n\n"
             "• Preparación de Juntas: Todos los extremos de los tubos deben biselarse con una notcher de tubo a un ajuste perfecto sin holguras (>0.5 mm de hueco invalidará la junta). Se eliminará la capa de calamina y óxido mediante cepillo de acero inoxidable.\n"
             "• Purga Interna: Llenado del interior del tubo con gas argón al 99.9% durante la soldadura para evitar la oxidación interna (back-purging). El caudal de purga se mantendrá entre 2 y 5 PSI.\n"
             "• Parámetros de Soldadura: Corriente continua con electrodo de tungsteno al 2%, varilla de aporte ER70S-6 o ER80S-D2 de 1.6 mm. Enfriamiento lento controlado mediante mantas térmicas ignífugas para evitar tensiones estructurales internas residuales. Queda prohibido enfriar las soldaduras con aire comprimido o agua."],
            ["3. Ensamble de Acumulador de Baterías", 
             "Las celdas de batería se soldarán por puntos utilizando una soldadora de pulso controlado de precisión y tiras de níquel de espesor adecuado. Queda estrictamente prohibido soldar celdas con soldador de estaño convencional, ya que el calor excesivo daña los separadores internos de la celda, provocando cortocircuitos térmicos."]
        ]
    }
    
    db["DOC-009"] = {
        "category": "01_Producto_e_Ingenieria",
        "title": "Quality and Testing Protocol",
        "subtitle": "Ensayos No Destructivos, Dinámicos y Certificaciones en Pista",
        "author": "Ingeniería CERO",
        "status": "APROBADO",
        "version": "v16.0",
        "date": "15.07.2026",
        "sections": [
            ["1. Ensayos No Destructivos de Soldaduras (NDT)", 
             "Todas las uniones soldadas del arco de seguridad y soportes de suspensión se someterán a inspección visual y ensayos por líquidos penetrantes (norma UNE-EN ISO 3452-1) en taller. Se aplicará el limpiador, luego el penetrante de contraste rojo durante 15 minutos, y finalmente el revelador blanco. Cualquier defecto de soldadura obligará a amolar y resoldar la junta de forma inmediata. Se realizará una prueba de resistencia de aislamiento aplicando tensión continua de seguridad entre el bus de alta tensión (HV) y el chasis metálico (LV), verificando la ausencia de fugas."],
            ["2. Gráfico de Física y Dinámica Lateral en Pista", "A continuación se presentan los resultados del ensayo dinámico de slalom de CERO, mostrando la trayectoria XY y el perfil de aceleración lateral en fuerzas G:"],
            ["3. Protocolo de Pruebas Dinámicas en Circuito Cerrado", 
             "Pruebas de validación en circuito privado antes de iniciar el dossier de homologación de calle:\n\n"
             "• Test de Slalom: Slalom a 40 km/h, 60 km/h and 80 km/h con telemetría de acelerómetros para verificar balanceo lateral, transferencias de peso y rigidez cinemática de los trapecios. Se comprobará que la frecuencia natural de balanceo se mantiene dentro de los límites calculados en Onshape.\n"
             "• Ensayo de Frenado de Emergencia: Detenciones completas consecutivas desde 80 km/h a 0 km/h. Verificación de desvanecimiento (fade) de frenos y ajuste mecánico de la bias bar del pedalier para asegurar que las ruedas delanteras bloquean ligeramente antes que las traseras, evitando trompos dinámicos.\n"
             "• Prueba de Stress de Temperatura de Baterías: Monitorear la temperatura de las celdas de litio durante 30 minutos de rodaje continuo. La temperatura de ninguna celda debe superar los 55°C, activándose el apagado de seguridad del BMS de forma automática si se rebasa dicha cota."]
        ],
        "image": "dynamics_plot.png"
    }

    # ----------------------------------------------------
    # CARPETA 02: RECLUTAMIENTO Y EQUIPO (CONVENIOS & ROLES)
    # ----------------------------------------------------
    
    db["DOC-010"] = {
        "category": "02_Reclutamiento_y_Equipo",
        "title": "Team Roles and Org Chart",
        "subtitle": "Estructura del Equipo Core y Colaboradores de Internet",
        "author": "Gobernanza CERO",
        "status": "APROBADO",
        "version": "v16.0",
        "date": "15.07.2026",
        "sections": [
            ["1. Estructura de Roles de la Comunidad", 
             "La organización de CERO se fundamenta en un equipo de coordinación local (Core Team) y comisiones de ingeniería descentralizadas. El Core Team de Móstoles de la asociación cultural gestiona las relaciones con talleres mecánicos físicos, la búsqueda del garaje y la caja del Patreon. Los colaboradores online aportan planos CAD en Onshape y simulaciones FEA. El Lead Engineer tiene la última palabra sobre el diseño del chasis tubular. Esta estructura garantiza agilidad operativa y control de calidad físico. La toma de decisiones estratégicas se realiza en asamblea de la DAO física, pero la implementación física en el taller recae exclusivamente en los miembros con firma técnica certificada."],
            ["2. Organigrama de Decisiones Técnicas y de Medios", 
             "• Founder/Mario: Coordinación estratégica, edición de vlogs en YouTube, contacto con sponsors, dueños de locales y gestión administrativa de la asociación cultural.\n"
             "• Lead Engineer: Aprobación final de archivos CAD Onshape, supervisión de rigidez estructural y diseño cinemático de suspensión. Valida los cupones de prueba de soldadura.\n"
             "• Sourcing Scouts: Voluntarios de Discord que buscan y catalogan locales comerciales, metalúrgicas de acero 4130 y distribuidores viales.\n"
             "• Moderadores de Discord: Gestión de la comunidad, bienvenida a ingenieros, resolución de conflictos online y organización de asambleas los domingos."],
            ["3. Criterios de Entrada al Core y Roles", 
             "Los ingenieros ganan peso de decisión mediante commits en GitHub o aportaciones al CAD de Onshape. Cualquier miembro que complete tres retos de diseño (challenges) consecutivos recibe invitación automática al Core Team de la DAO física. Los miembros del Core Team firman un pacto de permanencia y cesión de IP de forma innegociable, garantizando la viabilidad legal a largo plazo del monoplaza."]
        ]
    }
    
    db["DOC-011"] = {
        "category": "02_Reclutamiento_y_Equipo",
        "title": "Recruitment Playbook",
        "subtitle": "Estrategias de Reclutamiento en LinkedIn, Foros y Escuelas Técnicas",
        "author": "Operaciones CERO",
        "status": "APROBADO",
        "version": "v16.0",
        "date": "15.07.2026",
        "sections": [
            ["1. Canales de Reclutamiento y Captación de Ingenieros", 
             "La captación de talento en CERO es un proceso activo y estructurado. Dado que operamos bajo un modelo de bootstrapping de 0€, nuestro valor diferencial radica en ofrecer portfolio real, desafíos técnicos complejos y participación (equity) en la futura S.L. Buscamos estudiantes y graduados de Fórmula Student en LinkedIn, simuladores FEA en foros técnicos de Reddit y soldadores experimentados de talleres locales. Estableceremos convenios de prácticas con escuelas técnicas universitarias (ETSII Madrid, UC3M Leganés) para incorporar estudiantes como parte de su Trabajo de Fin de Grado (TFG), aportándoles tutorización y un caso de uso real a cambio de su trabajo de diseño y cálculo en Onshape. El reclutamiento se enfocará de forma prioritaria en ingenieros con conocimientos en sistemas de alta tensión y programación de buses CAN."],
            ["2. Guion de Contacto en LinkedIn", 
             "\"Hola [nombre], soy Mario y estoy construyendo CERO, el primer coche de calle hecho 100% desde internet (0€ iniciales, open-source). He visto tu perfil y tu experiencia en Fórmula Student y encajas perfectamente en nuestra comisión de diseño de suspensión. ¿Te apetece colaborar en un proyecto real? Te adjunto el Manifiesto: [link]. ¿Hablamos 15 minutos?\"\n\n"
             "Este mensaje se adapta según la especialidad del candidato. Si buscamos un especialista en FEA, nos enfocamos en las simulaciones de colisiones del chasis tubular; si es un editor de vídeo, nos centramos en la narrativa cruda del taller y el crecimiento en redes."]
        ]
    }
    
    db["DOC-012"] = {
        "category": "02_Reclutamiento_y_Equipo",
        "title": "Onboarding Guide",
        "subtitle": "Manual de Incorporación del Colaborador y Herramientas del Proyecto",
        "author": "Operaciones CERO",
        "status": "APROBADO",
        "version": "v16.0",
        "date": "15.07.2026",
        "sections": [
            ["1. Manual de Bienvenida del Colaborador", 
             "Bienvenido a CERO. Nuestro objetivo es que realices tu primera aportación al diseño conceptual en menos de 7 días. El primer paso obligatorio es la lectura del Manifiesto Fundacional (DOC-001) para comprender las dinámicas de bootstrapping con 0€, así como la firma del acuerdo de cesión de propiedad intelectual (DOC-023) para proteger el desarrollo open-source. Creemos en la autonomía y la responsabilidad compartida: no esperes órdenes, busca un issue abierto y empieza a proponer soluciones."],
            ["2. Configuración del Workspace Técnico", 
             "• Discord: Regístrate con tu nombre real e indica tu especialidad (CAD, FEA, CFD, soldadura o edición) en el canal #roles. Solicita los permisos técnicos correspondientes.\n"
             "• Onshape: Crea una cuenta gratuita de estudiante o entusiasta. Solicita acceso de edición en el canal #cad-chasis enviando tu email registrado.\n"
             "• GitHub: Clona el repositorio maestro `ErGranPepe/cero-website` para tener acceso a los scripts y documentos Markdown del proyecto. Configura tus credenciales Git locales."],
            ["3. Primer Challenge del Colaborador", 
             "Para validar tus habilidades y concederte permisos de fusión en la rama principal, debes resolver un reto menor. El challenge por defecto consiste en modelar en Onshape el soporte de la pinza de freno trasera respetando los radios de curvatura de aristas obligatorios de 2.5 mm de la ITV. Una vez finalizado, abre una pull request en GitHub o comparte el enlace Onshape en el canal #revision-cad para que el Lead Engineer valide la geometría."]
        ]
    }
    
    db["DOC-013"] = {
        "category": "02_Reclutamiento_y_Equipo",
        "title": "Equity and Compensation Plan",
        "subtitle": "Estructura de Equity de Colaboradores e Incentivos en Sociedad Limitada",
        "author": "Fundadores de CERO",
        "status": "APROBADO",
        "version": "v16.0",
        "date": "15.07.2026",
        "sections": [
            ["1. Reparto de Equity (Stock Options Pool)", 
             "Dado que el desarrollo inicial opera con 0€ de presupuesto, compensamos el tiempo de los ingenieros mediante un pool de stock options equivalente al 15% de las acciones de la futura CERO S.L. Las opciones se devengan mediante un vesting mensual de 12 meses con un cliff inicial de 3 meses para asegurar compromiso real. Esto garantiza que quienes participen activamente tengan una participación real en el valor comercial de los planos y la marca. El reparto de equity se calcula según una matriz de puntos: cada entregable CAD cerrado, simulación aprobada o gestión de sourcing concede puntos de participación. Al constituirse la S.L., los puntos acumulados se transforman en participaciones sociales."],
            ["2. Hitos de Compensación Financiera Directa", 
             "Cuando CERO consiga su primera ronda de inversión pre-semilla de 50.000€, los ingenieros con rol de 'Colaborador Activo' verificado tendrán prioridad absoluta para ser contratados con salario de mercado. El valor de su equity acumulado se respetará de forma íntegra en la constitución legal de la sociedad de capital, permitiendo liquidar una parte en forma de bonus si el inversor lo aprueba."],
            ["3. Registro de Contribuciones Técnicas y Auditoría", 
             "Cada hora de diseño CAD o cálculo FEA reportada y aprobada en las asambleas de Discord dominicales se registra en una hoja de cálculo del Data Room de inversores (DOC-022). Este historial sirve de base para el cálculo proporcional de stock options de cada colaborador al final del año, garantizando transparencia absoluta y evitando disputas sobre el reparto de valor estructural."]
        ]
    }

    # ----------------------------------------------------
    # CARPETA 03: FINANZAS Y LEGAL (ASOCIACIÓN & RUNWAY)
    # ----------------------------------------------------
    
    db["DOC-020"] = {
        "category": "03_Finanzas_y_Legal",
        "title": "Legal Structure",
        "subtitle": "Estructura Legal de Asociación Cultural y Pivotación a Sociedad Limitada",
        "author": "Legal y Cumplimiento CERO",
        "status": "APROBADO",
        "version": "v16.0",
        "date": "15.07.2026",
        "sections": [
            ["1. Constitución de Asociación Inicial y Ventajas", 
             "Para operar legalmente con 0€ y gestionar suscripciones Patreon y donaciones, se constituye la 'Asociación de Ingeniería de Código Abierto CERO' en España. Esta forma jurídica está exenta de IVA en sus cuotas asociativas (Patreon) y permite la firma de contratos de canje de patrocinio (branding por material) de forma legal. La asociación actúa como paraguas legal para evitar riesgos patrimoniales personales a los fundadores durante el desarrollo virtual.\n\n"
             "La asociación abrirá una cuenta bancaria dedicada donde se depositarán todas las cuotas de Patreon y donaciones de patrocinadores, gestionándose con total transparencia pública en las auditorías contables mensuales."],
            ["2. Pivotación Futura a Sociedad Limitada (S.L.)", 
             "En el Mes 18, de cara a la homologación final y comercialización de planos, se constituirá la S.L. aportando los activos intangibles de la asociación (CAD y marca CERO) como aportaciones no dinerarias, activando el plan de equity. La S.L. asumirá todos los derechos y obligations de la asociación, incluyendo los contratos de cesión de IP firmados por los ingenieros, garantizando la continuidad legal del Data Room ante inversores de capital riesgo."],
            ["3. Fiscalidad y Gestión de Exenciones", 
             "Se solicitará la declaración de utilidad pública para la asociación una vez cumplidos los plazos legales, permitiendo que las empresas que donen materiales o coticen como mecenas puedan desgravarse de sus aportaciones en el Impuesto de Sociedades. La gestión fiscal será externalizada a una gestoría colaboradora mediante acuerdo de canje publicitario."]
        ]
    }
    
    db["DOC-021"] = {
        "category": "03_Finanzas_y_Legal",
        "title": "Financial Model",
        "subtitle": "Proyecciones Financieras a 3-5 Años y Presupuestos Viales",
        "author": "Dirección Estratégica CERO",
        "status": "APROBADO",
        "version": "v16.0",
        "date": "15.07.2026",
        "sections": [
            ["1. Modelo Financiero de Caja", "El proyecto asume 0€ el primer mes y acumula caja mediante Patreon (Tier Boceto 2.99€, Tier CAD 5.99€, Tier Core 19.99€). Los gastos reales de compra de materiales y servicios se realizan con la caja acumulada al Mes 12. Las proyecciones contemplan un colchón financiero para cubrir comisiones bancarias y de Stripe, asegurando que el flujo neto sea suficiente para afrontar la compra de consumibles y herramientas de taller."],
            ["2. Crecimiento de Suscripciones y Runrate Recurrente", "A continuación se muestra de manera gráfica la curva de crecimiento del número de mecenas y el runrate de suscripciones acumuladas a lo largo de las fases de diseño virtual:"],
            ["3. Runway de Inversión y Tasa de Gasto (Burn Rate) Pre-Semilla", "A continuación se ilustra la simulación de flujo de caja y la tasa de consumo de capital (runway) proyectada tras asegurar la ronda de financiación pre-semilla de 50.000€:"],
            ["4. Estimaciones Financieras a 3 Años", "A continuación se detallan las proyecciones financieras de la organización:"]
        ],
        "image": "kpi_projections.png",
        "table": {
            "cols": [120, 100, 100, 184],
            "data": [
                ["Fase Proyecto", "Gasto Caja", "Ingreso Patreon", "Estado Financiación"],
                ["Mes 1-3 (Lanzamiento)", "0 €", "0 €", "Caja Cero, sin gastos operacionales"],
                ["Mes 4-12 (CAD & Simul)", "250 € (Gasto)", "3.600 € (Acu)", "Reserva libre de caja de 3.350 € para herramientas"],
                ["Mes 13-24 (Taller & Sold)", "5.500 €", "12.000 €", "Adquisición de acero, soldadura y piezas del prototipo"],
                ["Mes 25-28 (Homologación)", "10.050 € (Total)", "24.000 €", "Pago de tasas IDIADA/INTA y laboratorios oficiales"]
            ]
        }
    }
    
    db["DOC-022"] = {
        "category": "03_Finanzas_y_Legal",
        "title": "Investor Data Room",
        "subtitle": "Estructura de Activos Financieros y Técnicos para Ronda Semilla",
        "author": "Fundadores de CERO",
        "status": "APROBADO",
        "version": "v16.0",
        "date": "15.07.2026",
        "sections": [
            ["1. Organización del Repositorio de Inversores", 
             "El Data Room de inversores se estructura en el repositorio de forma indexada. Contiene los contratos de cesión de IP firmados por cada colaborador (DOC-023), el pacto de socios preliminar (DOC-024) y las proyecciones financieras (DOC-021). Este repositorio se mantiene actualizado de forma mensual por el área de finanzas del Core Team, permitiendo una debida diligencia rápida por parte de fondos de capital semilla.\n\n"
             "La documentación técnica adjunta incluye las simulaciones FEA y los informes de diseño de chasis, aportando confianza sobre la viabilidad física del monoplaza."],
            ["2. Activos Intangibles del Proyecto y Valoración", 
             "• CAD Completo de Suspensión, Chasis y Dirección en Onshape.\n"
             "• Certificados de Simulación Estructural de Torsión (FEA) del chasis.\n"
             "• Marca CERO registrada a nivel europeo en la Oficina de Propiedad Intelectual.\n"
             "• Registros de tracción orgánica en redes: seguidores y mecenas recurrentes en Patreon.\n"
             "La valoración inicial de los intangibles se estima en 60.000€, calculada en base al coste de mercado de las horas de ingeniería aportadas de forma gratuita por la comunidad."],
            ["3. Criterios de Acceso para Inversores Ángeles", 
             "El acceso al Data Room se concede bajo estricto acuerdo de confidencialidad (NDA). Los inversores interesados en la ronda pre-semilla de 50.000€ deben acreditar experiencia previa en automoción, desarrollo de hardware de código abierto o startups industriales antes de recibir acceso completo, buscando un perfil de Smart Money que aporte contactos en la industria de homologación."]
        ]
    }
    
    db["DOC-023"] = {
        "category": "03_Finanzas_y_Legal",
        "title": "Intellectual Property Strategy",
        "subtitle": "Estrategia de Propiedad Intelectual y Licencia Abierta",
        "author": "Legal y Cumplimiento CERO",
        "status": "APROBADO",
        "version": "v16.0",
        "date": "15.07.2026",
        "sections": [
            ["1. Estrategia de Código Abierto CC BY-NC 4.0", 
             "Los planos y simulaciones de CERO se liberan bajo licencia Creative Commons Attribution-NonCommercial 4.0 (CC BY-NC 4.0). Esto permite a entusiastas construir sus propios coches, pero protege comercialmente la marca CERO ante copias industriales sin convenio. Cualquier empresa que desee comercializar kits de montaje del chasis de CERO deberá adquirir una licencia comercial con CERO S.L.\n\n"
             "Esta estrategia equilibra la filosofía de código abierto y compartición de conocimiento con la sostenibilidad financiera del proyecto, reteniendo el Core Team los derechos comerciales para financiar futuras iteraciones del vehículo."],
            ["2. Contratos de Cesión de IP de Colaboradores", 
             "Todos los ingenieros colaboradores deben firmar un documento de cesión de IP en el onboarding de forma digital. Esto garantiza que CERO S.L. posee los derechos de los archivos CAD para poder homologar y fabricar el monoplaza de forma física ante laboratorios estatales sin bloqueos legales por derechos de autor. La firma es un paso previo innegociable para obtener permisos de edición en la rama principal de Onshape o fusiones en el repositorio."]
        ]
    }
    
    db["DOC-024"] = {
        "category": "03_Finanzas_y_Legal",
        "title": "Shareholders Agreement Template",
        "subtitle": "Borrador de Pacto de Socios para Inversores y Colaboradores Core",
        "author": "Legal y Cumplimiento CERO",
        "status": "APROBADO",
        "version": "v16.0",
        "date": "15.07.2026",
        "sections": [
            ["1. Cláusulas de Pacto de Socios de CERO S.L.", 
             "Este borrador regula las relaciones de capital tras la pivotación de la asociación a S.L. en el Mes 18:\n"
             "• Cláusula de Acompañamiento (Tag-Along): Los socios minoritarios (ingenieros colaboradores) tienen derecho a vender sus acciones en las mismas condiciones si los socios mayoritarios venden su participación.\n"
             "• Cláusula de Arrastre (Drag-Along): Si un comprador ofrece adquirir el 100% de CERO, los socios mayoritarios pueden obligar a los minoritarios a vender sus acciones al mismo precio.\n"
             "• Derecho de Adquisición Preferente: Los fundadores tienen prioridad de compra ante la salida de algún colaborador."],
            ["2. Cláusulas de Permanencia y Bad Leaver", 
             "Si un colaborador clave con derecho a stock options decide abandonar el proyecto de forma conflictiva o perjudicial, se le aplicarán penalizaciones financieras. Si abandona antes de cumplir 12 meses (cliff), perderá el 100% de sus opciones acumuladas. Si abandona de forma conflictiva perjudicando el desarrollo del CAD, sus participaciones se valorarán a valor nominal de 1€ (Bad Leaver)."],
            ["3. Protocolo de Resolución de Conflictos y Arbitraje", 
             "Cualquier disputa técnica o corporativa se someterá a mediación en la Corte de Arbitraje de Madrid. Esto previene juicios prolongados que paralicen las homologaciones de calle en IDIADA/INTA, garantizando que el chasis de CERO pueda fabricarse y probarse sin interrupciones legales."]
        ]
    }

    # ----------------------------------------------------
    # CARPETA 04: MARKETING Y CONTENIDO (VLOGS & REDES)
    # ----------------------------------------------------
    
    db["DOC-030"] = {
        "category": "04_Marketing_y_Contenido",
        "title": "Content Strategy and Calendar",
        "subtitle": "Estrategia de Contenido Semanal y Diario de Redes Sociales",
        "author": "Medios y Crecimiento CERO",
        "status": "APROBADO",
        "version": "v16.0",
        "date": "15.07.2026",
        "sections": [
            ["1. Estrategia Social Media y Crecimiento Orgánico", 
             "Producción de 1 vídeo largo semanal en YouTube (avance de operaciones, llamadas a desguaces, soldaduras) y 3-5 clips verticales en TikTok/Reels basados en 'hooks' de taller y debate. Esto generará tracción de seguidores para poder negociar canjes viales y locales comerciales. La narrativa debe enfocarse en el 'Build in Public', mostrando tanto las victorias como los fallos estrepitosos de la búsqueda del garaje y del montaje físico.\n\n"
             "El objetivo de marketing es acumular una base de 10.000 seguidores activos antes del Mes 4, permitiendo que el lanzamiento de Patreon tenga una tasa de conversión de suscripción del 1.5%, generando los primeros ingresos recurrentes para consumibles de taller."],
            ["2. Optimización Aerodinámica Conceptual del Chasis", "A continuación se ilustra la relación aerodinámica de arrastre (Drag) y sustentación negativa (Downforce) simulada a lo largo del chasis del vehículo a alta velocidad:"],
            ["3. Calendario Semanal de Publicación Tipo", 
             "• Lunes: TikTok corto sobre la ergonomía del cockpit o renders conceptuales de Onshape.\n"
             "• Miércoles: Detrás de cámaras en Reels sobre las llamadas de negociación para conseguir el garaje.\n"
             "• Jueves: Hilo técnico o de estrategia en X/LinkedIn (ej. cómo conseguir un garaje gratis mediante canje publicitario).\n"
             "• Sábado: Vídeo largo de YouTube de 10-15 minutos detallando las llamadas en directo, visitas a locales y montaje de la bancada.\n"
             "• Domingo: Asamblea de voz en Discord y votación comunitaria de diseño."]
        ],
        "image": "chasis_aerodynamics_lift_drag.png"
    }
    
    db["DOC-031"] = {
        "category": "04_Marketing_y_Contenido",
        "title": "Video Scripts Library",
        "subtitle": "Librería de Guiones y Estructuras de Vídeo para YouTube",
        "author": "Medios y Crecimiento CERO",
        "status": "APROBADO",
        "version": "v16.0",
        "date": "15.07.2026",
        "sections": [
            ["1. Estructura del Vídeo de YouTube de Lanzamiento (Episodio 1)", 
             "• 0:00 - 1:00: Gancho de alta retención. Mario frente a la cámara en un garaje vacío. 'Voy a construir un coche de carreras real para calle desde 0€ y solo con internet. No tengo taller ni dinero. Os muestro cómo'. Renders rápidos del chasis modular.\n"
             "• 1:00 - 3:00: El problema industrial. El coste prohibitivo de los karts y monoplazas tradicionales, y las trabas burocráticas europeas. La filosofía de código abierto de CERO.\n"
             "• 3:00 - 6:00: Conflicto del espacio. Mario visita tres locales en Móstoles que están en alquiler. Dos agencias le rechazan de inmediato al proponerles un canje de publicidad. Mario comparte su frustración ante la cámara. 'Nadie cree en esto al inicio. Pero vamos a seguir llamando'.\n"
             "• 6:00 - 8:00: La llamada de sourcing. Mario llama en directo a distribuidores de acero para conseguir tubos de cromoly 4130 a coste cero.\n"
             "• 8:00 - 10:00: Llamada a la acción. 'Si eres ingeniero, soldador o tienes un local, únete a Discord en buildcero.com'. Suscríbete."],
            ["2. Episodio 2: Negociando el Garaje y Primeros Planos", 
             "• 0:00 - 1:30: Gancho. '¿Hemos conseguido local? Hoy nos reunimos con el dueño de un taller cerrado para proponerle el trato de su vida'.\n"
             "• 1:30 - 5:00: Visita física al local. Medidas del espacio, discusión sobre la instalación eléctrica trifásica y colocación de la futura mesa jig.\n"
             "• 5:00 - 8:00: Avances de ingeniería. Mostrando los planos Onshape de las suspensiones realizados por colaboradores de Discord.\n"
             "• 8:00 - 10:00: Llamada a la acción: lanzamiento del Patreon oficial para financiar los primeros consumibles del taller."],
            ["3. Episodio 3: Consiguiendo el Acero Cromoly 4130", 
             "• 0:00 - 2:00: Gancho. Mario con el teléfono en altavoz. 'Hola, buscaba tubos de acero 4130 cromoly para ceder a cambio de salir de fondo en YouTube ante 20.000 ingenieros'.\n"
             "• 2:00 - 7:00: Grabación de las llamadas de sourcing de materiales. Negociaciones con metalúrgicas locales. Cierre del primer sponsor de metal.\n"
             "• 7:00 - 10:00: Lección de negociación. Cómo vender tracción online a negocios tradicionales de barrio. Enlace al manual de negociación (DOC-042)."]
        ]
    }
    
    db["DOC-032"] = {
        "category": "04_Marketing_y_Contenido",
        "title": "Social Media Playbook",
        "subtitle": "Manual de Publicación, Hashtags, Formatos y Respuestas",
        "author": "Medios y Crecimiento CERO",
        "status": "APROBADO",
        "version": "v16.0",
        "date": "15.07.2026",
        "sections": [
            ["1. Directrices de Publicación y Estilo Visual", 
             "• Estética: Fondo de vídeo limpio, luz de taller, renders CAD en Onshape de alta definición. Tomas de primer plano de llamadas de negociación y visitas a locales sin filtros artificiales.\n"
             "• Tono: Crudo, honesto y estratégico. Se responderá en los comentarios como un diario personal del fundador, no como una marca fría corporativa.\n"
             "• Hashtags a utilizar: #CERO #buildinpublic #open-source #ingenieria #Mostoles #garaje #startup #marketing"],
            ["2. Respuestas a Críticas Comunes en Comentarios", 
             "• Comentario: 'No vais a conseguir un local gratis, nadie regala nada'.\n"
             "  - Respuesta: 'Es lógico pensarlo. Pero no pedimos un regalo, ofrecemos un canje de publicidad: visibilidad semanal ante miles de ingenieros a cambio de un rincón libre de taller. Ya estamos en negociaciones avanzadas con dos locales en Madrid'.\n"
             "• Comentario: 'Sin ingenieros reales eso no se va a homologar'.\n"
             "  - Respuesta: 'Precisamente por eso compartimos todo en Onshape y GitHub. Los ingenieros y soldadores se están sumando en nuestro Discord para diseñar y validar juntos la jaula de seguridad. ¡Pásate a verlo!'"],
            ["3. Criterios de Reposteo de Contenido de la Comunidad", 
             "Se autoriza y fomenta que los colaboradores suban sus propios clips analizando partes del chasis de CERO o renders de Onshape a sus canales de X/LinkedIn, etiquetando siempre la landing buildcero.com para centralizar la tracción. Esto amplifica de forma exponencial el alcance orgánico de la marca sin coste."]
        ]
    }
    
    db["DOC-033"] = {
        "category": "04_Marketing_y_Contenido",
        "title": "Merch and Crowdfunding Plan",
        "subtitle": "Plan de Lanzamiento de Productos Físicos y Cuotas de Patreon",
        "author": "Medios y Crecimiento CERO",
        "status": "APROBADO",
        "version": "v16.0",
        "date": "15.07.2026",
        "sections": [
            ["1. Merchandising sin Stock (Mes 7+)", 
             "Lanzamiento de camisetas con el plano explotado del chasis mediante impresión bajo demanda (Print-on-Demand). Esto garantiza stock de 0€ y un margen del 40-50% por camiseta vendida. Los diseños de las camisetas incluirán detalles de los planos Onshape de suspensión, atrayendo a entusiastas de la ingeniería. Todo el dinero recaudado de la tienda online se ingresará en la cuenta bancaria de la asociación cultural, destinándose íntegramente a las herramientas y consumibles del garaje físico."],
            ["2. Tiers de Patreon (Mes 4+)", 
             "Patreon se activa en el Mes 4 para acumular el fondo de caja con el que compraremos consumibles de taller y piezas en el Mes 12:\n"
             "• Tier 1 (2.99€/mes): Acceso al canal de Discord de debates técnicos privados.\n"
             "• Tier 2 (5.99€/mes): Acceso a planos CAD Onshape en tiempo real y commits de GitHub.\n"
             "• Tier 3 (19.99€/mes): Grabado láser de tu nombre en el chasis físico del coche real de calle, con derecho a voto en las asambleas generales."]
        ]
    }
    
    db["DOC-034"] = {
        "category": "04_Marketing_y_Contenido",
        "title": "Press and Media Kit",
        "subtitle": "Dossier de Prensa y Plantillas de Comunicación con Periodistas",
        "author": "Medios y Crecimiento CERO",
        "status": "APROBADO",
        "version": "v16.0",
        "date": "15.07.2026",
        "sections": [
            ["1. Dossier de Prensa CERO", 
             "Dossier de 1 página con los datos clave: 'CERO: El primer monoplaza open-source de calle desarrollado de forma colaborativa por internet desde Móstoles con 0€'.\n"
             "• Fundador: Mario (26 años).\n"
             "• Filosofía: Construcción en público, código abierto y homologación vial.\n"
             "• Enlace de contacto: buildcero.com / prensa@buildcero.com.\n"
             "• Enlace a material de descarga en alta definición (renders del chasis, fotos de local y logotipos oficiales de marca).\n"
             "Se adjuntarán las biografías del Core Team técnico y los hitos clave alcanzados hasta el momento."],
            ["2. Plantilla de Correo de Pitch para Periodistas de Motor", 
             "\"Hola [Nombre del Periodista], te escribo porque sigo tu cobertura en [Medio] y creo que te interesará CERO. Es el primer monoplaza de carreras open-source homologable de calle desarrollado en abierto por internet por una comunidad de ingenieros en España.\n\n"
             "Operamos con 0€ iniciales, compartiendo cada fallo del CAD en Onshape y negociando el garaje y los tubos en directo. Hemos subido todo el Data Room y renders a buildcero.com. ¿Te apetece tener una llamada de 10 minutos para contarte cómo avanza la soldadura? Un saludo, Mario.\"\n\n"
             "El objetivo es conseguir reportajes en medios especializados en motor para aumentar el tráfico orgánico a buildcero.com."],
            ["3. Política de Embargo Informativo", 
             "Las exclusivas sobre hitos del proyecto (obtención final del garaje físico, soldadura final del chasis) se reservarán para medios con un acuerdo de embargo firmado de forma previa, previniendo filtraciones prematuras en redes."]
        ]
    }

    # ----------------------------------------------------
    # CARPETA 05: SOURCING Y LOGÍSTICA (GUIONES & PROVEEDORES)
    # ----------------------------------------------------
    
    db["DOC-040"] = {
        "category": "05_Sourcing_y_Logistica",
        "title": "Sourcing and Logistics Guide",
        "subtitle": "Guía Práctica de Adquisición de Tren Motriz, Chasis y Componentes de Moto",
        "author": "Alianzas y Sourcing CERO",
        "status": "APROBADO",
        "version": "v16.0",
        "date": "15.07.2026",
        "sections": [
            ["1. Adquisición de Materiales para el Chasis", 
             "• Metal: Distribuidores autorizados de acero cromoly 4130 con certificado de composición química de colada.\n"
             "• Comprobación física: Inspección visual de rectitud de los tubos recibidos y medición de espesores con micrómetro digital.\n"
             "• Requisito obligatorio: Almacenamiento horizontal en soporte elevado del suelo en el garaje para evitar la flexión residual de los tubos por gravedad."],
            ["2. Logística y Envío Seguro de Componentes Pesados", 
             "El transporte de tubos de acero de 6 metros de longitud requiere camión de carga abierta y descarga manual. Las manguetas mecanizadas y amortiguadores se enviarán por mensajería ordinaria bien embalados. La logística de las baterías y el motor de tracción se coordinará con transportistas autorizados una vez definidos los componentes concretos por el equipo técnico."]
        ]
    }
    
    db["DOC-041"] = {
        "category": "05_Sourcing_y_Logistica",
        "title": "Supplier Contact List",
        "subtitle": "Lista de Proveedores de Acero 4130, Mecanizados CNC y Locales Comerciales",
        "author": "Alianzas y Sourcing CERO",
        "status": "APROBADO",
        "version": "v16.0",
        "date": "15.07.2026",
        "sections": [
            ["1. Base de Proveedores Estratégicos", 
             "• Suministrador de Tubos: Metalúrgicas nacionales capaces de certificar tubos de acero 4130 cromoly estirados en frío y sin costura (seamless) con sus respectivos certificados de colada química de metal.\n"
             "• Taller de Corte Láser y CNC: Talleres locales metalúrgicos con centros de fresado de 5 ejes y corte por chorro de agua para manguetas de aluminio.\n"
             "• Locales Comerciales / Garajes: Inmobiliarias y propietarios particulares en el polígono industrial de Móstoles con naves industriales o garajes cerrados en desuso susceptibles de canje publicitario."],
            ["2. Sourcing de Neumáticos y Amortiguadores", 
             "Para la homologación individual, los neumáticos deben tener obligatoriamente grabado el marcado 'E' y el índice de velocidad correspondiente. Sourcing preferido: desguaces de neumáticos o canje directo con marcas de competición. Los amortiguadores se buscarán de segunda mano de motos de altas prestaciones."],
            ["3. Contactos de Ingeniería de Homologación", 
             "Lista de ingenieros homologadores independientes acreditados por el Ministerio de Industria en Madrid. Su asesoramiento desde la Fase 2 es crítico para validar los planos del cockpit y chasis tubular antes de soldar, evitando modificaciones estructurales posteriores sobre chasis ya soldados."]
        ]
    }
    
    db["DOC-042"] = {
        "category": "05_Sourcing_y_Logistica",
        "title": "Negotiation Scripts",
        "subtitle": "Guiones Telefónicos y de Correo para Alianzas, Garajes y Canjes Comerciales",
        "author": "Alianzas y Sourcing CERO",
        "status": "APROBADO",
        "version": "v16.0",
        "date": "15.07.2026",
        "sections": [
            ["1. Guion Telefónico para Conseguir el Garaje (Local Físico Vacío)", 
             "\"Hola, buenas tardes. Llamaba por el anuncio del local en alquiler en Móstoles. Me gustaría proponerle un trato alternativo: dirijo CERO (buildcero.com), el primer coche open-source de calle desarrollado de forma colaborativa por internet en Madrid.\n\n"
             "Tenemos una comunidad de miles de ingenieros y entusiastas siguiendo el proceso semanal en YouTube. Le proponemos cedernos el uso de su local cerrado o garaje como taller de montaje a cambio de un contrato de canje de publicidad: su local aparecerá de fondo en todos nuestros vlogs semanales y Shorts de YouTube, con enlaces de contacto y publicidad directa que llevarán visibilidad y clientes a su negocio o cartera inmobiliaria. ¿Le interesaría que nos reunamos 10 minutos en el local y le enseño los planos conceptuales del coche?\""],
            ["2. Guion Telefónico para Negociar Espacio en Taller Mecánico Activo (Plan B)", 
             "\"Hola, buenas tardes. Quería hablar con el dueño del taller. Mi nombre es Mario y estoy coordinando CERO (buildcero.com), un monoplaza open-source para calle desarrollado colaborativamente por internet.\n\n"
             "Viendo la calidad de sus instalaciones, queríamos proponerle un acuerdo de trueque comercial. Buscamos un rincón libre de su taller (de unos 15-20 m²) para soldar el chasis y ensamblar las piezas únicamente los sábados por la tarde, fuera de su horario comercial. A cambio, colocaremos un cartel gigante de su taller de fondo en todos nuestros vídeos semanales de YouTube y Shorts de taller (donde nos siguen miles de apasionados locales), ayudaremos a limpiar y ordenar el taller los fines de semana, y promocionaremos activamente sus servicios de mecánica en la zona de Móstoles. ¿Podríamos pasarnos el sábado por la tarde 10 minutos para mostrarle el diseño en Onshape?\""],
            ["3. Guion para Conseguir el Patrocinio de Tubos de Acero 4130", 
             "\"Hola, buenas. Quería hablar con el responsable de marketing o ventas. Les proponemos una colaboración: estamos fabricando CERO, un monoplaza de código abierto para calle (buildcero.com) seguido en vlogs de YouTube por miles de estudiantes de ingeniería y mecánicos.\n\n"
             "Les proponemos patrocinarnos con 50 metros de tubo de acero cromoly 4130 a cambio de colocar el logotipo de su metalúrgica grabado por láser en el chasis físico, menciones de su empresa en los vlogs del proceso de soldadura y enlaces directos en nuestro repositorio GitHub. ¿Podríamos enviarle una propuesta de patrocinio por correo electrónico para que la valoren?\""],
            ["4. Guion de Seguimiento por Correo Electrónico", 
             "\"Estimado [Nombre del Propietario / Proveedor],\n\n"
             "Le escribo para dar seguimiento a nuestra conversación de ayer. Le adjunto el dossier de patrocinio y el Manifiesto de CERO (DOC-001) donde detallamos el modelo operativo y la tracción en redes sociales. Estamos muy interesados en colaborar con usted para establecer el garaje del proyecto en su local o taller.\n\n"
             "Quedamos a su entera disposición para reunirnos de forma física. Un saludo cordial, Mario.\"\n\n"
             "Este correo se enviará de inmediato para mantener viva la negociación del espacio o materiales."]
        ]
    }
    
    return db

if __name__ == "__main__":
    project_root = r"C:\Users\mario\.gemini\antigravity-ide\scratch\cero-website"
    
    db = get_db()
    db_path = os.path.join(project_root, "cero_docs_db.json")
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4, ensure_ascii=False)
        
    print("cero_docs_db.json built with ultimate operational and marketing details successfully.")
