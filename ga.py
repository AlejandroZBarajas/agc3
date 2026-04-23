import random
from individuo import generar_individuo, calcular_if_promedio, calcular_duracion  # 🔴 NUEVO
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

            # -------------------------------
            # 1. DEFINIR RANGOS DE INTENSIDAD
            # -------------------------------
            if i == 0:
                if_min, if_max = (0.60, 0.75)

            elif i == len(individuo) - 1:
                if_min, if_max = (0.60, 0.75)

            elif i % 2 == 1:
                if_min, if_max = config["if_range"]

            else:
                if_min, if_max = (0.40, 0.65)

            # -------------------------------
            # 2. MUTACIÓN DE INTENSIDAD
            # -------------------------------
            if random.random() < 0.3:
                nueva_if = random.uniform(if_min, if_max)
            else:
                nueva_if = intensidad + random.uniform(-0.1, 0.1)

            nueva_if = max(if_min, min(if_max, nueva_if))

            # -------------------------------
            # 3. DEFINIR RANGOS DE DURACIÓN
            # -------------------------------
            if i == 0:
                dur_min, dur_max = config["duracion_calentamiento"]

            elif i == len(individuo) - 1:
                dur_min, dur_max = config["duracion_enfriamiento"]

            elif i % 2 == 1:
                dur_min, dur_max = config["duracion_intervalo"]

            else:
                dur_min, dur_max = config["recuperacion"]

            # -------------------------------
            # 4. MUTACIÓN DE DURACIÓN
            # -------------------------------
            if random.random() < 0.3:
                nueva_dur = random.randint(dur_min, dur_max)
            else:
                nueva_dur = dur + random.randint(-2, 2)

            nueva_dur = max(dur_min, min(dur_max, nueva_dur))

            # -------------------------------
            # 5. ASIGNAR CAMBIO
            # -------------------------------
            individuo[i] = (nueva_dur, nueva_if)

    # -------------------------------
    # 6. MUTACIÓN ESTRUCTURAL (FUERA DEL FOR)
    # -------------------------------
    if random.random() < 0.1:

        if len(individuo) > 6 and random.random() < 0.5:
            idx = random.randint(1, len(individuo) - 2)
            individuo.pop(idx)

        else:
            dur_int = random.randint(*config["duracion_intervalo"])
            if_int = random.uniform(*config["if_range"])

            dur_rec = random.randint(*config["recuperacion"])
            if_rec = random.uniform(0.4, 0.65)

            individuo.insert(1, (dur_int, if_int))
            individuo.insert(2, (dur_rec, if_rec))

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

    # 🔴 NUEVO: historial para gráficas
    historial = {
        "fitness_promedio": [],
        "fitness_mejor": [],
        "if_promedio": [],
        "duracion_promedio": []
    }

    # 🔴 NUEVO: mejor individuo global
    mejor_global = None
    mejor_fitness_global = -float("inf")

    for gen in range(generaciones):

        # 🔴 NUEVO: evaluar población actual
        fitness_vals = [funcion_aptitud(ind, config) for ind in poblacion]

        avg_fitness = sum(fitness_vals) / len(fitness_vals)
        best_fitness = max(fitness_vals)

        # 🔴 Guardar fitness en historial
        historial["fitness_promedio"].append(avg_fitness)
        historial["fitness_mejor"].append(best_fitness)

        # 🔴 NUEVO: métricas del modelo
        ifs = [calcular_if_promedio(ind) for ind in poblacion]
        durs = [calcular_duracion(ind) for ind in poblacion]

        historial["if_promedio"].append(sum(ifs) / len(ifs))
        historial["duracion_promedio"].append(sum(durs) / len(durs))

        # 🔴 NUEVO: guardar mejor individuo global
        for ind, fit in zip(poblacion, fitness_vals):
            if fit > mejor_fitness_global:
                mejor_fitness_global = fit
                mejor_global = ind

        # -------------------------------
        # Evolución (igual que antes)
        # -------------------------------
        nueva_poblacion = []

        for _ in range(tam_pob):

            p1 = seleccionar_padre(poblacion, config)
            p2 = seleccionar_padre(poblacion, config)

            hijo = cruza(p1, p2)
            hijo = mutacion(hijo, config)

            nueva_poblacion.append(hijo)

        poblacion = nueva_poblacion

        # Debug (lo dejamos)
        mejor = max(poblacion, key=lambda x: funcion_aptitud(x, config))
        print(f"Generación {gen+1} | Fitness: {funcion_aptitud(mejor, config):.4f}")

    # 🔴 Mantenemos top 3 (opcional, pero útil)
    mejores = poda_poblacion(poblacion, config, k=3)

    # 🔴 CAMBIO CLAVE: ahora regresamos historial
    return mejores, historial