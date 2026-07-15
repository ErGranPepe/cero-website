import os
import sys
import json
import shutil
import urllib.request
import matplotlib.pyplot as plt
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Download premium Outfit fonts from Google Fonts
def download_font(url, dest):
    try:
        if not os.path.exists(dest):
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            print(f"[FONT] Descargando fuente desde {url}...")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                with open(dest, 'wb') as out_file:
                    out_file.write(response.read())
            print(f"[FONT] Descargada con éxito en {dest}")
    except Exception as e:
        print(f"[FONT] Advertencia: No se pudo descargar la fuente {os.path.basename(dest)}: {e}")

base_dir = os.path.dirname(os.path.abspath(__file__))
font_dir = os.path.join(base_dir, "assets", "brand")
outfit_reg_path = os.path.join(font_dir, "Outfit-Regular.ttf")
outfit_bold_path = os.path.join(font_dir, "Outfit-Bold.ttf")

download_font("https://raw.githubusercontent.com/Outfitio/Outfit-Fonts/main/fonts/ttf/Outfit-Regular.ttf", outfit_reg_path)
download_font("https://raw.githubusercontent.com/Outfitio/Outfit-Fonts/main/fonts/ttf/Outfit-Bold.ttf", outfit_bold_path)

if os.path.exists(outfit_reg_path) and os.path.exists(outfit_bold_path):
    try:
        pdfmetrics.registerFont(TTFont('Outfit', outfit_reg_path))
        pdfmetrics.registerFont(TTFont('Outfit-Bold', outfit_bold_path))
        FONT_NAME = 'Outfit'
        FONT_BOLD = 'Outfit-Bold'
        print("[FONT] Usando fuente premium registrada: Outfit")
    except Exception as e:
        print(f"[FONT] Error al registrar la fuente: {e}. Usando Helvetica.")
        FONT_NAME = 'Helvetica'
        FONT_BOLD = 'Helvetica-Bold'
