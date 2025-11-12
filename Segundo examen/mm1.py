"""
mm1.py

Modelo de colas M/M/1 basado en el formulario, con menú interactivo y
procedimiento paso a paso (sin librerías externas).

Entradas (opciones):
- (A) lam (llegadas/h) y mu (servicios/h)
- (B) lam (llegadas/h) y tiempo promedio de servicio en minutos (Ts_min)

Fórmulas usadas (M/M/1 con ρ = λ/μ < 1):
    ρ  = λ / μ
    P0 = 1 - ρ
    Pn = (1 - ρ) * ρ^n
    L  = ρ / (1 - ρ) = λ / (μ - λ)
    Lq = λ^2 / [ μ (μ - λ) ]
    W  = 1 / (μ - λ)                   (en horas)
    Wq = λ / [ μ (μ - λ) ]             (en horas)

Verificaciones:
    L  ?= λ * W
    Lq ?= λ * Wq

Incluye atajo para "Ejercicio 4" del portafolio (dos escenarios).
"""

import math

# --------------------------
# Utilidades de impresión
# --------------------------

def fmt(x, dec=6):
    """Formateo estándar para números."""
    if isinstance(x, (int,)):
        return str(x)
    return "{0:.{1}f}".format(x, dec)

def horas_a_min(h):
    return h * 60.0

def print_header(titulo):
    print("\n" + "=" * 72)
    print(titulo)
    print("=" * 72)

def print_sub(titulo):
    print("\n--- " + titulo + " ---")

# --------------------------
# Núcleo M/M/1
# --------------------------

def resolver_mm1(lam, mu, n_consulta=None, detallar=True):
    """
    Calcula todas las métricas M/M/1 y opcionalmente imprime el procedimiento.

    lam: tasa de llegada (por hora)
    mu : tasa de servicio (por hora)
    n_consulta: entero n para calcular P(N=n)
    detallar: si True, imprime paso a paso

    Retorna diccionario con métricas y funciones auxiliares.
    """
    if lam <= 0 or mu <= 0:
        raise ValueError("λ y μ deben ser positivos.")
    rho = lam / mu
    if detallar:
        print_sub("Paso 1: Factor de utilización ρ")
        print("ρ = λ / μ = {} / {} = {}".format(fmt(lam), fmt(mu), fmt(rho)))
    if rho >= 1.0:
        raise ValueError("Sistema inestable: ρ = λ/μ debe ser < 1 para M/M/1.")

    P0 = 1.0 - rho
    if detallar:
        print_sub("Paso 2: Probabilidad de 0 clientes en el sistema")
        print("P0 = 1 - ρ = 1 - {} = {}".format(fmt(rho), fmt(P0)))

    def Pn(n):
        if n < 0:
            return 0.0
        return P0 * (rho ** n)

    # Métricas principales
    L  = rho / (1.0 - rho)
    L2 = lam / (mu - lam)  # forma equivalente
    Lq = (lam ** 2) / (mu * (mu - lam))
    W  = 1.0 / (mu - lam)           # horas
    Wq = lam / (mu * (mu - lam))    # horas

    if detallar:
        print_sub("Paso 3: Número promedio en el sistema L")
        print("L  = ρ / (1 - ρ) = {} / (1 - {}) = {}".format(fmt(rho), fmt(rho), fmt(L)))
        print("L' = λ / (μ - λ) = {} / ({} - {}) = {}  (verificación)".format(fmt(lam), fmt(mu), fmt(lam), fmt(L2)))

        print_sub("Paso 4: Número promedio en cola Lq")
        print("Lq = λ^2 / [ μ (μ - λ) ] = {}^2 / [ {} * ({} - {}) ] = {}".format(
            fmt(lam), fmt(mu), fmt(mu), fmt(lam), fmt(Lq)))

        print_sub("Paso 5: Tiempo promedio en el sistema W")
        print("W  = 1 / (μ - λ) = 1 / ({} - {}) = {} horas = {} min".format(
            fmt(mu), fmt(lam), fmt(W), fmt(horas_a_min(W), 4)))

        print_sub("Paso 6: Tiempo promedio en cola Wq")
        print("Wq = λ / [ μ (μ - λ) ] = {} / [ {} * ({} - {}) ] = {} horas = {} min".format(
            fmt(lam), fmt(mu), fmt(mu), fmt(lam), fmt(Wq), fmt(horas_a_min(Wq), 4)))

        print_sub("Paso 7: Verificación con Ley de Little")
        print("λ * W  = {} * {}  = {}  ≈ L = {}".format(fmt(lam), fmt(W), fmt(lam * W), fmt(L)))
        print("λ * Wq = {} * {} = {} ≈ Lq = {}".format(fmt(lam), fmt(Wq), fmt(lam * Wq), fmt(Lq)))

    Pn_val = None
    if n_consulta is not None:
        Pn_val = Pn(n_consulta)
        if detallar:
            print_sub("Paso 8: Probabilidad de exactamente n clientes (n = {})".format(n_consulta))
            print("Pn = (1 - ρ) * ρ^n = {} * {}^{} = {}".format(fmt(P0), fmt(rho), n_consulta, fmt(Pn_val)))

    return {
        "rho": rho,
        "P0": P0,
        "Pn_func": Pn,
        "L": L,
        "Lq": Lq,
        "W_horas": W,
        "Wq_horas": Wq,
        "W_min": horas_a_min(W),
        "Wq_min": horas_a_min(Wq),
        "Pn_val": Pn_val,
    }

