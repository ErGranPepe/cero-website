# DOC-027: Project Phase Dependencies and Gantt
**Secuencia Lógica de Construcción, Prerrequisitos de Hitos y Duración de Fases**

- **Autor**: Gestión de Proyectos CERO
- **Estado**: APROBADO
- **Versión**: v1.0
- **Fecha**: 15.07.2026

---

## 1. Duración del Proyecto y Criterio de Realismo

Aunque el objetivo es terminar el monoplaza de combustión en 28 meses, la falta de presupuesto inicial exige un control estricto de los prerrequisitos técnicos y la normativa de calle. Si un hito crítico se retrasa, el proyecto se congela automáticamente para evitar costes innecesarios. No compraremos materiales si no hay espacio físico donde almacenarlos.

## 2. Gráfico del Cronograma de Fases y Dependencias

A continuación se ilustra el cronograma general y la distribución temporal de las fases del monoplaza:

## 3. Dependencias Críticas (Qué debe estar listo antes de qué)

Para evitar fallos de montaje catastróficos, se establecen las siguientes dependencias innegociables:
• Dependencia 1: Motor Suzuki GSX-R físico medido (Fase 1) -> Requisito para Chasis CAD final (Fase 3).
No se puede cerrar el diseño de la parte trasera del chasis tubular en CAD sin haber escaneado en 3D (o medido físicamente) el motor Suzuki de desguace. Las tolerancias de los soportes del motor y la alineación del piñón de transmisión con el eje trasero deben ser exactas a nivel de décimas de milímetro para evitar que la cadena descarrile a alta velocidad.
• Dependencia 2: Congelación de CAD (Fase 3) -> Requisito para Encargar el Corte Láser (Fase 4).
No se puede solicitar a los patrocinadores el corte de tubos de acero 4130 cromoly antes de congelar las dimensiones del chasis. Cualquier modificación posterior obligará a tirar tubos inservibles, destruyendo la viabilidad financiera de 0 €.
• Dependencia 3: Cesión de Taller y Construcción de Jig (Fase 4) -> Requisito para Soldadura de Chasis (Fase 5).
Está prohibido empezar a soldar tubos en el aire. La soldadura TIG genera una distorsión térmica masiva que revira el metal. Se requiere construir una mesa de utillaje rígida (jig) de madera o acero atornillada al suelo plano para mantener los tubos en su sitio exacto mientras se sueldan.
• Dependencia 4: Circuitos de Dirección, Suspensión y Frenado (Fase 5) -> Requisito para Instalar el Escape y Motor (Fase 6).
La ergonomía y la seguridad de guiado son prioritarias. El motor de moto y el escape se montarán solo cuando la dirección manual y el pedalier de freno doble estén fijados y validados.
• Dependencia 5: Ensayos de Gases y Calibración de Emisiones (Fase 6) -> Requisito para Homologación de Calle IDIADA (Fase 7).
No se puede presentar el coche en las instalaciones de IDIADA para las pruebas dinámicas sin haber configurado y mapeado la sonda lambda y el catalizador Euro 6 en banco de potencia, asegurando que cumple los límites en frío.