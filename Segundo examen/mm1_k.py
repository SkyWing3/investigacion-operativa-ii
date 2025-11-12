"""
mm1_k.py

Modelo M/M/1/K (un servidor, capacidad total K) con menú interactivo y
procedimiento paso a paso (sin librerías externas).

Entradas:
- lam: λ (llegadas por hora)
- mu : μ (servicios por hora, un solo servidor)
- K  : capacidad total del sistema (0..K en sistema, incluyendo servicio)

Fórmulas principales:
    ρ = λ / μ

Caso general (ρ != 1):
    P0 = (1 - ρ) / (1 - ρ^{K+1})
    Pn = P0 * ρ^n,  0 ≤ n ≤ K

    L  = [ ρ * (1 - (K+1) ρ^K + K ρ^{K+1}) ] / [ (1 - ρ) (1 - ρ^{K+1}) ]
    Lq = L - (1 - P0)   (porque hay un servidor: E[n en servicio] = 1 - P0)

    PK = Pn(K)                           (prob. de bloqueo)
    λ̅ = λ (1 - PK)                      (tasa efectiva admitida)

    W  = L  / λ̅
    Wq = Lq / λ̅

Caso límite (ρ = 1):
    Pn = 1/(K+1) para todo n=0..K
    P0 = 1/(K+1)
    L  = K/2
    Lq = L - (1 - P0) = K/2 - K/(K+1) = (K(K-1)) / (2(K+1))
    PK = 1/(K+1)
    λ̅ = λ (1 - PK) = λ * K/(K+1)
    W  = L  / λ̅
    Wq = Lq / λ̅
"""

import math

# --------------------------
# Utilidades
# --------------------------

def fmt(x, dec=6):
    if isinstance(x, int):
        return str(x)
    return "{0:.{1}f}".format(x, dec)

def horas_a_min(h):
    return h * 60.0

def print_header(t):
    print("\n" + "=" * 76)
    print(t)
    print("=" * 76)

def print_sub(t):
    print("\n--- " + t + " ---")

# --------------------------
# Núcleo M/M/1/K
# --------------------------

