#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
==============================================================================
CERO MOTOR CO. - REUSABLE DOCUMENT TEMPLATE GENERATOR
==============================================================================
Use this script to compile additional CERO PDFs matching the official suite's 
premium technical styling (using the custom registered 'Outfit' Google Font,
mixed header logos, running footers, and structured section styling).

Usage:
  1. Modify the document metadata and sections array in the main block below.
  2. Run the script:
     $ .venv/Scripts/python.exe create_cero_document.py
==============================================================================
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.pdfgen import canvas

# Define project assets locations
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BRAND_DIR = os.path.join(PROJECT_ROOT, "assets", "brand")
LOGO_WHITE_PATH = os.path.join(BRAND_DIR, "logo_white_on_transparent.png")
LOGO_BLACK_PATH = os.path.join(BRAND_DIR, "logo_black_on_transparent.png")
FONT_REGULAR_PATH = os.path.join(BRAND_DIR, "Outfit-Regular.ttf")
FONT_BOLD_PATH = os.path.join(BRAND_DIR, "Outfit-Bold.ttf")

# ==========================================
# 1. FONT REGISTRATION
# ==========================================
def register_cero_fonts():
    try:
        pdfmetrics.registerFont(TTFont('Outfit', FONT_REGULAR_PATH))
        pdfmetrics.registerFont(TTFont('Outfit-Bold', FONT_BOLD_PATH))
        pdfmetrics.registerFontFamily('Outfit', normal='Outfit', bold='Outfit-Bold')
        print("[FONT] Outfit and Outfit-Bold registered successfully.")
    except Exception as e:
        print(f"[FONT WARNING] Failed to register local Outfit font, falling back to Helvetica: {e}")

