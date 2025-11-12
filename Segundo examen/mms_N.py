"""
mms_N.py

Modelo M/M/s/N (s servidores, fuente finita de tamaño N).

Datos:
- lam: λ
- mu : μ
- s  : número de servidores
- N  : número total de clientes potenciales (población)

Formulación basada en el formulario:

Para 0 ≤ n ≤ s:
    Pn ∝ [ N! / ( (N-n)! n! ) ] (λ/μ)^n

Para s ≤ n ≤ N:
    Pn ∝ [ N! / ( (N-n)! s! s^{n-s} ) ] (λ/μ)^n

Luego se normaliza:
    P0 = 1 / sum_{n=0}^N C_n

Lq = sum_{n=s}^N (n - s) * Pn
L  = sum_{n=0}^{s-1} n * Pn + Lq + s * (1 - sum_{n=0}^{s-1} Pn)

λ̅ = λ (N - L)
ρ  = λ̅ / (s μ)

W  = L  / λ̅
Wq = Lq / λ̅
"""

import math

def factorial(n):
    r = 1
    for k in range(1, n + 1):
        r *= k
    return r

def resolver_mms_N(lam, mu, s, N):
    if s > N:
        raise ValueError("Debe cumplirse s ≤ N en M/M/s/N")

    a = lam / mu

    # Paso 1: C_n no normalizados
    C = []
    for n in range(0, N + 1):
        if n <= s:
            # C_n = [N! / ((N-n)! n!)] (λ/μ)^n
            coef = factorial(N) / (factorial(N - n) * factorial(n))
            Cn = coef * (a ** n)
        else:
            # C_n = [N! / ((N-n)! s! s^{n-s})] (λ/μ)^n
            coef = factorial(N) / (factorial(N - n) * factorial(s) * (s ** (n - s)))
            Cn = coef * (a ** n)
        C.append(Cn)

    # Paso 2: normalización para P0
    suma_C = 0.0
    for n in range(0, N + 1):
        suma_C += C[n]
    P0 = 1.0 / suma_C

    # Paso 3: Pn
    Pn_array = []
    for n in range(0, N + 1):
        Pn_array.append(P0 * C[n])

    # Paso 4: Lq
    Lq = 0.0
    for n in range(s, N + 1):
        Lq += (n - s) * Pn_array[n]

    # Paso 5: L
    sum_nPn_0_s_1 = 0.0
    sum_Pn_0_s_1 = 0.0
    for n in range(0, s):
        sum_nPn_0_s_1 += n * Pn_array[n]
        sum_Pn_0_s_1 += Pn_array[n]

    L = sum_nPn_0_s_1 + Lq + s * (1.0 - sum_Pn_0_s_1)

    # Paso 6: λ efectivo
    lam_efectiva = lam * (N - L)

    # Paso 7: ρ, W, Wq
    rho = lam_efectiva / (s * mu)
    W = L / lam_efectiva
    Wq = Lq / lam_efectiva

    return {
        "P0": P0,
        "Pn_array": Pn_array,
        "Lq": Lq,
        "L": L,
        "lambda_efectiva": lam_efectiva,
        "rho": rho,
        "W": W,
        "Wq": Wq,
    }


if __name__ == "__main__":
    lam = 0.5
    mu = 1.0
    s = 2
    N = 5
    res = resolver_mms_N(lam, mu, s, N)
    print("P0 =", res["P0"])
    print("L =", res["L"])
    print("W =", res["W"])