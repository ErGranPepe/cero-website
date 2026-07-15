# DOC-008: Manufacturing Plan
**Plan de Corte, Soldadura TIG y Protocolo de Seguridad Eléctrica**

- **Autor**: Taller y Fabricación CERO
- **Estado**: APROBADO
- **Versión**: v16.0
- **Fecha**: 15.07.2026

---

## 1. Plan de Corte y Biselado CNC del Cromoly 4130

La fabricación del chasis spaceframe requiere precisión geométrica absoluta para evitar desviaciones axiales. Los tubos de acero 4130 Chromoly de 1.0 y 1.25 pulgadas se cortan y biselan utilizando una entalladora (notcher) CNC en base a las plantillas exportadas del Onshape. Las juntas deben quedar con una tolerancia de separación inferior a 0.5 mm para garantizar la penetración y resistencia del cordón de soldadura TIG, minimizando tensiones térmicas residuales que distorsionen el chasis.

## 2. Requerimientos Eléctricos y TIG de Taller

Para la soldadura TIG a 120-160 amperios de las uniones de cromoly, un garaje doméstico estándar con potencia contratada de 2.2 kW es totalmente insuficiente e inseguro. Es obligatorio disponer de una potencia contratada mínima de **5.5 kW a 230V** (o una toma industrial trifásica de 400V a 16A) para soportar de manera simultánea la soldadora de alta frecuencia, la refrigeración líquida de la antorcha, la bomba de vacío y el compresor de aire sin caídas de tensión que debiliten la penetración del arco. Se realizará purga de argón interna (back-purging) a 5L/min en el interior de los tubos estructurales para evitar la oxidación y la formación de 'flores de óxido' internas, garantizando una soldadura de calidad aeroespacial.

## 3. Protocolo de Seguridad de Celdas de Litio y Fuga Térmica

El ensamblaje y almacenamiento del pack de baterías (480 celdas 18650) exige un riguroso protocolo de seguridad química:
• Almacenamiento Refractario: Todas las celdas y módulos a medio montar deben almacenarse en contenedores metálicos herméticos llenos de arena seca de sílice o esferas de vidrio extinguibles especiales. Esto asfixia el oxígeno en caso de cortocircuito.
• Prevención de Fuga Térmica (Thermal Runaway): Queda terminantemente prohibido soldar celdas con calor directo (soldadura de estaño). El ensamblaje de contactos se realizará mediante soldadora de puntos por resistencia CNC por impulsos cortos de 5ms. El taller contará con ventilación forzada conectada a un extractor exterior y extintores de clase D específicos para fuego de metales y celdas de litio.