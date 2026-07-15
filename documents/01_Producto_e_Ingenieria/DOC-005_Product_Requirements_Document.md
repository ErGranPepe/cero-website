# DOC-005: Product Requirements Document
**Ficha de Requerimientos ITV de Calle, Ergonomía y Homologación**

- **Autor**: Ingeniería CERO
- **Estado**: APROBADO
- **Versión**: v16.0
- **Fecha**: 15.07.2026

---

## 1. Filosofía de Ingeniería y Sistemas Automotrices

El documento de requerimientos de producto (PRD) de CERO se ha estructurado bajo los estándares de ingeniería de sistemas de la NASA (NASA Systems Engineering Handbook, SP-2016-6105). El objetivo es diseñar, simular y fabricar un vehículo monoplaza de calle con un coste de adquisición inicial de 0€, optimizando al límite el peso estructural y la rigidez torsional.

El monoplaza debe combinar la agilidad en curva de un kart de competición con el cumplimiento estricto de los requisitos legales del Reglamento General de Vehículos en España y las directivas de homologación individual de la Unión Europea (Reglamento UE 2018/858).

## 2. Especificaciones de Sistemas Dinámicos y Mecánicos

• Chasis Tubular: Estructura espacial triangulada (spaceframe) fabricada en tubos de acero aleado al cromo-molibdeno 4130. El arco principal de seguridad antivuelco (Main Hoop) tendrá un diámetro de 25.4 mm y un espesor de pared mínimo de 2.0 mm, dimensionado para alojar un piloto del percentil 95 (1.90 m de altura).
• Susrubricación Cinemática: Configuración de doble trapecio independiente (double wishbone) delantero y trasero. Brazos fabricados en tubo 4130, unidos mediante rótulas esféricas de competición (uniball) de rosca métrica fina grado automotriz. Amortiguación ajustable montada con sistema de bieletas push-rod para optimizar el ratio de movimiento y el control de balanceo.
• Sistema de Frenado Independiente: Pinzas de doble pistón opuesto y discos ventilados. El pedalier de competición incluirá dos bombas de freno independientes conectadas mediante una barra de equilibrio (bias bar) mecánica ajustable en cabina. Esto garantiza el doble circuito independiente exigido por ley: si ocurre una fuga en el circuito delantero, el circuito trasero retiene capacidad de frenado estática superior al 45%.

## 3. Tren Motriz Eléctrico e Inversor de Tracción (Conceptual)

El coche utilizará un motor eléctrico síncrono de imanes permanentes montado en el subchasis trasero en una zona protegida contra colisiones laterales. La especificación exacta del motor y del inversor de tracción será definida por el equipo de ingenieros y patrocinadores una vez completada la fase conceptual, basándose en la disponibilidad de canje o compra Patreon:
• Tipo de Motor: Imanes permanentes de flujo axial, refrigeración líquida.
• Par y Potencia de Diseño: Potencia máxima objetivo de 80-100 kW, par máximo de 240 Nm.
• Inversor: Controlador trifásico de alta tensión controlado por bus CAN a 500 kbps.
• Sistema de Batería: Acumulador de iones de litio encapsulado en un contenedor ignífugo de fibra de carbono y Nomex.

## 4. Curva de Potencia y Par del Motor Eléctrico (Conceptual)

A continuación se ilustra la curva de potencia (hp) y par motor (Nm) en función de las revoluciones por minuto (RPM) proyectada para el bloque motor:

## 5. Distribución de Fuerzas de Frenado Frontal y Trasera

A continuación se muestra el análisis de distribución de fuerzas hidráulicas de frenado y la línea de adherencia óptima calculada para evitar el bloqueo del eje trasero:

## 6. Requerimientos Legales para Homologación de Calle en España (ITV)

Para la obtención de placas de matrícula ordinarias mediante el proceso de Homologación Individual de Vehículos (HIV):

• Ficha Reducida: Documento técnico detallado firmado por ingeniero colegiado que describe la geometría, masas y elementos de seguridad activa/pasiva.
• Informe de Conformidad: Emitido por un Servicio Técnico de Homologación oficial (como IDIADA o INTA), certificando que el diseño del chasis modular cumple con el Reglamento UE 2018/858. Se buscarán exenciones de crash-test destructivos mediante validaciones numéricas avanzadas por FEA.
• Ensayos en Pista Oficiales: Pruebas dinámicas de frenado en mojado, comportamiento dinámico de dirección a velocidad, nivel de ruido acústico y compatibilidad electromagnética en laboratorios acreditados.
• Inspección en Estación ITV: Verificación física final de los marcados de homologación 'E' en vidrios, ópticas, retrovisores convexos y radios de curvatura exteriores de carrocería superiores a 2.5 mm.
• Auditoría ex-ante: Se firmará un acuerdo con un laboratorio oficial (como IDIADA o el INTA) para realizar una revisión preliminar de los planos CAD antes de iniciar la fabricación física.