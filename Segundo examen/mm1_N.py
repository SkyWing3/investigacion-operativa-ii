"""
mm1_N.py

Modelo M/M/1/N (un servidor, fuente finita de tamaño N) con menú interactivo y
procedimiento paso a paso (sin librerías externas).

Contexto típico (taller de reparaciones / máquinas):
- Hay N "fuentes" potenciales (p.ej., máquinas). Si hay n en el sistema (cola+servicio),
  entonces (N - n) están "libres" y pueden fallar/ llegar.
- La tasa de intento de llegada por CADA fuente libre es λ (lam_per_source).
- Por eso, la tasa de llegada del sistema cuando hay n en el sistema es: λ_n = (N - n) * λ.
- Un único servidor repara con tasa μ (por hora).

Entradas:
- lam_per_source: λ por fuente libre (por hora)
- mu            : μ por hora (servidor único)
- N             : tamaño de la población (número total de fuentes)

Fórmulas (clásicas):
    a = λ/μ

    C_n = [ N! / (N-n)! ] * a^n
    Pn = C_n * P0,  con  P0 = 1 / (sum_{n=0}^N C_n)

    L  = sum_{n=0}^N n * Pn
    Lq = sum_{n=1}^N (n-1) * Pn   (un solo servidor)

    λ̅ = λ * (N - L)              (tasa efectiva admitida)
    ρ  = λ̅ / μ
    W  = L  / λ̅
    Wq = Lq / λ̅
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
# Núcleo M/M/1/N
# --------------------------

def resolver_mm1_N(lam_per_source, mu, N, n_consulta=None, detallar=True):
    """
    Calcula métricas de M/M/1/N y, si detallar=True, imprime el procedimiento.
    lam_per_source: λ por fuente libre (por hora)
    mu            : μ (por hora)
    N             : tamaño de la población (entero ≥ 1)
    n_consulta    : entero opcional para P(N=n)
    """
    if lam_per_source <= 0 or mu <= 0:
        raise ValueError("λ por fuente y μ deben ser positivos.")
    if int(N) != N or N < 1:
        raise ValueError("N debe ser un entero ≥ 1.")
    N = int(N)

    a = lam_per_source / mu

    if detallar:
        print_sub("Paso 1: Parámetros del sistema (fuente finita)")
        print("λ por fuente libre = {} /h".format(fmt(lam_per_source)))
        print("μ (servidor)       = {} /h".format(fmt(mu)))
        print("N (población)      = {}".format(N))
        print("a = λ/μ            = {} / {} = {}".format(fmt(lam_per_source), fmt(mu), fmt(a)))
        print("La tasa de llegada cuando hay n en el sistema es λ_n = (N - n) * λ.")

    # Paso 2: C_n y normalización
    if detallar:
        print_sub("Paso 2: Coeficientes no normalizados C_n y cálculo de P0")
        print("C_n = [N! / (N-n)!] * a^n")

    C = []
    for n in range(0, N + 1):
        coef = factorial(N) / factorial(N - n)
        Cn = coef * (a ** n)
        C.append(Cn)
        if detallar:
            print("  n={}: C_n = {}! / ({}-{})! * {}^{} = {}".format(
                n, N, N, n, fmt(a), n, fmt(Cn)))

    suma_C = sum(C)
    P0 = 1.0 / suma_C
    if detallar:
        print("Suma total Σ C_n = {}  ⇒  P0 = 1 / ΣC_n = {}".format(fmt(suma_C), fmt(P0)))

    # Paso 3: Probabilidades Pn
    Pn_array = [P0 * C[n] for n in range(0, N + 1)]
    if detallar:
        print_sub("Paso 3: Probabilidades de estado Pn")
        for n in range(0, N + 1):
            print("  P({}) = P0 * C_{} = {} * {} = {}".format(n, n, fmt(P0), fmt(C[n]), fmt(Pn_array[n])))
        print("Verificación: Σ Pn = {}".format(fmt(sum(Pn_array))))

    # Paso 4: L y Lq
    L  = sum(n * Pn_array[n] for n in range(0, N + 1))
    Lq = sum((n - 1) * Pn_array[n] for n in range(1, N + 1))
    if detallar:
        print_sub("Paso 4: Promedios L y Lq")
        print("L  = Σ n Pn = {}".format(fmt(L)))
        print("Lq = Σ (n-1) Pn (n=1..N) = {}".format(fmt(Lq)))

    # Paso 5: λ efectivo (dos formas equivalentes)
    lam_eff_1 = lam_per_source * (N - L)  # definición estándar
    # Alternativa: Σ λ_n Pn (sobre n=0..N-1), donde λ_n = (N-n) λ
    lam_eff_2 = sum((N - n) * lam_per_source * Pn_array[n] for n in range(0, N))
    lam_eff = lam_eff_1
    if detallar:
        print_sub("Paso 5: Tasa efectiva de entrada λ̅ (dos formas)")
        print("λ̅ (def.) = λ * (N - L) = {} * (N - {}) = {}".format(
            fmt(lam_per_source), fmt(L), fmt(lam_eff_1)))
        print("λ̅ (alt)  = Σ (N-n) λ Pn (n=0..N-1) = {}  (verificación)".format(fmt(lam_eff_2)))

    # Paso 6: ρ, W y Wq
    rho = lam_eff / mu
    if lam_eff <= 0:
        raise ValueError("λ̅ = 0 (no ingresan trabajos). No se definen W y Wq.")
    W  = L  / lam_eff
    Wq = Lq / lam_eff
    if detallar:
        print_sub("Paso 6: Utilización efectiva y tiempos promedios")
        print("ρ  = λ̅ / μ = {} / {} = {}".format(fmt(lam_eff), fmt(mu), fmt(rho)))
        print("W  = L  / λ̅ = {} / {} = {} h = {} min".format(
            fmt(L), fmt(lam_eff), fmt(W), fmt(horas_a_min(W), 4)))
        print("Wq = Lq / λ̅ = {} / {} = {} h = {} min".format(
            fmt(Lq), fmt(lam_eff), fmt(Wq), fmt(horas_a_min(Wq), 4)))

    # Paso 7: P(N=n) opcional y Little
    if detallar:
        print_sub("Paso 7: (Opcional) P(N = n) y verificaciones Little")
        if n_consulta is not None:
            if 0 <= n_consulta <= N:
                print("P(N={}) = {}".format(n_consulta, fmt(Pn_array[n_consulta])))
            else:
                print("n={} fuera de [0, {}]".format(n_consulta, N))
        print("Little: L  ≈ λ̅ * W  → {} ≈ {}".format(fmt(L), fmt(lam_eff * W)))
        print("Little: Lq ≈ λ̅ * Wq → {} ≈ {}".format(fmt(Lq), fmt(lam_eff * Wq)))

    return {
        "P0": P0,
        "Pn_array": Pn_array,
        "L": L,
        "Lq": Lq,
        "lambda_efectiva": lam_eff,
        "rho": rho,
        "W_horas": W,
        "W_min": horas_a_min(W),
        "Wq_horas": Wq,
        "Wq_min": horas_a_min(Wq),
    }

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

def ingresar_lam_mu_N():
    print_sub("Entrada directa λ (por fuente), μ y N")
    lam = leer_float("λ por fuente libre (llegadas/h): \n")
    mu  = leer_float("μ (servicios/h, un servidor): \n")
    N   = leer_int("N (tamaño de la población): \n")
    return lam, mu, N

def ingresar_Tf_Ts_N():
    print_sub("Entrada por tiempos promedio (min) y N")
    Tf_min = leer_float("Tiempo promedio entre fallos por máquina (min): \n")
    Ts_min = leer_float("Tiempo promedio de reparación (min): \n")
    if Tf_min <= 0 or Ts_min <= 0:
        raise ValueError("Los tiempos deben ser positivos.")
    lam = 60.0 / Tf_min  # λ por fuente libre
    mu  = 60.0 / Ts_min
    print("Conversión: λ = 60/Tf = 60/{} = {} /h".format(fmt(Tf_min, 3), fmt(lam, 6)))
    print("            μ = 60/Ts = 60/{} = {} /h".format(fmt(Ts_min, 3), fmt(mu, 6)))
    N   = leer_int("N (tamaño de la población): \n")
    return lam, mu, N

def consultar_n(N):
    n = input("n para calcular P(N = n) (ENTER para omitir): \n").strip()
    if n == "":
        return None
    if n.isdigit():
        n = int(n)
        if 0 <= n <= N:
            return n
        print("  -> Debe estar en el rango [0, {}]. Se omitirá.".format(N))
        return None
    print("  -> n inválido, se omite el cálculo de P(N=n).")
    return None

# --------------------------
# Caso guiado: Ejercicio 8
# --------------------------

def caso_ejercicio_8():
    """
    Ejercicio 8 (laboratorio):
      - Taller con 7 máquinas (N = 7)
      - Un técnico (un servidor)
      - Fallos de cada máquina ~ Exp(0.2/h)  -> λ por fuente = 0.2/h
      - Reparación ~ Exp(0.5/h)              -> μ = 0.5/h
    Pide:
      (a) P(0 averías), (b) P(3 averías), (c) P(7 averías),
      (d) Lq y L, (e) Wq y W.
    """
    print_header("Ejercicio 8 — Taller de 7 máquinas (M/M/1/N con N=7)")
    lam_per_source = 0.2  # por hora por máquina libre
    mu = 0.5              # por hora
    N = 7
    print("Datos: λ_por_fuente = {} /h, μ = {} /h, N = {}".format(
        fmt(lam_per_source), fmt(mu), N))

    out = resolver_mm1_N(lam_per_source, mu, N, n_consulta=None, detallar=True)
    P = out["Pn_array"]

    print_sub("Cálculos solicitados específicos (a–e)")
    print("(a) P(0 averías) = P(N=0) = {}".format(fmt(P[0])))
    print("(b) P(3 averías) = P(N=3) = {}".format(fmt(P[3])))
    print("(c) P(7 averías) = P(N=7) = {}".format(fmt(P[7])))
    print("(d) Lq = {}   |   L = {}".format(fmt(out["Lq"]), fmt(out["L"])))
    print("(e) Wq = {} h = {} min   |   W = {} h = {} min".format(
        fmt(out["Wq_horas"]), fmt(out["Wq_min"], 4),
        fmt(out["W_horas"]),  fmt(out["W_min"], 4)
    ))

# --------------------------
# Menú principal
# --------------------------

def menu():
    while True:
        print_header("MENÚ M/M/1/N — Paso a paso (fuente finita)")
        print("1) Ingresar λ_por_fuente, μ y N")
        print("2) Ingresar tiempos promedio Tf (fallo) y Ts (servicio) en minutos, y N")
        print("3) Caso guiado: Ejercicio 8 del laboratorio (N=7, λ=0.2, μ=0.5)")
        print("0) Salir")
        op = input("Selecciona una opción: \n").strip()

        if op == "0":
            print("¡Hasta luego!")
            return

        try:
            if op == "1":
                lam, mu, N = ingresar_lam_mu_N()
                n = consultar_n(N)
                print_header("Resultados M/M/1/N (entrada λ_por_fuente, μ y N)")
                resolver_mm1_N(lam, mu, N, n_consulta=n, detallar=True)

            elif op == "2":
                lam, mu, N = ingresar_Tf_Ts_N()
                n = consultar_n(N)
                print_header("Resultados M/M/1/N (entrada Tf, Ts y N)")
                resolver_mm1_N(lam, mu, N, n_consulta=n, detallar=True)

            elif op == "3":
                caso_ejercicio_8()

            else:
                print("Opción inválida. Intenta nuevamente.")

        except Exception as e:
            print("\n[ERROR] {}".format(e))

# --------------------------
# Main
# --------------------------

if __name__ == "__main__":
    menu()