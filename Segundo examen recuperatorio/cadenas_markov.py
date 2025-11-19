"""
markov_ultra_detallado.py

Script educativo para Cadenas de Markov.
Características:
1. SIN librerías externas.
2. SIN f-strings (solo .format).
3. NIVEL DE DETALLE MÁXIMO:
   - Muestra cómo se arman las ecuaciones teóricas.
   - Muestra la matriz aumentada inicial.
   - Muestra CADA operación de fila en Gauss (pivoteo, eliminación).
   - Muestra la matriz resultante tras cada paso de eliminación.
   - Muestra el despeje explícito en la sustitución hacia atrás.
"""

import math

# ==========================================
# Herramientas de Impresión y Matrices
# ==========================================

def copiar_matriz(M):
    filas = len(M)
    columnas = len(M[0])
    copia = []
    for i in range(filas):
        fila_nueva = []
        for j in range(columnas):
            fila_nueva.append(M[i][j])
        copia.append(fila_nueva)
    return copia

def multiplicar_matrices(A, B):
    m = len(A)
    n = len(A[0])
    p = len(B[0])
    R = [[0.0 for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            suma = 0.0
            for k in range(n):
                suma += A[i][k] * B[k][j]
            R[i][j] = suma
    return R

def imprimir_matriz_aumentada(A, b, titulo="Matriz Aumentada"):
    filas = len(A)
    print("\n    --- {} ---".format(titulo))
    for i in range(filas):
        fila_str = "  ".join(["{:8.4f}".format(x) for x in A[i]])
        print("    | {} | {:8.4f} |".format(fila_str, b[i]))
    print("")

# ==========================================
# ELIMINACIÓN DE GAUSS (Paso a Paso)
# ==========================================

def resolver_gauss_super_detallado(A, b):
    """
    Resuelve Ax = b imprimiendo CADA operación aritmética.
    """
    n = len(A)
    M = copiar_matriz(A)
    v = b[:]

    print("\n" + "#"*60)
    print("INICIO PROCEDIMIENTO GAUSS (Eliminación + Sustitución)")
    print("#"*60)
    imprimir_matriz_aumentada(M, v, "Sistema Inicial [A|b]")

    # --- FASE 1: Eliminación hacia adelante ---
    for k in range(n):
        print("\n>>> Paso {}: Pivote en columna {}".format(k+1, k))
        
        # 1. Buscar pivote
        max_fila = k
        max_valor = abs(M[k][k])
        for i in range(k + 1, n):
            if abs(M[i][k]) > max_valor:
                max_valor = abs(M[i][k])
                max_fila = i

        # 2. Intercambiar filas si es necesario
        if max_fila != k:
            print("    ! Intercambiando Fila {} <-> Fila {} (Mejor pivote encontrado)".format(k, max_fila))
            M[k], M[max_fila] = M[max_fila], M[k]
            v[k], v[max_fila] = v[max_fila], v[k]
            imprimir_matriz_aumentada(M, v, "Tras intercambio")
        else:
            print("    * El pivote actual ({:.4f}) en M[{}][{}] es adecuado.".format(M[k][k], k, k))

        pivote = M[k][k]
        if abs(pivote) < 1e-12:
            print("    ! ADVERTENCIA: Pivote cercano a 0. El sistema puede ser singular.")
            continue

        # 3. Hacer ceros debajo del pivote
        print("    * Eliminando entradas debajo del pivote...")
        cambios = False
        for i in range(k + 1, n):
            if abs(M[i][k]) > 1e-12:
                factor = M[i][k] / pivote
                print("      -> Fila {} = Fila {} - ({:.4f}) * Fila {}".format(i, i, factor, k))
                
                # Operación fila
                for j in range(k, n):
                    M[i][j] = M[i][j] - factor * M[k][j]
                v[i] = v[i] - factor * v[k]
                cambios = True
            else:
                print("      -> Fila {} ya tiene un 0 en la columna {}. Se omite.".format(i, k))

        if cambios:
            imprimir_matriz_aumentada(M, v, "Matriz tras eliminar columna {}".format(k))

    # --- FASE 2: Sustitución hacia atrás ---
    print("\n>>> FASE 2: Sustitución hacia atrás")
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        print("\n    Despejando variable x_{}:".format(i))
        
        # Ecuación: M[i][i]*x_i + sum(M[i][j]*x_j) = v[i]
        # x_i = (v[i] - suma) / M[i][i]
        
        suma_conocida = 0.0
        texto_suma = []
        
        for j in range(i + 1, n):
            val = M[i][j] * x[j]
            suma_conocida += val
            if abs(val) > 0:
                texto_suma.append("({:.4f} * {:.4f})".format(M[i][j], x[j]))
        
        termino_resta = " - ".join(texto_suma) if texto_suma else "0"
        
        if abs(M[i][i]) < 1e-12:
            print("      Error: Coeficiente diagonal es 0. No se puede despejar.")
            x[i] = 0.0
        else:
            resultado = (v[i] - suma_conocida) / M[i][i]
            print("      Ecuación: {:.4f} * x_{} + {} = {:.4f}".format(M[i][i], i, suma_conocida, v[i]))
            print("      Despeje:  x_{} = ({:.4f} - [suma_conocida]) / {:.4f}".format(i, v[i], M[i][i]))
            print("      x_{} = {:.4f}".format(i, resultado))
            x[i] = resultado

    print("\n" + "#"*60)
    print("FIN GAUSS. Solución encontrada.")
    print("#"*60 + "\n")
    return x

# ==========================================
# 1. Potencia (Chapman-Kolmogorov)
# ==========================================

def proc_potencia(P, n):
    print("\n" + "="*80)
    print("PROCEDIMIENTO DETALLADO: CHAPMAN-KOLMOGOROV (P^n)")
    print("="*80)
    
    if n == 0:
        print("Paso 1: n=0. La matriz de transición en 0 pasos es la Identidad.")
        return [[1.0 if i==j else 0.0 for j in range(len(P))] for i in range(len(P))]

    R = copiar_matriz(P)
    print("Matriz inicial P (P^1):")
    for fila in R: print("  {}".format(fila))

    for k in range(2, n + 1):
        print("\n--- Paso {}: Calculando P^{} = P^{} * P ---".format(k-1, k, k-1))
        print("Realizando multiplicación matricial estándar...")
        R = multiplicar_matrices(R, P)
        print("Resultado P^{}:".format(k))
        for fila in R:
            print("  [" + "  ".join(["{:7.4f}".format(x) for x in fila]) + "]")
    
    return R

# ==========================================
# 2. Estado Estable
# ==========================================

def proc_estado_estable(P):
    print("\n" + "="*80)
    print("PROCEDIMIENTO DETALLADO: DISTRIBUCIÓN ESTACIONARIA (π)")
    print("Fórmula: π_j = Σ (π_i * P_ij)  |  Normalización: Σ π_i = 1")
    print("="*80)

    n = len(P)
    A = []
    b = []

    print("\n[1] Planteamiento de Ecuaciones (Sistema Homogéneo Transformado):")
    print("Nota: De la ecuación π = πP, pasamos a π(P - I) = 0.")
    print("Nota: Reemplazamos una ecuación redundante por Σ π = 1.")

    # Usamos n-1 ecuaciones del sistema homogéneo
    for j in range(n - 1):
        print("\n  -> Analizando Columna j={} (para variable π_{}):".format(j, j))
        fila = []
        terms_str = []
        
        for i in range(n):
            # Coeficiente para pi_i en la ecuación j
            coef = P[i][j]
            if i == j:
                # Restamos 1 porque pasamos pi_j al otro lado (P_jj - 1)
                coef -= 1.0
                terms_str.append("({:.2f}-1)π_{}".format(P[i][j], i))
            else:
                terms_str.append("{:.2f}π_{}".format(P[i][j], i))
            fila.append(coef)
        
        print("     Ecuación cruda: 0 = " + " + ".join(terms_str))
        A.append(fila)
        b.append(0.0)

    # Ecuación de normalización
    print("\n  -> Ecuación de Normalización (Reemplaza a la última columna):")
    print("     1 = " + " + ".join(["π_{}".format(k) for k in range(n)]))
    A.append([1.0] * n)
    b.append(1.0)

    print("\n[2] Enviando sistema a Gauss...")
    return resolver_gauss_super_detallado(A, b)

# ==========================================
# 3. Tiempos de Recurrencia
# ==========================================

def proc_recurrencia(P):
    print("\n" + "="*80)
    print("PROCEDIMIENTO DETALLADO: TIEMPOS DE RECURRENCIA (μ_ii)")
    print("Fórmula: μ_ii = 1 / π_i")
    print("="*80)

    # Llamamos a la función detallada anterior
    pi = proc_estado_estable(P)
    
    print("\n[3] Cálculo final de Tiempos de Recurrencia:")
    tiempos = []
    print("    Se aplica la inversión del valor de probabilidad:")
    for i, val in enumerate(pi):
        if val > 1e-9:
            t = 1.0 / val
            print("    Estado {}: π_{} = {:.6f}  =>  μ_{}{} = 1 / {:.6f} = {:.4f}".format(i, i, val, i, i, val, t))
            tiempos.append(t)
        else:
            print("    Estado {}: π_{} = 0.0000  =>  μ_{}{} = Infinito (Estado Transitorio)".format(i, i, i, i))
            tiempos.append(float('inf'))
    return tiempos

# ==========================================
# 4. Tiempos de Primera Pasada
# ==========================================

def proc_primera_pasada(P):
    print("\n" + "="*80)
    print("PROCEDIMIENTO DETALLADO: TIEMPOS DE PRIMERA PASADA (μ_ij)")
    print("Fórmula: μ_ij = 1 + Σ (P_ik * μ_kj) para k ≠ j")
    print("Definición: μ_jj = 0")
    print("="*80)

    n = len(P)
    M = [[0.0] * n for _ in range(n)]

    for j in range(n):
        print("\n" + "*"*60)
        print("BLOQUE: Calculando columna destino j = {} (Tiempos para llegar a {})".format(j, j))
        print("*"*60)
        
        A = []
        b = []
        print("  Planteando sistema lineal para las variables μ_ij (donde j está fijo):")

        for i in range(n):
            fila = [0.0] * n
            
            if i == j:
                print("  [Fila i={}] Destino alcanzado. Definición: μ_{}{} = 0.".format(i, i, j))
                fila[j] = 1.0
                b.append(0.0)
            else:
                # Ecuación: u_ij = 1 + sum(P_ik * u_kj)
                # Despeje: u_ij - sum(P_ik * u_kj) = 1
                print("  [Fila i={}] Ecuación de paso: μ_{}{} = 1 + Σ P_{}k * μ_k{}".format(i, i, j, i, j))
                
                terms = []
                for k in range(n):
                    if k == j: 
                        # u_jj es 0, desaparece
                        fila[k] = 0.0
                    elif k == i:
                        # u_ij aparece en izquierda (1) y derecha (P_ii). 
                        # Izquierda - Derecha = 1 - P_ii
                        fila[k] = 1.0 - P[i][k]
                        terms.append("(1 - {:.2f})μ_{}{}".format(P[i][k], k, j))
                    else:
                        # u_kj aparece derecha como P_ik. Pasa restando.
                        fila[k] = -P[i][k]
                        terms.append("-{:.2f}μ_{}{}".format(P[i][k], k, j))
                
                b.append(1.0)
                # print("    -> Algebra lineal: " + " + ".join(terms) + " = 1")
                
            A.append(fila)
        
        # Resolver
        solucion_columna = resolver_gauss_super_detallado(A, b)
        for r in range(n):
            M[r][j] = solucion_columna[r]

    return M

# ==========================================
# 5. Absorción
# ==========================================

def proc_absorcion(P):
    print("\n" + "="*80)
    print("PROCEDIMIENTO DETALLADO: PROBABILIDAD DE ABSORCIÓN (f_ik)")
    print("Fórmula: f_ik = Σ P_ij * f_jk")
    print("="*80)

    try:
        k_str = input("Ingrese el estado destino k (Absorbente) [0-{}]: ".format(len(P)-1))
        k = int(k_str)
    except ValueError:
        print("Entrada inválida.")
        return

    if k < 0 or k >= len(P):
        print("Estado fuera de rango.")
        return

    n = len(P)
    A = []
    b = []

    print("\n[1] Análisis de Estados para destino k={}:".format(k))
    for i in range(n):
        fila = [0.0] * n
        
        # Caso A: Es el destino
        if i == k:
            print("  i={}: Es el estado destino. f_{}{} = 1.".format(i, i, k))
            fila[i] = 1.0
            val_b = 1.0
            
        # Caso B: Es otro absorbente
        elif abs(P[i][i] - 1.0) < 1e-9:
            print("  i={}: Es absorbente trampa (≠k). f_{}{} = 0.".format(i, i, k))
            fila[i] = 1.0
            val_b = 0.0
            
        # Caso C: Transitorio
        else:
            print("  i={}: Transitorio. f_{}{} = Σ P_{}j * f_j{}".format(i, i, k, i, k))
            # Despeje: f_ik - sum(P_ij * f_jk) = 0
            # Variables x_j = f_jk
            # x_i - sum P_ij x_j = 0
            
            for j in range(n):
                if i == j:
                    fila[j] = 1.0 - P[i][j]
                else:
                    fila[j] = -P[i][j]
            val_b = 0.0
        
        A.append(fila)
        b.append(val_b)

    print("\n[2] Resolviendo sistema para probabilidades f_ik...")
    res = resolver_gauss_super_detallado(A, b)
    
    print("\n--- RESULTADO FINAL f_ik ---")
    for i, val in enumerate(res):
        print("Probabilidad de ir de {} a {}: {:.4f}".format(i, k, val))

# ==========================================
# Menú Principal
# ==========================================

def leer_matriz():
    print("\n--- Entrada de Matriz P ---")
    try:
        n = int(input("Dimensión n: "))
        P = []
        print("Ingrese filas (números con espacio):")
        for i in range(n):
            while True:
                raw = input("Fila {}: ".format(i)).split()
                try:
                    fila = [float(x) for x in raw]
                    if len(fila) == n:
                        P.append(fila)
                        break
                    print("Error: longitud incorrecta.")
                except:
                    print("Error numérico.")
        return P
    except:
        return None

def menu():
    P = None
    while True:
        print("\n" + "="*40)
        print("   CADENAS DE MARKOV (ULTRA DETALLADO)")
        print("="*40)
        print("1. Cargar P")
        if P:
            print("2. Potencia P^n")
            print("3. Estado Estable (π)")
            print("4. Recurrencia (μ_ii)")
            print("5. Primera Pasada (μ_ij)")
            print("6. Absorción (f_ik)")
        print("0. Salir")
        
        op = input("Opción: ")
        if op == "1": P = leer_matriz()
        elif op == "0": break
        elif P:
            if op == "2": 
                try:
                    n = int(input("n: "))
                    proc_potencia(P, n)
                except: pass
            elif op == "3": proc_estado_estable(P)
            elif op == "4": proc_recurrencia(P)
            elif op == "5": 
                M = proc_primera_pasada(P)
                print("\nMATRIZ FINAL μ_ij:")
                for fila in M: print(["{:.2f}".format(x) for x in fila])
            elif op == "6": proc_absorcion(P)

if __name__ == "__main__":
    menu()