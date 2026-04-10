import random

def generar_individuo(config):

    bloques = []

    bloques.append((10, random.uniform(0.5, 0.65)))

    n_min, n_max = config["intervalos"]
    n = random.randint(n_min, n_max)

    if_min, if_max = config["if_range"]

    for _ in range(n):
        bloques.append((3, random.uniform(if_min, if_max)))  # intervalo
        bloques.append((2, random.uniform(0.4, 0.6)))        # recovery

    bloques.append((10, random.uniform(0.5, 0.65)))

    return bloques


# =========================
# 📊 MÉTRICAS
# =========================

def calcular_duracion(ind):
    return sum(d for d, _ in ind)


def calcular_if_promedio(ind):
    total = sum(d for d, _ in ind)
    return sum(d * i for d, i in ind) / total