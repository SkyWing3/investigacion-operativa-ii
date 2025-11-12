"""
mms.py

Modelo de colas M/M/s (s servidores) con menú interactivo y
procedimiento paso a paso (sin librerías externas).

Entradas:
- lam: tasa de llegada λ (por hora)
- mu : tasa de servicio por servidor μ (por hora)
- s  : número de servidores

Fórmulas (M/M/s estable: ρ = λ/(sμ) < 1):
    ρ = λ / (s μ)
    a = λ / μ

    P0 = [ sum_{n=0}^{s-1} (a^n / n!) + (a^s / s!) * (1 / (1 - ρ)) ]^{-1}

    Para 0 ≤ n ≤ s:
        Pn = (a^n / n!) * P0
    Para n ≥ s:
        Pn = (a^n / (s! * s^{n-s})) * P0

    Probabilidad de esperar (todas las servers ocupadas) – Erlang C:
        Pw = (a^s / (s! * (1 - ρ))) * P0

    Lq = P0 * (a^s * ρ) / ( s! * (1-ρ)^2 )
    Wq = Lq / λ
    W  = Wq + 1/μ
    L  = λ * W

Verificaciones:
    L  ?= Lq + (λ/μ)    (número promedio en servicio)
    L  ?= λ * W
    Lq ?= λ * Wq

Caso guiado: Ejercicio 5 del portafolio
  - s = 5 cajeras
  - λ = 90/h
  - Ts = 2 min ⇒ μ = 30/h
"""

import math

# --------------------------
# Utilidades
# --------------------------

def factorial(n):
    """Factorial simple (entero no negativo)."""
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
# Núcleo M/M/s
# --------------------------

