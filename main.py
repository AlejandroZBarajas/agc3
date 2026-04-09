from genetico import inicializar_poblacion, evaluar_poblacion, evolucionar
from config import AG_CONFIG
from utils import graficar_sesion, imprimir_individuo


def main():

    poblacion = inicializar_poblacion(AG_CONFIG["poblacion"])

    for gen in range(AG_CONFIG["generaciones"]):

        evaluar_poblacion(poblacion)

        mejor = max(poblacion, key=lambda x: x.fitness)

        print(f"Generacion {gen} | Fitness: {round(mejor.fitness,4)}")

        poblacion = evolucionar(poblacion, AG_CONFIG)

    # evaluación final
    evaluar_poblacion(poblacion)
    mejor = max(poblacion, key=lambda x: x.fitness)

    imprimir_individuo(mejor)
    graficar_sesion(mejor)


if __name__ == "__main__":
    main()