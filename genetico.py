import random
from generador import generar_individuo
from fitness import calcular_metricas, evaluar_fitness
from individuo import Individuo


def inicializar_poblacion(n):
    return [generar_individuo() for _ in range(n)]


def evaluar_poblacion(poblacion):
    for ind in poblacion:
        calcular_metricas(ind)
        evaluar_fitness(ind)


def seleccionar(poblacion):
    poblacion.sort(key=lambda x: x.fitness, reverse=True)
    return poblacion[: len(poblacion)//2]


def cruzar(p1, p2):

    # mantener warmup y cooldown
    warmup = p1.bloques[0]
    cooldown = p1.bloques[-1]

    # extraer solo intervalos + recoveries
    core1 = p1.bloques[1:-1]
    core2 = p2.bloques[1:-1]

    corte = len(core1)//2

    nuevo_core = core1[:corte] + core2[corte:]

    return Individuo([warmup] + nuevo_core + [cooldown])


def mutar(ind):

    b = random.choice(ind.bloques)

    if b.tipo == "intervalo":
        b.intensidad += random.uniform(-0.05, 0.05)

    # ❌ ELIMINAR ESTO:
    # b.repeticiones = ...

def evolucionar(poblacion, config):

    poblacion.sort(key=lambda x: x.fitness, reverse=True)

    elite = poblacion[:2]  # 🔥 conservar mejores

    nueva = elite.copy()

    while len(nueva) < config["poblacion"]:

        p1, p2 = random.sample(poblacion[:10], 2)

        hijo = cruzar(p1, p2)

        if random.random() < config["prob_mutacion"]:
            mutar(hijo)

        nueva.append(hijo)

    return nueva