def resolver_mms(lam, mu, s, n_consulta=None, detallar=True):
    """
    Calcula métricas M/M/s. Si detallar=True, imprime procedimiento paso a paso.
    lam: llegadas/hora, mu: servicios/hora por servidor, s: servidores (int >= 1)
    n_consulta: entero n opcional para P(N=n)
    """
    if lam <= 0 or mu <= 0 or s <= 0 or int(s) != s:
        raise ValueError("Parámetros inválidos: λ>0, μ>0, s entero ≥ 1.")

    s = int(s)
    a = lam / mu
    rho = lam / (s * mu)

    if detallar:
        print_sub("Paso 1: Parámetros y utilización")
        print("λ = {} por hora".format(fmt(lam)))
        print("μ = {} por hora (por servidor)".format(fmt(mu)))
        print("s = {} servidores".format(s))
        print("a = λ/μ = {} / {} = {}".format(fmt(lam), fmt(mu), fmt(a)))
        print("ρ = λ / (s μ) = {} / ({} * {}) = {}".format(fmt(lam), s, fmt(mu), fmt(rho)))

    if rho >= 1.0:
        raise ValueError("Sistema inestable: requiere ρ = λ/(sμ) < 1.")

    # P0
    if detallar:
        print_sub("Paso 2: Cálculo de P0 (prob. no hay en sistema)")
        print("P0 = [ sum_{n=0}^{s-1} (a^n/n!) + (a^s/s!) * (1/(1-ρ)) ]^{-1}")

    sum1 = 0.0
    if detallar:
        print("  sum1 = Σ_{n=0}^{s-1} a^n / n!:")
    for n in range(0, s):
        term = (a ** n) / factorial(n)
        sum1 += term
        if detallar:
            print("    n={}: a^n/n! = {}^{} / {}! = {}".format(n, fmt(a), n, n, fmt(term)))

    sum2 = (a ** s) / factorial(s) * (1.0 / (1.0 - rho))
    if detallar:
        print("  sum2 = (a^s / s!) * (1/(1-ρ)) = ({}^{}/ {}!) * (1/(1-{})) = {}".format(
            fmt(a), s, s, fmt(rho), fmt(sum2)))

    P0 = 1.0 / (sum1 + sum2)
    if detallar:
        print("  P0 = 1 / (sum1 + sum2) = 1 / ({} + {}) = {}".format(fmt(sum1), fmt(sum2), fmt(P0)))

    # Pn función
    def Pn(n):
        if n < 0:
            return 0.0
        if n <= s:
            return (a ** n) / factorial(n) * P0
        else:
            return (a ** n) / (factorial(s) * (s ** (n - s))) * P0

    # Probabilidad de esperar (Erlang C)
    Pw = (a ** s) / (factorial(s) * (1.0 - rho)) * P0
    if detallar:
        print_sub("Paso 3: Probabilidad de esperar (todas las servers ocupadas)")
        print("Pw = (a^s / (s! * (1-ρ))) * P0")
        print("   = ({}^{} / ({}! * (1 - {}))) * {} = {}".format(
            fmt(a), s, s, fmt(rho), fmt(P0), fmt(Pw)))

    # Lq
    Lq = P0 * (a ** s) * rho / (factorial(s) * ((1.0 - rho) ** 2))
    if detallar:
        print_sub("Paso 4: Número promedio en cola Lq (Clientes promedio esperando)")
        print("Lq = P0 * (a^s * ρ) / (s! * (1-ρ)^2)")
        print("   = {} * ({}^{} * {}) / ({}! * (1-{})^2)".format(
            fmt(P0), fmt(a), s, fmt(rho), s, fmt(rho)))
        print("   = {}".format(fmt(Lq)))

    # Wq, W, L
    Wq = Lq / lam
    W  = Wq + 1.0 / mu
    L  = lam * W

    if detallar:
        print_sub("Paso 5: Tiempos promedio (espera en fila (Wq) y espera en sistema (W))")
        print("Wq = Lq / λ = {} / {} = {} horas = {} min".format(
            fmt(Lq), fmt(lam), fmt(Wq), fmt(horas_a_min(Wq), 4)))
        print("W  = Wq + 1/μ = {} + 1/{} = {} horas = {} min".format(
            fmt(Wq), fmt(mu), fmt(W), fmt(horas_a_min(W), 4)))

        print_sub("Paso 6: Número promedio en el sistema L")
        print("L = λ * W = {} * {} = {}".format(fmt(lam), fmt(W), fmt(L)))

        print_sub("Paso 7: Verificaciones (consistencias)")
        print("¿L ≈ Lq + λ/μ?  LHS = {} | RHS = {}".format(fmt(L), fmt(Lq + (lam/mu))))
        print("¿L ≈ λ * W?     LHS = {} | RHS = {}".format(fmt(L), fmt(lam * W)))
        print("¿Lq ≈ λ * Wq?   LHS = {} | RHS = {}".format(fmt(Lq), fmt(lam * Wq)))

    Pn_val = None
    if n_consulta is not None:
        Pn_val = Pn(n_consulta)
        if detallar:
            print_sub("Paso 8: Probabilidad de exactamente n clientes en el sistema (n = {})".format(n_consulta))
            if n_consulta <= s:
                print("Pn = (a^n / n!) * P0 = ({}^{} / {}!) * {} = {}".format(
                    fmt(a), n_consulta, n_consulta, fmt(P0), fmt(Pn_val)))
            else:
                print("Pn = (a^n / (s! * s^(n-s))) * P0 = ({}^{} / ({}! * {}^({}-{}))) * {} = {}".format(
                    fmt(a), n_consulta, s, s, n_consulta, s, fmt(P0), fmt(Pn_val)))

    return {
        "rho": rho,
        "a": a,
        "P0": P0,
        "Pw": Pw,
        "Pn_func": Pn,
        "Lq": Lq,
        "Wq_horas": Wq,
        "Wq_min": horas_a_min(Wq),
        "W_horas": W,
        "W_min": horas_a_min(W),
        "L": L,
        "Pn_val": Pn_val,
    }

