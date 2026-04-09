# main.py

from ga import ejecutar_ag
from individuo import calcular_duracion, calcular_if_promedio
from validacion import validar_con_dataset


# -------------------------------
# Configuración
# -------------------------------
CONFIG = {
    "duracion_total": (40, 90),

    "intervalos": (3, 6),

    "duracion_intervalo": (3, 8),
    "recuperacion": (2, 5),

    "duracion_calentamiento": (8, 15),
    "duracion_enfriamiento": (5, 10),

    "if_intervalo": (0.85, 1.05),
    "if_recuperacion": (0.40, 0.55),
    "if_calentamiento": (0.40, 0.65),
    "if_enfriamiento": (0.40, 0.65),

    "if_range": (0.4, 1.05),

    "tam_pob": 50,
    "generaciones": 30
}

USER_INPUT = {
    "ftp": 250  # watts del ciclista
}


# -------------------------------
# Mostrar entrenamiento detallado
# -------------------------------
def imprimir_entrenamiento(ind, ftp):

    print("\n--- ENTRENAMIENTO GENERADO ---")

    for idx, (dur, if_) in enumerate(ind):

        watts = if_ * ftp

        if idx == 0:
            tipo = "Calentamiento"
        elif idx == len(ind) - 1:
            tipo = "Enfriamiento"
        elif idx % 2 == 1:
            tipo = "Intervalo"
        else:
            tipo = "Recuperación"

        print(f"{tipo}: {dur} min | {watts:.0f} W (IF {if_:.2f})")


# -------------------------------
# MAIN
# -------------------------------
def main():

    mejores = ejecutar_ag(CONFIG, USER_INPUT["ftp"])

    print("\n===== MEJORES ENTRENAMIENTOS =====")

    for i, ind in enumerate(mejores):

        print(f"\n--- Solución {i+1} ---")

        dur = calcular_duracion(ind)
        if_prom = calcular_if_promedio(ind)
        
        validar_con_dataset(ind, "final_window.csv", USER_INPUT["ftp"])
        

        print(f"Duración total: {dur:.2f} min")
        print(f"IF promedio: {if_prom:.2f}")

        imprimir_entrenamiento(ind, USER_INPUT["ftp"])


if __name__ == "__main__":
    main()