def resolver_mm1_k(lam, mu, K, n_consulta=None, detallar=True):
    """
    Calcula métricas de M/M/1/K y, si detallar=True, imprime el procedimiento.
    lam: llegadas/h, mu: servicios/h, K: capacidad total (entero ≥ 0)
    n_consulta: entero opcional para P(N=n)
    """
    if lam <= 0 or mu <= 0:
        raise ValueError("λ y μ deben ser positivos.")
    if int(K) != K or K < 0:
        raise ValueError("K debe ser un entero ≥ 0.")
    K = int(K)

    rho = lam / mu

    if detallar:
        print_sub("Paso 1: Parámetros básicos")
        print("λ = {} por hora".format(fmt(lam)))
        print("μ = {} por hora".format(fmt(mu)))
        print("K = {} (capacidad total)".format(K))
        print("ρ = λ/μ = {} / {} = {}".format(fmt(lam), fmt(mu), fmt(rho)))

    eps = 1e-12
    rho_es_uno = abs(rho - 1.0) < eps

    # Paso 2: Probabilidades de estado (P0 y Pn)
    if not rho_es_uno:
        if detallar:
            print_sub("Paso 2: Cálculo de P0 (ρ ≠ 1)")
            print("P0 = (1 - ρ) / (1 - ρ^{K+1})")
            print("   = (1 - {}) / (1 - {}^{})".format(fmt(rho), fmt(rho), K + 1))

        denom = 1.0 - (rho ** (K + 1))
        if abs(denom) < eps:
            raise ValueError("Inestabilidad numérica: denom ~ 0. Ajusta parámetros.")
        P0 = (1.0 - rho) / denom

        def Pn(n):
            if n < 0 or n > K:
                return 0.0
            return P0 * (rho ** n)

        if detallar:
            print("   = {}".format(fmt(P0)))

        # PK y λ efectivo
        PK = Pn(K)
        lam_eff = lam * (1.0 - PK)

        if detallar:
            print_sub("Paso 3: Probabilidad de bloqueo y tasa efectiva")
            print("P(K) = P_{} = {}   (prob. de sistema lleno / bloqueo)".format(K, fmt(PK)))
            print("λ̅ = λ (1 - P_K) = {} * (1 - {}) = {}".format(fmt(lam), fmt(PK), fmt(lam_eff)))

        # Paso 4: L y Lq
        if detallar:
            print_sub("Paso 4: Número promedio en el sistema L")
            print("L = [ ρ (1 - (K+1) ρ^K + K ρ^{K+1}) ] / [ (1 - ρ) (1 - ρ^{K+1}) ]")

        numerador = rho * (1.0 - (K + 1) * (rho ** K) + K * (rho ** (K + 1)))
        denominador = (1.0 - rho) * (1.0 - (rho ** (K + 1)))
        L = numerador / denominador

        if detallar:
            print(
                "L = [{} * (1 - {} * {}^{} + {} * {}^{})] / [ (1 - {}) * (1 - {}^{}) ] = {}".format(
                    fmt(rho), (K + 1), fmt(rho), K, K, fmt(rho), K + 1, fmt(rho), fmt(rho), K + 1, fmt(L)
                )
            )

        Lq = L - (1.0 - P0)
        if detallar:
            print_sub("Paso 5: Número promedio en cola Lq")
            print("Lq = L - (1 - P0)   (porque hay 1 servidor)")
            print("   = {} - (1 - {}) = {}".format(fmt(L), fmt(P0), fmt(Lq)))

        # Paso 6: Tiempos W y Wq (usando λ̅)
        if lam_eff <= 0:
            raise ValueError("λ̅ = 0 (bloqueo total). No se definen W y Wq.")

        W = L / lam_eff
        Wq = Lq / lam_eff

        if detallar:
            print_sub("Paso 6: Tiempos promedio")
            print("W  = L / λ̅ = {} / {} = {} horas = {} min".format(
                fmt(L), fmt(lam_eff), fmt(W), fmt(horas_a_min(W), 4)))
            print("Wq = Lq / λ̅ = {} / {} = {} horas = {} min".format(
                fmt(Lq), fmt(lam_eff), fmt(Wq), fmt(horas_a_min(Wq), 4)))

        # Paso 7: P(N=n) opcional y verificaciones
        if detallar:
            print_sub("Paso 7: (Opcional) P(N = n)")
            if n_consulta is not None:
                pn_val = Pn(n_consulta)
                print("P(N={}) = {}".format(n_consulta, fmt(pn_val)))
            else:
                print("No se solicitó n; puede ingresar n en el menú para P(N=n).")

            print_sub("Paso 8: Verificaciones (Little con admitidos)")
            print("λ̅ = λ (1 - P_K) = {}".format(fmt(lam_eff)))
            print("Little: L  ≈ λ̅ * W  → {} ≈ {}".format(fmt(L), fmt(lam_eff * W)))
            print("Little: Lq ≈ λ̅ * Wq → {} ≈ {}".format(fmt(Lq), fmt(lam_eff * Wq)))

        res = {
            "rho": rho,
            "P0": P0,
            "PK_bloqueo": PK,
            "lambda_efectiva": lam_eff,
            "L": L,
            "Lq": Lq,
            "W_horas": W,
            "W_min": horas_a_min(W),
            "Wq_horas": Wq,
            "Wq_min": horas_a_min(Wq),
        }
        if n_consulta is not None:
            res["Pn_val"] = Pn(n_consulta)
        res["Pn_func"] = Pn
        return res

    else:
        # ρ == 1 (caso límite)
        if detallar:
            print_sub("Paso 2: Caso límite ρ = 1 (fórmulas cerradas)")
            print("Pn = 1/(K+1) para n=0..K; P0 = 1/(K+1)")
        P0 = 1.0 / (K + 1)

        def Pn(n):
            if n < 0 or n > K:
                return 0.0
            return 1.0 / (K + 1)

        PK = Pn(K)
        lam_eff = lam * (1.0 - PK)
        L = K / 2.0
        Lq = L - (1.0 - P0)
        W = L / lam_eff if lam_eff > 0 else float("inf")
        Wq = Lq / lam_eff if lam_eff > 0 else float("inf")

        if detallar:
            print("P0 = {}".format(fmt(P0)))
            print_sub("Paso 3: Bloqueo y tasa efectiva")
            print("P(K) = {}   |   λ̅ = λ (1 - P_K) = {} * (1 - {}) = {}".format(
                fmt(PK), fmt(lam), fmt(PK), fmt(lam_eff)))
            print_sub("Paso 4: Promedios")
            print("L  = K/2 = {}/2 = {}".format(K, fmt(L)))
            print("Lq = L - (1 - P0) = {} - (1 - {}) = {}".format(fmt(L), fmt(P0), fmt(Lq)))
            print_sub("Paso 5: Tiempos")
            print("W  = L / λ̅ = {} horas = {} min".format(fmt(W), fmt(horas_a_min(W), 4)))
            print("Wq = Lq / λ̅ = {} horas = {} min".format(fmt(Wq), fmt(horas_a_min(Wq), 4)))
            print_sub("Paso 6: Verificaciones (Little con admitidos)")
            print("Little: L  ≈ λ̅ * W  → {} ≈ {}".format(fmt(L), fmt(lam_eff * W)))
            print("Little: Lq ≈ λ̅ * Wq → {} ≈ {}".format(fmt(Lq), fmt(lam_eff * Wq)))

        res = {
            "rho": rho,
            "P0": P0,
            "PK_bloqueo": PK,
            "lambda_efectiva": lam_eff,
            "L": L,
            "Lq": Lq,
            "W_horas": W,
            "W_min": horas_a_min(W),
            "Wq_horas": Wq,
            "Wq_min": horas_a_min(Wq),
        }
        if n_consulta is not None:
            res["Pn_val"] = Pn(n_consulta)
        res["Pn_func"] = Pn
        return res

