"""
mms_k.py

Modelo M/M/s/K (s servidores, capacidad total K) con menú interactivo y
procedimiento paso a paso (sin librerías externas).

Datos:
- lam: λ (llegadas/hora)
- mu : μ (servicios/hora por servidor)
- s  : número de servidores (entero ≥ 1)
- K  : capacidad total del sistema (incluye en servicio y en cola), K ≥ s

Fórmulas clave:
    ρ = λ / (s μ)
    a = λ / μ

    P0 = [ sum_{n=0}^{s-1} (a^n / n!)  +  sum_{n=s}^{K} (a^n / (s! s^{n-s})) ]^{-1}

    Para 0 ≤ n ≤ s:
        Pn = (a^n / n!) * P0
    Para s ≤ n ≤ K:
        Pn = (a^n / (s! * s^{n-s})) * P0

    Probabilidad de bloqueo (sistema lleno):  PB = P_K
    Tasa efectiva que entra al sistema:       λ̅ = λ * (1 - P_K)

    Lq = P0 * (a^s / s!) * [ ρ / (1-ρ)^2 ] * [ 1 - ρ^{K-s} - (K-s)(1-ρ) ρ^{K-s} ]

    L  = Lq + sum_{n=0}^{s-1} n Pn + s * (1 - sum_{n=0}^{s-1} Pn)
    W  = L / λ̅
    Wq = Lq / λ̅

    Prob. de esperar (servidores ocupados) incondicional:
        Pw_all_busy = sum_{n=s}^{K-1} Pn
    Prob. de esperar, condicionada a ser admitido:
        Pw_adm = Pw_all_busy / (1 - P_K)

Caso guiado (Ejercicio 6 del portafolio):
    λ = 15/h, Ts = 4 min ⇒ μ = 15/h, s = 2, K = 5 (2 agentes + 3 en espera)
"""

import math

# --------------------------
# Utilidades
# --------------------------

def factorial(n):
    if n < 0:
        raise ValueError("factorial indefinido para n < 0")
    r = 1
    for k in range(1, n + 1):
        r *= k
    return r

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
# Núcleo M/M/s/K
# --------------------------

