#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
==============================================================================
CERO MOTOR CO. - REUSABLE LIGHT-THEME DOCUMENT TEMPLATE GENERATOR
==============================================================================
Use this script to compile additional CERO PDFs matching the official suite's
exact light-theme styling (white background, red line dividers, Outfit typography,
black logo on cover, and technical page headers/footers).

Usage:
  1. Modify the document metadata and sections array in the main block below.
  2. Run the script:
     $ .venv/Scripts/python.exe create_cero_document.py
==============================================================================
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.pdfgen import canvas

# Define project assets locations
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BRAND_DIR = os.path.join(PROJECT_ROOT, "assets", "brand")
LOGO_BLACK_PATH = os.path.join(BRAND_DIR, "logo_black_on_transparent.png")
FONT_REGULAR_PATH = os.path.join(BRAND_DIR, "Outfit-Regular.ttf")
FONT_BOLD_PATH = os.path.join(BRAND_DIR, "Outfit-Bold.ttf")

FONT_NAME = 'Outfit'
FONT_BOLD = 'Outfit-Bold'

# ==========================================
# 1. FONT REGISTRATION
# ==========================================
def register_cero_fonts():
    global FONT_NAME, FONT_BOLD
    if os.path.exists(FONT_REGULAR_PATH) and os.path.exists(FONT_BOLD_PATH):
        try:
            pdfmetrics.registerFont(TTFont('Outfit', FONT_REGULAR_PATH))
            pdfmetrics.registerFont(TTFont('Outfit-Bold', FONT_BOLD_PATH))
            pdfmetrics.registerFontFamily('Outfit', normal='Outfit', bold='Outfit-Bold')
            FONT_NAME = 'Outfit'
            FONT_BOLD = 'Outfit-Bold'
            print("[FONT] Outfit and Outfit-Bold registered successfully.")
        except Exception as e:
            print(f"[FONT WARNING] Failed to register local Outfit font, falling back to Helvetica: {e}")
            FONT_NAME = 'Helvetica'
            FONT_BOLD = 'Helvetica-Bold'
    else:
        FONT_NAME = 'Helvetica'
        FONT_BOLD = 'Helvetica-Bold'
        print("[FONT] Outfit fonts not found, falling back to Helvetica")

