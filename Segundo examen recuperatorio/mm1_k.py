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
# Núcleo M/M/1/K
# --------------------------
def print_detalles(lam, mu, K):
    print_sub("Parámetros básicos")
    print("λ = {:.4f} por hora".format(lam))
    print("μ = {:.4f} por hora".format(mu))
    print("K = {} (capacidad total)".format(K))
    print("ρ = λ/μ = {:.4f} / {:.4f} = {:.4f}".format(lam, mu, lam / mu))

def ingresar_lam_mu_K():
    print_sub("Entrada directa λ, μ y K")
    lam = float(input("λ (llegadas por hora): \n"))
    mu  = float(input("μ (servicios por minuto): \n"))
    K   = int(input("K (capacidad total): \n"))
    return lam, 60.0 / mu, K

def calcular_p0(lam, mu, K):
    rho = lam / mu
    if rho == 1:
        print("p0 = 1 / (K + 1) = 1 / {:.4f}".format(1 / (K + 1)))
        P0 = 1 / (K + 1)
    else:
        print("p0 = (1 - ρ) / (1 - ρ^(K + 1)) = (1 - {:.4f}) / (1 - {:.4f}^({} + 1))".format(rho, rho, K))
        P0 = (1 - rho) / (1 - rho**(K + 1))
    
    print("P0 = {:.4f}".format(P0))
    return P0

def calcular_pn(lam, mu, K, n):
    rho = lam / mu
    P0 = calcular_p0(lam, mu, K)
    print("pn = p0 * ρ^n = {:.4f} * ({:.4f})^{}".format(P0, rho, n))
    Pn = P0 * (rho ** n)
    print("Pn = {:.4f}".format(Pn))
    return Pn

def calcular_l(lam, mu, K):
    rho = lam / mu
    print("L = ρ * (1 - (K + 1) * ρ^K + K * ρ^(K + 1)) / ((1 - ρ) * (1 - ρ^(K + 1)))")
    print("L = {:.4f} * (1 - ({} + 1) * ({:.4f})^{} + {} * ({:.4f})^({} + 1)) / ((1 - {:.4f}) * (1 - ({:.4f})^({} + 1)))".format(
        rho, K, rho, K, K, rho, K, rho, rho, K))
    L = (rho * (1 - (K + 1) * (rho ** K) + K * (rho ** (K + 1)))) / ((1 - rho) * (1 - rho ** (K + 1)))
    print("L = {:.4f}".format(L))
    return L

def calcular_lq(lam, mu, K):
    rho = lam / mu
    L = calcular_l(lam, mu, K)
    Lq = L - rho * (1 - calcular_pn(lam, mu, K, K))
    print("Lq = L - ρ * (1 - Pk) = {:.4f} - {:.4f} * (1 - {:.4f})".format(L, rho, calcular_pn(lam, mu, K, K)))
    print("Lq = {:.4f}".format(Lq))
    return Lq

def calcular_lambda_efectiva(lam, mu, K):
    Pk = calcular_pn(lam, mu, K, K)
    lambda_efectiva = lam * (1 - Pk)
    print("λef = λ * (1 - Pk) = {:.4f} * (1 - {:.4f})".format(lam, Pk))
    print("λef = {:.4f}".format(lambda_efectiva))
    return lambda_efectiva

def calcular_w(lam, mu, K):
    L = calcular_l(lam, mu, K)
    lambda_efectiva = calcular_lambda_efectiva(lam, mu, K)
    W = L / lambda_efectiva
    print("W = L / λef = {:.4f} / {:.4f}".format(L, lambda_efectiva))
    print("W = {:.4f}".format(W))
    return W

def calcular_wq(lam, mu, K):
    Lq = calcular_lq(lam, mu, K)
    lambda_efectiva = calcular_lambda_efectiva(lam, mu, K)
    Wq = Lq / lambda_efectiva
    print("Wq = Lq / λef = {:.4f} / {:.4f}".format(Lq, lambda_efectiva))
    print("Wq = {:.4f}".format(Wq))
    return Wq

def menu():
    print_header("Sistema M/M/1/K")
    lam, mu, K = ingresar_lam_mu_K()

    while True:
        print_header("MENÚ M/M/1/K — Paso a paso")
        print("1) Lambda, Mu, K y p")
        print("2) Probabilidad de que el sistema esté vacío")
        print("3) Probabilidad de que haya n clientes en el sistema")
        print("4) Número promedio de clientes en el sistema")
        print("5) Número promedio de clientes esperando en la cola")
        print("6) Tasa efectiva de llegada: las que sí entran al sistema (no rechazadas)")
        print("7) Tiempo promedio en el sistema (espera + servicio)")
        print("8) Tiempo promedio de espera en la cola")
        print("9) Salir")
        choice = input("Seleccione una opción: \n")

        if choice == "9":
            print("¡Hasta luego!")
            return

        try:
            if choice == "1":
                print_detalles(lam, mu, K)
            elif choice == "2":
                print_sub("Cálculo de P0")
                P0 = calcular_p0(lam, mu, K)
            elif choice == "3":
                n = int(input("Ingrese el valor de n (número de clientes en el sistema): \n"))
                print_sub("Cálculo de Pn")
                Pn = calcular_pn(lam, mu, K, n)
            elif choice == "4":
                print_sub("Cálculo de L")
                L = calcular_l(lam, mu, K)
            elif choice == "5":
                print_sub("Cálculo de Lq")
                Lq = calcular_lq(lam, mu, K)
            elif choice == "6":
                print_sub("Cálculo de λefectiva")
                lambda_efectiva = calcular_lambda_efectiva(lam, mu, K)
            elif choice == "7":
                print_sub("Cálculo de W")
                W = calcular_w(lam, mu, K)
            elif choice == "8":
                print_sub("Cálculo de Wq")
                Wq = calcular_wq(lam, mu, K)
            else:
                print("Opción inválida. Intenta nuevamente.")
        except Exception as e:
            print("\n[ERROR] {}".format(e))

if __name__ == "__main__":
    menu()