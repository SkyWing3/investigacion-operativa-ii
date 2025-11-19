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
# Núcleo M/M/s
# --------------------------
def print_detalles(lam, mu, s):
    print_sub("Parámetros básicos")
    print("λ = {:.4f} por hora".format(lam))
    print("μ = {:.4f} por hora".format(mu))
    print("s = número de servidores = {}".format(s))
    print("ρ = λ/(s*μ) = {:.4f} / ({} * {:.4f}) = {:.4f}".format(lam, s, mu, lam / (s * mu)))

def ingresar_lam_mu_s():
    print_sub("Entrada directa λ, μ y s")
    lam = float(input("λ (llegadas por hora): \n"))
    mu  = float(input("μ (servicios por minuto): \n"))
    s   = int(input("s (número de servidores): \n"))
    return lam, 60.0 / mu, s

def calcular_p0(lam, mu, s):
    rho = lam / (s * mu)
    sum_terms = sum(( (lam / mu) ** n ) / factorial(n) for n in range(s))
    last_term = ( (lam / mu) ** s ) / (factorial(s) * (1 - rho))
    P0 = 1 / (sum_terms + last_term)
    print("p0 = 1 / [Σ (λ/μ)^n / n! + (λ/μ)^s / (s! * (1 - ρ))]")
    print("p0 = 1 / [{:.4f} + {:.4f}]".format(sum_terms, last_term))
    print("p0 = {:.4f}".format(P0))
    return P0

def calcular_lq(lam, mu, s):
    rho = lam / (s * mu)
    P0 = calcular_p0(lam, mu, s)
    Lq = ( ( (lam / mu) ** s ) * rho ) / ( factorial(s) * (1 - rho) ** 2 ) * P0
    print("Lq = [ (λ/μ)^s * ρ ] / [ s! * (1 - ρ)^2 ] * p0")
    print("Lq = [ ({:.4f})^{} * {:.4f} ] / [ {}! * (1 - {:.4f})^2 ] * {:.4f}".format(lam/mu, s, rho, s, rho, P0))
    print("Lq = {:.4f}".format(Lq))
    return Lq

def calcular_wq(lam, mu, s):
    Lq = calcular_lq(lam, mu, s)
    Wq = Lq / lam
    print("Wq = Lq / λ = {:.4f} / {:.4f}".format(Lq, lam))
    print("Wq = {:.4f}".format(Wq))
    return Wq

def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def calcular_w(lam, mu, s):
    Wq = calcular_wq(lam, mu, s)
    W = Wq + (1 / mu)
    print("W = Wq + 1/μ = {:.4f} + 1/{:.4f}".format(Wq, mu))
    print("W = {:.4f}".format(W))
    return W

def calcular_l(lam, mu, s):
    W = calcular_w(lam, mu, s)
    L = lam * W
    print("L = λ * W = {:.4f} * {:.4f}".format(lam, W))
    print("L = {:.4f}".format(L))
    return L

def calcular_pn(lam, mu, s, n):
    P0 = calcular_p0(lam, mu, s)
    if n < s:
        Pn = ( (lam / mu) ** n ) / factorial(n) * P0
        print("pn = (λ/μ)^n / n! * p0 = ({:.4f})^{} / {}! * {:.4f}".format(lam/mu, n, n, P0))
    else:
        Pn = ( (lam / mu) ** n ) / ( factorial(s) * (s ** (n - s)) ) * P0
        print("pn = (λ/μ)^n / [s! * s^(n - s)] * p0 = ({:.4f})^{} / [{}! * {}^({} - {})] * {:.4f}".format(lam/mu, n, s, s, n, s, P0))
    print("Pn = {:.4f}".format(Pn))
    return Pn

def menu():
    print_header("Sistema M/M/s")
    lam, mu, s = ingresar_lam_mu_s()
    print_detalles(lam, mu, s)

    while True:
        print_sub("Seleccione una opción para calcular:")
        print("1. Probabilidad de que no haya clientes en el sistema (P0)")
        print("2. Probabilidad de que haya n clientes en el sistema (Pn)")
        print("3. Número promedio de clientes en la cola (Lq)")
        print("4. Tiempo promedio de espera en la cola (Wq)")
        print("5. Tiempo promedio en el sistema (W)")
        print("6. Número promedio de clientes en el sistema (L)")
        print("7. Salir")

        opcion = input("Ingrese el número de la opción deseada: ")

        if opcion == '1':
            calcular_p0(lam, mu, s)
        elif opcion == '2':
            n = int(input("Ingrese el número de clientes n: "))
            calcular_pn(lam, mu, s, n)
        elif opcion == '3':
            calcular_lq(lam, mu, s)
        elif opcion == '4':
            calcular_wq(lam, mu, s)
        elif opcion == '5':
            calcular_w(lam, mu, s)
        elif opcion == '6':
            calcular_l(lam, mu, s)
        elif opcion == '7':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    menu()