# --------------------------
# Entrada de datos
# --------------------------

def leer_float(msg):
    while True:
        s = input(msg).strip().replace(",", ".")
        try:
            v = float(s)
            return v
        except ValueError:
            print("  -> Ingresa un número válido, por favor.")

def ingresar_lam_mu():
    print_sub("Entrada directa λ y μ")
    lam = leer_float("λ (llegadas por hora): \n")
    mu  = leer_float("μ (servicios por hora): \n")
    return lam, mu

def ingresar_lam_Ts():
    print_sub("Entrada λ y tiempo de servicio promedio (en minutos)")
    lam = leer_float("λ (llegadas por hora): \n")
    Ts_min = leer_float("Tiempo promedio de servicio (minutos por cliente): \n")
    if Ts_min <= 0:
        raise ValueError("El tiempo de servicio debe ser positivo.")
    mu = 60.0 / Ts_min  # servicios por hora
    print("Conversión: μ = 60 / Ts = 60 / {} = {} servicios/hora".format(fmt(Ts_min, 3), fmt(mu, 6)))
    return lam, mu

def consultar_n():
    while True:
        n = input("n para P(N = n) (ENTER para omitir): \n").strip()
        if n == "":
            return None
        if n.isdigit() and int(n) >= 0:
            return int(n)
        print("  -> Debe ser un entero n ≥ 0, o ENTER para omitir.")

# --------------------------
# Casos guiados (Ejercicio 4)
# --------------------------

def caso_ejercicio_4():
    """
    Problema 4 (portafolio) – parte (a) y (b)
    (a) λ = 20/h, Ts = 2 minutos  => μ = 30/h
    (b) λ = 20/h, Ts = 1.5 minutos => μ = 40/h
    """
    print_header("Ejercicio 4 — Parte (a)")
    lam = 20.0
    Ts_a = 2.0
    mu_a = 60.0 / Ts_a  # 30/h
    print("Datos: λ = {} por hora, Ts = {} min  => μ = {} por hora".format(lam, Ts_a, fmt(mu_a)))
    n = 10  # prob de 10 clientes en el sistema (como pide el enunciado)
    resolver_mm1(lam, mu_a, n_consulta=n, detallar=True)

    print_header("Ejercicio 4 — Parte (b)")
    Ts_b = 1.5
    mu_b = 60.0 / Ts_b  # 40/h
    print("Datos: λ = {} por hora, Ts = {} min  => μ = {} por hora".format(lam, Ts_b, fmt(mu_b)))
    n = 10
    resolver_mm1(lam, mu_b, n_consulta=n, detallar=True)

# --------------------------
# Menú principal
# --------------------------

def menu():
    while True:
        print_header("MENÚ M/M/1 — Paso a paso")
        print("1) Ingresar λ y μ")
        print("2) Ingresar λ y tiempo de servicio promedio (minutos)")
        print("3) Caso guiado: Ejercicio 4 (partes a y b)")
        print("0) Salir")

        op = input("Selecciona una opción: \n").strip()
        if op == "0":
            print("¡Hasta luego!")
            return

        try:
            if op == "1":
                lam, mu = ingresar_lam_mu()
                n = consultar_n()
                print_header("Resultados M/M/1 (entrada λ y μ)")
                resolver_mm1(lam, mu, n_consulta=n, detallar=True)

            elif op == "2":
                lam, mu = ingresar_lam_Ts()
                n = consultar_n()
                print_header("Resultados M/M/1 (entrada λ y Ts en minutos)")
                resolver_mm1(lam, mu, n_consulta=n, detallar=True)

            elif op == "3":
                caso_ejercicio_4()

            else:
                print("Opción inválida. Intenta nuevamente.")
        except Exception as e:
            print("\n[ERROR] {}".format(e))

# --------------------------
# Main
# --------------------------

if __name__ == "__main__":
    menu()