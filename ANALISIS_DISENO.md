# Análisis y diseño previo del simulador

## Objetivo de aprendizaje

Que el estudiante explique los patrones clásicos de inhibición reversible a partir de los estados enzimáticos disponibles y de los cambios en la curva de Michaelis-Menten, en lugar de memorizar únicamente flechas de Km y Vmax.

## Núcleo del modelo

### Variable independiente principal
- Concentración de sustrato `[S]` (mM).

### Variables independientes adicionales
- Concentración de inhibidor `[I]` (mM).
- Kic, Kiu o Ki (mM), según el mecanismo.
- Km basal (mM) y Vmax basal (unidades/min), como parámetros explorables del sistema.

### Variables dependientes
- Velocidad inicial `v0` (unidades/min).
- Km aparente (mM).
- Vmax aparente (unidades/min).
- Factores adimensionales alpha y alpha_prime.

### Ecuaciones

Basal:

`v0 = Vmax*S/(Km+S)`

General reversible:

`alpha = 1 + I/Kic`

`alpha_prime = 1 + I/Kiu`

`v = Vmax*S/(alpha*Km + alpha_prime*S)`

`Vmax_app = Vmax/alpha_prime`

`Km_app = (alpha/alpha_prime)*Km`

## Condiciones iniciales pedagógicas

- Vmax = 100 unidades/min
- Km = 2.0 mM
- [S] = 2.0 mM
- [I] = 2.0 mM cuando corresponda
- Kic/Kiu/Ki = 2.0 mM como punto de partida general; en mixta se inicia con Kic = 1.0 y Kiu = 2.0 para mostrar un cambio visible de Km.

## Rangos permitidos

- [S]: 0.1–20 mM
- [I]: 0–10 mM
- Km: 0.1–10 mM
- Vmax: 10–200 unidades/min
- Kic/Kiu/Ki: 0.1–10 mM

Son rangos pedagógicos, no intervalos fisiológicos universales.

## Supuestos

1. Se trabaja con velocidad inicial.
2. La cinética basal es compatible con Michaelis-Menten simple.
3. La inhibición reversible se representa mediante alpha y alpha_prime.
4. La no competitiva pura se trata como caso especial de mixta con Kic = Kiu.
5. Las figuras representan estados cinéticos de manera didáctica, no toda la complejidad estructural molecular.

## Limitaciones

No se modelan cooperatividad, sistemas multisustrato, tight binding, inhibición por sustrato, unión lenta, residence time ni inactivación irreversible/dependiente del tiempo. Lineweaver-Burk se incluye únicamente con valor histórico y pedagógico.

## Diseño pedagógico

La experiencia sigue:

**predecir → modificar variables → simular → observar → comparar → registrar → analizar → interpretar → aplicar**.

Se incluyen cinco experimentos guiados y una actividad libre. Las figuras suministradas se muestran al lado de la gráfica para vincular representación molecular y matemática.

## Validación esperada

- Control: S=Km=2, Vmax=100 → v=50.
- Competitiva con alpha=2 → Km_app=4, Vmax_app=100.
- Acompetitiva con alpha_prime=2 → Km_app=1, Vmax_app=50.
- No competitiva pura con alpha=alpha_prime=2 → Km_app=2, Vmax_app=50.
- Mixta con alpha=2 y alpha_prime=1.5 → Km_app≈2.67, Vmax_app≈66.67.
