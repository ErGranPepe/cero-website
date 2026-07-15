# DOC-007: Technical Architecture
**Arquitectura Mecánica y Eléctrica del Monoplaza Eléctrico**

- **Autor**: Ingeniería CERO
- **Estado**: APROBADO
- **Versión**: v15.0
- **Fecha**: 15.07.2026

---

## 1. Arquitectura de Sistemas de Tracción Eléctrica

El tren motriz de CERO utiliza un motor síncrono de imanes permanentes y flujo axial Emrax 228 montado en el subchasis trasero. Transmisión directa mediante acoplamiento rígido hacia un diferencial autoblocante Drexler tarado para Formula Student, transmitiendo el par a los palieres traseros de acero 300M.

El sistema de acumulador de alta tensión (HV) utiliza celdas de litio 18650 encapsuladas en un contenedor estructural de fibra de carbono. Un sistema de gestión de baterías (Orion BMS) monitorea constantemente el voltaje de cada celda y su temperatura, comunicándose por bus CAN con el inversor Bamocar D3 para limitar la corriente en caso de sobretemperatura.

## 2. Geometría de Dirección y Comportamiento Dinámico Ackerman

A continuación se muestra el análisis geométrico de la dirección Ackerman y su porcentaje de desviación (85% Ackerman) para el comportamiento óptimo de guiado en curva del eje delantero:

## 3. Rigidez de Amortiguación y Ratio de Fuerza de Rueda

A continuación se ilustra la curva de rigidez de los coilovers progresivos de moto en función del recorrido de rueda (mm) y la fuerza aplicada (N):

## 4. Arquitectura de Suspensión y Geometría de Dirección

Geometría de suspensión de doble trapecio independiente en las 4 ruedas. El diseño cinemático en Onshape optimiza el centro de balanceo (Roll Center) manteniéndolo a 45 mm del suelo en reposo. Manguetas (uprights) delanteras y traseras fresadas por control numérico (CNC) en aluminio aeronáutico 7075-T6 para minimizar la masa no suspendida. Brazos de suspensión diseñados con perfiles elípticos aerodinámicos para reducir la resistencia al avance.

Cremallera de dirección mecánica directa de kart modificada con 1.5 vueltas de tope a tope, garantizando una respuesta inmediata y precisa en circuito cerrado y carreteras de curvas. El brazo de dirección incorpora un diseño de Ackerman al 85% para reducir el arrastre de neumáticos en curvas cerradas urbanas.

## 5. Arquitectura Eléctrica y Gestión Electrónica (ECU)

Mazo de cables de baja tensión (LV) aligerado de cables innecesarios. La ECU principal de diseño propio con microcontrolador Teensy 4.1 gestiona la adquisición de datos, lectura de aceleradores Hall duales redundantes y comunicación con el inversor.

Se integra un dispositivo de monitoreo de aislamiento (IMD Bender) que corta la línea de seguridad (Shutdown loop) si detecta una fuga de corriente entre el sistema de alta tensión (HV) y el chasis de baja tensión (LV). Todo el tendido eléctrico se aloja en fundas termorretráctiles Raychem DR-25.