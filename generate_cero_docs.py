import os
import sys
import shutil
import matplotlib.pyplot as plt
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

# Custom Canvas for professional running header/footer and front cover styling.
class CeroNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_elements(num_pages)
            super().showPage()
        super().save()

    def draw_cero_badge(self, x, y, size, stroke_color, badge_bg):
        self.saveState()
        self.setFillColor(colors.HexColor(badge_bg))
        self.setStrokeColor(colors.HexColor(badge_bg))
        r = size / 2
        self.circle(x + r, y + r, r, fill=1, stroke=0)
        
        lw = size * 0.05
        w = size * 0.38
        h = size * 0.62
        logo_x = x + (size - w) / 2
        logo_y = y + (size - h) / 2
        logo_r = size * 0.12
        
        self.setStrokeColor(colors.HexColor(stroke_color))
        self.setLineWidth(lw)
        self.roundRect(logo_x, logo_y, w, h, logo_r, stroke=1, fill=0)
        
        self.setFillColor(colors.HexColor(badge_bg))
        self.setStrokeColor(colors.HexColor(badge_bg))
        cover_w = w * 0.35
        cover_h = lw * 2.5
        
        self.rect(logo_x + (w - cover_w)/2, logo_y + h - cover_h/2, cover_w, cover_h, fill=1, stroke=0)
        self.rect(logo_x + (w - cover_w)/2, logo_y - cover_h/2, cover_w, cover_h, fill=1, stroke=0)
        self.restoreState()

    def draw_cero_letters(self, x, y, char_w, char_h, lw, stroke_color, bg_color):
        self.saveState()
        self.setStrokeColor(colors.HexColor(stroke_color))
        self.setFillColor(colors.HexColor(bg_color))
        self.setLineWidth(lw)
        self.setLineCap(1)
        self.setLineJoin(1)
        
        gap = char_w * 0.4
        r = char_w * 0.35
        
        # C
        self.arc(x, y + char_h - r*2, x + r*2, y + char_h, 90, 90)
        self.line(x, y + r, x, y + char_h - r)
        self.arc(x, y, x + r*2, y + r*2, 180, 90)
        self.line(x + r, y + char_h, x + char_w, y + char_h)
        self.line(x + r, y, x + char_w, y)
        
        x += char_w + gap
        # E
        self.arc(x, y + char_h - r*2, x + r*2, y + char_h, 90, 90)
        self.line(x, y + r, x, y + char_h - r)
        self.arc(x, y, x + r*2, y + r*2, 180, 90)
        self.line(x + r, y + char_h, x + char_w, y + char_h)
        self.line(x + r, y, x + char_w, y)
        self.line(x, y + char_h/2, x + char_w * 0.7, y + char_h/2)
        
        x += char_w + gap
        # R
        self.line(x, y, x, y + char_h)
        self.line(x, y + char_h, x + char_w - r, y + char_h)
        self.arc(x + char_w - r*2, y + char_h/2, x + char_w, y + char_h, 270, 180)
        self.line(x, y + char_h/2, x + char_w - r, y + char_h/2)
        self.line(x + char_w * 0.45, y + char_h/2, x + char_w * 0.9, y)
        
        x += char_w + gap
        # O
        self.roundRect(x, y, char_w, char_h, r, stroke=1, fill=0)
        self.setFillColor(colors.HexColor(bg_color))
        self.setStrokeColor(colors.HexColor(bg_color))
        cover_w = char_w * 0.35
        cover_h = lw * 2.5
        self.rect(x + (char_w - cover_w)/2, y + char_h - cover_h/2, cover_w, cover_h, fill=1, stroke=0)
        self.rect(x + (char_w - cover_w)/2, y - cover_h/2, cover_w, cover_h, fill=1, stroke=0)
        
        self.restoreState()

    def draw_page_elements(self, page_count):
        doc_template = getattr(self, "_doctemplate", None)
        doc_id = getattr(doc_template, "doc_id", "DOC-XXX")
        
        if self._pageNumber == 1:
            self.saveState()
            self.draw_cero_badge(306 - 45, 450, 90, "#FFFFFF", "#000000")
            self.draw_cero_letters(233.5, 385, 28, 42, 4.5, "#000000", "#FFFFFF")
            self.setFont("Helvetica", 9)
            self.setFillColor(colors.HexColor("#8E8E93"))
            self.drawCentredString(306, 360, "E L   P R O Y E C T O .")
            self.setStrokeColor(colors.HexColor("#FF3B30"))
            self.setLineWidth(4)
            self.line(54, 738, 54, 54)
            self.restoreState()
            return

        self.saveState()
        self.setStrokeColor(colors.HexColor("#FF3B30"))
        self.setLineWidth(1)
        self.line(54, 738, 558, 738)
        self.draw_cero_badge(54, 742, 24, "#FFFFFF", "#000000")
        
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1C1C1E"))
        self.drawString(84, 746, "CERO MOTOR CO. — DOCUMENTO OFICIAL")
        self.drawRightString(558, 746, doc_id)

        self.setStrokeColor(colors.HexColor("#E5E5EA"))
        self.setLineWidth(1)
        self.line(54, 54, 558, 54)
        
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#8E8E93"))
        self.drawString(54, 38, "CONFIDENCIAL — PROHIBIDA SU DISTRIBUCIÓN COMERCIAL")
        self.drawRightString(558, 38, f"Pág. {self._pageNumber} de {page_count}")
        self.draw_cero_badge(300, 36, 12, "#FFFFFF", "#000000")
        self.restoreState()


# Programmatic generator for the 104-week social media content calendar.
def get_detailed_104_week_calendar():
    phases = [
        ("Fase 1: Reclutamiento y Elección de Motor", 1, 13, 
         "Reclutar ingenieros y mecánicos entusiastas de internet. Debatir en Discord y YouTube la compra del motor de moto de desguace.",
         "¿Elegimos motor Suzuki GSX-R 600 o GSX-R 1000?", "Cómo encontrar un motor de moto barato en desguaces.", 
         "Por qué los coches con motor de moto suenan tan brutales.", "Suzuki GSX-R vs Yamaha R1 para un monoplaza."),
        
        ("Fase 2: Diseño Conceptual CAD Colaborativo", 14, 26,
         "Establecer flujos de diseño en Onshape (cuenta gratuita). Modelar chasis tubular inicial y cockpit con feedback de la comunidad.",
         "Diseñando la ergonomía del piloto en CAD.", "Los fallos de diseño de chasis más comunes que nos corregís.",
         "Cómo modelar suspensiones de doble trapecio sin morir en el intento.", "Decidiendo la posición de conducción ideal."),
        
        ("Fase 3: Ingeniería de Detalle y Simulación", 27, 52,
         "Hacer simulaciones FEA de rigidez torsional y CFD aerodinámica. Evaluar fatigas en juntas de soldadura. Sin gasto en software.",
         "FEA de chasis tubular: Simulación de impacto frontal.", "Cómo calculamos la flexión de los brazos de suspensión.",
         "CFD conceptual: ¿Sirve de algo la aerodinámica en este monoplaza?", "Simulación estructural: Evitando que el chasis se doble."),
        
        ("Fase 4: Alianzas y Sourcing de Materiales", 53, 65,
         "Buscar patrocinadores para tubos de acero 4130, ruedas, frenos y amortiguadores en canje por branding en el chasis y vídeos.",
         "Buscando acero 4130 cromoly por España en modo canje.", "Unboxing de las manguetas CNC donadas por nuestro primer sponsor.",
         "Cómo convencer a un fabricante de llantas para que nos patrocine.", "Conseguimos el embrague secuencial por cable."),
        
        ("Fase 5: Corte y Soldadura en Taller Físico", 66, 78,
         "Comenzar el corte de tubos y soldadura en el taller colaborador. Mostrar time-lapses de chispas, uniones TIG y progreso físico.",
         "Cortando el primer tubo del chasis físico.", "Soldadura TIG de precisión: El arco antivuelco toma forma.",
         "Montando el chasis en el jig de taller.", "Time-lapse: El esqueleto de acero de CERO está terminado."),
        
        ("Fase 6: Montaje de Motor y Transmisión por Cadena", 79, 91,
         "Montar el motor Suzuki GSX-R en el chasis. Conectar la transmisión por cadena al diferencial y diseñar la palanca secuencial.",
         "Instalando el motor de moto de 150hp en el chasis.", "El sistema de transmisión por cadena y corona trasera a medida.",
         "Diseñando el pedalier físico de aluminio.", "Cómo fabricar un escape de moto a medida para el monoplaza."),
        
        ("Fase 7: Puesta en Marcha y Pruebas Dinámicas", 92, 104,
         "Primer arranque del motor. Pruebas de dirección, frenado y primeros giros en pista privada. Ajustes de escape y dinámica final.",
         "El primer arranque de CERO: Sonido GSX-R a 14.000 RPM.", "First Roll: El coche se mueve en el patio del taller.",
         "Pruebas de frenado a fondo y balanceo de suspensiones.", "Vuelta rápida en circuito privado: El monoplaza de internet funciona.")
    ]
    
    calendar_text = "A continuación se detalla el plan editorial exhaustivo semana a semana para los próximos 2 años (104 semanas):\n\n"
    for phase_name, start_w, end_w, desc, yt, s1, s2, s3 in phases:
        calendar_text += f"=== {phase_name.upper()} (Semanas {start_w} a {end_w}) ===\n"
        calendar_text += f"{desc}\n\n"
        for w in range(start_w, end_w + 1):
            calendar_text += (
                f"• Semana {w:03d} - Hito Técnico:\n"
                f"  - YouTube (Sábado): \"CERO - {yt} (Progreso del diseño/construcción)\"\n"
                f"  - Short Lunes (TikTok/Reel): Hook: \"{s1}\" (Enfoque en interacción y debate).\n"
                f"  - Short Miércoles (Detrás de Cámaras): Hook: \"{s2}\" (Avances crudos del taller/CAD).\n"
                f"  - Short Viernes (Educativo): Hook: \"{s3}\" (Explicación técnica simplificada).\n"
                f"  - Post X/LinkedIn (Jueves): Debate abierto sobre componentes del monoplaza.\n"
                f"  - Discord (Domingo): Votación comunitaria de diseño o llamada de voz con el Core Team.\n\n"
            )
    return calendar_text


