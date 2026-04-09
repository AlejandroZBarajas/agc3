import pandas as pd

def cargar_dataset():
    df = pd.read_csv("final_window.csv")

    df = df.dropna()

    df = df[
        (df["TSS"] > 0) &
        (df["IF"] > 0) &
        (df["interval_count"] >= 0)
    ]

    return df


def obtener_rangos(df):
    return {
        "if_min": df["IF"].min(),
        "if_max": df["IF"].max(),
        "tss_min": df["TSS"].min(),
        "tss_max": df["TSS"].max(),
        "intervalos_min": df["interval_count"].min(),
        "intervalos_max": df["interval_count"].max()
    }