# ==========================================
# 2. RUNNING HEADER / FOOTER CANVAS (MATCHING SUITE EXACTLY)
# ==========================================
class CeroNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(CeroNumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_elements(num_pages)
            super(CeroNumberedCanvas, self).showPage()
        super(CeroNumberedCanvas, self).save()

    def draw_page_elements(self, page_count):
        # Extract doc_id from document template if available
        doc_template = getattr(self, "_doctemplate", None)
        doc_id = getattr(doc_template, "doc_id", "DOC-999")
        
        # Clean cover page (Page 1)
        if self._pageNumber == 1:
            return

        self.saveState()
        
        # Running header red line at Y=738
        self.setStrokeColor(colors.HexColor("#FF3B30"))
        self.setLineWidth(1)
        self.line(54, 738, 558, 738)
        
        # Small header logo on the left
        if os.path.exists(LOGO_BLACK_PATH):
            try:
                self.drawImage(LOGO_BLACK_PATH, 54, 742, width=18, height=18, mask='auto')
            except Exception:
                pass
        
        # Header text
        self.setFont(FONT_BOLD, 8)
        self.setFillColor(colors.HexColor("#1C1C1E"))
        self.drawString(80, 746, "CERO MOTOR CO. — DOCUMENTO OFICIAL")
        self.drawRightString(558, 746, doc_id)

        # Running footer line at Y=54
        self.setStrokeColor(colors.HexColor("#E5E5EA"))
        self.setLineWidth(1)
        self.line(54, 54, 558, 54)
        
        # Footer text
        self.setFont(FONT_NAME, 8)
        self.setFillColor(colors.HexColor("#8E8E93"))
        self.drawString(54, 38, "CONFIDENCIAL — PROHIBIDA SU DISTRIBUCIÓN COMERCIAL")
        self.drawRightString(558, 38, f"Pág. {self._pageNumber} de {page_count}")
        
        self.restoreState()

# ==========================================
# 3. PDF COMPILING ENGINE
# ==========================================
def build_cero_pdf(filename, doc_id, title, subtitle, author, version, date, sections, table_data=None):
    register_cero_fonts()
    
    pdf_path = os.path.join(PROJECT_ROOT, filename)
    
    # 54pt margins = 0.75 in (Letter size: 612 x 792 pt)
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=80,
        bottomMargin=80
    )
    # Inject doc_id into template object so canvas can read it dynamically
    doc.doc_id = doc_id

    styles = getSampleStyleSheet()
    
    # Define color scheme
    c_dark = colors.HexColor("#1C1C1E")
    c_red = colors.HexColor("#FF3B30")
    c_gray = colors.HexColor("#8E8E93")
    c_light_gray = colors.HexColor("#F8F9FA")
    c_border = colors.HexColor("#E5E5EA")

    # Typography styles
    style_cover_title = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName=FONT_BOLD,
        fontSize=24,
        leading=30,
        textColor=c_dark,
        spaceAfter=10
    )

    style_cover_sub = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=12,
        leading=16,
        textColor=c_gray,
        spaceAfter=25
    )

    style_h1 = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Normal'],
        fontName=FONT_BOLD,
        fontSize=13,
        leading=17,
        textColor=c_red,
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=9.5,
        leading=14.5,
        textColor=c_dark,
        spaceAfter=12
    )

    style_meta_label = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName=FONT_BOLD,
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#555559')
    )
    
    style_meta_val = ParagraphStyle(
        'MetaValue',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=8.5,
        leading=11,
        textColor=c_dark
    )

    style_disclosure = ParagraphStyle(
        'CoverDisclosure',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=8.5,
        leading=12.5,
        textColor=c_gray
    )

    story = []

    # ==========================================
    # COVER PAGE BLOCK (MATCHING OFFICIAL SUITE)
    # ==========================================
    if os.path.exists(LOGO_BLACK_PATH):
        try:
            story.append(Image(LOGO_BLACK_PATH, width=70, height=70))
        except Exception:
            story.append(Spacer(1, 40))
    else:
        story.append(Spacer(1, 40))
        
    story.append(Spacer(1, 15))
    story.append(Paragraph(doc_id, ParagraphStyle('CoverDocId', fontName=FONT_BOLD, fontSize=14, leading=18, textColor=c_red, spaceAfter=5)))
    story.append(Paragraph(title.upper(), style_cover_title))
    story.append(Paragraph(subtitle, style_cover_sub))
    
    # Red divider line (504 pt width matching columns width)
    story.append(Table([['']], colWidths=[504], rowHeights=[3], style=[
        ('BACKGROUND', (0,0), (-1,-1), c_red),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(Spacer(1, 20))

    # Disclosure metadata
    story.append(Paragraph("<b>DATA ROOM DE INGENIERÍA Y OPERACIONES CERO</b><br/>"
                           "Este documento contiene información de diseño cinemático, estratégico y financiero legal "
                           "propiedad de CERO Motor Co. Su uso está regulado bajo licencia abierta no-comercial CC BY-NC 4.0 "
                           "y los acuerdos de confidencialidad y cesión de propiedad intelectual vigentes.", style_disclosure))
    story.append(Spacer(1, 40))

    # Metadata table block
    meta_table_data = [
        [Paragraph("AUTORÍA:", style_meta_label), Paragraph(author, style_meta_val)],
        [Paragraph("VERSIÓN ACTIVA:", style_meta_label), Paragraph(version, style_meta_val)],
        [Paragraph("FECHA DE PUBLICACIÓN:", style_meta_label), Paragraph(date, style_meta_val)]
    ]
    meta_table = Table(meta_table_data, colWidths=[150, 354])
    meta_table.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.5, c_border),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(meta_table)
    
    # Pagebreak to start content on Page 2
    story.append(PageBreak())

    # ==========================================
    # SECTIONS BLOCK
    # ==========================================
    for sec_idx, (sec_title, sec_body) in enumerate(sections):
        story.append(Paragraph(f"{sec_idx + 1}. {sec_title}", style_h1))
        body_text_normalized = sec_body.replace("\n", "<br/>")
        story.append(Paragraph(body_text_normalized, style_body))
        story.append(Spacer(1, 8))

    # Add reference table if provided
    if table_data:
        story.append(Spacer(1, 10))
        story.append(Paragraph("DATOS DE REFERENCIA", style_h1))
        
        table_rows = []
        # Header formatting
        table_rows.append([Paragraph(f"<b>{cell}</b>", ParagraphStyle('TableHeader', parent=styles['Normal'], fontName=FONT_BOLD, fontSize=8.5, leading=11, textColor=colors.white)) for cell in table_data[0]])
        # Body formatting
        for row in table_data[1:]:
            table_rows.append([Paragraph(cell, style_body) for cell in row])
            
        col_width = 504 / len(table_data[0])
        t = Table(table_rows, colWidths=[col_width] * len(table_data[0]))
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), c_dark),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('TOPPADDING', (0, 0), (-1, 0), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, c_border),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [c_light_gray, colors.white]),
        ]))
        story.append(t)

    # Build document (Default ReportLab canvas background is white, matching suite)
    doc.build(
        story,
        canvasmaker=CeroNumberedCanvas
    )
    print(f"[COMPILER] Reusable CERO document successfully generated: {filename}")