# ==========================================
# 2. RUNNING HEADER / FOOTER CANVAS
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
            self.draw_page_decorations(num_pages)
            super(CeroNumberedCanvas, self).showPage()
        super(CeroNumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # Omit headers and footers on the cover page (Page 1)
        if self._pageNumber == 1:
            self.restoreState()
            return

        # Setup standard styles
        self.setFont("Outfit" if "Outfit" in pdfmetrics.getRegisteredFontNames() else "Helvetica", 9)
        self.setFillColor(colors.HexColor("#7a808a")) # Soft technical gray

        # Draw running header text (left side)
        self.drawString(54, 750, "CERO MOTOR CO. - DOCUMENTO DE OPERACIONES")
        self.setStrokeColor(colors.HexColor("#1d222b"))
        self.setLineWidth(1)
        self.line(54, 742, 558, 742) # Letter width is 612, margins 54pt each side

        # Draw small mixin logo in the header (right side)
        if os.path.exists(LOGO_WHITE_PATH):
            try:
                # Header is dark, draw white logo
                self.drawImage(LOGO_WHITE_PATH, 518, 748, width=40, height=18, mask='auto')
            except Exception:
                pass

        # Draw running footer line
        self.line(54, 60, 558, 60)
        self.drawString(54, 45, "PROYECTO CERO | MOTOR CO.")
        
        # Page numbers
        page_text = f"PÁGINA {self._pageNumber} DE {page_count}"
        self.drawRightString(558, 45, page_text)
        
        self.restoreState()

# ==========================================
# 3. PDF COMPILING ENGINE
# ==========================================
def build_cero_pdf(filename, title, subtitle, author, version, date, sections):
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

    styles = getSampleStyleSheet()
    
    # Define color scheme (Obsidian Stealth palette)
    c_white = colors.HexColor("#ffffff")
    c_neon = colors.HexColor("#00e5ff") # Neon blue accent
    c_gray = colors.HexColor("#9ca3af")
    c_border = colors.HexColor("#1d222b")

    # Font names mapping
    f_reg = 'Outfit' if 'Outfit' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'
    f_bold = 'Outfit-Bold' if 'Outfit-Bold' in pdfmetrics.getRegisteredFontNames() else 'Helvetica-Bold'

    # Typography styles
    style_cover_title = ParagraphStyle(
        'CoverTitle',
        fontName=f_bold,
        fontSize=28,
        leading=34,
        textColor=c_white,
        spaceAfter=15,
        alignment=0 # Left aligned
    )

    style_cover_sub = ParagraphStyle(
        'CoverSub',
        fontName=f_reg,
        fontSize=13,
        leading=18,
        textColor=c_gray,
        spaceAfter=30
    )

    style_h1 = ParagraphStyle(
        'SectionH1',
        fontName=f_bold,
        fontSize=15,
        leading=20,
        textColor=c_neon,
        spaceBefore=18,
        spaceAfter=10,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'BodyTextCustom',
        fontName=f_reg,
        fontSize=10.5,
        leading=15.5,
        textColor=c_white,
        spaceAfter=12
    )

    story = []

    # ==========================================
    # COVER PAGE BLOCK (Obsidian layout)
    # ==========================================
    story.append(Spacer(1, 40))
    # Mixin Brand Logo
    if os.path.exists(LOGO_WHITE_PATH):
        story.append(Image(LOGO_WHITE_PATH, width=120, height=54))
        story.append(Spacer(1, 30))
    
    # Decorative neon bar accent
    bar_data = [[""]]
    bar_table = Table(bar_data, colWidths=[150], rowHeights=[4])
    bar_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_neon),
        ('PADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(bar_table)
    story.append(Spacer(1, 20))

    # Titles and metadata
    story.append(Paragraph(title.upper(), style_cover_title))
    story.append(Paragraph(subtitle, style_cover_sub))
    story.append(Spacer(1, 80))

    # Meta-table (Author, version, date)
    meta_data = [
        [
            Paragraph(f"<b>AUTOR:</b> {author}", style_body),
            Paragraph(f"<b>VERSIÓN:</b> {version}", style_body),
            Paragraph(f"<b>FECHA:</b> {date}", style_body)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[200, 150, 150])
    meta_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(meta_table)
    
    # Pagebreak to start content on Page 2
    story.append(PageBreak())

    # ==========================================
    # SECTIONS BLOCK
    # ==========================================
    for sec_idx, (sec_title, sec_body) in enumerate(sections):
        story.append(Paragraph(f"{sec_idx + 1}. {sec_title}", style_h1))
        # Support formatting inside strings (like newlines)
        body_text_normalized = sec_body.replace("\n", "<br/>")
        story.append(Paragraph(body_text_normalized, style_body))
        story.append(Spacer(1, 10))

    # Build document in dark-mode base
    def on_first_page(canvas_obj, doc_obj):
        canvas_obj.saveState()
        canvas_obj.setFillColor(colors.HexColor("#05070a")) # Stealth background
        canvas_obj.rect(0, 0, doc_obj.pagesize[0], doc_obj.pagesize[1], fill=True, stroke=False)
        canvas_obj.restoreState()

    def on_later_pages(canvas_obj, doc_obj):
        canvas_obj.saveState()
        canvas_obj.setFillColor(colors.HexColor("#05070a"))
        canvas_obj.rect(0, 0, doc_obj.pagesize[0], doc_obj.pagesize[1], fill=True, stroke=False)
        canvas_obj.restoreState()

    doc.build(
        story,
        onFirstPage=on_first_page,
        onLaterPages=on_later_pages,
        canvasmaker=CeroNumberedCanvas
    )
    print(f"[COMPILER] Reusable CERO document successfully generated: {filename}")


# ==========================================
# 4. MAIN CUSTOMIZATION BLOCK
# ==========================================
if __name__ == "__main__":
    # Custom details for the new document template
    filename = "DOC-999_CERO_Custom_Template.pdf"
    title = "Template Document Title"
    subtitle = "Subtítulo explicativo del documento para inversores y colaboradores."
    author = "Tu Nombre / Área CERO"
    version = "v1.0"
    date = "16.07.2026"
    
    # Define paragraphs as a list of lists: [Section Title, Section Paragraph Content]
    sections = [
        ["Objetivo de la Plantilla", 
         "Esta plantilla sirve para expandir la biblioteca técnica de CERO de forma consistente. Cualquier ingeniero de la comunidad puede clonar este script de Python, añadir su contenido y compilar un PDF con el mismo estilo obsidian premium que el resto de documentos del Data Room."],
        
        ["Pautas de Estilo y Tipografía",
         "Asegúrate de registrar las fuentes Outfit en tu máquina de desarrollo o de tener la conexión a internet activa la primera vez que ejecutas el compilador. Se recomienda mantener los títulos de secciones en mayúsculas y las listas explicadas con saltos de línea claros."],
        
        ["Exclusividad de Marca CERO",
         "Cualquier documento generado con este script debe portar los logotipos oficiales de CERO en su cabecera y pie de página, indicando la versión de revisión activa."]
    ]
    
    # Run the builder
    build_cero_pdf(filename, title, subtitle, author, version, date, sections)
