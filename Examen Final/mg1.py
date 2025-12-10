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
# Núcleo M/G/1
# --------------------------
def print_detalles(lam, mu, sigma):
    print_sub("Parámetros básicos")
    rho = lam / mu
    print("λ (Lambda) = {:.4f} / hora".format(lam))
    print("μ (Mu)     = {:.4f} / hora".format(mu))
    print("σ (Sigma)  = {:.4f} horas (Desviación estándar)".format(sigma))
    print("ρ = λ/μ = {:.4f} / {:.4f} = {:.4f}".format(lam, mu, rho))
    
    if rho >= 1:
        print("\n[ALERTA] El sistema es inestable (ρ >= 1). La cola crecerá infinitamente.")

def ingresar_datos():
    print_sub("Entrada de datos M/G/1")
    print("NOTA: Asegúrate de usar la misma unidad de tiempo (ej. todo en horas).")
    lam = float(input("λ (Tasa de llegadas, ej. clientes/hora): \n"))
    mu  = float(input("μ (Tasa de servicio, ej. clientes/hora): \n"))
    sigma = float(input("σ (Desviación estándar del servicio en horas): \n"))
    return lam, mu, sigma

def calcular_p0(lam, mu):
    rho = lam / mu
    print("P0 = 1 - ρ")
    print("P0 = 1 - {:.4f}".format(rho))
    P0 = 1 - rho
    print("P0 = {:.4f} (Probabilidad de sistema vacío)".format(P0))
    return P0

def calcular_pn(lam, mu, n):
    # Nota: Según tu formulario, esta es una aproximación geométrica
    rho = lam / mu
    print("Pn ≈ (1 - ρ) * ρ^n")
    print("Pn ≈ (1 - {:.4f}) * ({:.4f})^{}".format(rho, rho, n))
    Pn = (1 - rho) * (rho ** n)
    print("Pn ≈ {:.4f}".format(Pn))
    return Pn

def calcular_lq(lam, mu, sigma):
    # Fórmula de Pollaczek-Khinchine (según tu imagen)
    rho = lam / mu
    numerador = (lam**2) * (sigma**2) + (rho**2)
    denominador = 2 * (1 - rho)
    
    print("Lq = (λ²σ² + ρ²) / 2(1 - ρ)")
    print("Lq = ({:.4f}² * {:.4f}² + {:.4f}²) / 2(1 - {:.4f})".format(lam, sigma, rho, rho))
    print("Lq = ({:.4f} + {:.4f}) / {:.4f}".format((lam**2)*(sigma**2), rho**2, denominador))
    
    Lq = numerador / denominador
    print("Lq = {:.4f} clientes en cola".format(Lq))
    return Lq

def calcular_l(lam, mu, sigma):
    rho = lam / mu
    # Para calcular L necesitamos Lq primero
    print("Calculando Lq para obtener L...")
    # Calculamos Lq internamente sin imprimir todo el detalle de nuevo si no se desea, 
    # pero para el paso a paso mostramos la suma final.
    numerador = (lam**2) * (sigma**2) + (rho**2)
    denominador = 2 * (1 - rho)
    Lq_val = numerador / denominador
    
    print("L = ρ + Lq")
    print("L = {:.4f} + {:.4f}".format(rho, Lq_val))
    
    L = rho + Lq_val
    print("L = {:.4f} clientes en el sistema".format(L))
    return L

def calcular_wq(lam, mu, sigma):
    # Necesitamos Lq primero
    print("Calculando Lq para obtener Wq...")
    rho = lam / mu
    numerador = (lam**2) * (sigma**2) + (rho**2)
    denominador = 2 * (1 - rho)
    Lq_val = numerador / denominador
    
    print("Wq = Lq / λ")
    print("Wq = {:.4f} / {:.4f}".format(Lq_val, lam))
    
    Wq = Lq_val / lam
    print("Wq = {:.4f} horas".format(Wq))
    return Wq

def calcular_w(lam, mu, sigma):
    # Necesitamos Wq primero
    print("Calculando Wq para obtener W...")
    rho = lam / mu
    numerador = (lam**2) * (sigma**2) + (rho**2)
    denominador = 2 * (1 - rho)
    Lq_val = numerador / denominador
    Wq_val = Lq_val / lam
    
    print("W = Wq + 1/μ")
    print("W = {:.4f} + 1/{:.4f}".format(Wq_val, mu))
    
    W = Wq_val + (1 / mu)
    print("W = {:.4f} horas".format(W))
    return W

def menu():
    print_header("Sistema M/G/1 (Pollaczek-Khinchine)")
    lam, mu, sigma = ingresar_datos()

    while True:
        print_header("MENÚ M/G/1 — Paso a paso")
        print("1) Mostrar parámetros (λ, μ, σ, ρ)")
        print("2) Probabilidad de que el sistema esté vacío (P0)")
        print("3) Probabilidad de n clientes (Pn - Aprox)")
        print("4) Número promedio de clientes en COLA (Lq)")
        print("5) Número promedio de clientes en SISTEMA (L)")
        print("6) Tiempo promedio de espera en COLA (Wq)")
        print("7) Tiempo promedio en el SISTEMA (W)")
        print("8) Cambiar datos de entrada")
        print("9) Salir")
        choice = input("Seleccione una opción: \n")

        if choice == "9":
            print("¡Hasta luego!")
            return
        
        if choice == "8":
            lam, mu, sigma = ingresar_datos()
            continue

        try:
            # Verificación de estabilidad básica antes de calcular
            if lam >= mu and choice != "1":
                print("\n[ERROR] El sistema es inestable (λ >= μ). Las fórmulas no convergen.")
                continue

            if choice == "1":
                print_detalles(lam, mu, sigma)
            elif choice == "2":
                print_sub("Cálculo de P0")
                calcular_p0(lam, mu)
            elif choice == "3":
                n = int(input("Ingrese el valor de n (número de clientes): \n"))
                print_sub("Cálculo de Pn")
                calcular_pn(lam, mu, n)
            elif choice == "4":
                print_sub("Cálculo de Lq (Fórmula Pollaczek-Khinchine)")
                calcular_lq(lam, mu, sigma)
            elif choice == "5":
                print_sub("Cálculo de L")
                calcular_l(lam, mu, sigma)
            elif choice == "6":
                print_sub("Cálculo de Wq")
                calcular_wq(lam, mu, sigma)
            elif choice == "7":
                print_sub("Cálculo de W")
                calcular_w(lam, mu, sigma)
            else:
                print("Opción inválida. Intenta nuevamente.")
        except Exception as e:
            print("\n[ERROR] Ocurrió un problema: {}".format(e))

if __name__ == "__main__":
    menu()