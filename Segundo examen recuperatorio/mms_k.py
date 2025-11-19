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
# Núcleo M/M/s/k
# --------------------------
def print_detalles(lam, mu, s, k):
    print_sub("Parámetros básicos")
    print("λ = {:.4f} por hora".format(lam))
    print("μ = {:.4f} por hora".format(mu))
    print("s = número de servidores = {}".format(s))
    print("k = capacidad total del sistema = {}".format(k))
    print("ρ = λ/(s*μ) = {:.4f} / ({} * {:.4f}) = {:.4f}".format(lam, s, mu, lam / (s * mu)))

def ingresar_lam_mu_s_k():
    print_sub("Entrada directa λ, μ, s y k")
    lam = float(input("λ (llegadas por hora): \n"))
    mu  = float(input("μ (servicios por minuto): \n"))
    s   = int(input("s (número de servidores): \n"))
    k   = int(input("k (capacidad total del sistema): \n"))
    return lam, 60.0 / mu, s, k

def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def calcular_p0(lam, mu, s, k):
    sum_terms = sum(( (lam / mu) ** n ) / factorial(n) for n in range(s))
    last_term = sum(( (lam / mu) ** n ) / (factorial(s) * (s ** (n - s))) for n in range(s, k + 1))
    P0 = 1 / (sum_terms + last_term)
    print("p0 = 1 / [Σ (λ/μ)^n / n! + Σ (λ/μ)^n / (s! * s^(n-s))]")
    print("p0 = 1 / [{:.4f} + {:.4f}]".format(sum_terms, last_term))
    print("p0 = {:.4f}".format(P0))
    return P0

def calcular_pn(lam, mu, s, k, n):
    P0 = calcular_p0(lam, mu, s, k)
    if n < s:
        Pn = ( (lam / mu) ** n ) / factorial(n) * P0
        print("pn = (λ/μ)^n / n! * p0")
        print("pn = ({:.4f})^{} / {}! * {:.4f}".format(lam/mu, n, n, P0))
    else:
        Pn = ( (lam / mu) ** n ) / (factorial(s) * (s ** (n - s))) * P0
        print("pn = (λ/μ)^n / (s! * s^(n-s)) * p0")
        print("pn = ({:.4f})^{} / ({}! * {}^({}-{})) * {:.4f}".format(lam/mu, n, s, s, n, s, P0))
    print("Pn = {:.4f}".format(Pn))
    return Pn

def calcular_lq(lam, mu, s, k):
    P0 = calcular_p0(lam, mu, s, k)
    numerator = sum(( (lam / mu) ** n ) * (n - s) / (factorial(s) * (s ** (n - s))) for n in range(s + 1, k + 1))
    Lq = numerator * P0
    print("Lq = Σ [ (λ/μ)^n * (n - s) ] / [ s! * s^(n-s) ] * p0")
    print("Lq = Σ [ ({:.4f})^n * (n - {}) ] / [ {}! * {}^(n-{}) ] * {:.4f}".format(lam/mu, s, s, s, s, P0))
    print("Lq = {:.4f}".format(Lq))
    return Lq

def calcular_l(lam, mu, s, k):
    Lq = calcular_lq(lam, mu, s, k)
    L = Lq + (lam / mu)
    print("L = Lq + λ/μ = {:.4f} + {:.4f}".format(Lq, lam/mu))
    print("L = {:.4f}".format(L))
    return L

def calcular_lam_eff(lam, mu, s, k):
    Pk = calcular_pn(lam, mu, s, k, k)
    lam_eff = lam * (1 - Pk)
    print("λ_eff = λ * (1 - pk) = {:.4f} * (1 - {:.4f})".format(lam, Pk))
    print("λ_eff = {:.4f}".format(lam_eff))
    return lam_eff

def calcular_w(lam, mu, s):
    print("W = 1 / (μ - λ/s) = 1 / ({:.4f} - {:.4f}/{})".format(mu, lam, s))
    W = 1 / (mu - (lam / s))
    print("W = {:.4f}".format(W))
    return W

def calcular_wq(lam, mu, s, k):
    Lq = calcular_lq(lam, mu, s, k)
    Wq = Lq / lam
    print("Wq = Lq / λ = {:.4f} / {:.4f}".format(Lq, lam))
    print("Wq = {:.4f}".format(Wq))
    return Wq

def menu():
    print_header("Sistema M/M/s/k")
    lam, mu, s, k = ingresar_lam_mu_s_k()
    print_detalles(lam, mu, s, k)

    while True:
        print_sub("Seleccione una métrica para calcular:")
        print("1. Probabilidad de que no haya clientes en el sistema (p0)")
        print("2. Probabilidad de que haya n clientes en el sistema (pn)")
        print("3. Número promedio de clientes en la cola (Lq)")
        print("4. Número promedio de clientes en el sistema (L)")
        print("5. Tasa efectiva de llegada (λ_eff)")
        print("6. Tiempo promedio en el sistema (W)")
        print("7. Tiempo promedio en la cola (Wq)")
        print("8. Salir")

        opcion = input("Ingrese el número de la opción deseada: \n")

        if opcion == '1':
            calcular_p0(lam, mu, s, k)
        elif opcion == '2':
            n = int(input("Ingrese el número de clientes n: \n"))
            calcular_pn(lam, mu, s, k, n)
        elif opcion == '3':
            calcular_lq(lam, mu, s, k)
        elif opcion == '4':
            calcular_l(lam, mu, s, k)
        elif opcion == '5':
            calcular_lam_eff(lam, mu, s, k)
        elif opcion == '6':
            calcular_w(lam, mu, s)
        elif opcion == '7':
            calcular_wq(lam, mu, s, k)
        elif opcion == '8':
            print("Saliendo del menú.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    menu()