# High-density database containing detailed technical text and guidelines.
doc_database = {
    "DOC-000": {
        "category": "00_Gobernanza_y_Operaciones",
        "title": "Document Control Manual",
        "subtitle": "Manual de Gestión y Ciclo de Vida del Ecosistema Documental",
        "author": "Comité de Gobernanza CERO",
        "status": "APROBADO",
        "version": "v1.2",
        "date": "15.07.2026",
        "sections": [
            ("1. Propósito y Control del Ecosistema Documental", 
             "Este manual establece la estructura, codificación, jerarquía y ciclo de vida de todos los documentos oficiales "
             "del proyecto CERO. Su objetivo es garantizar la consistencia, veracidad e integridad del conocimiento generado "
             "por la comunidad, permitiendo que cualquier persona entienda el estado operativo y técnico del proyecto en tiempo real. "
             "Toda la información reside de forma transparente en el repositorio público, impidiendo duplicados y reduciendo costes de mala organización."),
            ("2. Estructura de Codificación y Jerarquía de Carpetas",
             "Cada documento oficial dentro del ecosistema CERO debe estar codificado utilizando la nomenclatura DOC-XXX, donde XXX representa "
             "un número correlativo de tres dígitos. Los rangos de codificación se organizan por áreas funcionales de la siguiente manera:\n"
             "• DOC-000 a DOC-004: Gobernanza y Sistema Operativo Central (Estatutos, Manifiesto, Sistema de Reuniones y OS).\n"
             "• DOC-005 a DOC-009: Identidad, Crecimiento y Comunidad (Manual de Marca, Guía de Contenido, Redes y Reclutamiento).\n"
             "• DOC-010 a DOC-012: Aspectos Legales, Financieros y Relaciones con Inversores (Cesión de IP, Presupuesto de 0€ y Data Room).\n"
             "• DOC-013 a DOC-015: Requerimientos Técnicos, Arquitectura de Ingeniería y Riesgos (Fichas del Motor, Chasis y Mitigaciones).\n"
             "• DOC-016 a DOC-020: Control Métrico, Revisiones y Base de Proveedores (KPIs, Revisiones Semanales y Directorio de Canjes).\n"
             "• DOC-021 a DOC-028: Playbooks, Guiones, Homologación, Sourcing Audit, Copilot, Competidores, Dependencias y Overhaul Técnico."),
            ("3. Ciclo de Vida y Flujo de Aprobación",
             "El proceso de aprobación y actualización consta de las siguientes fases críticas:\n"
             "1. Borrador (Draft): Iniciado por cualquier miembro de la comunidad en los canales de trabajo correspondientes.\n"
             "2. Revisión Técnica (Under Review): Evaluación y comentarios del comité técnico o de gobernanza asignado al área.\n"
             "3. Aprobación (Approved): Firma y sello digital del comité de gobernanza central, tras cumplir los criterios de verificación.\n"
             "4. Deprecado (Deprecated): Archivo histórico cuando el documento ha sido superado por una versión más reciente."),
            ("4. Control de Versiones y Modificaciones",
             "Cualquier modificación requiere el incremento de versión (de v1.0 a v1.1 para cambios menores, o v2.0 para cambios mayores). "
             "Cada actualización debe ser registrada en la tabla de control de versiones del documento correspondiente, indicando la fecha, "
             "el autor y un resumen del cambio.")
        ]
    },
    "DOC-001": {
        "category": "00_Gobernanza_y_Operaciones",
        "title": "Foundational Manifest",
        "subtitle": "Declaración de Principios y Reglas de Coordinación",
        "author": "Fundadores de CERO",
        "status": "APROBADO",
        "version": "v1.1",
        "date": "15.07.2026",
        "sections": [
            ("1. La Pregunta Fundamental: Coche de Combustión Sencillo por Internet",
             "¿Puede internet coordinar talento, herramientas y conocimiento de forma descentralizada para diseñar y construir "
             "un coche real, de combustión, ligero y funcional desde 0 €? CERO no nace como una empresa automotriz tradicional, sino como un experimento "
             "social y técnico de código abierto. La idea es que CERO pueda ser construido gracias a la inteligencia colectiva del internet, "
             "sin contar inicialmente con un equipo cerrado de ingenieros profesionales, sino reclutando el talento a lo largo del proceso. "
             "El vehículo CERO no se limitará a circuitos de exhibición cerrados; su fin principal es ser un vehículo homologable de calle en España y Europa, "
             "lo que añade exigencias mecánicas, de control de emisiones y de visibilidad complejas que debemos afrontar desde el diseño en CAD."),
            ("2. Principios No Negociables de Bootstrapping",
             "Para mantener la integridad del proyecto, todos los participantes deben de adherirse a los siguientes principios:\n"
             "• Transparencia Radical: Todo el trabajo se realiza en público. Las simulaciones, el software, las actas de reuniones y las finanzas son de acceso libre.\n"
             "• Acción Verificable: Una idea teórica no tiene valor si no está acompañada de una simulación matemática, un modelo CAD o un prototipo físico probado.\n"
             "• Colaboración antes que Competición: Se premia el apoyo a otros departamentos y la resolución colectiva de bloqueos técnicos.\n"
             "• Iteración de Bajo Coste: Priorizamos la validación virtual y las pruebas a escala antes de gastar recursos materiales."),
            ("3. Estructura Organizativa Abierta",
             "La organización se articula en una estructura plana donde el mérito técnico y la consistencia en las entregas determinan "
             "los niveles de decisión. No hay cargos honoríficos; el estatus de colaborador activo se mantiene mediante contribuciones reales "
             "registradas en la base de datos de gobernanza.")
        ]
    },
    "DOC-002": {
        "category": "00_Gobernanza_y_Operaciones",
        "title": "Strategic Plan",
        "subtitle": "Plan Maestro de 24 Meses hacia el Concept Car de Combustión",
        "author": "Dirección Estratégica CERO",
        "status": "APROBADO",
        "version": "v1.1",
        "date": "15.07.2026",
        "sections": [
            ("1. Horizonte de Planificación (28 Meses)",
             "El objetivo estratégico principal de CERO es diseñar, ensamblar, homologar e instrumentar un coche de carreras monoplaza ligero, "
             "propulsado por un motor de motocicleta de combustión interna, en un plazo de 28 meses. La inclusión del proceso de homologación individual "
             "vial (ITV) exige ampliar nuestro horizonte de los 24 meses iniciales a los 28 meses reales, incorporando ensayos de laboratorio de emisiones, "
             "pruebas de ruido dinámico (ISO 362) y frenado de doble circuito en la fase final."),
            ("2. Cronograma de Fases del Proyecto",
             "Fase 1 (Mes 1 - Mes 3): Lanzamiento, captación de la comunidad de internet, y debate sobre la elección de motor (GSX-R 600/1000).\n"
             "Fase 2 (Mes 4 - Mes 6): Diseño CAD conceptual de la arquitectura del chasis tubular y cockpit (Onshape gratuito).\n"
             "Fase 3 (Mes 7 - Mes 12): Ingeniería detallada, optimización por simulación (FEA y CFD), y validación de componentes de moto.\n"
             "Fase 4 (Mes 13 - Mes 18): Selección de partners de taller y corte láser, obtención de acero 4130 y soldadura del chasis (Rolling Chassis).\n"
             "Fase 5 (Mes 19 - Mes 21): Montaje del motor de moto, cadena, escape a medida, cableado básico e instrumentación.\n"
             "Fase 6 (Mes 22 - Mes 24): Acabado de carrocería minimalista de aluminio/fibra, pruebas dinámicas en circuito y puesta a punto.\n"
             "Fase 7 (Mes 25 - Mes 28): Pruebas de laboratorio IDIADA/INTA, ajuste de emisiones Euro 6, y obtención de matrículas ordinarias de calle."),
            ("3. Alternativas Estratégicas y Puntos de Decisión",
             "Si en el Mes 12 no se ha conseguido financiación o partners de mecanizado para el chasis, el proyecto pivotará hacia un "
             "diseño híbrido basado en un chasis comercial modificado, priorizando la ejecución física sobre el diseño a medida.")
        ]
    },
    "DOC-003": {
        "category": "00_Gobernanza_y_Operaciones",
        "title": "Master Roadmap",
        "subtitle": "Hitos, Entregables y Dependencias Críticas",
        "author": "Gestión de Proyectos CERO",
        "status": "APROBADO",
        "version": "v1.1",
        "date": "15.07.2026",
        "sections": [
            ("1. Ruta Crítica de Desarrollo",
             "La ruta crítica está determinada por la adquisición del motor de motocicleta Suzuki GSX-R de desguace, la soldadura de la estructura de seguridad del chasis, "
             "y sobre todo, la consecución de las homologaciones viales europeas de calle. Para circular legalmente por la calle, cada componente de iluminación, "
             "frenado, vidrios y espejos debe poseer la marca 'E' (homologación europea), y el chasis debe de ser certificado ante impacto peatonal (Directiva de protección de peatones)."),
            ("2. Gráfico del Cronograma de Fases",
             "A continuación se ilustra de manera gráfica el calendario detallado de fases del plan maestro de 28 meses:"),
            ("3. Tabla de Hitos y Puertas de Control (Gates)",
             "A continuación se dejan detallados los hitos y fechas límite del proyecto:")
        ],
        "image": "project_timeline_gantt.png",
        "table": {
            "cols": [45, 45, 230, 80, 100],
            "data": [
                ["Hito", "Fase", "Entregable Clave", "Fecha Límite", "Estado"],
                ["MS-0", "Fase 1", "Freeze de Requerimientos Técnicos Básicos y Motor Suzuki GSX-R", "Mes 3", "Completado"],
                ["MS-1", "Fase 2", "Diseño Conceptual CAD y Distribución General", "Mes 6", "En Progreso"],
                ["MS-2", "Fase 3", "Diseño Detallado e Ingeniería de Detalle (FEA/CFD)", "Mes 12", "Planificado"],
                ["MS-3", "Fase 4", "Adquisición y Ensamblaje de Chasis Tubular", "Mes 18", "Planificado"],
                ["MS-4", "Fase 5", "Integración Tren Motriz y Electrónica", "Mes 21", "Planificado"],
                ["MS-5", "Fase 6", "Lanzamiento y Pruebas en Pista Privada", "Mes 24", "Planificado"],
                ["MS-6", "Fase 7", "Dossier IDIADA / INTA y Obtención de Placas de Calle", "Mes 28", "Planificado"]
            ]
        }
    },
    "DOC-004": {
        "category": "00_Gobernanza_y_Operaciones",
        "title": "Operating System",
        "subtitle": "Estructura Organizativa y Flujos de Comunicación",
        "author": "Operaciones CERO",
        "status": "APROBADO",
        "version": "v1.1",
        "date": "15.07.2026",
        "sections": [
            ("1. Estructura de Departamentos",
             "El proyecto se organiza en cinco departamentos clave, cada uno liderado por un Coordinador de Área:\n"
             "• Ingeniería (ENG): Responsable del CAD, FEA, CFD y dinámica vehicular.\n"
             "• Medios y Crecimiento (MED): Responsable del contenido diario, YouTube y crecimiento de marca.\n"
             "• Alianzas y Sourcing (PART): Responsable de conseguir patrocinios, materiales y talleres de fabricación.\n"
             "• Legal y Cumplimiento (LEG): Responsable de la propiedad intelectual, contratos e inspección técnica vehicular de calle.\n"
             "• Gobernanza y Comunidad (GOV): Responsable del mantenimiento del Discord, votaciones y organización interna."),
            ("2. Embudo de Crecimiento y Adquisición Organizativa",
             "A continuación se ilustra de manera gráfica el embudo de conversión para convertir espectadores pasivos de redes en colaboradores y miembros activos:"),
            ("3. Canales y Flujos de Trabajo",
             "• Discord: Comunicación diaria, resolución rápida de dudas y reuniones semanales.\n"
             "• GitHub: Repositorio central de archivos CAD, simulaciones de control y documentación Markdown.\n"
             "• Google Workspace / Drive: Almacenamiento de contratos, presupuestos e informes administrativos."),
            ("4. Matriz de Responsabilidades (RACI)",
             "A continuación se presenta la matriz RACI (Responsable, Aprobador, Consultado, Informado) para los departamentos de la organización:")
        ],
        "image": "growth_funnel.png",
        "table": {
            "cols": [150, 70, 70, 70, 70, 70],
            "data": [
                ["Actividad / Hito", "ENG (Ing.)", "MED (Medios)", "PART (Alian.)", "LEG (Legal)", "GOV (Gob.)"],
                ["Definición Requerimientos", "A", "C", "I", "C", "R"],
                ["Diseño CAD", "R", "I", "C", "I", "A"],
                ["Contenido Redes Sociales", "I", "R", "C", "I", "A"],
                ["Contratos de IP", "I", "I", "C", "R", "A"],
                ["Negociación de Canjes", "C", "C", "R", "A", "I"],
                ["Soldadura Chasis", "R", "I", "I", "I", "A"]
            ]
        }
    },
    "DOC-005": {
        "category": "01_Marca_y_Comunidad",
        "title": "Brand Bible",
        "subtitle": "Identidad Visual, Logotipo e Identidad Editorial",
        "author": "Medios y Crecimiento CERO",
        "status": "APROBADO",
        "version": "v1.0",
        "date": "15.07.2026",
        "sections": [
            ("1. Paleta de Colores Corporativos",
             "Nuestra identidad visual se fundamenta en un esquema técnico y de alto contraste:\n"
             "• Negro Carbón: #000000 (Representa el asfalto y la fibra de carbono cruda).\n"
             "• Blanco Roto: #F8F9FA (Contraste y lectura de textos, limpio e industrial).\n"
             "• Rojo Óxido: #FF3B30 (Acentos visuales, alertas, cables de alta tensión, líneas de freno).\n"
             "• Gris Técnico: #88888B (Textos secundarios, cotas y elementos de soporte gráfico)."),
            ("2. Logotipo e Iconografía",
             "El logotipo de CERO consta de la palabra 'CERO' escrita en mayúsculas en la tipografía Space Grotesk Bold, acompañada de un símbolo gráfico "
             "que consiste en un rectángulo vertical con bordes altamente redondeados (brackets redondeados), simulando un 0 o la forma en planta de un chasis de monoplaza. "
             "Este logo debe usarse sin sombras ni degradados, siempre en blanco puro sobre fondo negro, o rojo sobre fondo negro."),
            ("3. Tipografías Oficiales",
             "• Títulos y Cabeceras: Space Grotesk (sans-serif de corte geométrico y tecnológico).\n"
             "• Texto Corrido: Outfit (altamente legible en interfaces móviles y pantallas de ordenadores).\n"
             "• Datos y Código: JetBrains Mono (estilo consola técnica)."),
            ("4. Tono de Voz y Editorial",
             "El tono de CERO es técnico, transparente y crudo. No vendemos promesas de coches eléctricos de lujo; "
             "mostramos el metal doblado, el óxido, los fallos en la soldadura y las soluciones de ingeniería reales. Hablamos en primera persona del plural (Nosotros).")
        ]
    },
    "DOC-006": {
        "category": "01_Marca_y_Comunidad",
        "title": "Content OS",
        "subtitle": "Sistema Operativo de Producción y Distribución de Medios a 2 Años",
        "author": "Medios y Crecimiento CERO",
        "status": "APROBADO",
        "version": "v2.0",
        "date": "15.07.2026",
        "sections": [
            ("1. Filosofía del Canal de YouTube e Instagram",
             "La viabilidad de CERO depende 100% de la tracción de su audiencia para conseguir patrocinadores. Documentaremos todo "
             "de forma cruda: errores de soldadura, problemas para encajar el motor Suzuki GSX-R, piezas dobladas y discusiones de diseño. "
             "Esto generará debates naturales en los comentarios, disparando el alcance de los algoritmos."),
            ("2. Calendario Editorial Detallado (104 Semanas)", get_detailed_104_week_calendar())
        ]
    },
    "DOC-007": {
        "category": "01_Marca_y_Comunidad",
        "title": "Growth Engine",
        "subtitle": "Estrategias de Adquisición de Comunidad y Embudo Viral",
        "author": "Gobernanza y Comunidad CERO",
        "status": "APROBADO",
        "version": "v1.0",
        "date": "15.07.2026",
        "sections": [
            ("1. El Embudo de Crecimiento CERO",
             "La captación se realiza mediante un embudo de conversión de cuatro pasos:\n"
             "1. Alcance (Impresiones en Redes Sociales): Espectadores de contenido viral.\n"
             "2. Conversión a Comunidad (Miembros de Discord): Usuarios que entran a participar activamente.\n"
             "3. Activación a Colaborador (GitHub Commits/CAD submissions): Usuarios que aportan soluciones técnicas directas.\n"
             "4. Embajador (Core Team): Miembros consolidados que coordinan subgrupos de trabajo."),
            ("2. Ilustración Gráfica de Conversión",
             "A continuación se presenta el esquema estructural de conversión comunitaria del proyecto:"),
            ("3. Mecanismos de Viralidad Orgánica",
             "El contenido se basa en el 'Build in Public' (Construir en Público). Cada fallo de soldadura, problema con el regulador del motor "
             "o discusión sobre el presupuesto es documentado. Esto genera un debate técnico natural en la sección de comentarios, aumentando el alcance orgánico de los algoritmos."),
            ("4. Programas de Referidos y Gamificación",
             "Los miembros de Discord reciben roles especiales ('Ingeniero de Dinámica', 'Sourcing Scout') según sus contribuciones cuantificables, "
             "creando una jerarquía meritocrática atractiva para estudiantes de ingeniería y jóvenes profesionales.")
        ],
        "image": "growth_funnel.png"
    },
    "DOC-008": {
        "category": "01_Marca_y_Comunidad",
        "title": "Talent Acquisition",
        "subtitle": "Proceso de Reclutamiento, Evaluación e Incorporación de Internet",
        "author": "Gobernanza y Comunidad CERO",
        "status": "APROBADO",
        "version": "v1.1",
        "date": "15.07.2026",
        "sections": [
            ("1. El Enfoque del Talento Descentralizado",
             "Dado que CERO se financia con 0 € y se basa en la colaboración de internet, no contratamos un equipo clásico. "
             "En lugar de buscar ingenieros con salarios, abrimos las tareas técnicas a foros de CAD, estudiantes de ingeniería mecánica, "
             "equipos de Formula Student de universidades y entusiastas de los karts que quieren construir un historial público. "
             "El reclutamiento se realiza a través de retos cortos semanales publicados en Discord."),
            ("2. Proceso de Evaluación y Acceso",
             "No realizamos entrevistas de currículum tradicionales. La incorporación sigue tres pasos:\n"
             "1. Tarea de Prueba (Challenge): El candidato debe resolver un problema menor abierto en nuestro repositorio (ej. corregir una tolerancia en el pedalier en CAD o diseñar el soporte del escape en Onshape).\n"
             "2. Aprobación por la Comunidad: Los colaboradores principales revisan y aprueban el pull request.\n"
             "3. Asignación de Accesos: Asignación de permisos en el repositorio GitHub oficial y canales de decisión de Discord.")
        ]
    },
    "DOC-009": {
        "category": "03_Ingenieria_y_Producto",
        "title": "Partnership Strategy",
        "subtitle": "Plan de Alianzas con Universidades, Talleres e Industria",
        "author": "Alianzas y Sourcing CERO",
        "status": "APROBADO",
        "version": "v1.0",
        "date": "15.07.2026",
        "sections": [
            ("1. El Valor del Canje Tecnológico",
             "Sin capital financiero, CERO ofrece visibilidad en redes sociales a cambio de materiales y servicios. Las alianzas estratégicas "
             "son nuestra principal vía para la obtención de mecanizados CNC, corte láser, impresión 3D industrial y componentes de automoción."),
            ("2. Tiers de Patrocinio y Retribuciones",
             "• Partner de Taller: A cambio de mecanizar piezas de chasis o suspensiones, ofrecemos el logotipo en el chasis físico y menciones dedicadas en los vídeos de YouTube.\n"
             "• Partner Universitario: Colaboración con equipos de Formula Student de universidades locales para el uso compartido de bancos de prueba, simuladores de software y zonas de soldadura.\n"
             "• Partner Tecnológico: Proveedores de componentes electrónicos (inversores, celdas de batería) que proveen muestras gratuitas a cambio de análisis técnicos detallados y visibilidad de marca."),
            ("3. Protocolo de Contacto y Seguimiento",
             "Cada contacto debe registrarse en la Base de Proveedores (DOC-019). No realizamos llamadas de venta frías agresivas; "
             "les mostramos el diseño CAD completo del coche donde irá instalada su pieza o servicio para dar confianza técnica del proyecto.")
        ]
    },
    "DOC-010": {
        "category": "02_Legal_y_Finanzas",
        "title": "Legal and Compliance",
        "subtitle": "Propiedad Intelectual, Contratos e Implicaciones Normativas",
        "author": "Legal y Cumplimiento CERO",
        "status": "APROBADO",
        "version": "v1.0",
        "date": "15.07.2026",
        "sections": [
            ("1. Propiedad Intelectual Abierta y Licencias",
             "Todos los diseños de CERO se registran bajo una licencia Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0). "
             "Esto permite a cualquier persona descargar y modificar los archivos, pero impide la fabricación comercial del coche sin un acuerdo "
             "específico con la entidad gestora de CERO."),
            ("2. Contrato de Colaboración e Incorporación de IP",
             "Cualquier colaborador que envíe un archivo CAD o código debe firmar un Contrato de Cesión de Propiedad Intelectual (IP Assignment Agreement). "
             "Este contrato garantiza que CERO tiene los derechos necesarios para fabricar físicamente el monoplaza sin riesgo de reclamaciones posteriores."),
            ("3. Cumplimiento de Protección de Datos (RGPD)",
             "El registro de colaboradores y el tratamiento de datos de la comunidad cumple con la normativa europea RGPD. Los datos de contacto "
             "se almacenan de forma segura y solo se utilizan con fines organizativos internos del proyecto."),
            ("4. Homologación y Cumplimiento de Seguridad del Vehículo",
             "Para realizar pruebas en pistas autorizadas, el vehículo debe seguir las directrices básicas de la FIA (Federation Internationale de l'Automobile) "
             "en cuanto a la estructura del arco antivuelco (Roll Hoop) y los sistemas de desconexión rápida de alta tensión (High Voltage Shutdown Circuit).")
        ]
    },
    "DOC-011": {
        "category": "02_Legal_y_Finanzas",
        "title": "Financial Model",
        "subtitle": "Presupuesto Operativo Inicial de Cero Euros y Vías de Monetización",
        "author": "Alianzas y Sourcing CERO",
        "status": "APROBADO",
        "version": "v1.4",
        "date": "15.07.2026",
        "sections": [
            ("1. Principios del Presupuesto Inicial de 0 €",
             "El proyecto opera bajo la estricta premisa de 0 € de capital inicial. En la Fase 1 (Meses 1-3) no se realiza ningún desembolso. "
             "Las herramientas de diseño son gratuitas, la comunicación se gestiona por Discord/GitHub gratuitos y no hay gastos de marketing. "
             "Los gastos reales de caja (adquisición del motor de moto usado, cadena o cables) ocurren a partir de la Fase 3 y 4 (Mes 12+), y se financian "
             "exclusivamente con la caja acumulada de suscripciones de la comunidad acumuladas desde el Mes 4, eliminando cualquier gasto de bolsillo "
             "o inversión de capital previa de los fundadores."),
            ("2. Composición de Costes de Pasarela y Comisiones Ocultas",
             "Toda monetización digital cuenta con costes de intermediación financiera que se descuentan directamente en origen:\n"
             "• Comisión de Patreon: 8% sobre el PVP recaudado en el Plan Premium.\n"
             "• Comisión de Pasarela Stripe: 1.4% + 0.25 € por transacción nacional europea.\n"
             "• Retención de IRPF / IVA: Todos los servicios e-commerce se liquidan a través de una asociación cultural inicial exenta de IVA en sus cuotas comunitarias secundarias, derivando el IVA de merchandising (21%) al fabricante de Print-On-Demand (sourcing ex-ante)."),
            ("3. Presupuesto Vial Calle vs Pista Básico",
             "La decisión de hacer el coche homologable para circular por la calle introduce costes sustanciales que cambian el presupuesto. "
             "Mientras que el chasis y motor básicos de pista se estiman en 3.300 € de caja, las tasas de laboratorios de homologación (IDIADA/INTA), "
             "los catalizadores Euro 6 y el sistema de frenado de doble circuito exigen un total de 10.400 €."),
            ("4. Gráfica de Costes Comparativos (Pista vs Calle)",
             "A continuación se presenta la comparativa de costes del vehículo y los extras normativos requeridos para circular legalmente en calle:"),
            ("5. Presupuesto Operativo y Estimación Financiera Detallada",
             "A continuación se presenta el desglose del presupuesto incluyendo los costes de calle:")
        ],
        "image": "financial_breakdown.png",
        "table": {
            "cols": [110, 150, 80, 80, 80],
            "data": [
                ["Categoría Componente", "Especificación Sourcing", "Valor Canje (€)", "Coste Caja (€)", "Estrategia Financiera"],
                ["Motor de Moto Usado", "Suzuki GSX-R 600/1000cc (120-150hp)", "0", "1.200", "Patreon acumulado / Merchandising"],
                ["Estructura Chasis", "Tubos de Acero 4130 Cromoly (FIA)", "1.200", "0", "Patrocinio de Metalúrgica local"],
                ["Frenos y Dirección", "Doble circuito independiente (ITV)", "0", "1.100", "Fondos Acumulados de Patreon"],
                ["Seguridad y Luces", "Arnés FIA, faros y espejos 'E'", "0", "1.250", "Fondos Acumulados de Patreon"],
                ["Catalizador y Escape", "Silenciador DB y convertidor Euro 6", "0", "1.200", "Membresías Patreon del Mes 12+"],
                ["Tasas IDIADA / INTA", "Ensayos dinámicos e individual", "0", "2.500", "Sponsors corporativos del sector"],
                ["Laboratorio Ensayos", "Pruebas de ruido y gases en lab", "0", "1.800", "Sponsors corporativos del sector"],
                ["Software CAD/FEA", "Licencias Onshape / FEA gratuitas", "12.000", "0", "Licencia Educativa / Gratis"],
                ["TOTAL ESTIMADO VIAL", "Presupuesto Homologado Calle", "13.200 €", "10.050 €", "Financiación mixta comunitaria"]
            ]
        }
    },
    "DOC-012": {
        "category": "02_Legal_y_Finanzas",
        "title": "Investor Data Room",
        "subtitle": "Estructura de Activos para Financiación de Fase Semilla",
        "author": "Fundadores de CERO",
        "status": "APROBADO",
        "version": "v1.0",
        "date": "15.07.2026",
        "sections": [
            ("1. Estructura de la Data Room",
             "Este documento define la estructura de carpetas y archivos preparada para ser compartida con fondos de inversión semilla y ángeles inversores:\n"
             "• Carpeta 01: Corporativo e Identidad (Manifiesto, Brand Bible, Registro de Marcas).\n"
             "• Carpeta 02: Plan y Finanzas (Modelo Financiero, Proyecciones de Coste del Vehículo, Presupuesto Ejecutado).\n"
             "• Carpeta 03: Ingeniería y CAD (Planos del Chasis, Simulaciones de Suspensión, Requerimientos del Vehículo).\n"
             "• Carpeta 04: Crecimiento y Comunidad (Métricas de Tracción, Estadísticas de Audiencia, Conversión de Discord).\n"
             "• Carpeta 05: Legal (Contratos de Colaboradores, Acuerdos de Cesión de IP, Estatutos de la Sociedad Futura)."),
            ("2. Métricas de Tracción Solicitadas por Inversores",
             "El objetivo es convencer a un inversor potente de que la comunidad tiene un valor real cuantificable. Mostraremos:\n"
             "• Coste de Adquisición de Colaboradores (CAC): Actualmente 0 € debido a la tracción orgánica.\n"
             "• Horas de Ingeniería Aportadas: Suma total de las horas estimadas de los ingenieros colaboradores activos.\n"
             "• Tasa de Crecimiento Mensual de la Comunidad."),
            ("3. Uso Previsto de Fondos (Pre-Seed Goal: 50.000 €)",
             "Destinado a la creación de una sociedad limitada, contratación de seguros de pruebas, compra de motores comerciales homologados, "
             "y alquiler de un taller estable de montaje para la Fase 4.")
        ]
    },
    "DOC-013": {
        "category": "03_Ingenieria_y_Producto",
        "title": "Vehicle Requirements",
        "subtitle": "Especificación de Requerimientos Técnicos del Monoplaza de Combustión",
        "author": "Ingeniería CERO",
        "status": "APROBADO",
        "version": "v1.2",
        "date": "15.07.2026",
        "sections": [
            ("1. Filosofía del Vehículo: Ligereza y Motor de Moto",
             "El monoplaza CERO debe ser un coche de pista ultraligero propulsado por un motor de motocicleta. Se descarta la "
             "propulsión eléctrica por complejidad técnica y coste de batería. El uso de un motor Suzuki GSX-R de combustión de alta revolución "
             "(14.000 RPM) aporta una relación peso-potencia inmejorable, bajo coste y una banda sonora perfecta para contenido en redes sociales."),
            ("2. Especificaciones Técnicas Conceptuales",
             "• Motor: Suzuki GSX-R 600cc o 1000cc, 4 cilindros, DOHC, refrigeración líquida.\n"
             "• Potencia: 120 - 150 hp a 13.000 RPM.\n"
             "• Caja de Cambios: Transmisión secuencial de 6 marchas integrada en el motor de moto.\n"
             "• Peso Objetivo: Menor a 420 kg en orden de marcha.\n"
             "• Chasis: Tubular de acero cromoly (4130), jigs de soldadura sencillos.\n"
             "• Transmisión: Por cadena reforzada 530 hacia un eje trasero con diferencial autoblocante LSD o eje rígido ligero.\n"
             "• Seguridad: Cinturón de arnés de 6 puntos, interruptor de cortacorrientes general y sistema extintor FIA Appendix J."),
            ("3. Criterios de Homologación de Circuito",
             "El coche debe cumplir las directrices básicas de la FIA para eventos de Track Day, incluyendo barra antivuelco principal "
             "de acero cromoly (45mm x 2.5mm) y silenciador de escape homologado para cumplir los límites de ruido de los circuitos españoles.")
        ]
    },
    "DOC-014": {
        "category": "03_Ingenieria_y_Producto",
        "title": "Technical Architecture",
        "subtitle": "Arquitectura de Ingeniería, Chasis y Tren Motriz de Combustión",
        "author": "Ingeniería CERO",
        "status": "APROBADO",
        "version": "v1.2",
        "date": "15.07.2026",
        "sections": [
            ("1. Chasis y Configuración Mecánica",
             "Se selecciona una arquitectura de chasis tubular (Spaceframe) de acero estructural. Esto permite el corte láser de tubos y "
             "su soldadura en un taller mediano con utillajes relativamente sencillos, evitando los altos costes de moldes y autoclaves "
             "de un monocasco de fibra de carbono."),
            ("2. Tren Motriz de Combustión y Transmisión por Cadena",
             "• Motor: Montado transversalmente detrás del piloto (diseño central-trasero).\n"
             "• Caja de cambios: Secuencial de moto, operada mediante palanca de empuje/tirón en el cockpit (Push/Pull shifter).\n"
             "• Refrigeración: Radiador frontal o lateral con canalización de pontones.\n"
             "• Sistema de Escape: Escape 4-en-1 de acero inoxidable con silenciador deportivo para mantener el sonido agudo característico."),
            ("3. Sistema de Control Eléctrico Básico",
             "Un sistema de cableado simplificado basado en la ECU de moto de serie desbloqueada. Sensor de revoluciones, indicador de marchas, "
             "temperatura del agua y presión de aceite. Mantenemos la electrónica al mínimo para evitar fallos de software complejos.")
        ]
    },
    "DOC-015": {
        "category": "03_Ingenieria_y_Producto",
        "title": "Risk Register",
        "subtitle": "Matriz de Riesgos y Planes de Mitigación",
        "author": "Operaciones CERO",
        "status": "APROBADO",
        "version": "v1.0",
        "date": "15.07.2026",
        "sections": [
            ("1. Metodología de Evaluación de Riesgos",
             "Evaluamos los riesgos en función de su probabilidad (1 a 5) e impacto (1 a 5), multiplicando ambos factores para obtener un índice de severidad. "
             "Cualquier riesgo con severidad igual o superior a 12 requiere un Plan de Mitigación inmediato e informes de seguimiento semanales."),
            ("2. Tabla e Identificación de Riesgos Clave",
             "A continuación se presenta la matriz de riesgos principales y su correspondiente plan de contingencia:")
        ],
        "table": {
            "cols": [45, 135, 60, 60, 70, 130],
            "data": [
                ["Código", "Riesgo Identificado", "Prob. (1-5)", "Imp. (1-5)", "Severidad (P*I)", "Plan de Mitigación / Contingencia"],
                ["RSK-01", "Fallo de soldadura en chasis", "2", "5", "10", "FEA estructural y validación por soldador certificado."],
                ["RSK-02", "Pérdida de tracción en Discord", "3", "4", "12", "Lanzamientos constantes de retos interactivos semanales."],
                ["RSK-03", "Denegación de acceso a pista/ITV", "4", "5", "20", "Estudio previo IDIADA/INTA en la fase de CAD (Fase 3)."],
                ["RSK-04", "Rotura de cadena de transmisión", "2", "4", "8", "Cadena reforzada paso 530 y protector de cadena FIA."],
                ["RSK-05", "Retraso de piezas CNC", "3", "3", "9", "Tener 3 proveedores alternativos listos en base de datos."]
            ]
        }
    },
    "DOC-016": {
        "category": "03_Ingenieria_y_Producto",
        "title": "KPI Dashboard",
        "subtitle": "Métricas de Control de Operaciones e Ingeniería",
        "author": "Operaciones CERO",
        "status": "APROBADO",
        "version": "v1.0",
        "date": "15.07.2026",
        "sections": [
            ("1. Categorización de Métricas Clave",
             "Las métricas se dividen en tres áreas fundamentales:\n"
             "• Tracción y Audiencia (Crecimiento).\n"
             "• Velocidad y Calidad de Ingeniería (Producto).\n"
             "• Capacidad Logística e Integración (Operaciones)."),
            ("2. Gráfica de Proyecciones de Patreon",
             "A continuación se muestra de manera visual el crecimiento proyectado de las membresías premium en los primeros 24 meses:"),
            ("3. Cuadro de Control Operativo e Hitos Métricos",
             "A continuación se presentan los KPIs cuantificables definidos para monitorizar la salud operativa del proyecto:")
        ],
        "image": "kpi_projections.png",
        "table": {
            "cols": [120, 130, 80, 80, 90],
            "data": [
                ["Métrica (KPI)", "Fórmula / Origen", "Meta Semanal", "Meta Mensual", "Estado Target"],
                ["KPI-1: Followers Instagram", "Estadísticas de Cuenta", "+5.000", "+20.000", "Crítico"],
                ["KPI-2: Miembros Discord", "Estadísticas de Servidor", "+150", "+600", "Alto"],
                ["KPI-3: Commits GitHub", "Commits validados en Main", "+8", "+30", "Moderado"],
                ["KPI-4: Sourcing Barters", "Base de Datos de Canjes", "1 partner", "4 partners", "Crítico"],
                ["KPI-5: Peso de Diseño", "Modelo CAD consolidado", "N/A", "Ajustado a límites", "Control Diario"]
            ]
        }
    },
    "DOC-017": {
        "category": "00_Gobernanza_y_Operaciones",
        "title": "Weekly Review System",
        "subtitle": "Metodología de Reunión y Plantilla de Estado",
        "author": "Operaciones CERO",
        "status": "APROBADO",
        "version": "v1.0",
        "date": "15.07.2026",
        "sections": [
            ("1. Ritmo Operativo de Reuniones",
             "El equipo principal de coordinación se reúne todos los domingos a las 20:00 CEST. La reunión se limita a 45 minutos "
             "y sigue un orden del día estricto para evitar discusiones improductivas."),
            ("2. Estructura de la Reunión Semanal",
             "1. Repaso de KPIs Generales (5 minutos): Análisis de los datos semanales de tracción y desarrollo.\n"
             "2. Estado de los Departamentos (15 minutos): Cada coordinador tiene 3 minutos para detallar: Logros, Bloqueos y Plan de Acción de la semana entrante.\n"
             "3. Revisión de Bloqueos Críticos (15 minutos): Resolución colaborativa de problemas técnicos o de sourcing que impidan el avance.\n"
             "4. Planificación del Vídeo Semanal (10 minutos): Coordinación con el equipo de medios sobre el contenido de YouTube."),
            ("3. Semáforo de Salud del Proyecto (RYG)",
             "Cada hito se clasifica como: Verde (En tiempo), Amarillo (Con riesgo de retraso, requiere atención especial) o Rojo (Retrasado, requiere intervención del core team).")
        ]
    },
    "DOC-018": {
        "category": "00_Gobernanza_y_Operaciones",
        "title": "Decision Register",
        "subtitle": "Protocolo de Registro y Aprobación de Decisiones Críticas",
        "author": "Comité de Gobernanza CERO",
        "status": "APROBADO",
        "version": "v1.0",
        "date": "15.07.2026",
        "sections": [
            ("1. Introducción al Registro de Decisiones",
             "Para evitar discusiones recurrentes sobre decisiones tomadas en el pasado, toda decisión que afecte significativamente la arquitectura "
             "del vehículo, la marca, la legalidad o el presupuesto debe registrarse formalmente bajo el formato ADR (Architecture Decision Record)."),
            ("2. Proceso de Votación y Consenso",
             "Cuando surja un dilema técnico relevante (ej. soldar acero al carbono vs. usar aluminio), el equipo de ingeniería presentará un informe comparativo. "
             "La decisión se somete a debate durante 72 horas. Si no hay consenso técnico claro, el Coordinador de Ingeniería tiene el voto de calidad."),
            ("3. Plantilla Oficial de Registro de Decisiones",
             "Cada registro debe contener obligatoriamente:\n"
             "• Código Decision (ADR-XXX).\n"
             "• Título de la decisión.\n"
             "• Contexto y alternativas consideradas.\n"
             "• Decisión final adoptada y su justificación.\n"
             "• Consecuencias y cambios requeridos en otros documentos.")
        ]
    },
    "DOC-019": {
        "category": "03_Ingenieria_y_Producto",
        "title": "Supplier Database",
        "subtitle": "Base de Datos de Proveedores y Seguimiento de Materiales",
        "author": "Alianzas y Sourcing CERO",
        "status": "APROBADO",
        "version": "v1.0",
        "date": "15.07.2026",
        "sections": [
            ("1. Clasificación de Proveedores",
             "Para asegurar el suministro, catalogamos los proveedores en three categorías:\n"
             "• Tier 1: Proveedores estratégicos que donan piezas complejas o servicios de mecanizado completo bajo acuerdo firmado.\n"
             "• Tier 2: Proveedores con los que tenemos descuentos especiales o acuerdos de patrocinio parcial.\n"
             "• Tier 3: Tiendas y proveedores estándar para compras de consumibles de taller."),
            ("2. Criterios de Evaluación y Calidad",
             "Aunque las piezas sean obtenidas mediante canjes o donaciones, deben cumplir strictly los requerimientos de tolerancia y calidad "
             "definidos en los planos de ingeniería. No montaremos ninguna pieza usada o sospechosa en los sistemas de dirección, frenado o chasis principal."),
            ("3. Registro y Logística de Entregas",
             "Todas las entregas físicas se centralizarán en la dirección del taller colaborador designado para la Fase 4. Se requiere la inspección "
             "visual de cada pieza en un plazo máximo de 48 horas tras su recepción, firmando el albarán de conformidad correspondiente.")
        ]
    },
    "DOC-020": {
        "category": "01_Marca_y_Comunidad",
        "title": "Community Governance",
        "subtitle": "Gobernanza de Comunidad, Normas y Roles de Discord",
        "author": "Gobernanza y Comunidad CERO",
        "status": "APROBADO",
        "version": "v1.0",
        "date": "15.07.2026",
        "sections": [
            ("1. Estructura Meritocrática de Gobernanza",
             "CERO utiliza un modelo de gobernanza híbrido. El control del proyecto y la propiedad de la marca recaen sobre el Core Team fundador, "
             "pero la toma de decisiones técnicas secundarias está descentralizada en comités especializados elegidos por méritos de contribución."),
            ("2. Roles y Jerarquías en Discord",
             "Para organizar la comunidad de Discord, se establecen los siguientes roles:\n"
             "• Admin (Core Team): Acceso total a la administración y decisiones estratégicas corporativas.\n"
             "• Lead Engineer (Coordinadores de Área): Moderación técnica y aprobación de fusiones en GitHub.\n"
             "• Contributor Active (Colaborador Activo): Miembros que han resuelto al menos un challenge técnico.\n"
             "• Community (Comunidad General): Usuarios interesados en debatir y seguir el avance del coche."),
            ("3. Moderación y Resolución de Conflictos",
             "No se toleran comportamientos tóxicos, ataques personales o spam en los canales de debate. Los debates deben mantenerse estrictamente "
             "técnicos y constructivos. El equipo de gobernanza tiene la potestad de silenciar o expulsar a usuarios que infrinjan estas normas.")
        ]
    },
    "DOC-021": {
        "category": "02_Legal_y_Finanzas",
        "title": "Outreach and Pitch Scripts",
        "subtitle": "Plantillas de Comunicación y Guiones para Sourcing y Alianzas de Moto",
        "author": "Alianzas y Sourcing CERO",
        "status": "APROBADO",
        "version": "v1.1",
        "date": "15.07.2026",
        "sections": [
            ("1. Guion de Email para Desguaces de Motos (Suzuki GSX-R)",
             "Asunto: Colaboración CERO - Proyecto monoplaza de pista con motor de moto\n\n"
             "Estimado [Nombre del Desguace / Responsable]:\n"
             "Me pongo en contacto contigo de parte de CERO (buildcero.com), un proyecto abierto donde ingenieros y mecánicos de internet nos hemos "
             "unido para diseñar y construir un coche de carreras tubular desde 0 €.\n\n"
             "Para el tren motriz, buscamos un motor de moto Suzuki GSX-R de combustión (600cc o 1000cc). Queríamos proponeros participar "
             "como partners del proyecto mediante la donación o cesión a bajo coste de un motor usado que tengáis en stock. A cambio, ofrecemos:\n"
             "• Menciones de vuestro desguace en nuestros vídeos semanales de YouTube de montaje del motor, donde vuestra marca tendrá un impacto enorme ante "
             "entusiastas del motor.\n"
             "• Logotipo de vuestro negocio grabado por láser en el chasis físico del monoplaza.\n"
             "• Enlaces directos y banners en buildcero.com y en nuestra comunidad de Discord.\n\n"
             "¿Podemos agendar una llamada rápida de 5 minutos para ver si os cuadra la propuesta?\n\n"
             "Atentamente,\n"
             "[Tu Nombre]\n"
             "buildcero.com"),
            ("2. Guion para Talleres de Soldadura / CNC",
             "Asunto: Colaboración técnica CERO - Proyecto monoplaza eléctrico comunitario\n\n"
             "Estimado [Nombre del responsable / Taller]:\n"
             "Me pongo en contacto contigo en representación de CERO (buildcero.com), una iniciativa comunitaria donde estamos diseñando "
             "y construyendo un vehículo monoplaza de carreras desde 0 € con el apoyo de ingenieros y estudiantes de todo el país.\n\n"
             "Hemos completado el diseño del chasis tubular en CAD y buscamos un partner de manufactura local para el corte láser de tubos "
             "y soldadura TIG de precisión. A cambio, ofrecemos:\n"
             "• Presencia del logotipo de tu taller grabado con láser directamente en el chasis físico del coche.\n"
             "• Menciones dedicadas en nuestros vídeos semanales de YouTube (donde mostramos todo el proceso de soldadura en el taller).\n"
             "• Enlace directo y promoción constante en nuestras redes sociales y comunidad de Discord (>5.000 seguidores en crecimiento).\n\n"
             "¿Te interesaría tener una breve llamada de 5 minutos para ver si podemos encajar vuestros servicios en esta fase del proyecto?\n\n"
             "Atentamente,\n"
             "[Tu Nombre]\n"
             "buildcero.com"),
            ("3. Guion de Colaboración con Universidades",
             "Propuesta formal para departamentos de ingeniería mecánica de universidades locales. El objetivo es proponer el uso del monoplaza "
             "CERO como proyecto de fin de grado para alumnos o el intercambio de horas en el banco de pruebas hidráulico y de tracción torsional "
             "a cambio de tutorías del comité técnico de CERO a los alumnos participantes.")
        ]
    },
    "DOC-022": {
        "category": "02_Legal_y_Finanzas",
        "title": "Crowdfunding and Merch Launch Plan",
        "subtitle": "Plan de Lanzamiento de Suscripciones y Línea de Producto",
        "author": "Medios y Crecimiento CERO",
        "status": "APROBADO",
        "version": "v1.2",
        "date": "15.07.2026",
        "sections": [
            ("1. Fase de Cero Gasto y Cero Ventas (Meses 1 - 3)",
             "Durante la Fase 1 del proyecto CERO, no se intenta comercializar ningún producto, camisetas ni membresías. El objetivo "
             "es 100% el desarrollo técnico del CAD en Onshape y el crecimiento puramente orgánico de la comunidad en redes sociales y Discord. "
             "Se prohíbe abrir tiendas online o contratar dominios de pago no esenciales para no forzar costes derivados antes de "
             "contar con masa crítica de usuarios y credibilidad."),
            ("2. Estrategia de Merchandising sin Inversión (Mes 7+)",
             "Para la monetización física a partir del Mes 7, se utilizará estrictamente un modelo de impresión bajo demanda (Print-on-Demand) "
             "conectado a una plataforma de e-commerce con plan gratuito (ej. Ko-fi o Big Cartel). Esto garantiza que el inventario cuesta 0 € "
             "ya que el producto solo se fabrica una vez que el comprador final realiza el pago completo. Los diseños serán de corte técnico "
             "explotado (CAD blueprints):\n"
             "• T-Shirt Blueprint V1: Camiseta técnica en algodón blanco roto con el plano del chasis en la espalda. (PVP: 25 € / Coste: 11 €).\n"
             "• Póster de chapa técnica de aluminio grabado: Plano técnico de dimensiones generales del coche. (PVP: 35 € / Coste: 14 €)."),
            ("3. Tiers de Patreon y Discord Premium (Lanzamiento en Mes 4+)",
             "Las membresías recurrentes se lanzarán en el Mes 4 para acumular caja libre y financiar la compra del material físico (motor usado) en el Mes 12:")
        ],
        "table": {
            "cols": [90, 80, 160, 170],
            "data": [
                ["Tier de Suscripción", "Precio Mensual", "Beneficios en Discord", "Beneficios en el Vehículo"],
                ["Tier Boceto", "2,99 €", "Acceso a canales de debate técnico privado.", "Nombre en la sección de agradecimientos web."],
                ["Tier CAD Active", "5,99 €", "Acceso anticipado de 48h a archivos GitHub CAD.", "Votaciones en decisiones secundarias de diseño."],
                ["Tier Core Sponsor", "19,99 €", "Reunión mensual por voz con el Core Team.", "Nombre grabado por láser directamente en el chasis físico."]
            ]
        }
    },
    "DOC-023": {
        "category": "03_Ingenieria_y_Producto",
        "title": "European Homologation and Testing Protocol",
        "subtitle": "Ruta Normativa Europea y Protocolos de Ensayos en Pista de Combustión",
        "author": "Legal y Cumplimiento CERO",
        "status": "APROBADO",
        "version": "v1.2",
        "date": "15.07.2026",
        "sections": [
            ("1. Homologación Individual de Vehículos en España",
             "Para circular por la vía pública en España, el monoplaza de chasis tubular debe someterse a un procedimiento de "
             "Homologación Individual de Vehículos (según el Real Decreto 750/2010 y Reglamento UE 2018/858). Esto requiere la redacción "
             "de una Ficha Técnica Reducida por un ingeniero colegiado y ensayos físicos realizados por un Servicio Técnico de Homologación "
             "acreditado (ej: IDIADA o INTA)."),
            ("2. Requerimientos de Calle Obligatorios (Directivas Europeas)",
             "• Emisiones de Escape: Al instalar un motor Suzuki GSX-R de moto, el coche debe cumplir los límites de emisiones establecidos "
             "para turismos (categoría M1) correspondientes al año de matriculación (Euro 6d/Euro 6e), lo que exige instalar un catalizador de triple vía "
             "con sonda lambda de control y un mapeado específico de la ECU.\n"
             "• Iluminación y Espejos: Todos los proyectores de luz (cortas, largas, intermitentes, posición, antiniebla trasero e iluminación de matrícula) "
             "y retrovisores deben tener marcado de homologación 'E' y cumplir con las cotas de altura e inclinación reglamentarias.\n"
             "• Frenado y Mandos: Sistema de frenado de doble circuito hidráulico con balanceador de frenada y freno de mano mecánico de estacionamiento independiente.\n"
             "• Radio de Aristas Exteriores: Para proteger a peatones en caso de impacto, cualquier arista exterior o elemento de carrocería expuesto "
             "debe tener un radio de curvatura mínimo de 2.5 mm."),
            ("3. Protocolo de Pruebas Físicas en Laboratorio Acreditado",
             "A continuación se presenta la secuencia de ensayos que el prototipo deberá superar en las instalaciones del Servicio Técnico:")
        ],
        "table": {
            "cols": [65, 120, 180, 139],
            "data": [
                ["Ensayo", "Directiva/Reglamento", "Descripción de la Prueba", "Criterio de Aceptación"],
                ["Ruido Dinámico", "Reglamento ONU 51", "Paso acelerado a 50 km/h en 3ª marcha.", "Nivel sonoro menor a 74 dB(A)."],
                ["Emisiones Gases", "Reglamento UE 2017/1151", "Ciclo WLTP en banco de rodillos climático.", "CO, NOx y HC bajo límites Euro 6."],
                ["Eficacia Frenado", "Reglamento ONU 13-H", "Prueba de frenado a 100 km/h y fallo de circuito.", "Deceleración > 5.8 m/s² sin desvío."],
                ["Compatibilidad EM", "Reglamento ONU 10", "Prueba en cámara anecoica electromagnética.", "Sin interferencias en radiación y cableado."]
            ]
        }
    },
    "DOC-024": {
        "category": "02_Legal_y_Finanzas",
        "title": "Sourcing and Logistics Copilot Guide",
        "subtitle": "Guía de Acompañamiento Práctico de Adquisición y Transporte para No Iniciados",
        "author": "Alianzas y Sourcing CERO",
        "status": "APROBADO",
        "version": "v1.0",
        "date": "15.07.2026",
        "sections": [
            ("1. Introducción al Sourcing Práctico",
             "Esta guía ha sido diseñada específicamente para el fundador del proyecto CERO. Su objetivo es acompañarte paso a paso "
             "en la obtención física de las piezas sin que necesites conocimientos previos de mecánica. Aquí te explicamos exactamente qué buscar, "
             "qué preguntar al teléfono, cómo comprobar el estado de la pieza y cómo transportarla a tu garaje sin dañar tu coche ni la pieza."),
            ("2. Cómo Conseguir el Motor de Moto Suzuki GSX-R 600",
             "El motor objetivo es el de una Suzuki GSX-R 600 (años 2004 a 2008) por su gran stock en España y fiabilidad:\n"
             "• Dónde buscar: Llama a desguaces de motos especializados en España (ej: Motostión en Madrid, Desguace Motocoche, Desguaces El Choque).\n"
             "• Herramientas a traer al desguace: Maletín de llaves de vaso métricas (vasos de 10, 12, 14 y 17mm), mango articulado (breaker bar) de media pulgada, destornillador plano largo y alicates de punta.\n"
             "• Guion telefónico exacto:\n"
             "   - 'Hola, buenas. Buscaba un motor para una Suzuki GSX-R 600cc del año 2006. ¿Tenéis alguno en stock?'\n"
             "   - SI TIENEN: 'Perfecto. ¿Qué kilometraje tiene certificado y qué precio tiene?'\n"
             "   - PREGUNTA CRÍTICA: '¿El motor viene completo con su cableado eléctrico de motor, cuerpo de inyección y la centralita (ECU)?'\n"
             "   *Nota*: Si no viene con cableado e inyección, no lo compres. Comprar la electrónica suelta después es caro y un laberinto para un principiante.\n"
             "• Cómo verificar si el motor está sano (sin abrirlo):\n"
             "   - Pídele al mecánico del desguace que intente girar el cigüeñal a mano usando una llave en la tuerca del alternador. Si el motor gira libremente sin trabarse, está bien (no está gripado).\n"
             "   - Revisa visualmente que no tenga grietas en las tapas de aluminio, especialmente en el cárter de aceite (zona inferior) y la culata (zona superior)."),
            ("3. Logística y Transporte: Cómo llevártelo a casa sin derrames",
             "Un motor de moto de 600cc pesa unos 60-70 kg. Lo pueden levantar dos personas con facilidad, pero es un bloque metálico lleno de aceite. "
             "Sigue estas pautas para transportarlo de forma segura:\n"
             "• Drenado previo: Antes de moverlo, retira el tornillo del cárter inferior con una llave de 17mm y drena todo el aceite en una garrafa para evitar fugas desastrosas en la tapicería de tu maletero.\n"
             "• Preparación del maletero: Pon cartones gruesos y mantas viejas en el fondo del maletero de tu coche. El motor siempre tiene restos de aceite y marcará la tapicería si no la proteges.\n"
             "• Soporte rígido: Coloca el motor dentro de una caja de plástico fuerte de fruta o sobre un palet de madera pequeño. El motor no se sostiene de pie por sí solo; si lo dejas suelto, volcará en la primera curva, rompiendo algún sensor de plástico externo.\n"
             "• Cinchas de amarre (Tie-downs): Sujeta el motor con cinchas a las argollas del maletero para que no se mueva. Si das un frenazo, 70 kg de metal pueden ser muy peligrosos.\n"
             "• Al llegar a casa: No lo dejes en el suelo húmedo. Colócalo sobre un banco de madera o fabrica un soporte sencillo con tacos de madera para mantenerlo elevado y derecho."),
            ("4. Cómo Encontrar un Espacio Físico (Garaje o Taller Colaborador)",
             "Para montar el coche no necesitas un taller profesional de F1, pero sí un espacio mínimo:\n"
             "• Requisitos mínimos: Suelo plano de hormigón (para usar el gato y caballetes), 3 enchufes de corriente estándar de 230V, iluminación LED decente y espacio para rodear el coche (unos 4x5 metros mínimos).\n"
             "• Cómo conseguirlo gratis (El Canje): Si no tienes local, busca un taller mecánico de barrio local o un garaje de un aficionado. Ofréceles 'el rincón CERO'. A cambio de cederte el espacio para soldar el chasis los fines de semana, tú colocas el cartel de su taller detrás en todos tus vídeos semanales de YouTube e Instagram, llevándoles clientes locales de mantenimiento.")
        ]
    },
    "DOC-025": {
        "category": "00_Gobernanza_y_Operaciones",
        "title": "Critical Project Audit and Risk Analysis",
        "subtitle": "Auditoría de Viabilidad y Análisis Crítico del Ecosistema de Proyecto",
        "author": "Dirección Estratégica CERO",
        "status": "APROBADO",
        "version": "v1.0",
        "date": "15.07.2026",
        "sections": [
            ("1. El Bucle de la Muerte de la Tracción de $0 (Day-1 Exposure Loop)",
             "El plan maestro asume que conseguiremos patrocinios de materiales (acero cromoly, motor usado de 1.200 €) a cambio de "
             "'exposición y marketing en redes'. Sin embargo, en el Día 1 la cuenta tiene 40 seguidores y 3 posts. El valor comercial "
             "de canje de nuestra exposición es exactamente 0 € para cualquier desguace o metalúrgica. Ninguna empresa seria baratará "
             "materiales a cambio de menciones ante una audiencia inexistente.\n"
             "• Solución / Mitigación: La Fase 1 (Meses 1-3) debe dedicarse exclusivamente a crear 'ruido visual' y comunidad. Mostraremos debates, "
             "diseños de chasis en 3D impactantes en CAD y encuestas sobre la mecánica para inflar la cuenta a >5.000 seguidores "
             "ANTES de realizar la primera llamada de sourcing, evitando quemar los leads de proveedores con propuestas de escaso valor."),
            ("2. La Trampa del 'Ingeniero de Discord' (Falta de Validación Técnica)",
             "Dado que el fundador no tiene conocimientos de mecánica ni de ingeniería automotriz, CERO está a merced de los archivos CAD "
             "y cálculos FEA que envíen voluntarios anónimos de Discord. Un error en la fatiga de soldadura en los brazos de suspensión "
             "o en el arco antivuelco puede provocar un fallo estructural catastrófico en pista, poniendo en peligro real la vida del piloto (que será el fundador).\n"
             "• Solución / Mitigación: Se establece un filtro de seguridad estricto. Aunque el diseño esté descentralizado, la aprobación del "
             "chasis físico requerirá de la validación firmada de un Ingeniero Colegiado y la revisión de soldadura por un soldador certificado de "
             "forma externa antes de rodar en pista, financiado por la caja comunitaria acumulada."),
            ("3. La Logística Oculta y los Gastos Hormiga",
             "Aunque el coche cueste teóricamente 0 € en mano de obra y consigamos piezas por canje, existen costes físicos que no se pueden baratar:\n"
             "• Alquiler de furgoneta o grúa para mover el motor de moto y el chasis tubular entre el taller y el garaje.\n"
             "• Consumibles de taller: discos de radial, electrodos, gas argón para soldar, tornillería de alta resistencia (grado 8.8 o superior), "
             "gasolina para pruebas, y herramientas manuales.\n"
             "• Estos pequeños gastos sumarán entre 300 € y 600 € de caja real durante los primeros 12 meses.\n"
             "• Solución / Mitigación: El fondo de Patreon del Mes 4 debe reservarse prioritariamente para este fondo de maniobra operativo (consúmibles), "
             "prohibiendo la compra de componentes grandes hasta tener cubiertos los gastos hormiga."),
            ("4. Riesgo de Abandono (Voluntariado Inconstante)",
             "Los colaboradores de internet participan por entusiasmo. Cuando el trabajo CAD se vuelve monótono o surgen dificultades de "
             "cálculo complejas, la participación decae rápidamente. No podemos depender de un único 'diseñador estrella'.\n"
             "• Solución / Mitigación: Documentar en público las tareas de forma modular e independiente en GitHub. Si un colaborador "
             "desaparece, otro puede clonar el repositorio y continuar el soporte de suspensión o dirección desde el mismo punto.")
        ]
    },
    "DOC-026": {
        "category": "02_Legal_y_Finanzas",
        "title": "Competitor Analysis and Market Benchmark",
        "subtitle": "Análisis de Competidores de Internet, Casos Históricos y Propuesta de Valor Única",
        "author": "Dirección Estratégica CERO",
        "status": "APROBADO",
        "version": "v1.0",
        "date": "15.07.2026",
        "sections": [
            ("1. Benchmark del Mercado: Referentes de Coches Hechos en Internet",
             "Analizamos los competidores indirectos y creadores de contenido que han intentado construir vehículos en público:\n"
             "• Project Binky (Bad Obsession Motorsport - YT): El referente absoluto de calidad. Tardaron más de 10 años en terminar "
             "un Mini con tracción 4x4. Su error crítico fue el exceso de perfeccionismo artesanal de una sola persona y la nula delegación en la comunidad.\n"
             "• Wesley Kagan (YT): Construyó una réplica de Fórmula 1 de los años 50 usando un motor de Mazda Miata en 18 meses. Liberó los "
             "planos de su suspensión. Demostró que un monoplaza con motor sencillo de coche/moto es viable en plazos cortos si se usan piezas comerciales.\n"
             "• Local Motors (Rally Fighter): Proyecto industrial estadounidense que diseñó un coche todoterreno mediante crowdsourcing de internet. "
             "Tuvieron éxito y vendieron unidades, pero requerían millones de euros en infraestructura de micro-fábricas.\n"
             "• Equipos de Formula Student: Universidades de todo el mundo construyen monoplazas anualmente desde 0 €. Tienen presupuestos de "
             "miles de euros donados por empresas y equipos cerrados de 30 estudiantes. CERO se diferencia al abrir el diseño a cualquier persona de internet."),
            ("2. Propuesta de Valor Única de CERO (Nuestra Diferenciación)",
             "¿Por qué CERO es único ante patrocinadores y comunidad?\n"
             "1. Gobernanza Descentralizada: No es un youtuber construyendo su coche en su garaje. Las decisiones clave se votan en Discord, "
             "generando un sentimiento de co-propiedad emocional en la comunidad.\n"
             "2. Licencia CC BY-NC 4.0: Cualquiera puede clonar el CAD de buildcero.com y construirse su coche, democratizando la ingeniería.\n"
             "3. Transparencia de Bootstrapping Real: La mayoría de canales ocultan sus presupuestos. CERO muestra las facturas de 0 € y los "
             "problemas reales de la falta de financiación, creando un 'reality show' de ingeniería cruda y adictiva.")
        ]
    },
    "DOC-027": {
        "category": "00_Gobernanza_y_Operaciones",
        "title": "Project Phase Dependencies and Gantt",
        "subtitle": "Secuencia Lógica de Construcción, Prerrequisitos de Hitos y Duración de Fases",
        "author": "Gestión de Proyectos CERO",
        "status": "APROBADO",
        "version": "v1.0",
        "date": "15.07.2026",
        "sections": [
            ("1. Duración del Proyecto y Criterio de Realismo",
             "Aunque el objetivo es terminar el monoplaza de combustión en 28 meses, la falta de presupuesto inicial exige un "
             "control estricto de los prerrequisitos técnicos y la normativa de calle. Si un hito crítico se retrasa, el proyecto se congela automáticamente para "
             "evitar costes innecesarios. No compraremos materiales si no hay espacio físico donde almacenarlos."),
            ("2. Gráfico del Cronograma de Fases y Dependencias",
             "A continuación se ilustra el cronograma general y la distribución temporal de las fases del monoplaza:"),
            ("3. Dependencias Críticas (Qué debe estar listo antes de qué)",
             "Para evitar fallos de montaje catastróficos, se establecen las siguientes dependencias innegociables:\n"
             "• Dependencia 1: Motor Suzuki GSX-R físico medido (Fase 1) -> Requisito para Chasis CAD final (Fase 3).\n"
             "No se puede cerrar el diseño de la parte trasera del chasis tubular en CAD sin haber escaneado en 3D (o medido físicamente) "
             "el motor Suzuki de desguace. Las tolerancias de los soportes del motor y la alineación del piñón de transmisión con el eje trasero "
             "deben ser exactas a nivel de décimas de milímetro para evitar que la cadena descarrile a alta velocidad.\n"
             "• Dependencia 2: Congelación de CAD (Fase 3) -> Requisito para Encargar el Corte Láser (Fase 4).\n"
             "No se puede solicitar a los patrocinadores el corte de tubos de acero 4130 cromoly antes de congelar las dimensiones del chasis. "
             "Cualquier modificación posterior obligará a tirar tubos inservibles, destruyendo la viabilidad financiera de 0 €.\n"
             "• Dependencia 3: Cesión de Taller y Construcción de Jig (Fase 4) -> Requisito para Soldadura de Chasis (Fase 5).\n"
             "Está prohibido empezar a soldar tubos en el aire. La soldadura TIG genera una distorsión térmica masiva que revira el metal. "
             "Se requiere construir una mesa de utillaje rígida (jig) de madera o acero atornillada al suelo plano para mantener los tubos en su "
             "sitio exacto mientras se sueldan.\n"
             "• Dependencia 4: Circuitos de Dirección, Suspensión y Frenado (Fase 5) -> Requisito para Instalar el Escape y Motor (Fase 6).\n"
             "La ergonomía y la seguridad de guiado son prioritarias. El motor de moto y el escape se montarán solo cuando la dirección manual "
             "y el pedalier de freno doble estén fijados y validados.\n"
             "• Dependencia 5: Ensayos de Gases y Calibración de Emisiones (Fase 6) -> Requisito para Homologación de Calle IDIADA (Fase 7).\n"
             "No se puede presentar el coche en las instalaciones de IDIADA para las pruebas dinámicas sin haber configurado y mapeado "
             "la sonda lambda y el catalizador Euro 6 en banco de potencia, asegurando que cumple los límites en frío.")
        ],
        "image": "project_timeline_gantt.png"
    },
    "DOC-028": {
        "category": "00_Gobernanza_y_Operaciones",
        "title": "Multidisciplinary Team Audit and Strategic Overhaul",
        "subtitle": "Auditoría del Equipo Técnico, Lecciones de Wikispeed/Local Motors y Estándares FSAE",
        "author": "Comité Técnico Multidisciplinar CERO",
        "status": "APROBADO",
        "version": "v1.0",
        "date": "15.07.2026",
        "sections": [
            ("1. Análisis de Precedentes de la Industria (Wikispeed vs. Local Motors)",
             "CERO aprende de los fallos estratégicos de sus predecesores abiertos:\n"
             "• Wikispeed demostró que un equipo distribuido puede ensamblar un coche en meses usando modularidad extrema. Sin embargo, fallaron en "
             "la viabilidad de financiación y el escalado industrial debido a la falta de un control técnico centralizado y la complejidad de la homologación de calle.\n"
             "• Local Motors tuvo éxito con el Rally Fighter de código abierto, pero quebraron en 2022 debido a un cambio tecnológico masivo (el shuttle autónomo Olli) "
             "que requirió millones de dólares en desarrollo de software de nivel 4 y certificaciones gubernamentales inalcanzables.\n"
             "• Conclusión para CERO: Nos mantendremos estrictamente en un monoplaza de pista de combustión de baja complejidad y no intentaremos pivotar hacia "
             "sistemas autónomos o eléctricos comerciales de alto coste regulatorio. Enfocamos la homologación de calle mediante el procedimiento simplificado "
             "de homologación individual (ITV individual) bajo marcas de homologación 'E' preexistentes."),
            ("2. Estándares Técnicos del Chasis (Normas Formula SAE / FSAE)",
             "Para garantizar la seguridad física y la resistencia estructural del chasis espacial de CERO, se adoptan los criterios del reglamento FSAE:\n"
             "• Tubo del Arco Antivuelco Principal (Main Hoop): Acero al cromo-molibdeno 4130, con diámetro exterior mínimo de 25.4 mm (1.0 pulgada) "
             "y espesor de pared mínimo de 2.0 mm (0.095 pulgadas). El límite elástico debe ser superior a 360 MPa.\n"
             "• Tubos de Impacto Lateral y Diagonales: Diámetro mínimo de 25.0 mm y espesor de pared de 1.2 mm.\n"
             "• Control de Soldadura (Welding Coupons): Todos los soldadores colaboradores deben pasar una prueba destructiva previa. Deben soldar una junta "
             "de muestra (cupón de acero 4130) y enviarla a un laboratorio universitario colaborador para ser sometida a un ensayo de tracción. Solo si el "
             "ensayo valida que la rotura ocurre en el metal base y no en la costura de soldadura, el voluntario podrá soldar el chasis físico."),
            ("3. Gráfica de Resistencia de Materiales",
             "A continuación se presenta la comparativa de resistencia elástica de los tubos según el material y espesor seleccionados:"),
            ("4. Plan de Pruebas y Homologación en Pista (Homologation Gates)",
             "El monoplaza no rodará en calle ni pista abierta sin pasar tres puertas de control técnicas:\n"
             "• Gate 1 (CAD Validation): Verificación por análisis de elementos finitos (FEA) de flexión torsional de 2.500 N-m/grado.\n"
             "• Gate 2 (Welding Audit): Inspección por líquidos penetrantes en el 100% de las juntas soldadas del arco de seguridad para descartar porosidades.\n"
             "• Gate 3 (Dynamic Safety): Ensayo de frenado estático a 80 bar de presión y parada total desde 100 km/h en menos de 4.2 segundos.")
        ],
        "image": "fsae_structural_equivalency.png"
    }
}