def resolver_mms_k(lam, mu, s, K, n_consulta=None, detallar=True):
    """
    Calcula métricas de M/M/s/K y, si detallar=True, imprime el procedimiento.

    lam: llegadas/h
    mu : servicios/h por servidor
    s  : servidores (entero ≥ 1)
    K  : capacidad total (entero, K ≥ s)
    n_consulta: entero opcional para calcular P(N=n)
    """
    if lam <= 0 or mu <= 0:
        raise ValueError("λ y μ deben ser positivos.")
    if int(s) != s or s <= 0:
        raise ValueError("s debe ser un entero ≥ 1.")
    if int(K) != K or K < s:
        raise ValueError("K debe ser un entero y cumplir K ≥ s.")

    s = int(s)
    K = int(K)

    a = lam / mu
    rho = lam / (s * mu)

    if detallar:
        print_sub("Paso 1: Parámetros básicos")
        print("λ = {} por hora".format(fmt(lam)))
        print("μ = {} por hora (por servidor)".format(fmt(mu)))
        print("s = {} servidores,  K = {} capacidad total".format(s, K))
        print("a = λ/μ = {} / {} = {}".format(fmt(lam), fmt(mu), fmt(a)))
        print("ρ = λ / (s μ) = {} / ({} * {}) = {}".format(fmt(lam), s, fmt(mu), fmt(rho)))

    # Paso 2: P0
    if detallar:
        print_sub("Paso 2: Cálculo de P0")
        print("P0 = [ sum_{n=0}^{s-1} (a^n/n!) + sum_{n=s}^{K} (a^n / (s! s^{n-s})) ]^{-1}")

    sum1 = 0.0
    if detallar:
        print("  sum1 = Σ_{n=0}^{s-1} a^n / n!:")
    for n in range(0, s):
        term = (a ** n) / factorial(n)
        sum1 += term
        if detallar:
            print("    n={}: a^n/n! = {}^{} / {}! = {}".format(n, fmt(a), n, n, fmt(term)))

    sum2 = 0.0
    if detallar:
        n = s
        print("  sum2 = Σ_{}^{} a^n / (s! s^(n-s)):".format(n, K))
    for n in range(s, K + 1):
        term = (a ** n) / (factorial(s) * (s ** (n - s)))
        sum2 += term
        if detallar:
            print("    n={}: a^n / (s! s^(n-s)) = {}^{} / ({}! * {}^({}-{})) = {}".format(
                n, fmt(a), n, s, s, n, s, fmt(term)))

    P0 = 1.0 / (sum1 + sum2)
    if detallar:
        print("  P0 = 1 / (sum1 + sum2) = 1 / ({} + {}) = {}".format(fmt(sum1), fmt(sum2), fmt(P0)))

    # Paso 3: Pn y PK (bloqueo)
    def Pn(n):
        if n < 0 or n > K:
            return 0.0
        if n <= s:
            return (a ** n) / factorial(n) * P0
        else:
            return (a ** n) / (factorial(s) * (s ** (n - s))) * P0

    PK = Pn(K)  # bloqueo
    lam_eff = lam * (1.0 - PK)

    if detallar:
        print_sub("Paso 3: Probabilidades de estado y bloqueo")
        print("P(K) = P_{} = {}  (probabilidad de sistema lleno = prob. de bloqueo)".format(K, fmt(PK)))
        print("λ̅ = λ * (1 - P_K) = {} * (1 - {}) = {}  (tasa efectiva admitida)".format(
            fmt(lam), fmt(PK), fmt(lam_eff)))

    # Paso 4: Prob. de esperar
    Pw_all_busy = 0.0
    for n in range(s, K):
        Pw_all_busy += Pn(n)
    Pw_adm = Pw_all_busy / (1.0 - PK) if (1.0 - PK) > 0 else 0.0

    if detallar:
        print_sub("Paso 4: Probabilidad de esperar")
        print("Incondicional (arribos Poisson): Pw_all_busy = Σ_{n=s}^{K-1} Pn")
        print("  Pw_all_busy = {}".format(fmt(Pw_all_busy)))
        print("Condicionada a ser admitido: Pw_adm = Pw_all_busy / (1 - P_K)")
        print("  Pw_adm = {}".format(fmt(Pw_adm)))

    # Paso 5: Lq (fórmula cerrada) y L
    if abs(1.0 - rho) < 1e-12:
        raise ValueError("ρ muy cercano a 1, la fórmula de Lq se vuelve inestable numéricamente.")

    parte1 = P0 * (a ** s) / factorial(s)
    parte2 = rho / ((1.0 - rho) ** 2)
    parte3 = 1.0 - (rho ** (K - s)) - (K - s) * (1.0 - rho) * (rho ** (K - s))
    Lq = parte1 * parte2 * parte3

    if detallar:
        print_sub("Paso 5: Número promedio en cola Lq")
        print("Lq = P0 * (a^s / s!) * [ρ / (1-ρ)^2] * [1 - ρ^{K-s} - (K-s)(1-ρ)ρ^{K-s}]")
        print("   = {} * ({}^{} / {}!) * [{} / (1 - {})^2] * [1 - {}^{} - (K-s)(1 - {}){}^{}]".format(
            fmt(P0), fmt(a), s, s, fmt(rho), fmt(rho), K - s, fmt(rho), fmt(rho), K - s))
        print("   = {}".format(fmt(Lq)))

    sum_nPn_0_a_s1 = 0.0
    sum_Pn_0_a_s1 = 0.0
    for n in range(0, s):
        pn = Pn(n)
        sum_nPn_0_a_s1 += n * pn
        sum_Pn_0_a_s1 += pn

    L = sum_nPn_0_a_s1 + Lq + s * (1.0 - sum_Pn_0_a_s1)

    if detallar:
        print_sub("Paso 6: Número promedio en el sistema L")
        print("L = Lq + Σ_{n=0}^{s-1} n Pn + s * (1 - Σ_{n=0}^{s-1} Pn)")
        print("  Σ nPn (0..s-1) = {}   |   Σ Pn (0..s-1) = {}".format(fmt(sum_nPn_0_a_s1), fmt(sum_Pn_0_a_s1)))
        print("  L = {} + {} + {} * (1 - {}) = {}".format(
            fmt(Lq), fmt(sum_nPn_0_a_s1), s, fmt(sum_Pn_0_a_s1), fmt(L)))

    # Paso 7: W y Wq (usando λ efectivo)
    if lam_eff <= 0:
        raise ValueError("La tasa efectiva λ̅ es 0 (bloqueo total). No se definen W y Wq.")

    W = L / lam_eff
    Wq = Lq / lam_eff

    if detallar:
        print_sub("Paso 7: Tiempos promedio")
        print("W  = L / λ̅ = {} / {} = {} horas = {} min".format(
            fmt(L), fmt(lam_eff), fmt(W), fmt(horas_a_min(W), 4)))
        print("Wq = Lq / λ̅ = {} / {} = {} horas = {} min".format(
            fmt(Lq), fmt(lam_eff), fmt(Wq), fmt(horas_a_min(Wq), 4)))

        print_sub("Paso 8: (Opcional) P(N = n)")
        if n_consulta is not None:
            Pn_val = Pn(n_consulta)
            print("P(N={}) = {}".format(n_consulta, fmt(Pn_val)))
        else:
            print("No se solicitó n; puede ingresar n en el menú para P(N=n).")

        print_sub("Paso 9: Verificaciones")
        print("λ̅ = λ (1 - P_K) = {} * (1 - {}) = {}".format(fmt(lam), fmt(PK), fmt(lam_eff)))
        print("Little (admitidos):  L ≈ λ̅ * W  → {} ≈ {}".format(fmt(L), fmt(lam_eff * W)))
        print("Little (admitidos): Lq ≈ λ̅ * Wq → {} ≈ {}".format(fmt(Lq), fmt(lam_eff * Wq)))

    # Resultado
    out = {
        "rho": rho,
        "a": a,
        "P0": P0,
        "PK_bloqueo": PK,
        "lambda_efectiva": lam_eff,
        "Pw_all_busy": Pw_all_busy,
        "Pw_adm": Pw_adm,
        "Lq": Lq,
        "L": L,
        "W_horas": W,
        "W_min": horas_a_min(W),
        "Wq_horas": Wq,
        "Wq_min": horas_a_min(Wq),
    }
    if n_consulta is not None:
        out["Pn_val"] = Pn(n_consulta)
    out["Pn_func"] = Pn
    return out

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

