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
        doc_id = getattr(doc_template, "doc_id", "DOC-A1")
        
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
    
    # 1. project_timeline_gantt.png (Fase 0-1 Timeline)
    gantt_path = os.path.join(assets_dir, "project_timeline_gantt.png")
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=150)
    
    tasks = [
        ("1. Diseño de Narrativa y Storytelling", 0, 4, "Narrativa"),
        ("2. Lanzamiento Redes e Hype Inicial", 1, 6, "Medios"),
        ("3. Reclutamiento y Onboarding Discord", 3, 5, "Equipo"),
        ("4. Mapeo y Visita de Locales", 5, 5, "Sourcing"),
        ("5. Trueques y Canjes de Branding", 7, 5, "Sourcing"),
        ("6. Alquiler/Cierre de Garaje (Hito)", 11, 1, "Hito")
    ]
    
    category_colors = {
        "Narrativa": "#FF3B30",
        "Medios": "#1C1C1E",
        "Equipo": "#8E8E93",
        "Sourcing": "#444446",
        "Hito": "#AEAEB2"
    }
    
    y_labels = [t[0] for t in tasks]
    starts = [t[1] for t in tasks]
    durations = [t[2] for t in tasks]
    colors_list = [category_colors[t[3]] for t in tasks]
    
    y_pos = np.arange(len(tasks))
    ax.barh(y_pos, durations, left=starts, color=colors_list, edgecolor="black", height=0.5, zorder=3)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(y_labels, fontsize=8, fontweight="bold", color="#1C1C1E")
    ax.set_xlabel("Semanas de Ejecución (Fase 0-1)", fontsize=9, fontweight="bold", color="#1C1C1E", labelpad=10)
    ax.set_xlim(0, 12)
    ax.set_xticks(range(0, 13, 1))
    
    ax.grid(axis='x', linestyle='--', alpha=0.5, zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#8E8E93')
    ax.spines['bottom'].set_color('#8E8E93')
    
    ax.invert_yaxis()
    plt.title("GANTT DE FASE 0-1: CONCEPTO, COMUNIDAD Y ADQUISICIÓN DE GARAJE (12 SEMANAS)", 
              fontsize=9, fontweight="bold", pad=12, color="#000000")
    plt.tight_layout()
    plt.savefig(gantt_path, bbox_inches='tight')
    plt.close()
    print("Generado Diagrama: project_timeline_gantt.png")
    
    # 2. financial_breakdown.png (Costes Fase 0-1 y Homologación)
    fin_path = os.path.join(assets_dir, "financial_breakdown.png")
    fig, ax = plt.subplots(figsize=(7, 4), dpi=150)
    
    categories = [
        "Alojamiento Web & Discord",
        "Consumibles de Taller Inicial",
        "Merchandising y Muestras",
        "Patreon Stripe Fees",
        "Fondo Reserva Compra Motor",
        "Tasas Homologación (IDIADA)",
        "Ensayos Lab (Gases/Ruido)"
    ]
    
    conceptual_costs = [150, 300, 200, 150, 1200, 0, 0]
    homologation_extra = [0, 0, 0, 0, 0, 2500, 3000]
    
    y_pos = np.arange(len(categories))
    
    ax.barh(y_pos, conceptual_costs, color="#1C1C1E", edgecolor="black", height=0.5, label="Fase 0-1 Inicial (€2.000)", zorder=3)
    ax.barh(y_pos, homologation_extra, left=conceptual_costs, color="#FF3B30", edgecolor="black", height=0.5, label="Fase 2-3 Homologación Calle (+€5.500)", zorder=3)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories, fontsize=8, fontweight="bold")
    ax.set_xlabel("Coste Estimado (€)", fontsize=9, fontweight="bold", labelpad=10)
    ax.set_xlim(0, 6000)
    ax.grid(axis='x', linestyle='--', alpha=0.5, zorder=0)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#8E8E93')
    ax.spines['bottom'].set_color('#8E8E93')
    
    ax.legend(loc="lower right", fontsize=8)
    plt.title("PRESUPUESTO ESTRUCTURAL: FASE CONCEPTUAL VS VIAL CALLE", fontsize=10, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(fin_path, bbox_inches='tight')
    plt.close()
    print("Generado Diagrama: financial_breakdown.png")
    
    # 3. growth_funnel.png (Embudo de Adquisición de Espacios)
    funnel_path = os.path.join(assets_dir, "growth_funnel.png")
    fig, ax = plt.subplots(figsize=(6, 3.5), dpi=150)
    stages = [
        "1. Locales Cerrados\n(Firma del Barter)",
        "2. Visitas en Taller\n(Reunión Física)",
        "3. Llamadas / Leads\n(Idealista & Redes)",
        "4. Mapeo de Naves\n(Móstoles & Alcorcón)"
    ]
    values = [1, 5, 25, 60]
    y_pos = np.arange(len(stages))
    
    ax.barh(y_pos, values, color=['#FF3B30', '#1C1C1E', '#8E8E93', '#E5E5EA'], edgecolor='black', height=0.55)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(stages, fontsize=8, fontweight="bold")
    ax.set_xlabel("Número de Espacios Mapeados y Contactados", fontsize=8, fontweight="bold", labelpad=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#8E8E93')
    ax.spines['bottom'].set_color('#8E8E93')
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    ax.set_title("EMBUDO DE CAPTACIÓN DE ESPACIO FÍSICO", fontsize=10, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(funnel_path, bbox_inches='tight')
    plt.close()
    print("Generado Diagrama: growth_funnel.png")
    
    # 4. kpi_projections.png (KPI de Suscriptores)
    kpi_path = os.path.join(assets_dir, "kpi_projections.png")
    fig, ax = plt.subplots(figsize=(7, 3.5), dpi=150)
    weeks = np.arange(0, 13, 2)
    members = [0, 50, 200, 600, 1500, 3200, 5000]
    
    ax.plot(weeks, members, color='#FF3B30', linewidth=2.5, marker='o', markersize=5)
    ax.set_xlabel("Semanas desde Lanzamiento", fontsize=8, fontweight="bold", labelpad=10)
    ax.set_ylabel("Miembros de Discord Activos", fontsize=8, fontweight="bold", labelpad=10)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5500)
    ax.set_xticks(range(0, 13, 2))
    ax.grid(linestyle='--', alpha=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#8E8E93')
    ax.spines['bottom'].set_color('#8E8E93')
    ax.set_title("PROYECCIÓN DE CRECIMIENTO DE LA COMUNIDAD EN FASE 0-1", fontsize=10, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(kpi_path, bbox_inches='tight')
    plt.close()
    print("Generado Diagrama: kpi_projections.png")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    documents_dir = os.path.join(base_dir, "documents")
    assets_dir = os.path.join(documents_dir, "assets")
    
    # 1. Clean the old documents folder completely to make it a flat structure
    if os.path.exists(documents_dir):
        # We preserve only the assets subfolder
        for item in os.listdir(documents_dir):
            item_path = os.path.join(documents_dir, item)
            if item == "assets":
                continue
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
    else:
        os.makedirs(documents_dir, exist_ok=True)
        
    os.makedirs(assets_dir, exist_ok=True)
    
    # 2. Generate non-technical diagrams
    generate_diagrams(assets_dir)
    
    # 3. Load cero_docs_db.json
    db_path = os.path.join(base_dir, "cero_docs_db.json")
    if not os.path.exists(db_path):
        print(f"Error: {db_path} not found.")
        sys.exit(1)
        
    with open(db_path, "r", encoding="utf-8") as f:
        doc_database = json.load(f)
    
    # 4. Generate the DOC-A1 to DOC-A8 documents FLAT inside /documents/
    for doc_id, doc_info in doc_database.items():
        create_pdf(doc_id, doc_info, documents_dir, assets_dir)
        create_markdown(doc_id, doc_info, documents_dir)
        
    print("\n--- ¡ECOSISTEMA DOCUMENTAL CONCEPTUAL FASE 0-1 COMPILADO FLAT EXITOSAMENTE! ---")