def make_styled_table(data, col_widths, body_style, header_style):
    table_data = []
    header_row = [Paragraph(f"<b>{cell}</b>", header_style) for cell in data[0]]
    table_data.append(header_row)
    
    for row in data[1:]:
        body_row = []
        for cell in row:
            body_row.append(Paragraph(cell, body_style))
        table_data.append(body_row)
        
    t = Table(table_data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1C1C1E')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E5EA')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8F9FA'), colors.HexColor('#FFFFFF')]),
    ]))
    return t


def create_pdf(doc_id, doc_info, output_dir, assets_dir):
    filename = f"{doc_id}_{doc_info['title'].replace(' ', '_').replace('&', 'and')}.pdf"
    filepath = os.path.join(output_dir, filename)
    
    pdf = SimpleDocTemplate(
        filepath,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=80,
        bottomMargin=80
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=26,
        textColor=colors.HexColor('#000000'),
        spaceAfter=15,
        alignment=1
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#8E8E93'),
        spaceAfter=30,
        alignment=1
    )
    
    h1_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor('#000000'),
        spaceBefore=18,
        spaceAfter=8,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#1C1C1E'),
        spaceAfter=12
    )
    
    meta_label_style = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#8E8E93')
    )
    
    meta_val_style = ParagraphStyle(
        'MetaValue',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#1C1C1E')
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white
    )

    story = []
    
    # COVER PAGE
    story.append(Spacer(1, 380))
    story.append(Paragraph(doc_id, ParagraphStyle('CoverDocId', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=colors.HexColor('#FF3B30'), alignment=1)))
    story.append(Paragraph(doc_info['title'].upper(), title_style))
    story.append(Paragraph(doc_info['subtitle'], subtitle_style))
    story.append(Spacer(1, 15))
    
    meta_data = [
        [Paragraph("AUTOR:", meta_label_style), Paragraph(doc_info['author'].upper(), meta_val_style), Paragraph("ESTADO:", meta_label_style), Paragraph(doc_info['status'], meta_val_style)],
        [Paragraph("VERSIÓN:", meta_label_style), Paragraph(doc_info['version'], meta_val_style), Paragraph("FECHA:", meta_label_style), Paragraph(doc_info['date'], meta_val_style)]
    ]
    
    meta_table = Table(meta_data, colWidths=[80, 170, 70, 184])
    meta_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E5EA')),
    ]))
    
    story.append(meta_table)
    story.append(PageBreak())
    
    # RUNNING CONTENT
    for section_title, section_text in doc_info['sections']:
        story.append(Paragraph(section_title, h1_style))
        paragraphs = section_text.split('\n')
        for p_text in paragraphs:
            if p_text.strip():
                if p_text.strip().startswith('•') or p_text.strip().startswith('-') or (p_text.strip()[0].isdigit() and p_text.strip()[1] == '.'):
                    bullet_style = ParagraphStyle(
                        'BulletCustom',
                        parent=body_style,
                        leftIndent=15,
                        firstLineIndent=-10
                    )
                    story.append(Paragraph(p_text.strip(), bullet_style))
                else:
                    story.append(Paragraph(p_text.strip(), body_style))
        story.append(Spacer(1, 6))
        
    if "image" in doc_info:
        img_path = os.path.join(assets_dir, doc_info["image"])
        if os.path.exists(img_path):
            story.append(Spacer(1, 10))
            story.append(Image(img_path, width=400, height=200))
            story.append(Spacer(1, 10))
        
    if "table" in doc_info:
        story.append(Spacer(1, 10))
        table_flowable = make_styled_table(
            doc_info['table']['data'], 
            doc_info['table']['cols'],
            body_style,
            table_header_style
        )
        story.append(table_flowable)
        story.append(Spacer(1, 10))
        
    pdf.doc_id = doc_id
    pdf.doc_title = doc_info['title']

    pdf.build(story, canvasmaker=CeroNumberedCanvas)
    print(f"Generado PDF: {filename}")


