import pandas as pd
from individuo import calcular_if_promedio


def validar_con_dataset(individuo, path_csv, ftp):

    df = pd.read_csv(path_csv)

    # -------------------------
    # DATOS REALES (DATASET)
    # -------------------------
    if_real = df["IF"].mean()
    power_real = df["avg_power"].mean()

    # -------------------------
    # MODELO (AG)
    # -------------------------
    if_modelo = calcular_if_promedio(individuo)

    # convertir IF → watts
    power_modelo = if_modelo * ftp

    # -------------------------
    # ERRORES
    # -------------------------
    error_if = abs(if_modelo - if_real)
    error_power = abs(power_modelo - power_real)

    # -------------------------
    # OUTPUT
    # -------------------------
    print("\n--- VALIDACIÓN ---")

    print(f"IF real: {if_real:.4f}")
    print(f"IF modelo: {if_modelo:.4f}")
    print(f"Error IF: {error_if:.4f}")

    print(f"\nPotencia real: {power_real:.2f} W")
    print(f"Potencia modelo: {power_modelo:.2f} W")
    print(f"Error potencia: {error_power:.2f} W")

    return error_if, error_power