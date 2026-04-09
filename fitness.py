# fitness.py

from individuo import calcular_duracion, calcular_if_promedio


def funcion_aptitud(individuo, config):
    """
    Función de aptitud basada en:
    - duración total
    - IF promedio
    - contraste de intensidades
    """

    dur = calcular_duracion(individuo)
    if_prom = calcular_if_promedio(individuo)

    if_min, if_max = config["if_range"]
    dur_min, dur_max = config["duracion_total"]

    # --- Fitness IF ---
    centro_if = (if_min + if_max) / 2
    fit_if = 1 - abs(if_prom - centro_if)

    # --- Fitness duración ---
    centro_dur = (dur_min + dur_max) / 2
    fit_dur = 1 - abs(dur - centro_dur) / centro_dur

    # --- Contraste ---
    intensidades = [i for _, i in individuo]
    contraste = max(intensidades) - min(intensidades)
    fit_contraste = min(contraste / 0.5, 1.0)

    # --- Fitness total ---
    return 0.4 * fit_if + 0.4 * fit_dur + 0.2 * fit_contraste