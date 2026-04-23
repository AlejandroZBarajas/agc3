import numpy as np
import random
from individuo import calcular_duracion, calcular_if_promedio

def funcion_aptitud(individuo, config):

    dur = calcular_duracion(individuo)
    intensidades = [i for _, i in individuo]
    total = len(individuo)

    # -------------------------------
    # 1. FITNESS POR TIPO DE BLOQUE
    # -------------------------------
    fit_bloques = 0

    for idx, (_, if_) in enumerate(individuo):

        # calentamiento / enfriamiento (zona media)
        if idx == 0 or idx == total - 1:
            objetivo = 0.65
            fit_bloques += max(0, 1 - abs(if_ - objetivo))

        # intervalos (zonas altas)
        elif idx % 2 == 1:
            if_min, if_max = config["if_range"]

            # 🔥 en vez de un punto, usamos rango suave
            if if_min <= if_ <= if_max:
                fit_bloques += 1
            else:
                # cae suavemente fuera del rango
                dist = min(abs(if_ - if_min), abs(if_ - if_max))
                fit_bloques += max(0, 1 - dist)

        # recuperación (zonas bajas)
        else:
            if 0.4 <= if_ <= 0.65:
                fit_bloques += 1
            else:
                dist = min(abs(if_ - 0.4), abs(if_ - 0.65))
                fit_bloques += max(0, 1 - dist)

    fit_bloques /= total

    # -------------------------------
    # 2. DURACIÓN
    # -------------------------------
    dur_min, dur_max = config["duracion_total"]

    if dur_min <= dur <= dur_max:
        fit_dur = 1
    else:
        centro = (dur_min + dur_max) / 2
        error = abs(dur - centro) / centro
        fit_dur = max(0, 1 - error)

    # -------------------------------
    # 3. VARIABILIDAD (SIN PENALIZAR)
    # -------------------------------
    std_if = np.std(intensidades)

    # 🔥 premiar variabilidad directamente
    fit_var = min(std_if / 0.2, 1.0)

    # -------------------------------
    # 4. CONTRASTE GLOBAL
    # -------------------------------
    contraste = max(intensidades) - min(intensidades)
    fit_contraste = min(contraste / 0.6, 1.0)

    # -------------------------------
    # 5. FITNESS FINAL (SIN RESTAS)
    # -------------------------------
    fitness = (
        0.4 * fit_bloques +
        0.2 * fit_dur +
        0.2 * fit_var +
        0.2 * fit_contraste
    )

    # pequeño ruido para evitar clones exactos
    fitness += random.uniform(-0.01, 0.01)

    return max(0, fitness)