def create_markdown(doc_id, doc_info, output_dir):
    filename = f"{doc_id}_{doc_info['title'].replace(' ', '_').replace('&', 'and')}.md"
    filepath = os.path.join(output_dir, filename)
    
    content = []
    content.append(f"# {doc_id}: {doc_info['title']}")
    content.append(f"**{doc_info['subtitle']}**\n")
    content.append(f"- **Autor**: {doc_info['author']}")
    content.append(f"- **Estado**: {doc_info['status']}")
    content.append(f"- **Versión**: {doc_info['version']}")
    content.append(f"- **Fecha**: {doc_info['date']}\n")
    content.append("---")
    
    if doc_id == "DOC-004":
        content.append("\n### DIAGRAMA DE FLUJO OPERATIVO\n")
        content.append("```text\n"
                       "  [ Contenido Viral Shorts ] ──> [ Tracción a Web (buildcero.com) ]\n"
                       "                │\n"
                       "                ▼\n"
                       "  [ Comunidad de Discord ] ──> [ Tareas/Challenges en GitHub ]\n"
                       "                │\n"
                       "                ▼\n"
                       "  [ Colaboradores Activos ] ──> [ Partners / Recursos / Prototipo ]\n"
                       "```\n")
                       
    for section_title, section_text in doc_info['sections']:
        content.append(f"\n## {section_title}\n")
        content.append(section_text)
        
    if "table" in doc_info:
        content.append("\n### Tabla de Referencia / Calendario\n")
        table_data = doc_info['table']['data']
        headers = table_data[0]
        content.append("| " + " | ".join(headers) + " |")
        content.append("| " + " | ".join(["---"] * len(headers)) + " |")
        for row in table_data[1:]:
            content.append("| " + " | ".join(row) + " |")
        content.append("\n")
        
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(content))
    print(f"Generado MD:  {filename}")


