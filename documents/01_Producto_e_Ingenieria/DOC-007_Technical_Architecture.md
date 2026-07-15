# DOC-007: Technical Architecture
**Arquitectura Mecánica y Eléctrica del Monoplaza Eléctrico**

- **Autor**: Ingeniería CERO
- **Estado**: APROBADO
- **Versión**: v16.0
- **Fecha**: 15.07.2026

---

## 1. Arquitectura de Sistemas de Tracción Eléctrica (General)

El tren motriz de CERO utiliza un motor síncrono de imanes permanentes montado en el subchasis trasero. Transmisión directa mediante acoplamiento hacia un diferencial autoblocante, transmitiendo el par a los palieres traseros de acero. El sistema de acumulador de alta tensión (HV) utiliza celdas de litio encapsuladas en un contenedor estructural ignífugo. Un sistema de gestión de baterías (BMS) monitorea constantemente el voltaje de cada celda y su temperatura, comunicándose por bus CAN con el inversor de tracción para limitar la corriente en caso de sobretemperatura. La especificación final de marcas comerciales se cerrará junto con los ingenieros y patrocinadores definitivos.

## 2. Estructura y Flujo Legal de Propiedad Intelectual

A continuación se ilustra de forma gráfica el flujo legal de cesión de aportaciones técnicas por parte de los colaboradores a la Asociación Cultural CERO y su posterior aportación en la constitución de CERO S.L.:

## 3. Arquitectura de Suspensión y Geometría de Dirección

Geometría de suspensión de doble trapecio independiente en las 4 ruedas. El diseño cinemático en Onshape optimiza el centro de balanceo (Roll Center) manteniéndolo a 45 mm del suelo en reposo. Manguetas (uprights) delanteras y traseras fresadas por control numérico (CNC) en aluminio aeronáutico para minimizar la masa no suspendida. Brazos de suspensión diseñados con perfiles elípticos aerodinámicos para reducir la resistencia al avance. Cremallera de dirección mecánica directa de kart modificada con 1.5 vueltas de tope a tope, garantizando una respuesta inmediata y precisa. El brazo de dirección incorpora un diseño de Ackerman al 85% para reducir el arrastre de neumáticos en curvas cerradas.

## 4. Arquitectura Eléctrica y Gestión Electrónica (ECU)

Mazo de cables de baja tensión (LV) aligerado de cables innecesarios. La ECU principal de diseño propio gestiona la adquisición de datos, lectura de aceleradores Hall duales redundantes y comunicación con el inversor. Se integra un dispositivo de monitoreo de aislamiento (IMD) que corta la línea de seguridad (Shutdown loop) si detecta una fuga de corriente entre el sistema de alta tensión (HV) y el chasis de baja tensión (LV).