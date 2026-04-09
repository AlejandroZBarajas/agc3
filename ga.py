# ga.py

import random
from individuo import generar_individuo
from fitness import funcion_aptitud


# -------------------------------
# 1. Inicialización
# -------------------------------
def inicializar_poblacion(config, tam_pob, ftp):
    return [generar_individuo(config, ftp) for _ in range(tam_pob)]


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

            dur, if_actual = individuo[i]

            # 🔥 Paso 1: perturbación local
            delta = random.uniform(-0.05, 0.05)
            nuevo_if = if_actual + delta

            # 🔥 Paso 2: clamp según tipo de bloque
            if i == 0:
                # calentamiento
                nuevo_if = max(0.50, min(0.70, nuevo_if))

            elif i == len(individuo) - 1:
                # enfriamiento
                nuevo_if = max(0.50, min(0.70, nuevo_if))

            elif i % 2 == 1:
                # intervalo
                nuevo_if = max(0.85, min(1.05, nuevo_if))

            else:
                # recuperación
                nuevo_if = max(0.40, min(0.65, nuevo_if))

            individuo[i] = (dur, nuevo_if)

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

    poblacion = inicializar_poblacion(config, tam_pob, ftp)

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