import pandas as pd


def cargar_dataset():
    df = pd.read_csv("final_window.csv")

    df = df.dropna()

    df = df[
        (df["TSS"] > 0) &
        (df["IF"] > 0)
    ]

    return df