# ==========================================
# 4. MAIN CUSTOMIZATION BLOCK (LOREM IPSUM EXAMPLE)
# ==========================================
if __name__ == "__main__":
    # Custom details for the new document template
    filename = "DOC-999_CERO_Custom_Template.pdf"
    doc_id = "DOC-999"
    title = "Escribe Aquí el Título del Documento"
    subtitle = "Subtítulo descriptivo que explica la función de esta ficha técnica o legal."
    author = "Tu Nombre / Comisión CERO"
    version = "v1.0"
    date = "16.07.2026"
    
    # Define paragraphs: [Section Title, Section Paragraph Content]
    sections = [
        ["Propósito del Documento de Plantilla", 
         "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut ut molestie erat. In hac habitasse platea dictumst. Vestibulum molestie justo non nibh gravida eleifend. Pellentesque a convallis diam. Suspendisse potenti.\\n\\n"
         "Mauris et tristique magna, sed dapibus enim. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Nam accumsan risus vitae congue pellentesque. Cras tincidunt hendrerit magna ac ultrices."],
        
        ["Pautas para Inserción de Contenidos",
         "Puedes usar la etiqueta especial '\\\\n' (que el compilador traduce como salto de línea HTML '<br/>') para separar párrafos. Las fuentes se configuran automáticamente como Outfit (si están descargadas en el sistema) o Helvetica por defecto."],
        
        ["Cumplimiento y Regulación",
         "Este documento forma parte del Data Room oficial de CERO. Cualquier alteración de los logotipos, colores corporativos o tipografías anulará la validez técnica ante las auditorías del laboratorio IDIADA y los mecenas."]
    ]
    
    # Define optional table data (Columns widths are calculated automatically to distribute 504pt)
    table_data = [
        ["Identificador", "Parámetro Técnico", "Tolerancia", "Estado de Revisión"],
        ["ING-CHA-01", "Chasis Spaceframe Tubular", "± 0.5 mm", "Aprobado (FEA)"],
        ["ING-SUS-01", "Mangueta Delantera Al", "± 0.05 mm", "Comprado (COTS)"],
        ["ING-BAT-01", "Pack Celdas Litio 18650", "350V Nom.", "Fabricación"]
    ]
    
    # Run the builder
    build_cero_pdf(filename, doc_id, title, subtitle, author, version, date, sections, table_data)
