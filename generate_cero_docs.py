import os
import sys
import json
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
    filename = f"{doc_id}_{doc_info['title'].replace(' ', '_').replace('&', 'and').replace('/', '_')}.pdf"
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
        fontSize=14,
        leading=18,
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
    filename = f"{doc_id}_{doc_info['title'].replace(' ', '_').replace('&', 'and').replace('/', '_')}.md"
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
        make_cell("W9: Discord", "Voto Discord: Elección del ángulo de ataque de los trapecios delanteros. Duración del voto: 24 horas. Requisito: Canal #suspension.")
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
    ax.set_xlabel("Coste Estimado (€)", fontsize=9, fontweight="bold", labelpad=10)
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
    ax.set_xlabel("Número de Usuarios (Escala Logarítmica)", fontsize=8, fontweight="bold", labelpad=10)
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
    ax.set_xlabel("Meses del Proyecto", fontsize=8, fontweight="bold", labelpad=10)
    ax.set_ylabel("Suscripciones Activas", fontsize=8, fontweight="bold", labelpad=10)
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
    ax.set_xlabel("Límite Elástico de Tracción / Resistencia (MPa)", fontsize=8, fontweight="bold", labelpad=10)
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
    
    # 3. Load cero_docs_db.json
    db_path = os.path.join(base_dir, "cero_docs_db.json")
    if not os.path.exists(db_path):
        print(f"Error: {db_path} not found.")
        sys.exit(1)
        
    with open(db_path, "r", encoding="utf-8") as f:
        doc_database = json.load(f)
    
    # 4. Iterate through the database and write documents to organized category folders
    for doc_id, doc_info in doc_database.items():
        # Read folder mapping
        category = doc_info.get("category", "00_Gobernanza_y_Estrategia")
        category_dir = os.path.join(documents_dir, category)
        os.makedirs(category_dir, exist_ok=True)
        
        # Check for category overrides (e.g. DOC-018 having different directory name)
        if "category_override" in doc_info:
            category_dir = os.path.join(documents_dir, doc_info["category_override"])
            os.makedirs(category_dir, exist_ok=True)
            
        create_pdf(doc_id, doc_info, category_dir, assets_dir)
        create_markdown(doc_id, doc_info, category_dir)
        
    # Generate 4-page Landscape calendar inside the Brand & Community folder (mapped as 01_Marca_y_Comunidad)
    brand_comm_dir = os.path.join(documents_dir, "01_Marca_y_Comunidad")
    os.makedirs(brand_comm_dir, exist_ok=True)
    create_landscape_calendar(brand_comm_dir)
    
    print("\n--- ¡TODOS LOS DOCUMENTOS GENERADOS EXITOSAMENTE DESDE MANIFIESTO JSON! ---")
