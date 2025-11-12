"""
mm1_N.py

Modelo M/M/1/N (un servidor, fuente finita de tamaño N).

Datos:
- lam: λ (tasa de intento de llegada por cada fuente libre)
- mu : μ
- N  : tamaño de la población (número de "máquinas" o "clientes potenciales")

Formulación típica del formulario:

    Para n clientes en el sistema, hay (N-n) clientes libres.
    Entonces las tasas de llegada y salida dan lugar a:

    Pn ∝ [ N! / (N-n)! ] * (λ/μ)^n

    Es decir:
        Pn = C_n * P0
        C_n = [ N! / (N-n)! ] (λ/μ)^n

    1) Primero se calcula P0 usando la normalización:
       sum_{n=0}^N Pn = 1 => sum C_n * P0 = 1

    2) L = sum_{n=0}^N n * Pn
       Lq = sum_{n=1}^N (n-1) * Pn

    3) λ̅ = λ (N - L)
       ρ  = λ̅ / μ

    4) W  = L  / λ̅
       Wq = Lq / λ̅
"""

import math

def factorial(n):
    r = 1
    for k in range(1, n + 1):
        r *= k
    return r

def resolver_mm1_N(lam, mu, N):
    a = lam / mu

    # Paso 1: calcular C_n no normalizados
    C = []
    for n in range(0, N + 1):
        # C_n = N! / (N-n)! * (λ/μ)^n
        coef = factorial(N) / factorial(N - n)
        Cn = coef * (a ** n)
        C.append(Cn)

    # Paso 2: suma total para normalizar
    suma_C = 0.0
    for n in range(0, N + 1):
        suma_C += C[n]

    P0 = 1.0 / suma_C

    # Paso 3: vector Pn
    Pn_array = []
    for n in range(0, N + 1):
        Pn_array.append(P0 * C[n])

    # Paso 4: L y Lq
    L = 0.0
    Lq = 0.0
    for n in range(0, N + 1):
        L += n * Pn_array[n]
        if n >= 1:
            Lq += (n - 1) * Pn_array[n]

    # Paso 5: λ efectivo
    lam_efectiva = lam * (N - L)

    # Paso 6: ρ, W, Wq
    rho = lam_efectiva / mu
    W = L / lam_efectiva
    Wq = Lq / lam_efectiva

    return {
        "P0": P0,
        "Pn_array": Pn_array,
        "L": L,
        "Lq": Lq,
        "lambda_efectiva": lam_efectiva,
        "rho": rho,
        "W": W,
        "Wq": Wq,
    }


if __name__ == "__main__":
    lam = 0.5
    mu = 1.0
    N = 5
    res = resolver_mm1_N(lam, mu, N)
    print("P0 =", res["P0"])
    print("L =", res["L"])
    print("W =", res["W"])