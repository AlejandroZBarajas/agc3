import random

def generar_individuo(config, ftp):
    individuo = []

    # 🔹 NUEVO: obtenemos el FTP del usuario desde config
    #ftp = config["ftp"]

    # 🔹 NUEVO: definimos límites en términos de IF (no watts)
    # (recuerda: IF = potencia / FTP)
    MIN_IF_INTERVALO = 0.85
    MAX_IF_INTERVALO = 1.05

    MIN_IF_RECUP = 0.40
    MAX_IF_RECUP = 0.65

    # =========================
    # 🔥 CALENTAMIENTO
    # =========================
    dur_warm = random.randint(*config["duracion_calentamiento"])

    # ⚠️ CAMBIO: limitamos también el calentamiento a zona baja
    if_warm = random.uniform(0.50, 0.70)

    individuo.append((dur_warm, if_warm))


    # =========================
    # 🔁 INTERVALOS + RECUP
    # =========================
    num_intervalos = random.randint(*config["intervalos"])

    for _ in range(num_intervalos):

        # -------- INTERVALO --------
        dur_i = random.randint(*config["duracion_intervalo"])

        # 🔥 CAMBIO CLAVE:
        # Antes usabas config["if_intervalo"]
        # Ahora FORZAMOS a que cumpla mínimo 0.85 IF
        if_i = random.uniform(MIN_IF_INTERVALO, MAX_IF_INTERVALO)

        individuo.append((dur_i, if_i))


        # -------- RECUPERACIÓN --------
        dur_r = random.randint(*config["recuperacion"])

        # 🔥 CAMBIO CLAVE:
        # Limitamos recuperación para que nunca sea intensa
        if_r = random.uniform(MIN_IF_RECUP, MAX_IF_RECUP)

        individuo.append((dur_r, if_r))


    # =========================
    # ❄️ ENFRIAMIENTO
    # =========================
    dur_cool = random.randint(*config["duracion_enfriamiento"])

    # ⚠️ CAMBIO: igual que calentamiento → zona baja
    if_cool = random.uniform(0.50, 0.70)

    individuo.append((dur_cool, if_cool))


    return individuo


# =========================
# 📊 MÉTRICAS
# =========================

def calcular_duracion(ind):
    return sum(d for d, _ in ind)


def calcular_if_promedio(ind):
    total = sum(d for d, _ in ind)
    return sum(d * i for d, i in ind) / total