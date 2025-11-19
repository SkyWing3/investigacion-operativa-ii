import sys

# --------------------------
# Utilidades de Formato
# --------------------------

def print_header(t):
    print("\n" + "=" * 76)
    print(t)
    print("=" * 76)

def print_sub(t):
    print("\n--- " + t + " ---")

def print_matriz(M, nombre="Matriz"):
    print(f"{nombre}:")
    for fila in M:
        print("  " + " ".join([f"{x:.4f}" for x in fila]))

# --------------------------
# Motor Matemático (Sin Numpy)
# --------------------------

def crear_matriz_zeros(filas, cols):
    return [[0.0] * cols for _ in range(filas)]

def crear_identidad(n):
    M = crear_matriz_zeros(n, n)
    for i in range(n):
        M[i][i] = 1.0
    return M

def multiplicar_matrices(A, B):
    # A es mxn, B es nxp -> Resultado mxp
    filas_a = len(A)
    cols_a = len(A[0])
    filas_b = len(B)
    cols_b = len(B[0])
    
    if cols_a != filas_b:
        print("[ERROR] Dimensiones incompatibles para multiplicación.")
        return None
        
    C = crear_matriz_zeros(filas_a, cols_b)
    for i in range(filas_a):
        for j in range(cols_b):
            for k in range(cols_a):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matriz_potencia(A, n):
    res = crear_identidad(len(A))
    base = A
    for _ in range(n):
        res = multiplicar_matrices(res, base)
    return res

def transponer_matriz(M):
    filas = len(M)
    cols = len(M[0])
    T = crear_matriz_zeros(cols, filas)
    for i in range(filas):
        for j in range(cols):
            T[j][i] = M[i][j]
    return T

def resolver_sistema_lineal(A, b):
    """
    Resuelve Ax = b usando eliminación de Gauss-Jordan.
    A es matriz nxn, b es vector lista tamaño n.
    Retorna vector solución x.
    """
    n = len(A)
    # Crear matriz aumentada [A | b]
    M = [fila[:] + [val] for fila, val in zip(A, b)]

    for i in range(n):
        # 1. Pivoteo parcial (buscar el mayor valor en la columna actual)
        pivot_row = i
        for k in range(i + 1, n):
            if abs(M[k][i]) > abs(M[pivot_row][i]):
                pivot_row = k
        
        # Intercambiar filas
        M[i], M[pivot_row] = M[pivot_row], M[i]
        
        pivot = M[i][i]
        if abs(pivot) < 1e-10:
            # Sistema singular o infinitas soluciones
            return None 
        
        # 2. Normalizar la fila del pivote (hacer que el pivote sea 1)
        for j in range(i, n + 1):
            M[i][j] /= pivot
        
        # 3. Eliminación (hacer ceros arriba y abajo del pivote)
        for k in range(n):
            if k != i:
                factor = M[k][i]
                for j in range(i, n + 1):
                    M[k][j] -= factor * M[i][j]
    
    # Extraer solución (la última columna)
    solucion = [fila[-1] for fila in M]
    return solucion

def obtener_submatriz(P, filas_idx, cols_idx):
    # Extrae una submatriz basada en índices de filas y columnas
    res = []
    for r in filas_idx:
        fila_nueva = []
        for c in cols_idx:
            fila_nueva.append(P[r][c])
        res.append(fila_nueva)
    return res

# --------------------------
# Lógica de Markov
# --------------------------

def ingresar_matriz():
    print_sub("Configuración Manual de P")
    try:
        dim = int(input("Ingrese dimensión de la matriz (ej. 3 para 3x3): \n"))
        print(f"Ingrese las probabilidades fila por fila, separadas por espacio.")
        
        matriz = []
        for i in range(dim):
            entrada = input(f"Fila {i}: ")
            fila = list(map(float, entrada.split()))
            if len(fila) != dim:
                print(f"[ERROR] Se esperaban {dim} números.")
                return None
            if abs(sum(fila) - 1.0) > 0.01:
                print(f"[ADVERTENCIA] La fila suma {sum(fila)}, debería ser 1.0")
            matriz.append(fila)
        return matriz
    except ValueError:
        print("[ERROR] Entrada no válida.")
        return None

