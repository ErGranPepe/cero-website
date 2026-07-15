# DOC-005: Product Requirements Document
**Ficha de Especificaciones Técnicas del Vehículo, Dinámica de Fluidos y Homologación de Calle**

- **Autor**: Ingeniería CERO
- **Estado**: APROBADO
- **Versión**: v14.0
- **Fecha**: 15.07.2026

---

## 1. Filosofía de Ingeniería y Sistemas Automotrices

El documento de requerimientos de producto (PRD) de CERO se ha estructurado bajo los estándares de ingeniería de sistemas de la NASA (NASA Systems Engineering Handbook, SP-2016-6105). El objetivo es diseñar, simular y fabricar un vehículo monoplaza de calle con un coste de adquisición inicial de 0€, optimizando al límite el peso estructural y la rigidez torsional.

El monoplaza debe combinar la agilidad en curva de un kart de competición con el cumplimiento estricto de los requisitos legales del Reglamento General de Vehículos en España y las directivas de homologación individual de la Unión Europea (Reglamento UE 2018/858).

## 2. Especificaciones de Sistemas Dinámicos y Mecánicos

• Chasis Tubular: Estructura espacial triangulada (spaceframe) fabricada en tubos de acero aleado al cromo-molibdeno 4130 (normativa aeronáutica MIL-T-6736 B). El arco principal de seguridad antivuelco (Main Hoop) tendrá un diámetro de 25.4 mm y un espesor de pared mínimo de 2.0 mm. La rigidez torsional estructural de diseño objetivo es de 1.800 Nm/grado, validada por simulaciones numéricas de elementos finitos (FEA) bajo cargas estáticas axiales y de torsión de 5G.
• Suspensión Cinemática: Configuración de doble trapecio independiente (double wishbone) delantero y trasero. Brazos fabricados en tubo 4130 de 19.0 mm x 1.5 mm, unidos mediante rótulas esféricas de competición (uniball) de rosca métrica fina grado automotriz. Amortiguación ajustable de moto de alto rendimiento (tipo Coilover) montada con sistema de bieletas push-rod para optimizar el ratio de movimiento y el control de balanceo.
• Sistema de Frenado Independiente: Pinzas Brembo de doble pistón opuesto y discos ventilados delanteros de 240 mm. El pedalier de competición incluirá dos bombas de freno independientes Wilwood conectadas mediante una barra de equilibrio (bias bar) mecánica ajustable en cabina. Esto garantiza el doble circuito independiente exigido por ley: si ocurre una fuga en el circuito delantero, el circuito trasero retiene capacidad de frenado estática superior al 45%.

## 3. Tren Motriz de Combustión e Inyección Electrónica

El motor seleccionado es el bloque de cuatro cilindros en línea de la Suzuki GSX-R 600 K6-K7. Especificaciones de ingeniería:
• Cilindrada: 599 cc, relación de compresión de 12.5:1.
• Potencia: 125 hp a 13.500 RPM, par motor de 64 Nm a 11.500 RPM.
• Transmisión: Caja de cambios secuencial de 6 velocidades integrada, embrague de moto multidisco en baño de aceite. Transmisión secundaria por cadena de competición paso 530 de alta resistencia al estiramiento (resistencia a la rotura por tracción > 40 kN).
• Sistema de Escape de Calle: Colector de escape de acero inoxidable 304, convertidor catalítico de tres vías homologado Euro 6, sonda lambda para control de mezcla estequiométrica (ECU cerrada) y silenciador acústico (ONU 51) con dB-killer para mantener el nivel de presión sonora por debajo de los 74 dB(A) a 5.000 RPM.

## 4. Requerimientos Legales para Homologación de Calle en España (ITV)

Para la obtención de placas de matrícula ordinarias mediante el proceso de Homologación Individual de Vehículos (HIV):
• Iluminación: Integración de luces de posición, cruce, carretera, intermitentes, emergencia, luz de marcha atrás, antiniebla trasera y luz de matrícula con código de homologación europeo 'E' grabado en las lentes.
• Seguridad Peatonal (Radios de Curvatura): El exterior de la carrocería de composite (fibra de vidrio) debe ser completamente suave, sin salientes punzantes ni aristas. Todos los radios de curvatura exteriores en superficies expuestas deben ser superiores a 2.5 mm.
• Retrovisores: Dos retrovisores exteriores con espejo convexo que permitan un campo de visión horizontal mínimo de 15 metros a una distancia de 10 metros detrás del coche.