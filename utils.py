import matplotlib.pyplot as plt


def graficar_sesion(ind):

    timeline = []

    for b in ind.bloques:
        for _ in range(b.repeticiones):
            for _ in range(int(b.duracion)):
                timeline.append(b.intensidad)

    plt.figure()
    plt.plot(timeline)
    plt.title("Perfil de entrenamiento")
    plt.xlabel("Minutos")
    plt.ylabel("IF")
    plt.savefig("sesion.png")
    plt.close()


def imprimir_individuo(ind):

    print("\n=== SESION GENERADA ===")

    for b in ind.bloques:
        print(f"{b.tipo} | {b.duracion} min | IF {round(b.intensidad,2)} | reps {b.repeticiones}")

    print("\n--- METRICAS ---")
    print(f"Duracion: {round(ind.duracion,2)} min")
    print(f"TSS: {round(ind.TSS,2)}")
    print(f"IF: {round(ind.IF,2)}")
    print(f"Intervalos: {ind.intervalos}")
    print(f"Fitness: {round(ind.fitness,4)}")