# Generates the 4-page Landscape Monthly Model Social Media Calendar (16 Weeks).
def create_landscape_calendar(output_dir):
    filepath = os.path.join(output_dir, "DOC-006_Content_OS_Landscape.pdf")
    
    pdf = SimpleDocTemplate(
        filepath,
        pagesize=(792, 612),
        leftMargin=36,
        rightMargin=36,
        topMargin=45,
        bottomMargin=45
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CalendarTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor('#000000'),
        alignment=0
    )
    
    subtitle_style = ParagraphStyle(
        'CalendarSub',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#8E8E93'),
        alignment=0
    )
    
    header_cell_style = ParagraphStyle(
        'HeaderCell',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=1
    )
    
    cell_style = ParagraphStyle(
        'CellText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.5,
        leading=8.5,
        textColor=colors.HexColor('#1C1C1E')
    )
    
    cell_title_style = ParagraphStyle(
        'CellTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=9,
        textColor=colors.HexColor('#FF3B30')
    )

    story = []
    col_widths = [102.8] * 7
    
    def make_cell(day_title, topic_text):
        return [
            Paragraph(f"<b>{day_title}</b>", cell_title_style),
            Spacer(1, 3),
            Paragraph(topic_text, cell_style)
        ]

    headers = [
        Paragraph("LUNES (TikTok/Reel)", header_cell_style),
        Paragraph("MARTES (Carousel)", header_cell_style),
        Paragraph("MIÉRCOLES (Taller/Short)", header_cell_style),
        Paragraph("JUEVES (Post X/LinkedIn)", header_cell_style),
        Paragraph("VIERNES (Edu/Short)", header_cell_style),
        Paragraph("SÁBADO (YouTube)", header_cell_style),
        Paragraph("DOMINGO (Discord)", header_cell_style)
    ]
    
    # MONTH 1: Launch & Motor Selection (W1-W4)
    m1_w1 = [
        make_cell("W1: Lanzamiento", "Hook: ¿Construir un coche de carreras real con 0 euros? Buscamos ingenieros y mecánicos en TikTok.\nVisual: Fundador hablando a cámara frente a pizarra vacía.\nCTA: Enlace a Discord en bio."),
        make_cell("W1: Explicación", "Carrusel: Presentando las reglas de CERO y el CAD de Onshape libre. ¿Cómo unirte al equipo?\nVisual: Captura explotada de un chasis tubular genérico.\nCTA: Deja tu comentario en Onshape."),
        make_cell("W1: Taller", "Short: Buscando el motor Suzuki GSX-R 600. Llamada al primer desguace en directo.\nVisual: Pantalla dividida con llamada telefónica y desguace.\nCTA: ¿Deberíamos ir a desguace físico?"),
        make_cell("W1: X Debate", "Post: ¿Suzuki GSX-R 600cc de 120hp o GSX-R 1000cc de 180hp para el chasis? Razona tu respuesta.\nVisual: Imagen lado a lado de ambos motores.\nCTA: Comenta con tu opción técnica."),
        make_cell("W1: Edu Short", "Short: Por qué usamos motores de moto (14.000 RPM, peso pluma, cambio secuencial integrado).\nVisual: Animación rápida de caja secuencial.\nCTA: ¿Qué motor suena mejor?"),
        make_cell("W1: Episodio 1", "YT: 'PROYECTO CERO: Buscando ingenieros por internet para hacer un coche real desde 0 €.'\nEstructura: Intro del reto -> Llamadas desguaces -> Setup del Discord.\nDuración: 12 mins."),
        make_cell("W1: Discord", "Reunión de voz: Elección oficial de la cilindrada de motor. Votación de comunidad. Orden del día: 1. Presupuesto, 2. Peso/potencia, 3. Fiabilidad del desguace. Hora: 20:00 CEST.")
    ]
    m1_w2 = [
        make_cell("W2: Ergonomía", "Hook: Cómo meter al piloto en un chasis tubular estrecho. Estudios de posición en Onshape.\nVisual: Modelo 3D de maniquí en posición de conducción.\nCTA: ¿Prefieres ir tumbado o recto?"),
        make_cell("W2: CAD chasis", "Carrusel: Vistas de alambre del espacio del chasis. Cotas del arco antivuelco FIA.\nVisual: Planos técnicos con cotas en rojo.\nCTA: ¿Falta triangulación en el arco?"),
        make_cell("W2: Medidas", "Short: ¿Cómo medimos el motor de moto sin planos oficiales? Fotogrametría con móvil.\nVisual: Captura de pantalla de la nube de puntos 3D.\nCTA: ¿Conocías este truco de escaneo?"),
        make_cell("W2: X Debate", "Post: ¿Embrague hidráulico o por cable de acero clásico? Pros/contras de mantenimiento.\nVisual: Diagrama simplificado de pedal de embrague. CTA: Comenta tu experiencia."),
        make_cell("W2: Edu Short", "Short: ¿Qué es el acero 4130 cromoly y por qué no usamos acero dulce de ferretería?\nVisual: Prueba de flexión teórica en barra de acero. CTA: Comenta si soldarías con TIG o MIG."),
        make_cell("W2: Episodio 2", "YT: 'Diseñando el chasis en CAD y metiendo el motor Suzuki en Onshape (Fase conceptual).'\nEstructura: Tutorial Onshape -> Feedback de Discord -> Ajustes de cockpit. Duración: 15 mins."),
        make_cell("W2: Discord", "Voto Discord: Elección del tipo de pedalera (colgante vs pivotada en suelo). Duración del voto: 24 horas. Requisito: Justificar en el canal #pedales.")
    ]
    m1_w3 = [
        make_cell("W3: FEA Simul", "Hook: Simulando un choque a 80 km/h en ordenador. ¿Se dobla el chasis de CERO?\nVisual: Animación de deformación de chasis coloreada. CTA: ¿Crees que aguantará el arco?"),
        make_cell("W3: CFD Aero", "Carrusel: Colores de presión de aire en carrocería conceptual. Resistencia aerodinámica. Visual: Renders de flujo de aire alrededor del coche. CTA: ¿Deberíamos ensanchar los pontones?"),
        make_cell("W3: Bloqueo", "Short: Error de cotas en la suspensión delantera. Mostrando el fallo en el CAD. Visual: Interferencia de brazos con los tubos de dirección. CTA: Ayúdanos a solucionarlo en GitHub."),
        make_cell("W3: X Debate", "Post: ¿Deberíamos usar amortiguadores de moto (coilovers) o de coche comercial ligero? Visual: Fotos de ambos amortiguadores en escala real. CTA: Vota en el hilo de X."),
        make_cell("W3: Edu Short", "Short: Qué es el centro de gravedad (CG) y cómo influye el peso del piloto y motor. Visual: Diagrama estático con CG marcado. CTA: ¿Sabes cómo calcular el CG?"),
        make_cell("W3: Episodio 3", "YT: 'Simulaciones estructurales extremas (FEA) de nuestro chasis en internet (¿Es seguro?).'\nEstructura: Explicación FEA -> Errores críticos detectados -> Correcciones. Duración: 14 mins."),
        make_cell("W3: Discord", "Llamada Discord: Repaso general de cotas de chasis antes del Freeze de CAD de Fase 1. Participantes: Todos los ingenieros colaboradores activos. Hora: 20:00 CEST.")
    ]
    m1_w4 = [
        make_cell("W4: Sourcing", "Hook: Buscando patrocinador para los tubos de acero. Emailing a metalúrgicas. Visual: Time-lapse del envío de emails y llamadas. CTA: Etiqueta a tu metalúrgica favorita."),
        make_cell("W4: Alianzas", "Carrusel: Plantilla del pitch para empresas de corte láser. Qué les ofrecemos. Visual: Capturas de la propuesta comercial de CERO. CTA: Comparte este post con dueños de talleres."),
        make_cell("W4: Taller local", "Short: Visitando un taller de soldadura TIG local para proponer el canje de espacio. Visual: Entrevista de 15 segundos con el soldador. CTA: ¿Crees que aceptará el rincón CERO?"),
        make_cell("W4: X Debate", "Post: Hilo sobre coste de consumibles de taller (gases, radial, discos) y cómo financiarlos. Visual: Lista de precios estimados de ferretería. CTA: Comenta alternativas baratas."),
        make_cell("W4: Edu Short", "Short: Explicación de la soldadura TIG de precisión vs electrodo o hilo (MIG). Visual: Macro de la soldadura TIG y formación del arco. CTA: ¿Has soldado alguna vez TIG?"),
        make_cell("W4: Episodio 4", "YT: 'Llamando a desguaces y talleres locales en directo para conseguir el motor Suzuki GSX-R.'\nEstructura: Guion de llamadas -> Negociaciones de canje -> Cierre del trato. Duración: 18 mins."),
        make_cell("W4: Discord", "Voto Discord: Aprobación del contrato de IP y cesión de diseños de colaboradores. Requisito: Lectura previa de DOC-010. Hora: 20:00 CEST.")
    ]
    
    # MONTH 2: CAD & Aerodynamics (W5-W8)
    m2_w5 = [
        make_cell("W5: Chasis CAD", "Hook: Diseñando el arco principal en CAD. Medidas de seguridad FIA. Visual: Chasis girando con arco pintado en rojo. CTA: ¿Deberíamos subir el arco 5 cm?"),
        make_cell("W5: Triángulos", "Carrusel: Cómo triangular un chasis para evitar flexión lateral. Teoría de cerchas. Visual: Gráficas de tensión en nudos de soldadura. CTA: Comenta tu duda sobre flexión."),
        make_cell("W5: Espacio", "Short: Mostrando cómo encaja el tanque de combustible detrás del asiento en 3D. Visual: Despiece del cortafuegos y el tanque. CTA: ¿Prefieres tanque central o lateral?"),
        make_cell("W5: X Debate", "Post: ¿Usar barras estabilizadoras ajustables o suspensiones duras? Pros de dinamismo. Visual: Diagrama de barra estabilizadora trasera. CTA: Comenta tu opinión técnica."),
        make_cell("W5: Edu Short", "Short: Explicación del chasis Spaceframe vs Monocasco. Costes y peso. Visual: Comparación de chasis Caterham vs F1 moderno. CTA: ¿Cuál construirías tú?"),
        make_cell("W5: Episodio 5", "YT: 'Estructurando la jaula de seguridad del chasis en Onshape con la FIA en mano.'\nEstructura: Normas FIA -> Ajustes del cockpit -> Renders de seguridad. Duración: 16 mins."),
        make_cell("W5: Discord", "Voto Discord: Anchura de cockpit (¿estrecho para aerodinámica o cómodo?). Duración: 48 horas. Requisito: Canal #ergonomia.")
    ]
    m2_w6 = [
        make_cell("W6: Cockpit", "Hook: Simulando la posición de conducción del piloto. Ángulo de las rodillas. Visual: Animación del maniquí estirando las piernas. CTA: ¿Crees que roza con los pedales?"),
        make_cell("W6: Asiento", "Carrusel: Cómo fabricar un asiento de espuma expansiva a medida del piloto. Visual: Pasos para rellenar bolsas de poliuretano. CTA: ¿Te atreverías a sentarte ahí?"),
        make_cell("W6: Volante", "Short: Integrando la cremallera de dirección rápida de kart. ¿Cuántas vueltas de volante? Visual: Movimiento del eje de dirección en el CAD. CTA: ¿Dirección asistida o directa?"),
        make_cell("W6: X Debate", "Post: ¿Volante redondo clásico de cuero o estilo F1 cortado en aluminio 3D? Visual: Fotos de ambos volantes renderizados. CTA: Vota en el post de X."),
        make_cell("W6: Edu Short", "Short: Qué es el efecto Ackerman en la dirección y cómo influye al girar cerrado. Visual: Animación de las ruedas girando a distinto ángulo. CTA: ¿Conocías este efecto mecánico?"),
        make_cell("W6: Episodio 6", "YT: 'Colocando el pedalier y la columna de dirección en el espacio del chasis tubular.'\nEstructura: Montaje de cremallera -> Tolerancias de pedales -> Renders finales. Duración: 15 mins."),
        make_cell("W6: Discord", "Llamada Discord: Debate sobre la posición de la palanca de cambios secuencial. Temario: Palanca central vs levas mecánicas en volante. Hora: 20:00 CEST.")
    ]
    m2_w7 = [
        make_cell("W7: CFD Nose", "Hook: Simulando la aerodinámica del morro en CFD. ¿Fuerza lateral o arrastre? Visual: Animación de líneas de corriente sobre el morro. CTA: ¿Añadimos un labio inferior?"),
        make_cell("W7: Pontones", "Carrusel: Diseñando las entradas de aire laterales para enfriar el motor trasero. Visual: Pontones con canalización interna de aire. CTA: ¿Deberíamos cambiar el radiador?"),
        make_cell("W7: Radiador", "Short: Mostrando cómo el flujo de aire golpea el radiador en la simulación. Visual: Mapa térmico de entrada de aire del pontón. CTA: Comenta si usarías ventilador."),
        make_cell("W7: X Debate", "Post: ¿Añadir un alerón trasero estilo biplano o dejar la zaga limpia e industrial? Renders con y sin alerón trasero. CTA: Comenta tu estética preferida."),
        make_cell("W7: Edu Short", "Short: Qué es el arrastre aerodinámico (Cx) y cómo penaliza la velocidad en pista. Visual: Gráfico comparativo de Cx de distintos perfiles. CTA: ¿Qué perfil tiene menos arrastre?"),
        make_cell("W7: Episodio 7", "YT: 'Pasando el coche por el túnel de viento digital: Análisis de CFD aerodinámico.'\nEstructura: Configuración OpenFOAM -> Simulación -> Resultados de arrastre. Duración: 17 mins."),
        make_cell("W7: Discord", "Voto Discord: Ángulo de inclinación del radiador lateral. Duración del voto: 24 horas. Requisito: Canal #refrigeracion.")
    ]
    m2_w8 = [
        make_cell("W8: Firewall", "Hook: Protegiendo al piloto. Diseño de la mampara de fuego entre motor y espalda. Visual: Render del piloto separado del motor por chapa. CTA: ¿Aluminio o acero para la mampara?"),
        make_cell("W8: Alum chapa", "Carrusel: Diseño de paneles de aluminio del chasis en corte plano para remachar. Visual: Planos 2D de desarrollo de chapa. CTA: ¿Remaches de acero o aluminio?"),
        make_cell("W8: Peso total", "Short: Control de peso de diseño en Onshape. ¿Cuánto pesa el CAD hasta hoy? Visual: Pantalla de propiedades de masa de Onshape. CTA: ¿Lograremos bajar de 420 kg?"),
        make_cell("W8: X Debate", "Post: Hilo sobre la visibilidad del piloto con el arco antivuelco y retrovisores. Visual: Captura en primera persona desde el cockpit. CTA: Comenta si ves algún punto ciego."),
        make_cell("W8: Edu Short", "Short: Normativa FIA sobre mamparas parallamas y aislamiento de gasolina/fuego. Visual: Esquema del recorrido de mangueras de gasolina. CTA: ¿Sabes qué es el cortafuegos?"),
        make_cell("W8: Episodio 8", "YT: 'Cerramos la Fase 2: El chasis conceptual de CERO está terminado (Freeze CAD V1).'\nEstructura: Paseo virtual 3D -> Pesos finales -> Plan de Fase 3. Duración: 18 mins."),
        make_cell("W8: Discord", "Llamada Discord: Celebración y lanzamiento de retos de suspensión para la Fase 3. Participantes: Core Team e ingenieros de Discord. Hora: 20:00 CEST.")
    ]

    # MONTH 3: Suspension Design & FEA (W9-W12)
    m3_w9 = [
        make_cell("W9: Wishbones", "Hook: Diseñando los dobles trapecios de suspensión delantera. Geometría inicial. Visual: Movimiento del trapecio superior e inferior. CTA: ¿Deberíamos inclinar el brazo?"),
        make_cell("W9: Camber", "Carrusel: Explicación gráfica de la variación de caída (camber) al comprimir amortiguador. Visual: Animación de la rueda ganando camber. CTA: ¿Qué camber inicial pondrías?"),
        make_cell("W9: Rótulas", "Short: Por qué usamos rótulas uniball de competición y no silentblocks de goma. Visual: Foto de rótula esférica de competición en mano. CTA: Comenta tu experiencia con rótulas."),
        make_cell("W9: X Debate", "Post: ¿Suspensión trasera por puente rígido ligero o dobles trapecios independientes? Visual: Render de ambos trenes traseros. CTA: Vota y justifica tu voto técnico."),
        make_cell("W9: Edu Short", "Short: Qué es el Roll Center (Centro de Balanceo) y cómo influye en el paso por curva. Visual: Animación de las fuerzas cruzándose en el chasis. CTA: ¿Sabes cómo encontrar el RC?"),
        make_cell("W9: Episodio 9", "YT: 'Geometría de suspensión: Calculando los brazos del monoplaza en Onshape.'\nEstructura: Cálculos de roll center -> Simulación de recorrido -> Modelado CAD. Duración: 15 mins."),
        make_cell("W9: Discord", "Voto Discord: Elección del ángulo de ataque de los trapecios delateros. Duración del voto: 24 horas. Requisito: Canal #suspension.")
    ]
    m3_w10 = [
        make_cell("W10: FEA Arms", "Hook: Simulación de rotura de los trapecios ante un bache de 3G de fuerza. Visual: Animación de flexión con colores de tensión FEA. CTA: ¿Crees que aguantará el tubo?"),
        make_cell("W10: Soldaduras", "Carrusel: Puntos calientes de tensión en los trapecios de suspensión. Fatiga. Visual: Zoom en los extremos del soporte roscado. CTA: ¿Añadirías una cartela de refuerzo?"),
        make_cell("W10: Tubo grosor", "Short: ¿Brazos de suspensión de tubo redondo o perfil ovalado? Comparativa en software. Visual: Renders de ambos tubos en flexión. CTA: Comenta cuál prefieres soldar."),
        make_cell("W10: X Debate", "Post: Hilo de debate: ¿Cromoly 4130 soldado TIG o brazos de aluminio CNC atornillados? Visual: Fotos de brazos de coche de carreras real. CTA: Comenta tu opinión mecánica."),
        make_cell("W10: Edu Short", "Short: Qué es el límite elástico de un material y por qué el acero dobla antes de partir. Visual: Curva de tracción del acero 4130. CTA: ¿Sabías esta propiedad física?"),
        make_cell("W10: Episodio 10", "YT: 'Poniendo a prueba de flexión (FEA) la suspensión delantera de CERO.'\nEstructura: Simulación FEA en Solidworks -> Modificación de grosores -> Renders. Duración: 14 mins."),
        make_cell("W10: Discord", "Llamada Discord: Revisión de tensiones de soldadura con estudiantes de Formula Student. Temario: Análisis de fallos comunes en suspensión. Hora: 20:00 CEST.")
    ]
    m3_w11 = [
        make_cell("W11: Uprights", "Hook: Diseñando las manguetas (uprights) delanteras a medida en 3D para pinzas Brembo. Visual: Mangueta de aluminio mecanizada en Onshape. CTA: ¿Mecanizarías en 3D o chapa soldada?"),
        make_cell("W11: Maza rueda", "Carrusel: Integrando los bujes y rodamientos de rueda comercial ligera. Tolerancias. Visual: Despiece de buje, rodamiento y disco. CTA: Comenta si has montado bujes."),
        make_cell("W11: Frenos", "Short: Colocando la pinza de freno y midiendo la holgura del latiguillo metálico. Visual: Pinza encajando en los soportes en Onshape. CTA: ¿Doble pistón o pistón simple?"),
        make_cell("W11: X Debate", "Post: ¿Usar bujes de 4 tornillos de Seat Ibiza o bujes ligeros a medida mecanizados? Visual: Foto comparativa de bujes de Ibiza. CTA: Vota en el post de X."),
        make_cell("W11: Edu Short", "Short: Qué es la masa no suspendida y por qué cada gramo ahorrado en la rueda vale oro. Visual: Simulación física de rueda pesada vs ligera. CTA: ¿Sabías cómo influye en el agarre?"),
        make_cell("W11: Episodio 11", "YT: 'Diseñando las manguetas del chasis en Onshape para mecanizado CNC.'\nEstructura: Modelado de manguetas -> Ajuste de frenos -> Preparación de archivos CNC. Duración: 16 mins."),
        make_cell("W11: Discord", "Voto Discord: Diámetro de disco de freno trasero (¿ventilado o macizo?). Duración del voto: 24 horas. Requisito: Canal #frenos.")
    ]
    m3_w12 = [
        make_cell("W12: Dampers", "Hook: ¿Push-rod o amortiguador directo? Diseñando los balancines de suspensión. Visual: Movimiento del amortiguador mediante balancín triangular. CTA: ¿Te gusta el diseño push-rod?"),
        make_cell("W12: Push-rod", "Carrusel: Gráfica del ratio de compresión de suspensión progresivo vs lineal. Visual: Gráfico de ReportLab de ratio de movimiento. CTA: Comenta tus dudas de balancines."),
        make_cell("W12: Geometría", "Short: Ensamblaje completo de dirección, frenos y manguetas girando en CAD. Visual: Animación de giro y compresión de suspensión. CTA: ¿Falta algún soporte de dirección?"),
        make_cell("W12: X Debate", "Post: ¿Es mejor una suspensión progresiva dura al final o una blanda y lineal? Visual: Gráfico de curva progresiva vs lineal. CTA: Comenta tu preferencia técnica."),
        make_cell("W12: Edu Short", "Short: Explicación de cómo funciona un amortiguador de doble vía (compresión y rebote). Visual: Animación de las válvulas de aceite internas. CTA: ¿Sabes ajustar la compresión?"),
        make_cell("W12: Episodio 12", "YT: 'Fase 3 Cerrada: El chasis y las suspensiones de CERO listas para soldar (Freeze CAD V2).'\nEstructura: Renders de suspensión -> Lista de piezas finales -> Plan de sourcing. Duración: 18 mins."),
        make_cell("W12: Discord", "Discord Meet: Planificación del sourcing físico y preparación de la campaña de emails. Hitos: 1. Tubos, 2. Motor Suzuki, 3. Taller. Hora: 20:00 CEST.")
    ]

    # MONTH 4: Sourcing & Logistics (W13-W16)
    m3_w13 = [
        make_cell("W13: Tubos cost", "Hook: ¿Cuánto cuesta el acero de CERO? 0 €. Buscando patrocinador de metalurgia. Visual: Emails y llamadas a proveedores en time-lapse. CTA: Comparte con tu metalúrgica de confianza."),
        make_cell("W13: Pitch Deck", "Carrusel: Presentando el documento comercial de CERO. Qué ve una metalúrgica en nosotros. Visual: Capturas de DOC-021 y branding. CTA: ¿Falta algún dato comercial?"),
        make_cell("W13: Emails", "Short: Mandando correos de patrocinio en directo a suministradores de tubos 4130. Visual: Redacción del email y click en enviar. CTA: ¿Crees que responderán esta semana?"),
        make_cell("W13: X Debate", "Post: ¿Deberíamos aceptar dinero de patrocinadores tradicionales o solo canje de piezas? Visual: Logos de patrocinadores ficticios en el coche. CTA: Comenta tu opinión ética."),
        make_cell("W13: Edu Short", "Short: Qué es el canje de marketing (branding por piezas) y por qué le sirve a las empresas. Visual: Explicación gráfica de retorno de inversión. CTA: ¿Sabes qué es el ROI?"),
        make_cell("W13: Episodio 13", "YT: 'Presentando CERO a empresas metalúrgicas de España (¿Nos darán tubos gratis?).'\nEstructura: Envío de emails -> Seguimiento -> Primera llamada de aceptación. Duración: 15 mins."),
        make_cell("W13: Discord", "Llamada Discord: Lista de patrocinadores de acero contactados y seguimiento de leads. Participantes: Core Team y scouts de sourcing. Hora: 20:00 CEST.")
    ]
    m3_w14 = [
        make_cell("W14: Motor call", "Hook: Llamando a 3 desguaces en busca del motor Suzuki GSX-R 600 completo. Visual: Pantalla dividida con llamadas telefónicas reales. CTA: ¿Cuál crees que tendrá stock?"),
        make_cell("W14: Desguaces", "Carrusel: Comparativa de precios de motores de moto usados en desguaces de España. Visual: Tabla de precios y estados de conservación. CTA: Comenta tu consejo al comprar motores."),
        make_cell("W14: Centralita", "Short: Comprobando si el motor viene con la centralita ECU original y el ramal. Visual: Caja negra y cables de centralita en primer plano. CTA: ¿Desbloquearías la ECU de serie?"),
        make_cell("W14: X Debate", "Post: Hilo: ¿Centralita programable de carreras (Link ECU) o centralita desbloqueada de serie? Visual: Fotos de ambas centralitas mecánicas. CTA: Comenta pros y contras de costes."),
        make_cell("W14: Edu Short", "Short: Cómo desbloquear el inmovilizador de llave (HISS/antirrobo) en una ECU de serie. Visual: Esquema del puente de cables en ramal. CTA: ¿Has saltado un inmovilizador?"),
        make_cell("W14: Episodio 14", "YT: 'Conseguimos el motor Suzuki GSX-R en desguace: Negociación y transporte a casa.'\nEstructura: Visita a desguace -> Truco del alternador -> Carga en el maletero. Duración: 18 mins."),
        make_cell("W14: Discord", "Voto Discord: ¿Limpiar el motor por fuera en chorro de arena o dejarlo crudo? (Estética). Duración: 24 horas. Requisito: Canal #motor.")
    ]
    m3_w15 = [
        make_cell("W15: Taller deal", "Hook: ¿Dónde soldamos el coche? Negociando rincón en un taller mecánico local. Visual: Presentando el plano del taller al dueño. CTA: ¿Nos cederá los 20 metros cuadrados?"),
        make_cell("W3: Canje local", "Carrusel: La propuesta al dueño del taller: Su cartel de fondo en YouTube por el espacio. Visual: Renders del cartel detrás del chasis. CTA: Comparte con dueños de talleres."),
        make_cell("W15: Visita", "Short: Enseñándole el CAD del coche al mecánico del taller de barrio. ¿Acepta? Visual: Grabación disimulada mostrando las reacciones. CTA: ¿Crees que nos dará las llaves?"),
        make_cell("W15: X Debate", "Post: ¿Soldar con electrodo revestido o TIG? Los mecánicos de barrio nos dan su opinión. Visual: Foto de soldadura TIG vs electrodo dulce. CTA: Comenta cuál prefieres tú."),
        make_cell("W15: Edu Short", "Short: Requisitos de ventilación y seguridad eléctrica para soldar un chasis tubular. Visual: Esquema de extracción de humo de taller. CTA: ¿Sabes qué es el gas argón?"),
        make_cell("W15: Episodio 15", "YT: 'Tenemos Taller Colaborador: Mudamos el motor Suzuki al espacio de soldadura.'\nEstructura: Entrada al taller -> Descarga del motor -> Primer café con mecánicos. Duración: 15 mins."),
        make_cell("W15: Discord", "Llamada Discord: Presentación del taller partner y bienvenida al equipo de mecánicos. Participantes: Dueño del taller e ingenieros de CERO. Hora: 20:00 CEST.")
    ]
    m3_w16 = [
        make_cell("W16: CNC parts", "Hook: Unboxing de las manguetas CNC de aluminio donadas por un patrocinador. Visual: Pieza de aluminio brillante saliendo de la caja. CTA: ¿Qué nota le das al fresado?"),
        make_cell("W16: Llantas", "Carrusel: Mostrando el ajuste de las llantas de kart en las manguetas físicas. Visual: Fotos de la rueda atornillada al buje. CTA: Comenta tu elección de neumáticos."),
        make_cell("W16: Resumen S", "Short: Hitos de sourcing de Fase 4: Chasis, Taller, Motor y Llantas conseguidos con 0 €. Visual: Time-lapse rápido de todos los unboxings. CTA: Únete al Discord para Fase 5."),
        make_cell("W16: X Debate", "Post: Hilo sobre los siguientes pasos de la Fase 5: El inicio físico del corte de tubos. Visual: Fotos del esqueleto CAD listo para corte. CTA: Comenta tus dudas sobre corte láser."),
        make_cell("W16: Edu Short", "Short: Explicación de cómo mecanizar aluminio aeronáutico 7075 en centros CNC. Visual: Broca de fresado cortando bloque de aluminio. CTA: ¿Sabías qué es el temple T6?"),
        make_cell("W16: Episodio 16", "YT: 'Unboxing de locura: Tenemos todas las piezas listas para cortar y soldar el chasis.'\nEstructura: Unboxing masivo -> Agradecimiento a sponsors -> Preparación de jig. Duración: 19 mins."),
        make_cell("W16: Discord", "Discord Meet: Planificación del primer corte físico de tubos y soldadura en el taller. Temario: 1. Compra de sierra de cinta, 2. Medidas de jig. Hora: 20:00 CEST.")
    ]

    # Month 1
    story.append(Paragraph("MES 1: LANZAMIENTO, COMUNIDAD Y ELECCIÓN DE MOTOR (SEMANAS 1-4)", subtitle_style))
    story.append(Paragraph("PLAN EDITORIAL DIARIO - MES 1", title_style))
    story.append(Spacer(1, 10))
    table_m1 = Table([headers, m1_w1, m1_w2, m1_w3, m1_w4], colWidths=col_widths)
    table_m1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1C1C1E')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#8E8E93')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8F9FA')]),
    ]))
    story.append(table_m1)
    story.append(PageBreak())
    
    # Month 2
    story.append(Paragraph("MES 2: DISEÑO CONCEPTUAL CAD Y ERGONOMÍA (SEMANAS 5-8)", subtitle_style))
    story.append(Paragraph("PLAN EDITORIAL DIARIO - MES 2", title_style))
    story.append(Spacer(1, 10))
    table_m2 = Table([headers, m2_w5, m2_w6, m2_w7, m2_w8], colWidths=col_widths)
    table_m2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1C1C1E')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#8E8E93')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8F9FA')]),
    ]))
    story.append(table_m2)
    story.append(PageBreak())
    
    # Month 3
    story.append(Paragraph("MES 3: DISEÑO DE SUSPENSIÓN E INGENIERÍA DE SIMULACIÓN (SEMANAS 9-12)", subtitle_style))
    story.append(Paragraph("PLAN EDITORIAL DIARIO - MES 3", title_style))
    story.append(Spacer(1, 10))
    table_m3 = Table([headers, m3_w9, m3_w10, m3_w11, m3_w12], colWidths=col_widths)
    table_m3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1C1C1E')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#8E8E93')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8F9FA')]),
    ]))
    story.append(table_m3)
    story.append(PageBreak())

    # Month 4
    story.append(Paragraph("MES 4: ALIANZAS, SOURCING DE PIEZAS Y NEGOCIACIONES (SEMANAS 13-16)", subtitle_style))
    story.append(Paragraph("PLAN EDITORIAL DIARIO - MES 4", title_style))
    story.append(Spacer(1, 10))
    table_m4 = Table([headers, m3_w13, m3_w14, m3_w15, m3_w16], colWidths=col_widths)
    table_m4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1C1C1E')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#8E8E93')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8F9FA')]),
    ]))
    story.append(table_m4)

    def draw_landscape_decorations(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#FF3B30"))
        canvas.setLineWidth(1)
        canvas.line(36, 565, 756, 565)
        canvas.setStrokeColor(colors.HexColor("#E5E5EA"))
        canvas.line(36, 40, 756, 40)
        
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#8E8E93"))
        canvas.drawString(36, 25, "CONFIDENCIAL — PROHIBIDA SU DISTRIBUCIÓN COMERCIAL")
        canvas.drawRightString(756, 25, f"DOC-006 LANDSCAPE CALENDAR — Pág. {doc.page} de 4")
        canvas.restoreState()
        
    pdf.build(story, onFirstPage=draw_landscape_decorations, onLaterPages=draw_landscape_decorations)
    print("Generado PDF Horizontal de 4 Páginas: DOC-006_Content_OS_Landscape.pdf")


# Generates high-contrast matplotlib diagrams inside the assets folder.
def generate_diagrams(assets_dir):
    os.makedirs(assets_dir, exist_ok=True)
    
    # 1. project_timeline_gantt.png (28 Months detailed Gantt)
    gantt_path = os.path.join(assets_dir, "project_timeline_gantt.png")
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=150)
    
    tasks = [
        ("1. Concepto y Ergonomía (Onshape)", 0, 3, "Diseño"),
        ("2. Modelado de Chasis CAD V1", 3, 3, "Diseño"),
        ("3. FEA Estructural y CFD Aire", 6, 3, "Diseño"),
        ("4. Diseño de Dirección y Pedales", 9, 3, "Diseño"),
        ("5. Congelación CAD V2 (Hito)", 11.5, 0.5, "Diseño"),
        
        ("6. Compra de Motor Suzuki GSX-R", 11, 2, "Sourcing"),
        ("7. Sourcing Acero 4130 Cromoly", 12, 2, "Sourcing"),
        ("8. Adquisición Llantas/Frenos", 13, 2, "Sourcing"),
        
        ("9. Mesa Jig de Soldadura", 14, 2, "Fabricación"),
        ("10. Corte y Biselado de Tubos", 15, 2, "Fabricación"),
        ("11. Soldadura TIG del Chasis", 16, 3, "Fabricación"),
        ("12. Pintura en Polvo Chasis", 18.5, 1, "Fabricación"),
        
        ("13. Montaje de Suspensión y Ruedas", 19, 2, "Integración"),
        ("14. Instalación de Motor y Cadena", 20, 2, "Integración"),
        ("15. Fontanería Frenos y Refrigeración", 21, 2, "Integración"),
        ("16. Cableado y ECU Desbloqueada", 22, 2, "Integración"),
        
        ("17. Shakedown y Pruebas Pista", 23, 2, "Validación"),
        ("18. Ensayos Ruido y Emisiones", 24, 2, "Validación"),
        ("19. Dossier IDIADA / INTA", 25, 2, "Validación"),
        ("20. Inspección ITV / Placas Calle", 26, 2, "Validación")
    ]
    
    category_colors = {
        "Diseño": "#FF3B30",
        "Sourcing": "#8E8E93",
        "Fabricación": "#1C1C1E",
        "Integración": "#444446",
        "Validación": "#AEAEB2"
    }
    
    y_labels = [t[0] for t in tasks]
    starts = [t[1] for t in tasks]
    durations = [t[2] for t in tasks]
    colors_list = [category_colors[t[3]] for t in tasks]
    
    y_pos = np.arange(len(tasks))
    
    ax.barh(y_pos, durations, left=starts, color=colors_list, edgecolor="black", height=0.55, zorder=3)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(y_labels, fontsize=8, fontweight="bold", color="#1C1C1E")
    ax.set_xlabel("Línea de Tiempo (Meses)", fontsize=9, fontweight="bold", color="#1C1C1E", labelpad=10)
    ax.set_xlim(0, 28)
    ax.set_xticks(range(0, 29, 2))
    
    ax.grid(axis='x', linestyle='--', alpha=0.5, zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#8E8E93')
    ax.spines['bottom'].set_color('#8E8E93')
    
    ax.axvline(x=12, color='#FF3B30', linestyle=':', linewidth=1.2)
    ax.axvline(x=24, color='#1C1C1E', linestyle=':', linewidth=1.2)
    
    ax.invert_yaxis()
    
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor="#FF3B30", edgecolor="black", label="Diseño CAD & Simulación"),
        Patch(facecolor="#8E8E93", edgecolor="black", label="Logística & Sourcing"),
        Patch(facecolor="#1C1C1E", edgecolor="black", label="Fabricación & Taller"),
        Patch(facecolor="#444446", edgecolor="black", label="Integración Tren Motriz"),
        Patch(facecolor="#AEAEB2", edgecolor="black", label="Homologación & ITV Calle")
    ]
    ax.legend(handles=legend_elements, loc="lower right", fontsize=7.5, framealpha=0.9)
    
    plt.title("GANTT MAESTRO CERO: PLAN DE DESARROLLO Y HOMOLOGACIÓN VIAL DE CALLE (28 MESES)", 
              fontsize=9, fontweight="bold", pad=12, color="#000000")
    plt.tight_layout()
    plt.savefig(gantt_path, bbox_inches='tight')
    plt.close()
    print("Generado Diagrama: project_timeline_gantt.png")
    
    # 2. financial_breakdown.png (Pista vs Calle)
    fin_path = os.path.join(assets_dir, "financial_breakdown.png")
    fig, ax = plt.subplots(figsize=(7, 4.2), dpi=150)
    
    categories = [
        "Motor Suzuki GSX-R",
        "Chasis Acero 4130",
        "Frenos y Dirección",
        "Seguridad FIA/Calle",
        "Electrónica y Cableado",
        "Tasas Homologación (IDIADA)",
        "Ensayos Lab (Ruido/Gases)",
        "Catalizador Euro 6 + ESC"
    ]
    
    track_costs = [1200, 0, 900, 850, 350, 0, 0, 0]
    street_extra = [0, 600, 200, 400, 400, 2500, 1800, 1200]
    
    y_pos = np.arange(len(categories))
    
    ax.barh(y_pos, track_costs, color="#1C1C1E", edgecolor="black", height=0.55, label="Proyecto Pista Básico (€3.300)", zorder=3)
    ax.barh(y_pos, street_extra, left=track_costs, color="#FF3B30", edgecolor="black", height=0.55, label="Coste Extra Homologación Calle (+€7.100)", zorder=3)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories, fontsize=8, fontweight="bold")
    ax.set_xlabel("Coste Estimado (€)", fontsize=9, fontweight="bold")
    ax.set_xlim(0, 4000)
    ax.grid(axis='x', linestyle='--', alpha=0.5, zorder=0)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#8E8E93')
    ax.spines['bottom'].set_color('#8E8E93')
    
    ax.legend(loc="lower right", fontsize=8)
    plt.title("COMPARATIVA ESTRUCTURAL DE COSTES: PISTA VS HOMOLOGACIÓN CALLE", fontsize=10, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(fin_path, bbox_inches='tight')
    plt.close()
    print("Generado Diagrama: financial_breakdown.png")
    
    # 3. growth_funnel.png
    funnel_path = os.path.join(assets_dir, "growth_funnel.png")
    fig, ax = plt.subplots(figsize=(7, 3.5), dpi=150)
    stages = [
        "Core Team\n(Votos en Discord)",
        "Colaboradores\n(GitHub Commits)",
        "Comunidad Discord\n(Miembros Activos)",
        "Alcance Social\n(Espectadores Reels)"
    ]
    values = [10, 150, 5000, 200000]
    y_pos = np.arange(len(stages))
    
    ax.barh(y_pos, values, color=['#FF3B30', '#1C1C1E', '#8E8E93', '#E5E5EA'], edgecolor='black', height=0.6)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(stages, fontsize=8, fontweight="bold")
    ax.set_xscale('log')
    ax.set_xlabel("Número de Usuarios (Escala Logarítmica)", fontsize=8, fontweight="bold")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#8E8E93')
    ax.spines['bottom'].set_color('#8E8E93')
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    ax.set_title("EMBUDO DE CRECIMIENTO Y CONVERSIÓN", fontsize=10, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(funnel_path, bbox_inches='tight')
    plt.close()
    print("Generado Diagrama: growth_funnel.png")
    
    # 4. kpi_projections.png
    kpi_path = os.path.join(assets_dir, "kpi_projections.png")
    fig, ax = plt.subplots(figsize=(7, 3.5), dpi=150)
    months = np.arange(0, 25, 2)
    members = [0, 5, 25, 60, 120, 190, 250, 310, 370, 420, 460, 480, 500]
    
    ax.plot(months, members, color='#FF3B30', linewidth=2.5, marker='o', markersize=5)
    ax.set_xlabel("Meses del Proyecto", fontsize=8, fontweight="bold")
    ax.set_ylabel("Suscripciones Activas", fontsize=8, fontweight="bold")
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 550)
    ax.set_xticks(range(0, 25, 2))
    ax.grid(linestyle='--', alpha=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#8E8E93')
    ax.spines['bottom'].set_color('#8E8E93')
    ax.set_title("PROYECCIÓN DE CRECIMIENTO DE MEMBRESÍAS DE PAGO", fontsize=10, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(kpi_path, bbox_inches='tight')
    plt.close()
    print("Generado Diagrama: kpi_projections.png")

    # 5. fsae_structural_equivalency.png
    fsae_path = os.path.join(assets_dir, "fsae_structural_equivalency.png")
    fig, ax = plt.subplots(figsize=(7, 3.5), dpi=150)
    materials = [
        "Acero Dulce\n25.4mm x 2.0mm",
        "Cromoly 4130\n25.4mm x 1.2mm",
        "Cromoly 4130\n25.4mm x 1.6mm",
        "Cromoly 4130\n25.4mm x 2.0mm\n(FIA/FSAE Min)"
    ]
    strength = [250, 360, 480, 630]
    
    ax.barh(materials, strength, color=['#E5E5EA', '#8E8E93', '#1C1C1E', '#FF3B30'], edgecolor='black', height=0.55)
    ax.set_xlabel("Límite Elástico de Tracción / Resistencia (MPa)", fontsize=8, fontweight="bold")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#8E8E93')
    ax.spines['bottom'].set_color('#8E8E93')
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    ax.set_title("COMPARATIVA DE RESISTENCIA ESTRUCTURAL DE MATERIALES", fontsize=10, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(fsae_path, bbox_inches='tight')
    plt.close()
    print("Generado Diagrama: fsae_structural_equivalency.png")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    documents_dir = os.path.join(base_dir, "documents")
    assets_dir = os.path.join(documents_dir, "assets")
    
    # 1. Clean the old documents folder to prevent duplicate or unstructured files
    if os.path.exists(documents_dir):
        shutil.rmtree(documents_dir)
    os.makedirs(documents_dir, exist_ok=True)
    os.makedirs(assets_dir, exist_ok=True)
    
    # 2. Generate Matplotlib diagrams for embedding
    generate_diagrams(assets_dir)
    
    # 3. Iterate through the database and write documents to organized category folders
    for doc_id, doc_info in doc_database.items():
        category = doc_info.get("category", "00_Gobernanza_y_Operaciones")
        category_dir = os.path.join(documents_dir, category)
        os.makedirs(category_dir, exist_ok=True)
        
        create_pdf(doc_id, doc_info, category_dir, assets_dir)
        create_markdown(doc_id, doc_info, category_dir)
        
    # Generate 4-page Landscape calendar inside the Brand & Community folder
    brand_comm_dir = os.path.join(documents_dir, "01_Marca_y_Comunidad")
    create_landscape_calendar(brand_comm_dir)
    
    print("\n--- ¡TODOS LOS DOCUMENTOS GENERADOS EXITOSAMENTE EN CARPETAS ORGANIZADAS! ---")