else:
    FONT_NAME = 'Helvetica'
    FONT_BOLD = 'Helvetica-Bold'
    print("[FONT] Usando fuente por defecto: Helvetica")


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

    def draw_page_elements(self, page_count):
        doc_template = getattr(self, "_doctemplate", None)
        doc_id = getattr(doc_template, "doc_id", "DOC-XXX")
        
        # Clean cover page (let the story handle cover visual layout)
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setStrokeColor(colors.HexColor("#FF3B30"))
        self.setLineWidth(1)
        self.line(54, 738, 558, 738)
        
        # Draw the official black logo in running page header
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "brand", "logo_black_on_transparent.png")
        if os.path.exists(logo_path):
            try:
                self.drawImage(logo_path, 54, 742, width=18, height=18, mask='auto')
            except Exception:
                pass
        
        self.setFont(FONT_BOLD, 8)
        self.setFillColor(colors.HexColor("#1C1C1E"))
        self.drawString(80, 746, "CERO MOTOR CO. — DOCUMENTO OFICIAL")
        self.drawRightString(558, 746, doc_id)

        self.setStrokeColor(colors.HexColor("#E5E5EA"))
        self.setLineWidth(1)
        self.line(54, 54, 558, 54)
        
        self.setFont(FONT_NAME, 8)
        self.setFillColor(colors.HexColor("#8E8E93"))
        self.drawString(54, 38, "CONFIDENCIAL — PROHIBIDA SU DISTRIBUCIÓN COMERCIAL")
        self.drawRightString(558, 38, f"Pág. {self._pageNumber} de {page_count}")
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
        fontName=FONT_BOLD,
        fontSize=24,
        leading=30,
        textColor=colors.HexColor('#1C1C1E'),
        spaceAfter=10
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#8E8E93'),
        spaceAfter=25
    )
    
    h1_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Normal'],
        fontName=FONT_BOLD,
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#FF3B30'),
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=9.5,
        leading=14.5,
        textColor=colors.HexColor('#1C1C1E'),
        spaceAfter=12
    )
    
    meta_label_style = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName=FONT_BOLD,
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#555559')
    )
    
    meta_val_style = ParagraphStyle(
        'MetaValue',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#1C1C1E')
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName=FONT_BOLD,
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    story = []
    
    # PREMIUM REDESIGNED COVER PAGE
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "brand", "logo_black_on_transparent.png")
    if os.path.exists(logo_path):
        try:
            story.append(Image(logo_path, width=70, height=70))
        except Exception:
            story.append(Spacer(1, 40))
    else:
        story.append(Spacer(1, 40))
        
    story.append(Spacer(1, 15))
    story.append(Paragraph(doc_id, ParagraphStyle('CoverDocId', fontName=FONT_BOLD, fontSize=14, leading=18, textColor=colors.HexColor('#FF3B30'), spaceAfter=5)))
    story.append(Paragraph(doc_info['title'].upper(), title_style))
    story.append(Paragraph(doc_info['subtitle'], subtitle_style))
    
    # Red accent divider line
    story.append(Table([['']], colWidths=[504], rowHeights=[3], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FF3B30')), ('BOTTOMPADDING', (0,0), (-1,-1), 0), ('TOPPADDING', (0,0), (-1,-1), 0)]))
    story.append(Spacer(1, 20))
    
    # Branded disclosure text
    disclosure_style = ParagraphStyle(
        'CoverDisclosure',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#8E8E93')
    )
    story.append(Paragraph("<b>DATA ROOM DE INGENIERÍA Y OPERACIONES CERO</b><br/>"
                           "Este documento contiene especificaciones técnicas, estratégicas, de sourcing y de marketing del primer coche de calle del mundo co-diseñado por internet. "
                           "Toda contribución queda bajo la licencia abierta Creative Commons Attribution-NonCommercial 4.0 (CC BY-NC 4.0). "
                           "La reproducción o uso comercial de esta información sin la aprobación explícita del Core Team de CERO está prohibida.", disclosure_style))
    
    story.append(Spacer(1, 150))
    
    # Metadata card table
    meta_data = [
        [Paragraph("AUTOR:", meta_label_style), Paragraph(doc_info['author'].upper(), meta_val_style), Paragraph("ESTADO:", meta_label_style), Paragraph(doc_info['status'], meta_val_style)],
        [Paragraph("VERSIÓN:", meta_label_style), Paragraph(doc_info['version'], meta_val_style), Paragraph("FECHA:", meta_label_style), Paragraph(doc_info['date'], meta_val_style)]
    ]
    
    meta_table = Table(meta_data, colWidths=[80, 170, 70, 184])
    meta_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F2F2F7')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E5EA')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E5EA')),
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
            story.append(Image(img_path, width=400, height=220))
            story.append(Spacer(1, 10))
            
        # Additional mapped images for illustrated functional documents
        if doc_id == "DOC-021":
            ex_path = os.path.join(assets_dir, "funding_burn_rate.png")
            if os.path.exists(ex_path):
                story.append(Spacer(1, 10))
                story.append(Image(ex_path, width=400, height=220))
                story.append(Spacer(1, 10))
        elif doc_id == "DOC-004":
            ex_path = os.path.join(assets_dir, "channel_roles_diagram.png")
            if os.path.exists(ex_path):
                story.append(Spacer(1, 10))
                story.append(Image(ex_path, width=400, height=220))
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
    
    for section_title, section_text in doc_info['sections']:
        content.append(f"\n## {section_title}\n")
        content.append(section_text)
        
    if "table" in doc_info:
        content.append("\n### Tabla de Referencia\n")
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


# Generates high-contrast matplotlib diagrams inside the assets folder.
def generate_diagrams(assets_dir):
    os.makedirs(assets_dir, exist_ok=True)
    
    # 1. project_timeline_gantt.png
    gantt_path = os.path.join(assets_dir, "project_timeline_gantt.png")
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=150)
    tasks = [
        ("1. Concepto y Ergonomía (Onshape)", 0, 3, "Diseño"),
        ("2. Modelado de Chasis CAD V1", 3, 3, "Diseño"),
        ("3. FEA Estructural y CFD Aire", 6, 3, "Diseño"),
        ("4. Diseño de Acumulador y BMS", 9, 3, "Diseño"),
        ("5. Congelación CAD V2 (Hito)", 11.5, 0.5, "Diseño"),
        ("6. Adquisición del Motor Emrax 228", 11, 2, "Sourcing"),
        ("7. Sourcing Acero 4130 Cromoly", 12, 2, "Sourcing"),
        ("8. Adquisición Celdas Litio 18650", 13, 2, "Sourcing"),
        ("9. Mesa Jig de Soldadura", 14, 2, "Fabricación"),
        ("10. Corte y Biselado de Tubos", 15, 2, "Fabricación"),
        ("11. Soldadura TIG del Chasis", 16, 3, "Fabricación"),
        ("12. Pintura en Polvo Chasis", 18.5, 1, "Fabricación"),
        ("13. Soldadura de Celdas Acumulador", 19, 2, "Integración"),
        ("14. Montaje de Suspensión y Ruedas", 20, 2, "Integración"),
        ("15. Fontanería Frenos y Refrigeración", 21, 2, "Integración"),
        ("16. Cableado Inversor y Baja Tensión", 22, 2, "Integración"),
        ("17. Shakedown y Pruebas Pista", 23, 2, "Validación"),
        ("18. Medidas de Aislamiento IMD bender", 24, 2, "Validación"),
        ("19. Dossier IDIADA / INTA (EV)", 25, 2, "Validación"),
        ("20. Inspección ITV / Placas Calle", 26, 2, "Validación")
    ]
    category_colors = {
        "Diseño": "#FF3B30", "Sourcing": "#8E8E93", "Fabricación": "#1C1C1E",
        "Integración": "#444446", "Validación": "#AEAEB2"
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
        Patch(facecolor="#FF3B30", edgecolor="black", label="Diseño CAD & Simulación (EV)"),
        Patch(facecolor="#8E8E93", edgecolor="black", label="Logística & Sourcing (Baterías)"),
        Patch(facecolor="#1C1C1E", edgecolor="black", label="Fabricación & Taller Jig"),
        Patch(facecolor="#444446", edgecolor="black", label="Integración Tren Motriz (HV/LV)"),
        Patch(facecolor="#AEAEB2", edgecolor="black", label="Homologación & ITV Calle")
    ]
    ax.legend(handles=legend_elements, loc="lower right", fontsize=7.5, framealpha=0.9)
    plt.title("GANTT MAESTRO CERO ELÉCTRICO: PLAN DE DESARROLLO Y HOMOLOGACIÓN VIAL (28 MESES)", fontsize=9, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(gantt_path, bbox_inches='tight')
    plt.close()
    print("Generado Diagrama: project_timeline_gantt.png")

    # 2. financial_breakdown.png
    fin_path = os.path.join(assets_dir, "financial_breakdown.png")
    fig, ax = plt.subplots(figsize=(7, 4.2), dpi=150)
    categories = [
        "Motor Emrax 228", "Chasis Acero 4130", "Frenos y Dirección",
        "Seguridad / Extintor", "Electrónica y Cableado", "Tasas Homologación (IDIADA)",
        "Ensayos Lab (Ruido/Aisla)", "Celdas Litio 18650 + BMS"
    ]
    track_costs = [1500, 0, 900, 850, 350, 0, 0, 0]
    street_extra = [2000, 600, 200, 400, 600, 2500, 1800, 2450]
    y_pos = np.arange(len(categories))
    ax.barh(y_pos, track_costs, color="#1C1C1E", edgecolor="black", height=0.55, label="Proyecto Pista Básico (€3.600)", zorder=3)
    ax.barh(y_pos, street_extra, left=track_costs, color="#FF3B30", edgecolor="black", height=0.55, label="Coste Extra Homologación Eléctrica Calle (+€10.550)", zorder=3)
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
    plt.title("COMPARATIVA ESTRUCTURAL DE COSTES: PISTA VS HOMOLOGACIÓN CALLE EV", fontsize=10, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(fin_path, bbox_inches='tight')
    plt.close()
    print("Generado Diagrama: financial_breakdown.png")

    # 3. growth_funnel.png
    funnel_path = os.path.join(assets_dir, "growth_funnel.png")
    fig, ax = plt.subplots(figsize=(7, 3.5), dpi=150)
    stages = ["Core Team\n(Votos en Discord)", "Colaboradores\n(GitHub Commits)", "Comunidad Discord\n(Miembros Activos)", "Alcance Social\n(Espectadores Reels)"]
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
    materials = ["Acero Dulce\n25.4mm x 2.0mm", "Cromoly 4130\n25.4mm x 1.2mm", "Cromoly 4130\n25.4mm x 1.6mm", "Cromoly 4130\n25.4mm x 2.0mm\n(FIA/FSAE Min)"]
    strength = [250, 360, 480, 630]
    ax.barh(materials, strength, color=['#E5E5EA', '#8E8E93', '#1C1C1E', '#FF3B30'], edgecolor='black', height=0.55)
    ax.set_xlabel("Límite Elástico de Tracción / Resistencia (MPa)", fontsize=8, fontweight="bold", labelpad=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#8E8E93')
    ax.spines['bottom'].set_color('#8E8E93')
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    ax.set_title("EMBUDO DE CONVERSIÓN EN CANALES DE PARTICIPACIÓN", fontsize=10, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(fsae_path, bbox_inches='tight')
    plt.close()
    print("Generado Diagrama: growth_funnel.png")

    # 5. volunteer_onboarding_pipeline.png
    onb_path = os.path.join(assets_dir, "volunteer_onboarding_pipeline.png")
    fig, ax = plt.subplots(figsize=(7, 3.5), dpi=150)
    ax.axis('off')
    steps_onb = [
        ("1. Discord", "Unión vía Link\nen Redes"),
        ("2. Asignar Rol", "Elección de Perfil\n#roles (CAD/Mkt)"),
        ("3. Micro-Reto", "Reto de 2 horas\n(Filtro de Interés)"),
        ("4. Core Review", "Aprobación y\nFusión en GitHub"),
        ("5. Contrato", "Devengo de Equity\nvesting de 12m")
    ]
    x_pos_onb = [0.1, 0.3, 0.5, 0.7, 0.9]
    for i, (title, desc) in enumerate(steps_onb):
        ax.text(x_pos_onb[i], 0.5, f"{title}\n\n{desc}",
                ha='center', va='center', fontsize=7,
                bbox=dict(boxstyle="round,pad=0.7", fc="#F2F2F7" if i < 4 else "#FF3B30", ec="#E5E5EA", lw=1),
                color="#1C1C1E" if i < 4 else "#FFFFFF")
        if i < 4:
            ax.annotate('', xy=(x_pos_onb[i+1] - 0.07, 0.5), xytext=(x_pos_onb[i] + 0.07, 0.5),
                        arrowprops=dict(arrowstyle="-|>", color="#FF3B30", lw=1.2))
    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 1.0)
    plt.title("FLUJO DE RECLUTAMIENTO Y ONBOARDING DE VOLUNTARIOS CERO", fontsize=9, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(onb_path, bbox_inches='tight')
    plt.close()
    print("Generado Diagrama: volunteer_onboarding_pipeline.png")

    # 6. weekly_operational_cycle.png
    cycle_path = os.path.join(assets_dir, "weekly_operational_cycle.png")
    fig, ax = plt.subplots(figsize=(7, 3.5), dpi=150)
    ax.axis('off')
    days = [
        ("Lunes", "TikTok/Reels\nLanzamiento teaser"),
        ("Miércoles", "Filmar Vlog\nGrabación en garaje"),
        ("Jueves", "Hilo X/LinkedIn\nExplicación operacional"),
        ("Sábado", "YouTube Vlog\nVídeo largo semanal"),
        ("Domingo", "Asamblea General\nDiscord 20:00 CEST")
    ]
    x_pos_cycle = [0.1, 0.3, 0.5, 0.7, 0.9]
    for i, (day, action) in enumerate(days):
        ax.text(x_pos_cycle[i], 0.5, f"{day}\n\n{action}",
                ha='center', va='center', fontsize=7,
                bbox=dict(boxstyle="round,pad=0.7", fc="#FFFFFF", ec="#1C1C1E" if i == 4 else "#8E8E93", lw=1.2),
                color="#1C1C1E")
        if i < 4:
            ax.annotate('', xy=(x_pos_cycle[i+1] - 0.07, 0.5), xytext=(x_pos_cycle[i] + 0.07, 0.5),
                        arrowprops=dict(arrowstyle="-|>", color="#FF3B30", lw=1.2))
    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 1.0)
    plt.title("CICLO EDITORIAL Y OPERATIVO SEMANAL CERO", fontsize=9, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(cycle_path, bbox_inches='tight')
    plt.close()
    print("Generado Diagrama: weekly_operational_cycle.png")

    # 7. garage_sourcing_flow.png
    gar_path = os.path.join(assets_dir, "garage_sourcing_flow.png")
    fig, ax = plt.subplots(figsize=(7, 3.5), dpi=150)
    ax.axis('off')
    nodes = [
        ("Búsqueda", "Móstoles/Alcorcón\nNaves industriales"),
        ("Contacto", "Llamada fría\nAgencias y dueños"),
        ("Propuesta", "Permuta publicitaria\nEspacio por vlogs"),
        ("Negociación", "Fijar consumo luz\nLímite TIG welding"),
        ("Cierre", "Firma contrato\nBorrador Permuta")
    ]
    x_pos_gar = [0.1, 0.3, 0.5, 0.7, 0.9]
    for i, (node, desc) in enumerate(nodes):
        ax.text(x_pos_gar[i], 0.5, f"{node}\n\n{desc}",
                ha='center', va='center', fontsize=7,
                bbox=dict(boxstyle="round,pad=0.7", fc="#FFFFFF", ec="#FF3B30", lw=1.2),
                color="#1C1C1E")
        if i < 4:
            ax.annotate('', xy=(x_pos_gar[i+1] - 0.07, 0.5), xytext=(x_pos_gar[i] + 0.07, 0.5),
                        arrowprops=dict(arrowstyle="-|>", color="#8E8E93", lw=1.2))
    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 1.0)
    plt.title("PROCESO DE PROSPECCIÓN Y NEGOCIACIÓN DEL GARAJE CERO", fontsize=9, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(gar_path, bbox_inches='tight')
    plt.close()
    print("Generado Diagrama: garage_sourcing_flow.png")

    # 8. patreon_revenue_distribution.png
    pat_path = os.path.join(assets_dir, "patreon_revenue_distribution.png")
    fig, ax = plt.subplots(figsize=(7, 3.5), dpi=150)
    labels = ['Baterías (Litio)', 'Herramientas/CO2', 'Tasas Homologación', 'Consumibles (Argón)', 'Stripe/Patreon']
    sizes = [35, 20, 25, 15, 5]
    colors_list = ['#FF3B30', '#1C1C1E', '#8E8E93', '#AEAEB2', '#E5E5EA']
    ax.pie(sizes, labels=labels, autopct='%1.0f%%', startangle=90, colors=colors_list, 
           textprops={'fontsize': 8, 'weight': 'bold'}, wedgeprops={'edgecolor': 'black', 'linewidth': 0.8})
    ax.axis('equal')
    plt.title("DISTRIBUCIÓN FUNCIONAL DE FONDOS DE PATREON / CROWDFUNDING", fontsize=9, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(pat_path, bbox_inches='tight')
    plt.close()
    print("Generado Diagrama: patreon_revenue_distribution.png")

    # 9. legal_ip_transfer_map.png
    ip_path = os.path.join(assets_dir, "legal_ip_transfer_map.png")
    fig, ax = plt.subplots(figsize=(7, 3.5), dpi=150)
    ax.axis('off')
    ax.text(0.15, 0.5, "Colaboradores\n(Cesión de IP)", ha='center', va='center', fontsize=7.5,
            bbox=dict(boxstyle="square,pad=0.5", fc="#F8F9FA", ec="#8E8E93"), color="#1C1C1E")
    ax.annotate('', xy=(0.32, 0.5), xytext=(0.25, 0.5),
                arrowprops=dict(arrowstyle="-|>", color="#FF3B30", lw=1.2))
    ax.text(0.5, 0.5, "Asociación Cultural CERO\n(Entidad Abierta sin Ánimo de Lucro)", ha='center', va='center', fontsize=7.5,
            bbox=dict(boxstyle="square,pad=0.5", fc="#E5E5EA", ec="#1C1C1E"), color="#1C1C1E")
    ax.annotate('', xy=(0.7, 0.5), xytext=(0.63, 0.5),
                arrowprops=dict(arrowstyle="-|>", color="#FF3B30", lw=1.2))
    ax.text(0.85, 0.5, "CERO S.L.\n(Sociedad Comercial\ny Producción)", ha='center', va='center', fontsize=7.5,
            bbox=dict(boxstyle="square,pad=0.5", fc="#FF3B30", ec="#FF3B30"), color="#FFFFFF")
    ax.text(0.85, 0.8, "Ronda Semilla\nInversores (€)", ha='center', va='center', fontsize=7,
            bbox=dict(boxstyle="round,pad=0.4", fc="#1C1C1E", ec="#1C1C1E"), color="#FFFFFF")
    ax.annotate('', xy=(0.85, 0.6), xytext=(0.85, 0.72),
                arrowprops=dict(arrowstyle="-|>", color="#1C1C1E", lw=1.0))
    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 1.0)
    plt.title("MAPA ESTRUCTURAL DE TRANSFERENCIA DE PROPIEDAD INTELECTUAL (IP)", fontsize=9, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(ip_path, bbox_inches='tight')
    plt.close()
    print("Generado Diagrama: legal_ip_transfer_map.png")

    # 10. itv_homologation_steps.png
    itv_path = os.path.join(assets_dir, "itv_homologation_steps.png")
    fig, ax = plt.subplots(figsize=(7, 3.5), dpi=150)
    ax.axis('off')
    steps_itv = [
        ("1. Ficha\nReducida", "Firma Ingeniero\nColegiado"),
        ("2. Informe\nConformidad", "IDIADA / INTA\nFEA Crash exemption"),
        ("3. Ensayos\nPista", "Pruebas de freno\ny nivel de ruido"),
        ("4. ITV\nEstación", "Inspección física\ny pesaje oficial"),
        ("5. Placas\nCalle", "Obtención de matrícula\nordinaria de calle")
    ]
    x_pos_itv = [0.1, 0.3, 0.5, 0.7, 0.9]
    for i, (step, desc) in enumerate(steps_itv):
        ax.text(x_pos_itv[i], 0.5, f"{step}\n\n{desc}",
                ha='center', va='center', fontsize=7,
                bbox=dict(boxstyle="round,pad=0.7", fc="#F2F2F7", ec="#8E8E93", lw=1),
                color="#1C1C1E")
        if i < 4:
            ax.annotate('', xy=(x_pos_itv[i+1] - 0.07, 0.5), xytext=(x_pos_itv[i] + 0.07, 0.5),
                        arrowprops=dict(arrowstyle="-|>", color="#FF3B30", lw=1.2))
    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 1.0)
    plt.title("FLUJO ADMINISTRATIVO EN ESPAÑA: HOMOLOGACIÓN INDIVIDUAL (HIV)", fontsize=9, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(itv_path, bbox_inches='tight')
    plt.close()
    print("Generado Diagrama: itv_homologation_steps.png")

    # 11. funding_burn_rate.png
    burn_path = os.path.join(assets_dir, "funding_burn_rate.png")
    fig, ax = plt.subplots(figsize=(7, 3.5), dpi=150)
    months = np.arange(0, 13, 1)
    reserves_base = 50000 - 3500 * months
    reserves_opt = 50000 - 2500 * months + 1000 * np.sqrt(months)
    ax.plot(months, reserves_base, color="#1C1C1E", linewidth=2, label="Runway Escenario Base (Gasto Fijo)")
    ax.plot(months, reserves_opt, color="#FF3B30", linewidth=2.2, label="Runway Escenario Eficiente CERO")
    ax.set_xlabel("Meses de Desarrollo (Ronda Semilla)", fontsize=8, fontweight="bold", labelpad=10)
    ax.set_ylabel("Reservas Financieras de Caja (€)", fontsize=8, fontweight="bold", labelpad=10)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 60000)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#8E8E93')
    ax.spines['bottom'].set_color('#8E8E93')
    ax.legend(loc="lower left", fontsize=8)
    plt.title("PROYECCIÓN DE RUNWAY Y CONSUMO DE CAJA (BURN RATE)", fontsize=9, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(burn_path, bbox_inches='tight')
    plt.close()
    print("Generado Diagrama: funding_burn_rate.png")

    # 12. channel_roles_diagram.png
    roles_path = os.path.join(assets_dir, "channel_roles_diagram.png")
    fig, ax = plt.subplots(figsize=(7, 3.5), dpi=150)
    ax.text(0.5, 0.85, "CORE TEAM (Mario / Lead Engineer)\n[Aprobación Estratégica, Caja, Sourcing]", 
            ha="center", va="center", bbox=dict(boxstyle="round,pad=0.5", facecolor="#FF3B30", edgecolor="black"), 
            fontsize=9, color="white", fontweight="bold")
    ax.text(0.5, 0.55, "COMISIONES DE INGENIERÍA (Online Volunteers)\n[CAD Baterías, FEA Estructural, CFD Aerodinámica, BMS]", 
            ha="center", va="center", bbox=dict(boxstyle="round,pad=0.5", facecolor="#1C1C1E", edgecolor="black"), 
            fontsize=8.5, color="white")
    ax.text(0.5, 0.25, "COMUNIDAD GENERAL (Discord / Patreon)\n[Debates Abiertos, Votaciones de Diseño, Soporte]", 
            ha="center", va="center", bbox=dict(boxstyle="round,pad=0.5", facecolor="#8E8E93", edgecolor="black"), 
            fontsize=8, color="white")
    ax.arrow(0.5, 0.77, 0, -0.12, head_width=0.03, head_length=0.05, fc='black', ec='black')
    ax.arrow(0.5, 0.47, 0, -0.12, head_width=0.03, head_length=0.05, fc='black', ec='black')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    plt.title("JERARQUÍA DE GOBERNANZA Y ROLES COMUNITARIOS CERO", fontsize=9, fontweight="bold", pad=10)
    plt.tight_layout()
    plt.savefig(roles_path, bbox_inches='tight')
    plt.close()
    print("Generado Diagrama: channel_roles_diagram.png")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    documents_dir = os.path.join(base_dir, "documents")
    assets_dir = os.path.join(documents_dir, "assets")
    
    # Clean the old documents folder (except assets/brand)
    if os.path.exists(documents_dir):
        for item in os.listdir(documents_dir):
            item_path = os.path.join(documents_dir, item)
            if item == "assets":
                # Clean assets children except brand
                for asset_item in os.listdir(item_path):
                    asset_item_path = os.path.join(item_path, asset_item)
                    if asset_item != "brand":
                        if os.path.isdir(asset_item_path):
                            shutil.rmtree(asset_item_path)
                        else:
                            os.remove(asset_item_path)
                continue
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
    os.makedirs(documents_dir, exist_ok=True)
    os.makedirs(assets_dir, exist_ok=True)
    
    # 1. Generate standard Matplotlib diagrams
    generate_diagrams(assets_dir)
    
    # 2. Copy the actual FEA and vehicle dynamics simulation plots from output_cad/ (if they exist)
    fea_source = os.path.join(base_dir, "output_cad", "chassis_fea.png")
    dyn_source = os.path.join(base_dir, "output_cad", "dynamics_plot.png")
    
    if os.path.exists(fea_source):
        shutil.copy(fea_source, os.path.join(assets_dir, "chassis_fea.png"))
        print("[COMPILER] Copiado mapa de tensiones estructurales real: chassis_fea.png")
    else:
        print("[COMPILER] Advertencia: No se encontró chassis_fea.png real. Usando placeholder.")
        
    if os.path.exists(dyn_source):
        shutil.copy(dyn_source, os.path.join(assets_dir, "dynamics_plot.png"))
        print("[COMPILER] Copiado gráfico dinámico real de slalom: dynamics_plot.png")
    else:
        print("[COMPILER] Advertencia: No se encontró dynamics_plot.png real. Usando placeholder.")

    # 2.5 Copy generated reference images from brain artifacts using glob
    import glob
    brain_dir = os.path.join(base_dir, "..", "..", "brain", "ef78b327-4617-43fd-842c-68d7f84986df")
    
    wood_matches = glob.glob(os.path.join(brain_dir, "cero_wood_mockup_*.png"))
    if wood_matches:
        shutil.copy(wood_matches[0], os.path.join(assets_dir, "cero_wood_mockup.png"))
        print("[COMPILER] Copiado mockup de madera real: cero_wood_mockup.png")
    else:
        print("[COMPILER] Advertencia: No se encontró cero_wood_mockup.png en artifacts.")
        
    garage_matches = glob.glob(os.path.join(brain_dir, "cero_garage_workshop_*.png"))
    if garage_matches:
        shutil.copy(garage_matches[0], os.path.join(assets_dir, "cero_garage_workshop.png"))
        print("[COMPILER] Copiado taller mecánico real: cero_garage_workshop.png")
    else:
        print("[COMPILER] Advertencia: No se encontró cero_garage_workshop.png en artifacts.")
    
    # 3. Load cero_docs_db.json
    db_path = os.path.join(base_dir, "cero_docs_db.json")
    if not os.path.exists(db_path):
        print(f"Error: {db_path} not found.")
        sys.exit(1)
        
    with open(db_path, "r", encoding="utf-8") as f:
        doc_database = json.load(f)
    
    # 4. Iterate through the database and write documents to organized category folders
    for doc_id, doc_info in doc_database.items():
        category = doc_info.get("category", "00_Gobernanza_y_Estrategia")
        category_dir = os.path.join(documents_dir, category)
        os.makedirs(category_dir, exist_ok=True)
        
        create_pdf(doc_id, doc_info, category_dir, assets_dir)
        create_markdown(doc_id, doc_info, category_dir)
        
    print("\n--- ¡TODOS LOS 31 DOCUMENTOS COMPILADOS CON 12 GRÁFICOS ILUSTRADOS (Y REALES DE SIMULACIÓN)! ---")