def calcular_chapman_kolmogorov(P):
    print_sub("Ecuaciones Chapman-Kolmogorov")
    print("P(n) = P^n")
    try:
        n = int(input("Ingrese número de pasos (n): \n"))
        Pn = matriz_potencia(P, n)
        print(f"\nMatriz de Transición a {n} pasos:")
        print_matriz(Pn)
        return Pn
    except ValueError:
        print("[ERROR] Debe ingresar un número entero.")

def calcular_estado_estable(P):
    print_sub("Probabilidades de Estado Estable (π)")
    # Se resuelve: π * P = π  =>  π * (P - I) = 0
    # Transponiendo para resolver Ax=b convencional: (P^T - I) * π^T = 0
    # Con restricción suma(π) = 1
    
    n = len(P)
    PT = transponer_matriz(P)
    I = crear_identidad(n)
    
    # A = PT - I
    A = crear_matriz_zeros(n, n)
    for i in range(n):
        for j in range(n):
            A[i][j] = PT[i][j] - I[i][j]
            
    # Reemplazar la última ecuación con la restricción de suma = 1
    # Esto asegura que no obtengamos la solución trivial (todos ceros)
    for j in range(n):
        A[n-1][j] = 1.0
        
    b = [0.0] * n
    b[n-1] = 1.0 # La suma debe dar 1
    
    pi = resolver_sistema_lineal(A, b)
    
    if pi:
        print("Solución del sistema:")
        for i, valor in enumerate(pi):
            print(f"π{i} = {valor:.4f}")
        return pi
    else:
        print("[ERROR] El sistema no tiene solución única (posible matriz reducible).")
        return None

def calcular_tiempos_recurrencia(P):
    print_sub("Tiempos de Recurrencia")
    print("μ_ii = 1 / π_i")
    
    # Reutilizamos la función de estado estable
    pi = calcular_estado_estable(P)
    
    if pi:
        print("\nResultados Tiempos de Recurrencia:")
        for i, p in enumerate(pi):
            if p > 1e-6:
                mu = 1.0 / p
                print(f"μ_{i}{i} = 1 / {p:.4f} = {mu:.4f} pasos")
            else:
                print(f"μ_{i}{i} = Infinito (estado transitorio)")

def calcular_primera_pasada(P):
    print_sub("Tiempos de Primera Pasada (μ_ij)")
    print("Ecuación: (I - Q) * μ = 1")
    
    n = len(P)
    # Matriz resultado llena de ceros
    M_res = crear_matriz_zeros(n, n)
    
    # Para cada columna j (destino), calculamos los tiempos desde cualquier i != j
    for j in range(n):
        # Índices de estados que NO son el destino j
        indices_transitorios = [x for x in range(n) if x != j]
        
        # Crear submatriz Q eliminando fila j y col j
        Q = obtener_submatriz(P, indices_transitorios, indices_transitorios)
        dim_q = len(Q)
        
        # Crear I del tamaño correcto
        I_sub = crear_identidad(dim_q)
        
        # Crear matriz del sistema (I - Q)
        A_sis = crear_matriz_zeros(dim_q, dim_q)
        for r in range(dim_q):
            for c in range(dim_q):
                A_sis[r][c] = I_sub[r][c] - Q[r][c]
        
        # Vector de unos (el "1 +" de la fórmula)
        b_sis = [1.0] * dim_q
        
        # Resolver
        soluciones = resolver_sistema_lineal(A_sis, b_sis)
        
        if soluciones:
            # Mapear las soluciones de vuelta a la matriz grande
            for k, val in enumerate(soluciones):
                fila_original = indices_transitorios[k]
                M_res[fila_original][j] = val
        else:
            print(f"[INFO] No se puede alcanzar el estado {j} desde algunos estados.")

    # Llenar la diagonal con recurrencia si es posible
    print("\n[INFO] Calculando diagonal (recurrencia) para completar la matriz...")
    pi = calcular_estado_estable(P) # Esto imprime π de nuevo, pero es necesario
    if pi:
        for i in range(n):
            if pi[i] > 0:
                M_res[i][i] = 1.0 / pi[i]
    
    print("\nMatriz de Tiempos Medios (Filas=Origen -> Cols=Destino):")
    print_matriz(M_res)


