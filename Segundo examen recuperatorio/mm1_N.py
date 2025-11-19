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
# Núcleo M/M/1/N
# --------------------------
def print_detalles(lam, mu, N):
    print_sub("Parámetros básicos")
    print("λ = {:.4f} por hora".format(lam))
    print("μ = {:.4f} por hora".format(mu))
    print("N = capacidad total del sistema = {}".format(N))
    print("ρ = λ/μ = {:.4f} / {:.4f} = {:.4f}".format(lam, mu, lam / mu))

def ingresar_lam_mu_N():
    print_sub("Entrada directa λ, μ y N")
    lam = float(input("λ (llegadas por hora): \n"))
    mu  = float(input("μ (servicios por minuto): \n"))
    N   = int(input("N (capacidad total del sistema): \n"))
    return lam, 60.0 / mu, N

def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def calcular_p0(lam, mu, N):
    rho = lam / mu
    P0 = [sum((factorial(N) / (factorial(N - n)) * (rho**n)) for n in range(0, N + 1))]**-1
    print("p0 = 1 / [Σ (N! / (N - n)!) * ρ^n]^-1")
    print("p0 = 1 / [{:.4f}]".format(sum((factorial(N) / (factorial(N - n)) * (rho**n) for n in range(0, N + 1)))))
    print("p0 = {:.4f}".format(P0))
    return P0

def calcular_pn(lam, mu, N, n):
    rho = lam / mu
    P0 = calcular_p0(lam, mu, N)
    Pn = (factorial(N) / factorial(N - n)) * (rho ** n) * P0
    print("pn = (N! / (N - n)!) * ρ^n * p0")
    print("pn = ({}! / ({} - {})!) * ({:.4f})^{} * {:.4f}".format(N, N, n, rho, n, P0))
    print("Pn = {:.4f}".format(Pn))
    return Pn

def calcular_lq(lam, mu, N):
    Lq = sum((n - 1) * calcular_pn(lam, mu, N, n) for n in range(1, N + 1))
    print("Lq = Σ (n - 1) * pn")
    print("Lq = {:.4f}".format(Lq))
    return Lq

def calcular_l(lam, mu, N):
    Lq = calcular_lq(lam, mu, N)
    L = Lq + (1 - calcular_p0(lam, mu, N))
    print("L = Lq + (1 - p0) = {:.4f} + (1 - {:.4f})".format(Lq, calcular_p0(lam, mu, N)))
    print("L = {:.4f}".format(L))
    return L

def calcular_lambda_ef(lam, mu, N):
    Pn = calcular_pn(lam, mu, N, N)
    L = calcular_l(lam, mu, N)
    lambda_efectiva = lam * (N - L)
    print("λef = λ * (N - L) = {:.4f} * ({} - {:.4f})".format(lam, N, L))
    print("λef = {:.4f}".format(lambda_efectiva))
    return lambda_efectiva

def calcular_w(lam, mu, N):
    L = calcular_l(lam, mu, N)
    lambda_efectiva = calcular_lambda_ef(lam, mu, N)
    W = L / lambda_efectiva
    print("W = L / λef = {:.4f} / {:.4f}".format(L, lambda_efectiva))
    print("W = {:.4f}".format(W))
    return W

def calcular_wq(lam, mu, N):
    Lq = calcular_lq(lam, mu, N)
    lambda_efectiva = calcular_lambda_ef(lam, mu, N)
    Wq = Lq / lambda_efectiva
    print("Wq = Lq / λef = {:.4f} / {:.4f}".format(Lq, lambda_efectiva))
    print("Wq = {:.4f}".format(Wq))
    return Wq

def menu():
    print_header("Sistema M/M/1/N")
    lam, mu, N = ingresar_lam_mu_N()
    print_detalles(lam, mu, N)

    while True:
        print_sub("Seleccione una métrica para calcular:")
        print("1. Probabilidad de que no haya clientes en el sistema (P0)")
        print("2. Probabilidad de que haya n clientes en el sistema (Pn)")
        print("3. Número promedio de clientes en la cola (Lq)")
        print("4. Número promedio de clientes en el sistema (L)")
        print("5. Tasa efectiva de llegada (λef)")
        print("6. Tiempo promedio en el sistema (W)")
        print("7. Tiempo promedio en la cola (Wq)")
        print("8. Salir")

        opcion = input("Ingrese el número de la opción deseada: ")

        if opcion == '1':
            calcular_p0(lam, mu, N)
        elif opcion == '2':
            n = int(input("Ingrese el número de clientes n: "))
            calcular_pn(lam, mu, N, n)
        elif opcion == '3':
            calcular_lq(lam, mu, N)
        elif opcion == '4':
            calcular_l(lam, mu, N)
        elif opcion == '5':
            calcular_lambda_ef(lam, mu, N)
        elif opcion == '6':
            calcular_w(lam, mu, N)
        elif opcion == '7':
            calcular_wq(lam, mu, N)
        elif opcion == '8':
            print("Saliendo del menú del sistema M/M/1/N.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    menu()