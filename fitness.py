# fitness.py

from individuo import calcular_duracion, calcular_if_promedio

def funcion_aptitud(individuo, config):

    dur = calcular_duracion(individuo)
    if_prom = calcular_if_promedio(individuo)

    if_min, if_max = config["if_range"]
    dur_min, dur_max = config["duracion_total"]

    # 🎯 Objetivo REAL
    objetivo_if = (if_min + if_max) / 2

    # 🔥 Error IF (más agresivo)
    error_if = abs(if_prom - objetivo_if)
    fit_if = max(0, 1 - (error_if * 2))  # penalización fuerte

    # 🔥 Error duración
    centro_dur = (dur_min + dur_max) / 2
    error_dur = abs(dur - centro_dur) / centro_dur
    fit_dur = max(0, 1 - error_dur)

    # 🔥 Contraste útil
    intensidades = [i for _, i in individuo]
    contraste = max(intensidades) - min(intensidades)
    fit_contraste = min(contraste / 0.5, 1.0)

    # 🔥 NUEVO: penalización por incoherencia fisiológica
    penalizacion = 0

    for idx, (_, if_) in enumerate(individuo):

        if idx == 0 or idx == len(individuo) - 1:
            if if_ > 0.75:
                penalizacion += 0.1

        elif idx % 2 == 1:
            if if_ < if_min:
                penalizacion += 0.2

        else:
            if if_ > if_max:
                penalizacion += 0.2

    fitness = (0.5 * fit_if + 0.3 * fit_dur + 0.2 * fit_contraste) - penalizacion

    return max(0, fitness)