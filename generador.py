import random
from individuo import Bloque, Individuo   # 🔥 FALTABA ESTO


def generar_individuo():

    bloques = []

    # Warmup
    bloques.append(Bloque("warmup", 10, 0.6))

    n = 6  # restricción dura

    for _ in range(n):
        bloques.append(Bloque("intervalo", 3, random.uniform(0.95, 1.05)))
        bloques.append(Bloque("recovery", 2, 0.5))

    # Cooldown
    bloques.append(Bloque("cooldown", 10, 0.5))

    return Individuo(bloques)