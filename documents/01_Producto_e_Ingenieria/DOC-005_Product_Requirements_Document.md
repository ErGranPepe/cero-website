# DOC-005: Product Requirements Document
**Ficha de Especificaciones Técnicas del Vehículo, Dinámica de Fluidos y Homologación de Calle**

- **Autor**: Ingeniería CERO
- **Estado**: APROBADO
- **Versión**: v15.0
- **Fecha**: 15.07.2026

---

## 1. Filosofía de Ingeniería y Sistemas Automotrices

El documento de requerimientos de producto (PRD) de CERO se ha estructurado bajo los estándares de ingeniería de sistemas de la NASA (NASA Systems Engineering Handbook, SP-2016-6105). El objetivo es diseñar, simular y fabricar un vehículo monoplaza de calle con un coste de adquisición inicial de 0€, optimizando al límite el peso estructural y la rigidez torsional.

El monoplaza debe combinar la agilidad en curva de un kart de competición con el cumplimiento estricto de los requisitos legales del Reglamento General de Vehículos en España y las directivas de homologación individual de la Unión Europea (Reglamento UE 2018/858).

## 2. Especificaciones de Sistemas Dinámicos y Mecánicos

• Chasis Tubular: Estructura espacial triangulada (spaceframe) fabricada en tubos de acero aleado al cromo-molibdeno 4130 (normativa aeronáutica MIL-T-6736 B). El arco principal de seguridad antivuelco (Main Hoop) tendrá un diámetro de 25.4 mm y un espesor de pared mínimo de 2.0 mm. La rigidez torsional estructural de diseño objetivo es de 1.800 Nm/grado, validada por simulaciones numéricas de elementos finitos (FEA) bajo cargas estáticas axiales y de torsión de 5G.
• Suspensión Cinemática: Configuración de doble trapecio independiente (double wishbone) delantero y trasero. Brazos fabricados en tubo 4130 de 19.0 mm x 1.5 mm, unidos mediante rótulas esféricas de competición (uniball) de rosca métrica fina grado automotriz. Amortiguación ajustable de moto de alto rendimiento (tipo Coilover) montada con sistema de bieletas push-rod para optimizar el ratio de movimiento y el control de balanceo.
• Sistema de Frenado Independiente: Pinzas Brembo de doble pistón opuesto y discos ventilados delanteros de 240 mm. El pedalier de competición incluirá dos bombas de freno independientes Wilwood conectadas mediante una barra de equilibrio (bias bar) mecánica ajustable en cabina. Esto garantiza el doble circuito independiente exigido por ley: si ocurre una fuga en el circuito delantero, el circuito trasero retiene capacidad de frenado estática superior al 45%.

## 3. Tren Motriz Eléctrico e Inversor de Tracción

El motor seleccionado es el bloque síncrono de imanes permanentes y flujo axial Emrax 228, de alto rendimiento y bajo peso. Especificaciones de ingeniería:
• Tipo de Motor: Imanes permanentes de flujo axial, refrigeración líquida.
• Potencia: Pico de 100 kW (134 hp), par máximo de 240 Nm a 6.000 RPM.
• Inversor: Bamocar D3, refrigerado por líquido, controlado por bus CAN a 500 kbps.
• Sistema de Acumulador: Tensión nominal de 350V, configuración 80S6P (480 celdas de iones de litio 18650 Samsung 30Q), contenedor ignífugo de fibra de carbono y Nomex.

## 4. Curva de Potencia y Par del Motor Eléctrico Emrax 228

A continuación se ilustra la curva de potencia (hp) y par motor (Nm) en función de las revoluciones por minuto (RPM) del bloque motor seleccionado:

## 5. Distribución de Fuerzas de Frenado Frontal y Trasera

A continuación se muestra el análisis de distribución de fuerzas hidráulicas de frenado y la línea de adherencia óptima calculada para evitar el bloqueo del eje trasero:

## 6. Requerimientos Legales para Homologación de Calle en España (ITV)

Para la obtención de placas de matrícula ordinarias mediante el proceso de Homologación Individual de Vehículos (HIV):
• Secuencia de Luces: Integración de luces de posición, cruce, carretera, intermitentes, emergencia, luz de marcha atrás, antiniebla trasera y luz de matrícula con código de homologación europeo 'E' grabado en las lentes.
• Seguridad Peatonal (Radios de Curvatura): El exterior de la carrocería de composite (fibra de vidrio) debe ser completamente suave, sin salientes punzantes ni aristas. Todos los radios de curvatura exteriores en superficies expuestas deben ser superiores a 2.5 mm.
• Retrovisores: Dos retrovisores exteriores con espejo convexo que permitan un campo de visión horizontal mínimo de 15 metros a una distancia de 10 metros detrás del coche.