def calcular_absorcion(P):
    print_sub("Probabilidades de Absorción")
    print("Solución de: (I - Q) * F = R")
    
    n = len(P)
    absorbentes = []
    transitorios = []
    
    # Identificar estados
    for i in range(n):
        if abs(P[i][i] - 1.0) < 1e-6: # Si P[i][i] == 1
            absorbentes.append(i)
        else:
            transitorios.append(i)
            
    if not absorbentes:
        print("No hay estados absorbentes (P_ii = 1).")
        return

    print(f"Estados Absorbentes: {absorbentes}")
    print(f"Estados Transitorios: {transitorios}")
    
    # Construir Q (de transitorio a transitorio)
    Q = obtener_submatriz(P, transitorios, transitorios)
    
    # Construir R (de transitorio a absorbente)
    R = obtener_submatriz(P, transitorios, absorbentes)
    
    # Construir I - Q
    dim_t = len(transitorios)
    I = crear_identidad(dim_t)
    A_sis = crear_matriz_zeros(dim_t, dim_t)
    
    for r in range(dim_t):
        for c in range(dim_t):
            A_sis[r][c] = I[r][c] - Q[r][c]
            
    # Resolver para cada columna de R (cada estado absorbente es un vector b distinto)
    # Esto nos da las probabilidades de terminar en ese estado absorbente específico
    dim_abs = len(absorbentes)
    F_res = crear_matriz_zeros(dim_t, dim_abs)
    
    for k in range(dim_abs):
        # Extraer la columna k de R como vector b
        b = [R[row][k] for row in range(dim_t)]
        
        # Resolver (I-Q) * x = b
        # Nota: Tenemos que copiar A_sis porque el solver gaussiano modifica la matriz
        A_copia = [fila[:] for fila in A_sis]
        solucion = resolver_sistema_lineal(A_copia, b)
        
        if solucion:
            for i in range(dim_t):
                F_res[i][k] = solucion[i]
                
    print("\nProbabilidades de Absorción (Transitorios -> Absorbentes):")
    # Formato bonito de salida
    print(f"{'Origen':<10} | ", end="")
    for k in absorbentes:
        print(f"Destino {k:<8} | ", end="")
    print("\n" + "-"*40)
    
    for i in range(dim_t):
        origen = transitorios[i]
        print(f"Estado {origen:<3} | ", end="")
        for k in range(dim_abs):
            val = F_res[i][k]
            print(f"{val:<16.4f} | ", end="")
        print("")

# --------------------------
# Menú Principal
# --------------------------

def menu():
    print_header("Calculadora Cadenas de Markov (Nativo Python)")
    P = None
    
    # Matriz de prueba (comentar para producción)
    # P = [[0.5, 0.5], [0.2, 0.8]]
    
    while True:
        print_header("MENÚ PRINCIPAL")
        print("1) Ingresar Matriz de Transición (P)")
        print("2) Ecuaciones Chapman-Kolmogorov P(n)")
        print("3) Probabilidades de Estado Estable")
        print("4) Tiempos de Primera Pasada")
        print("5) Tiempos de Recurrencia")
        print("6) Probabilidades de Absorción")
        print("9) Salir")
        
        choice = input("Seleccione una opción: \n")

        if choice == "9":
            print("¡Hasta luego!")
            return

        if choice == "1":
            P = ingresar_matriz()
            if P: print_matriz(P, "Matriz Cargada")
            
        elif P is None:
            print("\n[!] Primero debe cargar una matriz (Opción 1)")
            
        else:
            if choice == "2":
                calcular_chapman_kolmogorov(P)
            elif choice == "3":
                calcular_estado_estable(P)
            elif choice == "4":
                calcular_primera_pasada(P)
            elif choice == "5":
                calcular_tiempos_recurrencia(P)
            elif choice == "6":
                calcular_absorcion(P)
            else:
                print("Opción inválida.")

if __name__ == "__main__":
    menu()