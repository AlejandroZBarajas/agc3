# ga.py

import random
from individuo import generar_individuo
from fitness import funcion_aptitud


# -------------------------------
# 1. Inicialización
# -------------------------------
def inicializar_poblacion(config, tam_pob):
    return [generar_individuo(config) for _ in range(tam_pob)]


# -------------------------------
# 2. Selección (torneo)
# -------------------------------
def seleccionar_padre(poblacion, config):
    candidatos = random.sample(poblacion, 3)
    return max(candidatos, key=lambda x: funcion_aptitud(x, config))


# -------------------------------
# 3. Cruza
# -------------------------------
def cruza(padre1, padre2):
    punto = random.randint(1, min(len(padre1), len(padre2)) - 1)
    hijo = padre1[:punto] + padre2[punto:]
    return hijo


# -------------------------------
# 4. Mutación
# -------------------------------
def mutacion(individuo, config, prob=0.1):

    for i in range(len(individuo)):

        if random.random() < prob:

            dur, intensidad = individuo[i]

            # 🔵 Mutar intensidad (como ya haces)
            delta_if = random.uniform(-0.08, 0.08)
            nueva_if = intensidad + delta_if

            if i == 0:
                if_min, if_max = (0.60, 0.75)

            elif i == len(individuo) - 1:
                if_min, if_max = (0.60, 0.75)

            elif i % 2 == 1:
                    # intervalo
                if_min, if_max = config["if_range"]

            else:
                # recuperación
                if_min, if_max = (0.40, 0.65)
                    
            nueva_if = max(if_min, min(if_max, nueva_if))

            # 🔴 NUEVO: mutar duración
            if i == 0:
                # calentamiento
                dur_min, dur_max = config["duracion_calentamiento"]

            elif i == len(individuo) - 1:
                # enfriamiento
                dur_min, dur_max = config["duracion_enfriamiento"]

            elif i % 2 == 1:
                # intervalo
                dur_min, dur_max = config["duracion_intervalo"]

            else:
                # recuperación
                dur_min, dur_max = config["recuperacion"]

            # pequeña mutación de duración
            delta_dur = random.randint(-1, 1)
            nueva_dur = dur + delta_dur
            nueva_dur = max(dur_min, min(dur_max, nueva_dur))

            individuo[i] = (nueva_dur, nueva_if)

    return individuo


# -------------------------------
# 5. Poda (elitismo)
# -------------------------------
def poda_poblacion(poblacion, config, k):
    poblacion.sort(key=lambda x: funcion_aptitud(x, config), reverse=True)
    return poblacion[:k]


# -------------------------------
# 6. Algoritmo Genético
# -------------------------------
def ejecutar_ag(config, ftp):

    tam_pob = config["tam_pob"]
    generaciones = config["generaciones"]

    poblacion = inicializar_poblacion(config, tam_pob)

    for gen in range(generaciones):

        nueva_poblacion = []

        for _ in range(tam_pob):

            p1 = seleccionar_padre(poblacion, config)
            p2 = seleccionar_padre(poblacion, config)

            hijo = cruza(p1, p2)
            hijo = mutacion(hijo, config)

            nueva_poblacion.append(hijo)

        poblacion = nueva_poblacion

        # Debug opcional
        mejor = max(poblacion, key=lambda x: funcion_aptitud(x, config))
        print(f"Generación {gen+1} | Fitness: {funcion_aptitud(mejor, config):.4f}")

    # Top 3
    mejores = poda_poblacion(poblacion, config, k=3)

    return mejores