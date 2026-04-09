from config import USER_INPUT


def calcular_metricas(ind):

    total_tiempo = 0
    suma_if = 0
    total_intervalos = 0

    for b in ind.bloques:

        dur_total = b.duracion * b.repeticiones

        total_tiempo += dur_total
        suma_if += b.intensidad * dur_total

        if b.tipo == "intervalo":
            total_intervalos += b.repeticiones

    ind.duracion = total_tiempo
    ind.IF = suma_if / total_tiempo

    horas = total_tiempo / 60
    ind.TSS = horas * (ind.IF ** 2) * 100

    ind.intervalos = total_intervalos


def evaluar_fitness(ind):

    f_time = 1 - abs(ind.duracion - USER_INPUT["duracion_obj"]) / USER_INPUT["duracion_obj"]
    f_tss = 1 - abs(ind.TSS - USER_INPUT["tss_obj"]) / USER_INPUT["tss_obj"]
    f_int = 1 - abs(ind.intervalos - USER_INPUT["intervalos_obj"]) / USER_INPUT["intervalos_obj"]

    ind.fitness = (f_time * 0.4 + f_int * 0.4 + f_tss * 0.2)