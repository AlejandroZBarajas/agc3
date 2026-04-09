class Bloque:
    def __init__(self, tipo, duracion, intensidad, repeticiones=1):
        self.tipo = tipo
        self.duracion = duracion
        self.intensidad = intensidad
        self.repeticiones = repeticiones


class Individuo:
    def __init__(self, bloques):
        self.bloques = bloques

        self.TSS = 0
        self.IF = 0
        self.duracion = 0
        self.intervalos = 0
        self.fitness = 0