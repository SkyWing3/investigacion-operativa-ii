# --------------------------
# Utilidades
# --------------------------

def print_header(t):
    print("\n" + "=" * 76)
    print(t)
    print("=" * 76)

def print_sub(t):
    print("\n--- " + t + " ---")

# --------------------------
# Núcleo M/M/s/N
# --------------------------
def print_detalles(lam, mu, s, N):
    print_sub("Parámetros básicos")
    print("λ = {:.4f} por hora".format(lam))
    print("μ = {:.4f} por hora".format(mu))
    print("s = número de servidores = {}".format(s))
    print("N = capacidad total del sistema = {}".format(N))
    print("ρ = λ/(s*μ) = {:.4f} / ({} * {:.4f}) = {:.4f}".format(lam, s, mu, lam / (s * mu)))

def ingresar_lam_mu_s_N():
    print_sub("Entrada directa λ, μ, s y N")
    lam = float(input("λ (llegadas por hora): \n"))
    mu  = float(input("μ (servicios por minuto): \n"))
    s   = int(input("s (número de servidores): \n"))
    N   = int(input("N (capacidad total del sistema): \n"))
    return lam, 60.0 / mu, s, N

def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def calcular_p0(lam, mu, s, N):
    sum1 = sum((factorial(N) / (factorial(N - n) * factorial(n))) * ((lam / mu)**n) for n in range(0, s))
    sum2 = sum((factorial(N) / (factorial(N - n) * factorial(s) * (s**(n - s)))) * ((lam / mu)**n) for n in range(s, N + 1))
    p0 = 1 / (sum1 + sum2)
    print("p0 = [ Σ (λ/μ)^n / n!  +  Σ (λ/μ)^n / (s! * s^(n-s)) ]^-1")
    print("p0 = [{:.4f} + {:.4f}]^-1".format(sum1, sum2))
    print("p0 = {:.4f}".format(p0))
    return p0

def calcular_pn(lam, mu, s, N, n):
    P0 = calcular_p0(lam, mu, s, N)
    if n < s:
        Pn = (factorial(N) / (factorial(N - n) * factorial(n))) * ((lam / mu)**n) * P0
        print("pn = (N! / ((N-n)! * n!)) * (λ/μ)^n * p0")
        print("pn = ({}! / ({}-{})! * {}!) * ({:.4f})^{} * {:.4f}".format(N, N, n, n, lam/mu, n, P0))
    else:
        Pn = (factorial(N) / (factorial(N - n) * factorial(s) * (s**(n - s)))) * ((lam / mu)**n) * P0
        print("pn = (N! / ((N-n)! * s! * s^(n-s))) * (λ/μ)^n * p0")
        print("pn = ({}! / ({}-{})! * {}! * {}^({}-{})) * ({:.4f})^{} * {:.4f}".format(N, N, n, s, s, n, s, lam/mu, n, P0))
    print("Pn = {:.4f}".format(Pn))
    return Pn

def calcular_lq(lam, mu, s, N):
    lq = sum((n - s) * calcular_pn(lam, mu, s, N, n) for n in range(s, N + 1))
    print("Lq = Σ (n - s) * pn")
    print("Lq = {:.4f}".format(lq))
    return lq

def calcular_l(lam, mu, s, N):
    lq = calcular_lq(lam, mu, s, N)
    l = sum(n * calcular_pn(lam, mu, s, N, n) for n in range(0, s)) + lq + s * (1 - sum(calcular_pn(lam, mu, s, N, n) for n in range(0, s)))
    print("L = Σ n * pn + Lq + s * (1 - Σ pn)")
    print("L = {:.4f} + {:.4f} + {} * (1 - {:.4f})".format(sum(n * calcular_pn(lam, mu, s, N, n) for n in range(0, s)), lq, s, sum(calcular_pn(lam, mu, s, N, n) for n in range(0, s))))
    print("L = {:.4f}".format(l))
    return l

def calcular_lam_eff(lam, mu, s, N):
    l = calcular_l(lam, mu, s, N)
    lam_eff = lam * (N - l)
    print("λeff = λ * (N - L)")
    print("λeff = {:.4f} * ({:.4f} - {:.4f})".format(lam, N, l))
    print("λeff = {:.4f} por hora".format(lam_eff))
    return lam_eff

def calcular_w(lam, mu, s, N):
    L = calcular_l(lam, mu, s, N)
    lam_eff = calcular_lam_eff(lam, mu, s, N)
    W = L / lam_eff
    print("W = L / λeff")
    print("W = {:.4f} / {:.4f}".format(L, lam_eff))
    print("W = {:.4f} horas".format(W))
    return W

def calcular_wq(lam, mu, s, N):
    Lq = calcular_lq(lam, mu, s, N)
    lam_eff = calcular_lam_eff(lam, mu, s, N)
    Wq = Lq / lam_eff
    print("Wq = Lq / λeff")
    print("Wq = {:.4f} / {:.4f}".format(Lq, lam_eff))
    print("Wq = {:.4f} horas".format(Wq))
    return Wq

def menu():
    print_header("Sistema M/M/s/N")
    lam, mu, s, N = ingresar_lam_mu_s_N()
    print_detalles(lam, mu, s, N)

    while True:
        print_sub("Seleccione una métrica para calcular:")
        print("1. Probabilidad de que no haya clientes en el sistema (p0)")
        print("2. Probabilidad de que haya n clientes en el sistema (pn)")
        print("3. Número promedio de clientes en la cola (Lq)")
        print("4. Número promedio de clientes en el sistema (L)")
        print("5. Tasa efectiva de llegada (λeff)")
        print("6. Tiempo promedio en el sistema (W)")
        print("7. Tiempo promedio en la cola (Wq)")
        print("8. Salir")

        choice = input("Ingrese su elección (1-8): ")

        if choice == '1':
            calcular_p0(lam, mu, s, N)
        elif choice == '2':
            n = int(input("Ingrese el número de clientes n: "))
            calcular_pn(lam, mu, s, N, n)
        elif choice == '3':
            calcular_lq(lam, mu, s, N)
        elif choice == '4':
            calcular_l(lam, mu, s, N)
        elif choice == '5':
            calcular_lam_eff(lam, mu, s, N)
        elif choice == '6':
            calcular_w(lam, mu, s, N)
        elif choice == '7':
            calcular_wq(lam, mu, s, N)
        elif choice == '8':
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida. Por favor intente de nuevo.")

if __name__ == "__main__":
    menu()