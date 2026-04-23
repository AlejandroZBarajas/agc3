""" import streamlit as st
import matplotlib.pyplot as plt

from ga import ejecutar_ag
from config import INTENSIDAD_MAP, CONFIG_BASE
from individuo import calcular_duracion, calcular_if_promedio


# -------------------------------
# UI CONFIG
# -------------------------------
st.title("Generador de Entrenamientos con Algoritmo Genético")

# -------------------------------
# INPUTS
# -------------------------------
ftp = st.number_input("FTP del usuario", min_value=100, max_value=500, value=250)

intensidad = st.selectbox(
    "Nivel de intensidad",
    ["baja", "moderada", "alta"]
)

# -------------------------------
# BOTÓN
# -------------------------------
if st.button("Generar entrenamiento"):

    # -------------------------------
    # CONFIGURACIÓN DEL AG
    # -------------------------------
    config_intensidad = INTENSIDAD_MAP[intensidad]

    config = {
        **config_intensidad,
        **CONFIG_BASE,
        "tam_pob": 50,
        "generaciones": 30
    }

    # -------------------------------
    # EJECUTAR AG
    # -------------------------------
    mejores, historial = ejecutar_ag(config, ftp)

    st.success("Entrenamiento generado")

    # ===============================
    # 📊 GRÁFICA 1: FITNESS
    # ===============================
    st.subheader("Evolución del Fitness")

    fig1, ax1 = plt.subplots()
    ax1.plot(historial["fitness_mejor"], label="Mejor fitness")
    ax1.plot(historial["fitness_promedio"], label="Fitness promedio")
    ax1.set_xlabel("Generaciones")
    ax1.set_ylabel("Fitness")
    ax1.legend()

    st.pyplot(fig1)

    # ===============================
    # 📊 GRÁFICA 2: VARIABLES
    # ===============================
    st.subheader("Evolución de Variables")

    fig2, ax2 = plt.subplots()
    ax2.plot(historial["if_promedio"], label="IF promedio")
    ax2.plot(historial["duracion_promedio"], label="Duración promedio")
    ax2.set_xlabel("Generaciones")
    ax2.legend()

    st.pyplot(fig2)

    # ===============================
    # 📊 GRÁFICA 3: ENTRENAMIENTO
    # ===============================
    st.subheader("Entrenamientos generados (Watts vs Tiempo)")

    for idx, mejor in enumerate(mejores):

        st.write(f"### Solución {idx+1}")

        tiempos = []
        watts = []
        tiempo_acumulado = 0

        for dur, if_ in mejor:
            w = if_ * ftp

            tiempos.extend([tiempo_acumulado, tiempo_acumulado + dur])
            watts.extend([w, w])

            tiempo_acumulado += dur

        fig, ax = plt.subplots()
        ax.plot(tiempos, watts)
        ax.set_xlabel("Tiempo (min)")
        ax.set_ylabel("Watts")

        #st.pyplot(fig3)
        st.pyplot(fig)    

    # ===============================
    # 📋 RESUMEN
    # ===============================
    st.subheader("Resumen")

    dur_total = calcular_duracion(mejor)
    if_prom = calcular_if_promedio(mejor)

    st.write(f"Duración total: {dur_total} min")
    st.write(f"IF promedio: {if_prom:.2f}")

    # ===============================
    # 📄 DETALLE DEL ENTRENAMIENTO
    # ===============================
    st.subheader("Detalle del entrenamiento")

    for i, (dur, if_) in enumerate(mejor):

        watts = if_ * ftp

        if i == 0:
            tipo = "Calentamiento"
        elif i == len(mejor) - 1:
            tipo = "Enfriamiento"
        elif i % 2 == 1:
            tipo = "Intervalo"
        else:
            tipo = "Recuperación"

        st.write(f"{tipo}: {dur} min | {watts:.0f} W (IF {if_:.2f})") """
        
    
