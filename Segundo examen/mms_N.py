"""
mms_N.py

Modelo M/M/s/N (s servidores, fuente finita de tamaño N) con menú interactivo y
procedimiento paso a paso (sin librerías externas).

Contexto típico (taller de servicio / dispositivos):
- Hay N "fuentes" potenciales (p.ej., dispositivos). Si hay n en el sistema (cola+servicio),
  entonces (N - n) están "libres" y pueden fallar/ llegar.
- La tasa de intento de llegada por CADA fuente libre es λ (lam_per_source).
- Por eso, la tasa de llegada del sistema cuando hay n en el sistema es: λ_n = (N - n) * λ.
- Hay s técnicos/servidores, cada uno con tasa μ (por hora).

Entradas:
- lam_per_source: λ por fuente libre (por hora)
- mu            : μ por hora (por servidor)
- s             : número de servidores (entero ≥ 1)
- N             : tamaño de la población (entero ≥ s)

Formulación (clásica del formulario):
Para 0 ≤ n ≤ s:
    C_n = [ N! / ((N-n)! n!) ] * (λ/μ)^n
Para s ≤ n ≤ N:
    C_n = [ N! / ((N-n)! s! s^{n-s}) ] * (λ/μ)^n

Normalización:
    P0 = 1 / ( Σ_{n=0}^N C_n ),  Pn = P0 * C_n

Promedios:
    Lq = Σ_{n=s}^N (n - s) * Pn
    L  = Σ_{n=0}^{s-1} n * Pn + Lq + s * (1 - Σ_{n=0}^{s-1} Pn)

Tasa efectiva (admitida):
    λ̅ = λ * (N - L) = Σ_{n=0}^{N-1} (N - n) λ Pn      (verificación)

Utilización efectiva:
    ρ  = λ̅ / (s μ)

Tiempos:
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
# Núcleo M/M/s/N
# --------------------------

def resolver_mms_N(lam_per_source, mu, s, N, n_consulta=None, detallar=True):
    """
    Calcula métricas de M/M/s/N y, si detallar=True, imprime el procedimiento.

    lam_per_source: λ por fuente libre (por hora)
    mu            : μ (por hora) por servidor
    s             : servidores (entero ≥ 1)
    N             : tamaño de la población (entero ≥ s)
    n_consulta    : entero opcional para P(N=n)
    """
    if lam_per_source <= 0 or mu <= 0:
        raise ValueError("λ por fuente y μ deben ser positivos.")
    if int(s) != s or s < 1:
        raise ValueError("s debe ser un entero ≥ 1.")
    if int(N) != N or N < s:
        raise ValueError("N debe ser un entero ≥ s.")
    s = int(s)
    N = int(N)

    a = lam_per_source / mu

    if detallar:
        print_sub("Paso 1: Parámetros del sistema (fuente finita con s servidores)")
        print("λ por fuente libre = {} /h".format(fmt(lam_per_source)))
        print("μ por servidor     = {} /h".format(fmt(mu)))
        print("s (servidores)     = {}".format(s))
        print("N (población)      = {}".format(N))
        print("a = λ/μ            = {} / {} = {}".format(fmt(lam_per_source), fmt(mu), fmt(a)))
        print("La tasa de llegada instantánea es λ_n = (N - n) * λ, y el servicio hasta sμ.")

    # Paso 2: C_n y normalización
    if detallar:
        print_sub("Paso 2: Coeficientes no normalizados C_n y cálculo de P0")
        print("Para 0 ≤ n ≤ s:   C_n = [N! / ((N-n)! n!)] * a^n")
        print("Para s ≤ n ≤ N:   C_n = [N! / ((N-n)! s! s^{n-s})] * a^n")

    C = []
    for n in range(0, N + 1):
        if n <= s:
            coef = factorial(N) / (factorial(N - n) * factorial(n))
            Cn = coef * (a ** n)
        else:
            coef = factorial(N) / (factorial(N - n) * factorial(s) * (s ** (n - s)))
            Cn = coef * (a ** n)
        C.append(Cn)
        if detallar:
            if n <= s:
                print("  n={}: C_n = {}! / (({}-{})! * {}!) * {}^{} = {}".format(
                    n, N, N, n, n, fmt(a), n, fmt(Cn)))
            else:
                print("  n={}: C_n = {}! / (({}-{})! * {}! * {}^({}-{})) * {}^{} = {}".format(
                    n, N, N, n, s, s, n, s, fmt(a), n, fmt(Cn)))

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

    # Paso 4: Lq
    Lq = sum((n - s) * Pn_array[n] for n in range(s, N + 1))
    if detallar:
        print_sub("Paso 4: Número promedio en cola Lq")
        print("Lq = Σ_{n=s}^{N} (n - s) Pn = {}".format(fmt(Lq)))

    # Paso 5: L
    sum_nPn_0_s_1 = sum(n * Pn_array[n] for n in range(0, s))
    sum_Pn_0_s_1 = sum(Pn_array[n] for n in range(0, s))
    L = sum_nPn_0_s_1 + Lq + s * (1.0 - sum_Pn_0_s_1)
    if detallar:
        print_sub("Paso 5: Número promedio en el sistema L")
        print("L = Σ_{n=0}^{s-1} n Pn + Lq + s * (1 - Σ_{n=0}^{s-1} Pn)")
        print("  Σ nPn (0..s-1) = {}   |   Σ Pn (0..s-1) = {}".format(fmt(sum_nPn_0_s_1), fmt(sum_Pn_0_s_1)))
        print("  L = {} + {} + {} * (1 - {}) = {}".format(
            fmt(sum_nPn_0_s_1), fmt(Lq), s, fmt(sum_Pn_0_s_1), fmt(L)))

    # Paso 6: λ efectivo (dos formas equivalentes)
    lam_eff_1 = lam_per_source * (N - L)  # definición estándar
    lam_eff_2 = sum((N - n) * lam_per_source * Pn_array[n] for n in range(0, N))  # verificación
    lam_eff = lam_eff_1
    if detallar:
        print_sub("Paso 6: Tasa efectiva de entrada λ̅ (dos formas)")
        print("λ̅ (def.) = λ * (N - L) = {} * (N - {}) = {}".format(
            fmt(lam_per_source), fmt(L), fmt(lam_eff_1)))
        print("λ̅ (alt)  = Σ (N-n) λ Pn (n=0..N-1) = {}  (verificación)".format(fmt(lam_eff_2)))

    if lam_eff <= 0:
        raise ValueError("λ̅ = 0 (no ingresan trabajos). No se definen W y Wq.")

    # Paso 7: ρ, W, Wq
    rho = lam_eff / (s * mu)
    W  = L  / lam_eff
    Wq = Lq / lam_eff
    if detallar:
        print_sub("Paso 7: Utilización efectiva y tiempos promedios")
        print("ρ  = λ̅ / (s μ) = {} / ({} * {}) = {}".format(fmt(lam_eff), s, fmt(mu), fmt(rho)))
        print("W  = L  / λ̅ = {} / {} = {} h = {} min".format(
            fmt(L), fmt(lam_eff), fmt(W), fmt(horas_a_min(W), 4)))
        print("Wq = Lq / λ̅ = {} / {} = {} h = {} min".format(
            fmt(Lq), fmt(lam_eff), fmt(Wq), fmt(horas_a_min(Wq), 4)))

        print_sub("Paso 8: (Opcional) P(N = n) y verificaciones Little")
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
        "Lq": Lq,
        "L": L,
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

def ingresar_lam_mu_s_N():
    print_sub("Entrada directa λ_por_fuente, μ, s y N")
    lam = leer_float("λ por fuente libre (llegadas/h): \n")
    mu  = leer_float("μ (servicios/h por servidor): \n")
    s   = leer_int("s (número de servidores): \n")
    N   = leer_int("N (tamaño de la población): \n")
    return lam, mu, s, N

def ingresar_Tf_Ts_s_N():
    print_sub("Entrada por tiempos promedio (min) y s, N")
    Tf_min = leer_float("Tiempo promedio entre fallos por dispositivo (min): \n")
    Ts_min = leer_float("Tiempo promedio de reparación (min): \n")
    if Tf_min <= 0 or Ts_min <= 0:
        raise ValueError("Los tiempos deben ser positivos.")
    lam = 60.0 / Tf_min  # λ por fuente libre
    mu  = 60.0 / Ts_min  # μ por servidor
    print("Conversión: λ = 60/Tf = 60/{} = {} /h".format(fmt(Tf_min, 3), fmt(lam, 6)))
    print("            μ = 60/Ts = 60/{} = {} /h".format(fmt(Ts_min, 3), fmt(mu, 6)))
    s  = leer_int("s (número de servidores): \n")
    N  = leer_int("N (tamaño de la población): \n")
    return lam, mu, s, N

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
# Caso guiado: Ejercicio 9
# --------------------------

def caso_ejercicio_9():
    """
    Ejercicio 9 (laboratorio):
      - N = 10 dispositivos
      - s = 3 técnicos
      - Fallos por dispositivo ~ Exp(0.1/h)  -> λ por fuente = 0.1/h
      - Reparación por técnico ~ Exp(0.5/h)  -> μ = 0.5/h
    Pide:
      (a) P(0 fallos), (b) P(2 fallos), (c) P(5 fallos),
      (d) Lq y L, (e) Wq y W.
    """
    print_header("Ejercicio 9 — Taller de 10 dispositivos con 3 técnicos (M/M/3/N)")
    lam_per_source = 0.1  # por hora por dispositivo libre
    mu = 0.5              # por hora por técnico
    s = 3
    N = 10
    print("Datos: λ_por_fuente = {} /h, μ = {} /h, s = {}, N = {}".format(
        fmt(lam_per_source), fmt(mu), s, N))

    out = resolver_mms_N(lam_per_source, mu, s, N, n_consulta=None, detallar=True)
    P = out["Pn_array"]

    print_sub("Cálculos solicitados específicos (a–e)")
    print("(a) P(0 fallos) = P(N=0) = {}".format(fmt(P[0])))
    print("(b) P(2 fallos) = P(N=2) = {}".format(fmt(P[2])))
    print("(c) P(5 fallos) = P(N=5) = {}".format(fmt(P[5])))
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
        print_header("MENÚ M/M/s/N — Paso a paso (fuente finita)")
        print("1) Ingresar λ_por_fuente, μ, s y N")
        print("2) Ingresar tiempos promedio Tf (fallo) y Ts (servicio) en minutos, y s, N")
        print("3) Caso guiado: Ejercicio 9 del laboratorio (N=10, s=3, λ=0.1, μ=0.5)")
        print("0) Salir")
        op = input("Selecciona una opción: \n").strip()

        if op == "0":
            print("¡Hasta luego!")
            return

        try:
            if op == "1":
                lam, mu, s, N = ingresar_lam_mu_s_N()
                n = consultar_n(N)
                print_header("Resultados M/M/s/N (entrada λ_por_fuente, μ, s y N)")
                resolver_mms_N(lam, mu, s, N, n_consulta=n, detallar=True)

            elif op == "2":
                lam, mu, s, N = ingresar_Tf_Ts_s_N()
                n = consultar_n(N)
                print_header("Resultados M/M/s/N (entrada Tf, Ts, s y N)")
                resolver_mms_N(lam, mu, s, N, n_consulta=n, detallar=True)

            elif op == "3":
                caso_ejercicio_9()

            else:
                print("Opción inválida. Intenta nuevamente.")

        except Exception as e:
            print("\n[ERROR] {}".format(e))

# --------------------------
# Main
# --------------------------

if __name__ == "__main__":
    menu()