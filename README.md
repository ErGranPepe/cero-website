# 🏁 CERO — El Coche de Internet

> **El primer monoplaza de calle desarrollado 100% en abierto por internet, partiendo de 0€ y construido mediante el poder de la comunidad.**

---

## 🎯 Fase Actual: Fase 0-1 (Concepto + Gente + Garaje)
CERO no es una multinacional del automóvil ni un proyecto industrial cerrado. Es un experimento social y creativo de código abierto.

**En esta fase inicial, no hay chasis soldados, no hay motores en el taller ni compras de materiales. Estamos concentrados en:**
1. Definir la narrativa humana del proyecto.
2. Construir la base de la comunidad en redes sociales y Discord.
3. Buscar y conseguir nuestro primer espacio físico (garaje o taller partner) en Móstoles o alrededores sin capital inicial.
4. Diseñar las dinámicas de gobierno abierto de los colaboradores.

---

## 📂 Estructura del Repositorio

Para facilitar la auditoría de la comunidad y la integración de inteligencias artificiales (como Perplexity), el repositorio está estructurado de manera simple y directa:

### 📄 Documentos de Operación Conceptual (`/documents/`)
Una lista plana de 8 documentos fundamentales que guían el día a día de esta fase 0-1:
*   [DOC-A1: Story and Narrative](file:///C:/Users/mario/.gemini/antigravity-ide/scratch/cero-website/documents/DOC-A1_Story_and_Narrative.md) — La historia humana detrás de CERO y el por qué del proyecto.
*   [DOC-A2: Social Media Playbook](file:///C:/Users/mario/.gemini/antigravity-ide/scratch/cero-website/documents/DOC-A2_Social_Media_Playbook.md) — Voz, tono y directrices de publicación en redes (vulnerabilidad radical).
*   [DOC-A3: 12-Week Content Calendar](file:///C:/Users/mario/.gemini/antigravity-ide/scratch/cero-website/documents/DOC-A3_12-Week_Content_Calendar.md) — Planificación temporal de contenidos semanales y ganchos virales.
*   [DOC-A4: Recruitment and Roles Guide](file:///C:/Users/mario/.gemini/antigravity-ide/scratch/cero-website/documents/DOC-A4_Recruitment_and_Roles_Guide.md) — Perfiles y roles humanos requeridos inicialmente.
*   [DOC-A5: Garage and Space Acquisition Plan](file:///C:/Users/mario/.gemini/antigravity-ide/scratch/cero-website/documents/DOC-A5_Garage_and_Space_Acquisition_Plan.md) — Rutas y estrategias de trueque para conseguir taller físico.
*   [DOC-A6: Community and Governance Charter](file:///C:/Users/mario/.gemini/antigravity-ide/scratch/cero-website/documents/DOC-A6_Community_and_Governance_Charter.md) — Dinámicas de voto y asambleas de Discord.
*   [DOC-A7: Pre-Seed Funding Strategy](file:///C:/Users/mario/.gemini/antigravity-ide/scratch/cero-website/documents/DOC-A7_Pre-Seed_Funding_Strategy.md) — Crowdfunding, tiers de Patreon y merch en impresión bajo demanda.
*   [DOC-A8: First 10 Videos Script Pack](file:///C:/Users/mario/.gemini/antigravity-ide/scratch/cero-website/documents/DOC-A8_First_10_Videos_Script_Pack.md) — Guiones y hooks de los vlogs iniciales de YouTube y TikTok.

### 🎨 Activos de Marca (`/assets/brand/`)
Logotipos de marca consistentes y listos para producción digital e impresa:
*   `logo_original_glow.png` — El logotipo original con el resplandor de iluminación de redes.
*   `logo_white_on_transparent.png` / `logo_black_on_transparent.png` / `logo_red_on_transparent.png` — PNGs limpios de alta resolución con fondo transparente.
*   `logo_white.svg` / `logo_black.svg` / `logo_red.svg` — Archivos vectoriales SVG reconstruidos geométricamente de forma ultra-ligera (<1KB).

### 🏛️ Histórico Técnico (`/legacy/`)
Contiene los borradores preliminares de especificaciones técnicas del vehículo (chasis tubular FSAE specs, motor GSX-R, frenado dual y tasas de homologación ITV) archivados para su uso en las fases 2 y 3.

---

## 🛠️ Herramientas de Compilación y Validación
*   `generate_cero_docs.py` — Script que genera los PDFs formales y Markdowns leyendo del manifiesto JSON.
*   `validate_cero_docs.py` — Suite de validación de calidad del repositorio. Comprueba esquemas JSON, enlaces internos, ausencia de regresiones de Matplotlib y peso de los archivos SVG.

---

## 🤝 Cómo Colaborar
Si eres diseñador CAD, editor de vídeo, gestor de redes o simplemente te apasiona el proyecto:
1. Únete al canal de Discord de CERO.
2. Preséntate en `#presentaciones` y cuéntanos qué te gustaría aprender o aportar.
3. Solicita acceso de lectura a los planos compartidos de Onshape.