import streamlit as st
import matplotlib.pyplot as plt

from ga import ejecutar_ag
from config import INTENSIDAD_MAP, CONFIG_BASE
from individuo import calcular_duracion, calcular_if_promedio


# -------------------------------
# UI CONFIG
# -------------------------------
st.title("Generador de Entrenamientos con Algoritmo Genético")

# -------------------------------
# INPUTS
# -------------------------------
ftp = st.number_input("FTP del usuario", min_value=100, max_value=500, value=250)

intensidad = st.selectbox(
    "Nivel de intensidad",
    ["baja", "moderada", "alta"]
)

# -------------------------------
# BOTÓN
# -------------------------------
if st.button("Generar entrenamiento"):

    config_intensidad = INTENSIDAD_MAP[intensidad]

    config = {
        **config_intensidad,
        **CONFIG_BASE,
        "tam_pob": 50,
        "generaciones": 30
    }

    # Guardamos en session_state
    st.session_state["resultados"] = ejecutar_ag(config, ftp)
    st.session_state["ftp"] = ftp


# -------------------------------
# RESULTADOS
# -------------------------------
if "resultados" in st.session_state:

    mejores, historial = st.session_state["resultados"]
    ftp = st.session_state["ftp"]

    st.success("Entrenamientos generados")

    # ===============================
    # 📊 GRÁFICA 1: FITNESS
    # ===============================
    st.subheader("Evolución del Fitness")

    fig1, ax1 = plt.subplots()
    ax1.plot(historial["fitness_mejor"], label="Mejor fitness")
    ax1.plot(historial["fitness_promedio"], label="Fitness promedio")
    ax1.set_xlabel("Generaciones")
    ax1.set_ylabel("Fitness")
    ax1.legend()

    st.pyplot(fig1)

    # ===============================
    # 📊 GRÁFICA 2: VARIABLES
    # ===============================
    st.subheader("Evolución de Variables")

    fig2, ax2 = plt.subplots()
    ax2.plot(historial["if_promedio"], label="IF promedio")
    ax2.plot(historial["duracion_promedio"], label="Duración promedio")
    ax2.set_xlabel("Generaciones")
    ax2.legend()

    st.pyplot(fig2)

    # ===============================
    # 📊 GRÁFICA 3: ENTRENAMIENTOS
    # ===============================
    st.subheader("Entrenamientos generados (Watts vs Tiempo)")

    for idx, mejor in enumerate(mejores):

        st.write(f"## 🔹 Solución {idx+1}")

        tiempos = []
        watts = []
        tiempo_acumulado = 0

        for dur, if_ in mejor:
            w = if_ * ftp

            tiempos.extend([tiempo_acumulado, tiempo_acumulado + dur])
            watts.extend([w, w])

            tiempo_acumulado += dur

        fig, ax = plt.subplots()
        ax.plot(tiempos, watts)
        ax.set_xlabel("Tiempo (min)")
        ax.set_ylabel("Watts")

        st.pyplot(fig)

        # ===============================
        # 📋 RESUMEN POR SOLUCIÓN
        # ===============================
        st.subheader(f"Resumen - Solución {idx+1}")

        dur_total = calcular_duracion(mejor)
        if_prom = calcular_if_promedio(mejor)

        st.write(f"Duración total: {dur_total} min")
        st.write(f"IF promedio: {if_prom:.2f}")

        # ===============================
        # 📄 DETALLE
        # ===============================
        st.subheader("Detalle del entrenamiento")

        for i, (dur, if_) in enumerate(mejor):

            watts = if_ * ftp

            if i == 0:
                tipo = "Calentamiento"
            elif i == len(mejor) - 1:
                tipo = "Enfriamiento"
            elif i % 2 == 1:
                tipo = "Intervalo"
            else:
                tipo = "Recuperación"

            st.write(f"{tipo}: {dur} min | {watts:.0f} W (IF {if_:.2f})")

        st.divider()