def ingresar_lam_mu_s_K():
    print_sub("Entrada directa λ, μ, s y K")
    lam = leer_float("λ (llegadas por hora): \n")
    mu  = leer_float("μ (servicios por hora, por servidor): \n")
    s   = leer_int("s (número de servidores): \n")
    K   = leer_int("K (capacidad total, incluye en cola y servicio): \n")
    return lam, mu, s, K

def ingresar_lam_Ts_s_K():
    print_sub("Entrada λ, tiempo de servicio promedio (min) y s, K")
    lam    = leer_float("λ (llegadas por hora): \n")
    Ts_min = leer_float("Tiempo promedio de servicio (min por cliente): \n")
    if Ts_min <= 0:
        raise ValueError("El tiempo de servicio debe ser positivo.")
    mu = 60.0 / Ts_min
    print("Conversión: μ = 60 / Ts = 60 / {} = {} servicios/hora".format(fmt(Ts_min, 3), fmt(mu, 6)))
    s  = leer_int("s (número de servidores): \n")
    K  = leer_int("K (capacidad total, incluye en cola y servicio): \n")
    return lam, mu, s, K

def consultar_n():
    n = input("n para calcular P(N = n) (ENTER para omitir): \n").strip()
    if n == "":
        return None
    if n.isdigit():
        return int(n)
    print("  -> n inválido, se omite el cálculo de P(N=n).")
    return None

# --------------------------
# Caso guiado: Ejercicio 6
# --------------------------

def caso_ejercicio_6():
    """
    Ejercicio 6 (portafolio):
      - Dos agentes (s=2)
      - Tres en espera ⇒ capacidad total K = 2 + 3 = 5
      - Llegadas Poisson: λ = 15 por hora
      - Servicio exponencial: Ts = 4 minutos ⇒ μ = 60/4 = 15 por hora
    Pide:
      a) Probabilidad de que todas las líneas estén ocupadas (sistema lleno): P_K
      b) Lq
      c) L
      d) Wq
      e) W
    """
    print_header("Ejercicio 6 — Oficina de boletos (M/M/2/5)")
    lam = 15.0
    Ts_min = 4.0
    mu = 60.0 / Ts_min   # 15/h
    s = 2
    K = 5
    print("Datos: λ = {} por hora, Ts = {} min ⇒ μ = {} por hora, s = {}, K = {}".format(
        fmt(lam), fmt(Ts_min), fmt(mu), s, K))
    print("Se calcularán P0, P_K (bloqueo), λ̅, Lq, L, Wq, W y prob. de espera.")
    resolver_mms_k(lam, mu, s, K, n_consulta=None, detallar=True)

# --------------------------
# Menú principal
# --------------------------

def menu():
    while True:
        print_header("MENÚ M/M/s/K — Paso a paso")
        print("1) Ingresar λ, μ, s y K")
        print("2) Ingresar λ, Ts (min) y s, K")
        print("3) Caso guiado: Ejercicio 6 del portafolio (M/M/2/5)")
        print("0) Salir")
        op = input("Selecciona una opción: \n").strip()

        if op == "0":
            print("¡Hasta luego!")
            return

        try:
            if op == "1":
                lam, mu, s, K = ingresar_lam_mu_s_K()
                n = consultar_n()
                print_header("Resultados M/M/s/K (entrada λ, μ, s, K)")
                resolver_mms_k(lam, mu, s, K, n_consulta=n, detallar=True)

            elif op == "2":
                lam, mu, s, K = ingresar_lam_Ts_s_K()
                n = consultar_n()
                print_header("Resultados M/M/s/K (entrada λ, Ts, s, K)")
                resolver_mms_k(lam, mu, s, K, n_consulta=n, detallar=True)

            elif op == "3":
                caso_ejercicio_6()

            else:
                print("Opción inválida. Intenta nuevamente.")
        except Exception as e:
            print("\n[ERROR] {}".format(e))

# --------------------------
# Main
# --------------------------

if __name__ == "__main__":
    menu()