# --------------------------
# Entrada interactiva
# --------------------------

def leer_float(msg):
    while True:
        s = input(msg).strip().replace(",", ".")
        try:
            return float(s)
        except ValueError:
            print("  -> Ingresa un número válido.")

def leer_int(msg):
    while True:
        s = input(msg).strip()
        if s.isdigit():
            return int(s)
        print("  -> Ingresa un entero válido.")

def ingresar_lam_mu_K():
    print_sub("Entrada directa λ, μ y K")
    lam = leer_float("λ (llegadas por hora): \n")
    mu  = leer_float("μ (servicios por hora): \n")
    K   = leer_int("K (capacidad total): \n")
    return lam, mu, K

def ingresar_lam_Ts_K():
    print_sub("Entrada λ y tiempo de servicio promedio (min) y K")
    lam    = leer_float("λ (llegadas por hora): \n")
    Ts_min = leer_float("Tiempo promedio de servicio (min por cliente): \n")
    if Ts_min <= 0:
        raise ValueError("El tiempo de servicio debe ser positivo.")
    mu = 60.0 / Ts_min
    print("Conversión: μ = 60 / Ts = 60 / {} = {} servicios/hora".format(fmt(Ts_min, 3), fmt(mu, 6)))
    K  = leer_int("K (capacidad total): \n")
    return lam, mu, K

def consultar_n():
    n = input("n para calcular P(N = n) (ENTER para omitir): \n").strip()
    if n == "":
        return None
    if n.isdigit():
        return int(n)
    print("  -> n inválido, se omite el cálculo de P(N=n).")
    return None

# --------------------------
# Caso guiado: Ejercicio 7
# --------------------------

def caso_ejercicio_7():
    """
    Ejercicio 7 (portafolio):
      - Un cardiólogo (un servidor)
      - Capacidad de la sala: 14 pacientes ⇒ K = 14
      - Llegadas: λ = 12 por hora
      - Servicio: 10 minutos por paciente ⇒ μ = 60/10 = 6 por hora
    Pide:
      a) P0
      b) P(N=8)
      c) P(N=K) (consultorio lleno)
      d) Lq y L
      e) Wq y W
    """
    print_header("Ejercicio 7 — Consultorio (M/M/1/14)")
    lam = 12.0
    Ts_min = 10.0
    mu = 60.0 / Ts_min   # 6/h
    K = 14
    print("Datos: λ = {} por hora, Ts = {} min ⇒ μ = {} por hora, K = {}".format(
        fmt(lam), fmt(Ts_min), fmt(mu), K))

    # Resolvemos con detalle
    out = resolver_mm1_k(lam, mu, K, n_consulta=None, detallar=True)

    # Muestras específicas del enunciado
    Pn = out["Pn_func"]
    print_sub("Cálculos solicitados específicos (a–e)")
    print("(a) P0 = {}".format(fmt(out["P0"])))
    print("(b) P(N=8) = {}".format(fmt(Pn(8))))
    print("(c) P(consultorio lleno) = P(N=K) = P(N={}) = {}".format(K, fmt(Pn(K))))
    print("(d) Lq = {}   |   L = {}".format(fmt(out["Lq"]), fmt(out["L"])))
    print("(e) Wq = {} h = {} min   |   W = {} h = {} min".format(
        fmt(out["Wq_horas"]), fmt(out["Wq_min"], 4), fmt(out["W_horas"]), fmt(out["W_min"], 4)
    ))

# --------------------------
# Menú principal
# --------------------------

def menu():
    while True:
        print_header("MENÚ M/M/1/K — Paso a paso")
        print("1) Ingresar λ, μ y K")
        print("2) Ingresar λ, Ts (min) y K")
        print("3) Caso guiado: Ejercicio 7 del portafolio (M/M/1/14)")
        print("0) Salir")
        op = input("Selecciona una opción: \n").strip()

        if op == "0":
            print("¡Hasta luego!")
            return

        try:
            if op == "1":
                lam, mu, K = ingresar_lam_mu_K()
                n = consultar_n()
                print_header("Resultados M/M/1/K (entrada λ, μ y K)")
                resolver_mm1_k(lam, mu, K, n_consulta=n, detallar=True)

            elif op == "2":
                lam, mu, K = ingresar_lam_Ts_K()
                n = consultar_n()
                print_header("Resultados M/M/1/K (entrada λ, Ts y K)")
                resolver_mm1_k(lam, mu, K, n_consulta=n, detallar=True)

            elif op == "3":
                caso_ejercicio_7()

            else:
                print("Opción inválida. Intenta nuevamente.")
        except Exception as e:
            print("\n[ERROR] {}".format(e))

# --------------------------
# Main
# --------------------------

if __name__ == "__main__":
    menu()