# --------------------------
# Entrada interactiva
# --------------------------

def leer_float(msg):
    while True:
        s = input(msg).strip().replace(",", ".")
        try:
            v = float(s)
            return v
        except ValueError:
            print("  -> Ingresa un número válido.")

def leer_int(msg):
    while True:
        s = input(msg).strip()
        if s.isdigit():
            return int(s)
        print("  -> Ingresa un entero válido.")

def ingresar_lam_mu_s():
    print_sub("Entrada directa λ, μ y s")
    lam = leer_float("λ (llegadas por hora): \n")
    mu  = leer_float("μ (servicios por hora, por servidor): \n")
    s   = leer_int("s (número de servidores): \n")
    return lam, mu, s

def ingresar_lam_Ts_s():
    print_sub("Entrada λ, tiempo de servicio promedio (min) y s")
    lam    = leer_float("λ (llegadas por hora): \n")
    Ts_min = leer_float("Tiempo promedio de servicio (min por cliente): \n")
    if Ts_min <= 0:
        raise ValueError("El tiempo de servicio debe ser positivo.")
    mu = 60.0 / Ts_min
    print("Conversión: μ = 60 / Ts = 60 / {} = {} servicios/hora".format(fmt(Ts_min, 3), fmt(mu, 6)))
    s  = leer_int("s (número de servidores): \n")
    return lam, mu, s

def consultar_n():
    n = input("n para calcular P(N = n) (ENTER para omitir): \n").strip()
    if n == "":
        return None
    if n.isdigit():
        return int(n)
    print("  -> n inválido, se omite el cálculo de P(N=n).")
    return None

# --------------------------
# Caso guiado: Ejercicio 5
# --------------------------

def caso_ejercicio_5():
    """
    Ejercicio 5 (portafolio):
      - Cinco cajeras (s=5)
      - Llegan 90 clientes/h (λ = 90/h)
      - Servicio promedio 2 min (μ = 60/2 = 30/h por cajera)
    Pide:
      a) P0
      b) Lq
      c) L
      d) Wq
      e) W
    """
    print_header("Ejercicio 5 — Banco con 5 cajeras")
    lam = 90.0
    Ts_min = 2.0
    mu = 60.0 / Ts_min     # 30/h
    s  = 5
    print("Datos: λ = {} por hora, Ts = {} min ⇒ μ = {} por hora, s = {}".format(
        fmt(lam), fmt(Ts_min), fmt(mu), s))
    print("Se calcularán P0, Lq, L, Wq, W y la probabilidad de espera (Erlang C).")
    resolver_mms(lam, mu, s, n_consulta=None, detallar=True)

# --------------------------
# Menú principal
# --------------------------

def menu():
    while True:
        print_header("MENÚ M/M/s — Paso a paso")
        print("1) Ingresar λ, μ y s")
        print("2) Ingresar λ, Ts (minutos) y s")
        print("3) Caso guiado: Ejercicio 5 del portafolio")
        print("0) Salir")
        op = input("Selecciona una opción: \n").strip()

        if op == "0":
            print("¡Hasta luego!")
            return

        try:
            if op == "1":
                lam, mu, s = ingresar_lam_mu_s()
                n = consultar_n()
                print_header("Resultados M/M/s (entrada λ, μ y s)")
                resolver_mms(lam, mu, s, n_consulta=n, detallar=True)

            elif op == "2":
                lam, mu, s = ingresar_lam_Ts_s()
                n = consultar_n()
                print_header("Resultados M/M/s (entrada λ, Ts y s)")
                resolver_mms(lam, mu, s, n_consulta=n, detallar=True)

            elif op == "3":
                caso_ejercicio_5()

            else:
                print("Opción inválida. Intenta nuevamente.")

        except Exception as e:
            print("\n[ERROR] {}".format(e))

# --------------------------
# Main
# --------------------------

if __name__ == "__main__":
    menu()