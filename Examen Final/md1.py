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
# Núcleo M/D/1
# --------------------------
def print_detalles(lam, mu):
    print_sub("Parámetros básicos")
    rho = lam / mu
    print("λ (Lambda) = {:.4f} / hora".format(lam))
    print("μ (Mu)     = {:.4f} / hora".format(mu))
    print("ρ = λ/μ    = {:.4f} / {:.4f} = {:.4f}".format(lam, mu, rho))
    
    if rho >= 1:
        print("\n[ALERTA] El sistema es inestable (ρ >= 1). La cola crecerá infinitamente.")

def ingresar_datos():
    print_sub("Entrada de datos M/D/1")
    print("NOTA: Asegúrate de usar la misma unidad de tiempo (ej. todo en horas).")
    lam = float(input("λ (Tasa de llegadas, ej. clientes/hora): \n"))
    mu  = float(input("μ (Tasa de servicio, ej. clientes/hora): \n"))
    return lam, mu

def calcular_p0(lam, mu):
    rho = lam / mu
    print("P0 = 1 - ρ")
    print("P0 = 1 - {:.4f}".format(rho))
    P0 = 1 - rho
    print("P0 = {:.4f} (Probabilidad de sistema vacío)".format(P0))
    return P0

def calcular_pn(lam, mu, n):
    # Fórmula basada en la imagen proporcionada por el usuario
    rho = lam / mu
    print("Pn = (1 - ρ) * ρ^n")
    print("Pn = (1 - {:.4f}) * ({:.4f})^{}".format(rho, rho, n))
    Pn = (1 - rho) * (rho ** n)
    print("Pn = {:.4f}".format(Pn))
    return Pn

def calcular_l(lam, mu):
    rho = lam / mu
    # Fórmula: L = ρ + (ρ² / 2(1-ρ))
    numerador_frac = rho ** 2
    denominador_frac = 2 * (1 - rho)
    fraccion = numerador_frac / denominador_frac
    
    print("L = ρ + [ρ² / 2(1 - ρ)]")
    print("L = {:.4f} + [{:.4f}² / 2(1 - {:.4f})]".format(rho, rho, rho))
    print("L = {:.4f} + [{:.4f} / {:.4f}]".format(rho, numerador_frac, denominador_frac))
    print("L = {:.4f} + {:.4f}".format(rho, fraccion))
    
    L = rho + fraccion
    print("L = {:.4f} clientes en el sistema".format(L))
    return L

def calcular_lq(lam, mu):
    rho = lam / mu
    # Fórmula: Lq = ρ² / 2(1 - ρ)
    numerador = rho ** 2
    denominador = 2 * (1 - rho)
    
    print("Lq = ρ² / 2(1 - ρ)")
    print("Lq = {:.4f}² / 2(1 - {:.4f})".format(rho, rho))
    print("Lq = {:.4f} / {:.4f}".format(numerador, denominador))
    
    Lq = numerador / denominador
    print("Lq = {:.4f} clientes en cola".format(Lq))
    return Lq

def calcular_w(lam, mu):
    rho = lam / mu
    # Fórmula: W = (1/μ) + [ρ / 2μ(1 - ρ)]
    inv_mu = 1 / mu
    numerador_frac = rho
    denominador_frac = 2 * mu * (1 - rho)
    fraccion = numerador_frac / denominador_frac

    print("W = (1/μ) + [ρ / 2μ(1 - ρ)]")
    print("W = (1/{:.4f}) + [{:.4f} / 2*{:.4f}*(1 - {:.4f})]".format(mu, rho, mu, rho))
    print("W = {:.4f} + [{:.4f} / {:.4f}]".format(inv_mu, numerador_frac, denominador_frac))
    
    W = inv_mu + fraccion
    print("W = {:.4f} horas".format(W))
    return W

def calcular_wq(lam, mu):
    rho = lam / mu
    # Fórmula: Wq = ρ / 2μ(1 - ρ)
    numerador = rho
    denominador = 2 * mu * (1 - rho)
    
    print("Wq = ρ / 2μ(1 - ρ)")
    print("Wq = {:.4f} / (2 * {:.4f} * (1 - {:.4f}))".format(rho, mu, rho))
    print("Wq = {:.4f} / {:.4f}".format(numerador, denominador))
    
    Wq = numerador / denominador
    print("Wq = {:.4f} horas".format(Wq))
    return Wq

def menu():
    print_header("Sistema M/D/1 (Servicio Constante)")
    lam, mu = ingresar_datos()

    while True:
        print_header("MENÚ M/D/1 — Paso a paso")
        print("1) Mostrar parámetros (λ, μ, ρ)")
        print("2) Probabilidad de que el sistema esté vacío (P0)")
        print("3) Probabilidad de n clientes (Pn)")
        print("4) Número promedio de clientes en SISTEMA (L)")
        print("5) Número promedio de clientes en COLA (Lq)")
        print("6) Tiempo promedio en el SISTEMA (W)")
        print("7) Tiempo promedio en COLA (Wq)")
        print("8) Cambiar datos de entrada")
        print("9) Salir")
        choice = input("Seleccione una opción: \n")

        if choice == "9":
            print("¡Hasta luego!")
            return
        
        if choice == "8":
            lam, mu = ingresar_datos()
            continue

        try:
            # Verificación de estabilidad
            if lam >= mu and choice != "1":
                print("\n[ERROR] El sistema es inestable (λ >= μ). Las fórmulas no convergen.")
                continue

            if choice == "1":
                print_detalles(lam, mu)
            elif choice == "2":
                print_sub("Cálculo de P0")
                calcular_p0(lam, mu)
            elif choice == "3":
                n = int(input("Ingrese el valor de n (número de clientes): \n"))
                print_sub("Cálculo de Pn")
                calcular_pn(lam, mu, n)
            elif choice == "4":
                print_sub("Cálculo de L")
                calcular_l(lam, mu)
            elif choice == "5":
                print_sub("Cálculo de Lq")
                calcular_lq(lam, mu)
            elif choice == "6":
                print_sub("Cálculo de W")
                calcular_w(lam, mu)
            elif choice == "7":
                print_sub("Cálculo de Wq")
                calcular_wq(lam, mu)
            else:
                print("Opción inválida. Intenta nuevamente.")
        except Exception as e:
            print("\n[ERROR] Ocurrió un problema: {}".format(e))

if __name__ == "__main__":
    menu()