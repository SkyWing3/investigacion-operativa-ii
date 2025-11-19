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
# Núcleo M/M/1
# --------------------------

def print_detalles(lam, mu):
    print_sub("Parámetros básicos")
    print("λ = {:.4f} por hora".format(lam))
    print("μ = {:.4f} por hora".format(mu))
    print("ρ = λ/μ = {:.4f} / {:.4f} = {:.4f}".format(lam, mu, lam / mu))

def ingresar_lam_mu():
    print_sub("Entrada directa λ y μ")
    lam = float(input("λ (llegadas por hora): \n"))
    mu  = float(input("μ (servicios por minuto): \n"))
    return lam, 60.0 / mu

def calcular_p0(lam, mu):
    rho = lam / mu
    print("p0 = 1 - ρ = 1 - {:.4f}".format(rho))
    P0 = 1 - rho
    return P0

def calcular_pn(lam, mu, n):
    rho = lam / mu
    P0 = calcular_p0(lam, mu)
    print("pn = p0 * ρ^n = {:.4f} * ({:.4f})^{}".format(P0, rho, n))
    Pn = P0 * (rho ** n)
    print("Pn = {:.4f}".format(Pn))
    return Pn

def calcular_l(lam, mu):
    rho = lam / mu
    print("L = ρ / (1 - ρ) = {:.4f} / (1 - {:.4f})".format(rho, rho))
    L = rho / (1 - rho)
    print("L = {:.4f}".format(L))
    return L

def calcular_lq(lam, mu):
    rho = lam / mu
    print("Lq = ρ^2 / (1 - ρ) = ({:.4f})^2 / (1 - {:.4f})".format(rho, rho))
    Lq = (rho ** 2) / (1 - rho)
    print("Lq = {:.4f}".format(Lq))
    return Lq

def calcular_w(lam, mu):
    print("W = 1 / (μ - λ) = 1 / ({:.4f} - {:.4f})".format(mu, lam))
    W = 1 / (mu - lam)
    print("W = {:.4f}".format(W))
    return W

def calcular_wq(lam, mu):
    rho = lam / mu
    print("Wq = ρ / (μ - λ) = {:.4f} / ({:.4f} - {:.4f})".format(rho, mu, lam))
    Wq = rho / (mu - lam)
    print("Wq = {:.4f}".format(Wq))
    return Wq

def calcular_p_tiempo_sistema(lam, mu, t):
    rho = lam / mu
    print("P(T > t) = e^(- (μ - λ) * t) = e^(- ({:.4f} - {:.4f}) * {:.4f})".format(mu, lam, t))
    P = 2.71828 ** (-(mu - lam) * t)
    print("P(T > {:.4f}) = {:.4f}".format(t, P))
    return P

def calcular_p_tiempo_cola(lam, mu, t):
    rho = lam / mu
    print("P(Wq > t) = ρ * e^(- (μ - λ) * t) = {:.4f} * e^(- ({:.4f} - {:.4f}) * {:.4f})".format(rho, mu, lam, t))
    P = rho * (2.71828 ** (-(mu - lam) * t))
    print("P(Wq > {:.4f}) = {:.4f}".format(t, P))
    return P

def menu():
    print_header("Sistema M/M/1")
    lam, mu = ingresar_lam_mu()
    print_detalles(lam, mu)

    while True:
        print_sub("Menú de opciones")
        print("1. Probabilidad de que el sistema esté vacío")
        print("2. Probabilidad de que haya n clientes en el sistema")
        print("3. Número promedio de clientes en el sistema")
        print("4. Número promedio de clientes esperando en la cola")
        print("5. Tiempo promedio en el sistema (espera + servicio)")
        print("6. Tiempo promedio de espera en la cola")
        print("7. Probabilidad de que un cliente pase más de t tiempo en el sistema")
        print("8. Probabilidad de esperar más de t en la cola")
        print("0. Salir")

        choice = input("Seleccione una opción: \n")

        if choice == "0":
            print("Saliendo del programa.")
            break

        try:
            if choice == "1":
                print_sub("Cálculo de P0")
                P0 = calcular_p0(lam, mu)
                print("P0 = {:.4f}".format(P0))
            elif choice == "2":
                n = int(input("Ingrese el valor de n (número de clientes en el sistema): \n"))
                print_sub("Cálculo de Pn")
                Pn = calcular_pn(lam, mu, n)
                print("Pn = {:.4f}".format(Pn))
            elif choice == "3":
                print_sub("Cálculo de L")
                L = calcular_l(lam, mu)
                print("L = {:.4f} clientes".format(L))
            elif choice == "4":
                print_sub("Cálculo de Lq")
                Lq = calcular_lq(lam, mu)
                print("Lq = {:.4f} clientes".format(Lq))
            elif choice == "5":
                print_sub("Cálculo de W")
                W = calcular_w(lam, mu)
                print("W = {:.4f} horas".format(W))
            elif choice == "6":
                print_sub("Cálculo de Wq")
                Wq = calcular_wq(lam, mu)
                print("Wq = {:.4f} horas".format(Wq))
            elif choice == "7":
                t = float(input("Ingrese el valor de t (tiempo en horas): \n"))
                print_sub("Cálculo de P(T > t)")
                P = calcular_p_tiempo_sistema(lam, mu, t)
                print("P(T > {:.4f}) = {:.4f}".format(t, P))
            elif choice == "8":
                t = float(input("Ingrese el valor de t (tiempo en horas): \n"))
                print_sub("Cálculo de P(Wq > t)")
                P = calcular_p_tiempo_cola(lam, mu, t)
                print("P(Wq > {:.4f}) = {:.4f}".format(t, P))
            else:
                print("Opción inválida. Intenta nuevamente.")
        except Exception as e:
            print("Error durante el cálculo: {}".format(e))

if __name__ == "__main__":
    menu()