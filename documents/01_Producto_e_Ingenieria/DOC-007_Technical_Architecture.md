# DOC-007: Technical Architecture
**Arquitectura Mecánica y Eléctrica del Monoplaza de Combustión**

- **Autor**: Ingeniería CERO
- **Estado**: APROBADO
- **Versión**: v12.0
- **Fecha**: 15.07.2026

---

## 1. Arquitectura de Sistemas de Combustión

El tren motriz de CERO utiliza un motor de moto Suzuki GSX-R transversal montado directamente en cunas antivibración soldadas al chasis trasero. Transmisión secuencial a cadena paso 530 hacia un eje trasero equipado con un diferencial Quaife ATB LSD para asegurar tracción en curva sin pérdidas de potencia.

El sistema de combustible cumple normas de seguridad de la FIA: depósito de combustible de aluminio con espuma interna deflactora para evitar el oleaje, bomba de inyección externa de alta presión (3 bar) con regulador de presión integrado, y tuberías de combustible trenzadas de teflón AN-6 con racores roscados blindados contra el calor.

## 2. Arquitectura de Suspensión y Geometría de Dirección

Geometría de suspensión de doble trapecio independiente en las 4 ruedas. El diseño cinemático en Onshape optimiza el centro de balanceo (Roll Center) manteniéndolo a 45 mm del suelo en reposo. Manguetas (uprights) delanteras y traseras fresadas por control numérico (CNC) en aluminio aeronáutico 7075-T6 para minimizar la masa no suspendida.

Cremallera de dirección mecánica directa de kart modificada con 1.5 vueltas de tope a tope, garantizando una respuesta inmediata y precisa en circuito cerrado y carreteras de curvas.

## 3. Arquitectura Eléctrica y Gestión Electrónica (ECU)

Cableado original de la moto Suzuki aligerado de cables innecesarios. Mantenemos la ECU Keihin original desbloqueada (mapeo con inmovilizador HISS puenteado) para no tener que invertir en una ECU programable de competición de 2.000€.

Cuadro de mandos digital multifunción conectado por bus de datos K-line original para visualizar en cabina las revoluciones, temperatura del refrigerante y presión del aceite, con sistema de corte de corriente de emergencia (cortacorrientes FIA) accesible tanto por el piloto desde el interior como por los comisarios desde el exterior en el arco principal.