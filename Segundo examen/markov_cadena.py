"""
markov_cadena.py

Herramientas básicas para cadenas de Markov en tiempo discreto, SIN numpy.

- Representamos la matriz de transición P como lista de listas:
  P[i][j] = P(X_{n+1} = j | X_n = i)

Funciones principales:
- multiplicar_matrices(A, B)
- potencia_matriz(P, n)
- multiplicar_vector_matriz(v, M)
- distribucion_estacionaria(P)   (usando método de Gauss)
- tiempos_recurrencia(P)
- matriz_tiempos_primera_pasad(P)

Además incluye un MENÚ INTERACTIVO para resolver lo que se pueda de:
- Problema 1 (círculo de 5 estados)
- Problema 2 (cervecerías A, B, C)
- Problema 3 (máquina buena/mala, potencias de transición)
o cualquier otra cadena de Markov que ingreses.
"""

import math

# ============================
# Utilidades de matrices
# ============================

def copiar_matriz(M):
    """Copia una matriz (lista de listas)."""
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
    """
    Multiplica dos matrices A (m x n) y B (n x p) de forma clásica.

    Paso 1: Determinar dimensiones.
    Paso 2: Crear matriz resultado llena de ceros.
    Paso 3: Para cada posición (i, j) del resultado:
            resultado[i][j] = sum_{k} A[i][k] * B[k][j]
    """
    m = len(A)
    n = len(A[0])
    n2 = len(B)
    p = len(B[0])

    if n != n2:
        raise ValueError("Dimensiones incompatibles para multiplicar matrices")

    # Crear matriz resultado m x p llena de ceros
    R = []
    for i in range(m):
        fila = []
        for j in range(p):
            fila.append(0.0)
        R.append(fila)

    # Calcular cada elemento de R
    for i in range(m):
        for j in range(p):
            suma = 0.0
            for k in range(n):
                suma += A[i][k] * B[k][j]
            R[i][j] = suma

    return R


def potencia_matriz(P, n):
    """
    Calcula P^n multiplicando sucesivamente.

    Paso 1: Si n = 0, P^0 = I (matriz identidad).
    Paso 2: Si n >= 1, iniciar resultado = P.
    Paso 3: Repetir n-1 veces: resultado = resultado * P.
    """
    if n < 0:
        raise ValueError("n debe ser >= 0")

    tamaño = len(P)

    # Caso n = 0: devolver identidad
    if n == 0:
        I = []
        for i in range(tamaño):
            fila = []
            for j in range(tamaño):
                if i == j:
                    fila.append(1.0)
                else:
                    fila.append(0.0)
            I.append(fila)
        return I

    # Caso n >= 1
    R = copiar_matriz(P)
    for _ in range(n - 1):
        R = multiplicar_matrices(R, P)
    return R


def multiplicar_vector_matriz(v, M):
    """
    Multiplica un vector fila v (1 x m) por una matriz M (m x n):

        resultado[j] = sum_i v[i] * M[i][j]

    Paso 1: revisar dimensiones.
    Paso 2: calcular cada componente j del vector resultado.
    """
    m = len(v)
    m2 = len(M)
    n = len(M[0])

    if m != m2:
        raise ValueError("Dimensiones incompatibles vector-matriz")

    resultado = []
    for j in range(n):
        suma = 0.0
        for i in range(m):
            suma += v[i] * M[i][j]
        resultado.append(suma)

    return resultado


# ============================
# Gauss para sistemas lineales
# ============================

def resolver_sistema_lineal(A, b, verbose=False):
    """
    Resuelve A x = b usando eliminación de Gauss con sustitución hacia atrás.
    
    A: matriz cuadrada n x n
    b: vector de tamaño n
    verbose: si es True, imprime CADA paso de la eliminación.
    """
    n = len(A)

    # Copias
    M = copiar_matriz(A)
    v = b[:]

    if verbose:
        print("\n  [Gauss] Iniciando Eliminación. Matriz/Vector Inicial (A|b):")
        _imprimir_matriz_aumentada(M, v, "A|b inicial", decimales=6)

    # --- ELIMINACIÓN HACIA ADELANTE ---
    for k in range(n):
        # k = fila del pivote
        
        # 1. Buscar pivote máximo en columna k (desde fila k hasta n-1)
        max_fila = k
        max_valor = abs(M[k][k])
        for i in range(k + 1, n):
            if abs(M[i][k]) > max_valor:
                max_valor = abs(M[i][k])
                max_fila = i

        if max_valor == 0.0:
            raise ValueError("Matriz singular, no se puede resolver el sistema")

        # 2. Intercambiar fila k con fila max_fila
        if max_fila != k:
            M[k], M[max_fila] = M[max_fila], M[k]
            v[k], v[max_fila] = v[max_fila], v[k]
            if verbose:
                print("\n  [Gauss] Paso {} (Pivote): Fila {} <-> Fila {}".format(k + 1, k, max_fila))
                _imprimir_matriz_aumentada(M, v, "Tras intercambio F{}-F{}".format(k, max_fila), decimales=6)

        # 3. Eliminar entradas por debajo del pivote
        pivote = M[k][k]
        if verbose:
             print("\n  [Gauss] Paso {} (Eliminación): Usando Fila {} (Pivote = {:.6f})".format(k + 1, k, pivote))

        for i in range(k + 1, n):
            # i = fila que vamos a modificar
            factor = M[i][k] / pivote
            
            if verbose and abs(factor) > 1e-10: # No imprimir si el factor es cero
                print("    - Fila {} = Fila {} - ({:.6f}) * Fila {}".format(i, i, factor, k))

            # Aplicar la resta a la fila i
            for j in range(k, n):
                # j = columna
                M[i][j] = M[i][j] - factor * M[k][j]
            v[i] = v[i] - factor * v[k]
            
            # (Opcional)
            # if verbose:
            #    _imprimir_matriz_aumentada(M, v, "  (estado F{})".format(i), decimales=6)

        if verbose:
            print("  [Gauss] Estado de (M|v) después de eliminar con Fila {}:".format(k))
            _imprimir_matriz_aumentada(M, v, "Matriz post-pivote {}".format(k), decimales=6)

    # --- FIN DE ELIMINACIÓN ---
    if verbose:
        print("\n  [Gauss] ELIMINACIÓN HACIA ADELANTE COMPLETA.")
        print("  Sistema triangular M'x = v' alcanzado.")
        _imprimir_matriz_aumentada(M, v, "M'|v' (Triangular)", decimales=6)

    # --- SUSTITUCIÓN HACIA ATRÁS ---
    x = [0.0] * n
    if verbose:
        print("\n  [Gauss] Iniciando Sustitución Hacia Atrás...")

    for i in range(n - 1, -1, -1):
        # i = fila que estamos despejando (de n-1 a 0)
        suma = 0.0
        for j in range(i + 1, n):
            suma += M[i][j] * x[j]
        
        # Ecuación: M[i][i] * x[i] + suma = v[i]
        x[i] = (v[i] - suma) / M[i][i]
        
        if verbose:
            print("    - Despejando Fila {}:".format(i))
            print("      Ecuación: {:.6f} * x{} + ({:.6f}) = {:.6f}".format(M[i][i], i, suma, v[i]))
            print("      => x{} = ({:.6f} - {:.6f}) / {:.6f}".format(i, v[i], suma, M[i][i]))
            print("      => x{} = {:.6f}".format(i, x[i]))

    if verbose:
        print("\n  [Gauss] SUSTITUCIÓN HACIA ATRÁS COMPLETA.")
        
    return x


# ============================
# Distribución estacionaria
# ============================

def distribucion_estacionaria(P, verbose=False):
    """
    Calcula el vector estacionario π para una cadena irreducible.
    Acepta 'verbose' para mostrar el sistema lineal.
    """
    n = len(P)

    # Construimos matriz A (n x n) y vector b (n)
    A = []
    b = []

    # Ecuaciones para j = 0..n-2
    for j in range(n - 1):
        fila = []
        for i in range(n):
            valor = P[i][j]
            if i == j:
                valor -= 1.0
            fila.append(valor)
        A.append(fila)
        b.append(0.0)

    # Última ecuación: sum_i π_i = 1
    fila_ultima = []
    for i in range(n):
        fila_ultima.append(1.0)
    A.append(fila_ultima)
    b.append(1.0)

    # --- INICIO DE IMPRESIÓN VERBOSA ---
    if verbose:
        print("\nPaso 2a: Construyendo sistema A*π = b")
        imprimir_matriz(A, "Matriz A")
        imprimir_vector(b, "Vector b")
        print("\nPaso 2b: Resolviendo sistema A*π = b con Gauss...")
    # --- FIN DE IMPRESIÓN VERBOSA ---

    pi = resolver_sistema_lineal(A, b, verbose=verbose)
    return pi


# ============================
# Tiempos de recurrencia
# ============================

def tiempos_recurrencia(P, verbose=False):
    """
    Devuelve una lista con los tiempos esperados de recurrencia de cada estado.
    Acepta 'verbose' para pasarlo al cálculo de la distribución estacionaria.
    """
    # Pasamos el flag 'verbose' al cálculo de pi
    pi = distribucion_estacionaria(P, verbose=verbose)
    
    tiempos = []
    for i in range(len(pi)):
        if pi[i] == 0:
            tiempos.append(float('inf'))
        else:
            tiempos.append(1.0 / pi[i])
    return pi, tiempos


# ============================
# Tiempos de primera pasada
# ============================

def matriz_tiempos_primera_pasad(P, verbose=False):
    """
    Calcula la matriz de tiempos esperados de primera pasada m_ij.
    Acepta 'verbose' para mostrar los n sistemas lineales que se resuelven.
    """
    n = len(P)
    M = []
    for _ in range(n):
        M.append([0.0] * n)

    for j in range(n):
        # Para cada destino j construimos y resolvemos el sistema lineal
        
        # --- INICIO DE IMPRESIÓN VERBOSA ---
        if verbose:
            print("\n-----------------------------------------------------")
            print("--- Resolviendo para el estado destino j = {} ---".format(j))
            print("--- (Buscando la columna {} de la matriz m_ij) ---".format(j))
            print("-----------------------------------------------------")
        # --- FIN DE IMPRESIÓN VERBOSA ---
        
        A = []
        b = []

        for i in range(n):
            fila = [0.0] * n
            if i == j:
                # m_jj = 0
                fila[j] = 1.0
                A.append(fila)
                b.append(0.0)
            else:
                # Ecuación: m_ij - sum_{k != j} P[i][k] m_kj = 1
                for l in range(n):
                    if l == j:
                        fila[l] = 0.0
                    elif l == i:
                        fila[l] = 1.0 - P[i][l]
                    else:
                        fila[l] = -P[i][l]
                A.append(fila)
                b.append(1.0)

        # --- INICIO DE IMPRESIÓN VERBOSA ---
        if verbose:
            print("\nPaso {}.a: Construyendo sistema A*m_j = b para m_j = [m_0{}, ..., m_{}{}]^T".format(j + 1, j, n - 1, j))
            imprimir_matriz(A, "Matriz A (para j={})".format(j))
            imprimir_vector(b, "Vector b (para j={})".format(j))
            print("\nPaso {}.b: Resolviendo sistema A*m_j = b con Gauss...".format(j + 1))
        # --- FIN DE IMPRESIÓN VERBOSA ---

        # Resolver el sistema para este j
        m_col = resolver_sistema_lineal(A, b, verbose=verbose)
        
        if verbose:
            imprimir_vector(m_col, "Solución m_j (columna {} de la matriz final)".format(j))

        for i in range(n):
            M[i][j] = m_col[i]

    return M


# ============================
# Funciones de impresión
# ============================

def imprimir_matriz(M, nombre="Matriz", decimales=4):
    filas = len(M)
    columnas = len(M[0])
    print("\n{} ({} x {}):".format(nombre, filas, columnas))
    for i in range(filas):
        fila_str = []
        for j in range(columnas):
            valor = M[i][j]
            if isinstance(valor, float):
                fila_str.append(("{:." + str(decimales) + "f}").format(valor))
            else:
                fila_str.append(str(valor))
        print("  fila {}: [{}]".format(i, ", ".join(fila_str)))


def imprimir_vector(v, nombre="Vector", decimales=4):
    print("\n{} (tamaño {}):".format(nombre, len(v)))
    comps = []
    for x in v:
        if isinstance(x, float):
            comps.append(("{:." + str(decimales) + "f}").format(x))
        else:
            comps.append(str(x))
    print("  [{}]".format(", ".join(comps)))


# ============================
# Entrada interactiva de P
# ============================

def leer_matriz_transicion():
    """
    Permite al usuario ingresar una matriz de transición P.

    Paso 1: Pedir número de estados n.
    Paso 2: Leer cada fila como números separados por espacios.
    Paso 3: Verificar (solo informativo) que cada fila sume aproximadamente 1.
    """
    print("\n=== Ingreso de la matriz de transición P ===")
    n = int(input("Ingrese el número de estados (n): \n").strip())
    P = []
    for i in range(n):
        while True:
            fila_str = input(
                "Ingrese la fila {} con {} probabilidades separadas por espacios: \n".format(
                    i, n
                )
            )
            partes = fila_str.strip().split()
            if len(partes) != n:
                print("  -> Debe ingresar exactamente {} números.".format(n))
                continue
            try:
                fila = [float(x) for x in partes]
            except ValueError:
                print("  -> Error: todos los valores deben ser numéricos.")
                continue

            suma = sum(fila)
            if abs(suma - 1.0) > 1e-6:
                print("  -> Advertencia: la suma de la fila es {:.6f}, no 1.0 exacto.".format(suma))
                print("     Asegúrese de que sea una matriz de transición (las filas deben sumar 1).")
            P.append(fila)
            break

    imprimir_matriz(P, nombre="Matriz de transición P")
    return P


# ============================
# Funciones de “procedimiento paso a paso”
# ============================

def procedimiento_potencia(P):
    print("\n=== Cálculo de P^n (probabilidades de transición en n pasos) ===")
    n = int(input("Ingrese el número de pasos n (entero >= 0): \n").strip())
    print("\nPaso 1: Identificamos la matriz de transición de un paso P.")
    imprimir_matriz(P, nombre="P")

    print("\nPaso 2: Queremos obtener P^n.")
    if n == 0:
        print("  - Por definición, P^0 es la matriz identidad del mismo tamaño que P.")
    else:
        print("  - Para n >= 1, usamos multiplicaciones sucesivas:")
        print("      P^2 = P * P")
        print("      P^3 = P^2 * P")
        print("      ...")
        print("      P^n = P^(n-1) * P")

    Pn = potencia_matriz(P, n)
    imprimir_matriz(Pn, nombre="P^{}".format(n))
    print("\nInterpretación: el elemento (i, j) de P^{} es P(X_{} = j | X_0 = i).".format(n, n))


def procedimiento_distribucion_estacionaria(P):
    print("\n=== Cálculo de la distribución estacionaria π ===")
    print("Paso 1: Recordamos la definición.")
    print("  - Una distribución estacionaria π satisface:  π = π P  y  sum_i π_i = 1.")
    print("  - Esto significa que si el sistema empieza con distribución π, entonces")
    print("    en el siguiente paso seguirá teniendo la misma distribución.\n")

    print("Paso 2: Construimos el sistema lineal equivalente:")
    print("  - Para j = 0..n-2:  sum_i π_i (P[i][j] - δ_ij) = 0")
    print("  - Última ecuación: sum_i π_i = 1\n")

    # AÑADIMOS verbose=True
    pi = distribucion_estacionaria(P, verbose=True)
    
    print("\n--- Resultado Final ---")
    imprimir_vector(pi, nombre="Distribución estacionaria π")
    print("\nVerificación conceptual: si multiplicamos π por P, deberíamos obtener de nuevo π (hasta error numérico).")


def procedimiento_tiempos_recurrencia(P):
    print("\n=== Cálculo de tiempos esperados de recurrencia ===")
    print("Para cadenas finitas irreducibles, el tiempo esperado de recurrencia de un estado i")
    print("viene dado por:   E[T_ii] = 1 / π_i,  donde π es la distribución estacionaria.\n")

    print("Paso 1: Calculamos la distribución estacionaria π (mostrando pasos).")
    
    # AÑADIMOS verbose=True
    pi, tiempos = tiempos_recurrencia(P, verbose=True)
    
    print("\n--- Resultado Intermedio (Dist. Estacionaria) ---")
    imprimir_vector(pi, nombre="Distribución estacionaria π")

    print("\nPaso 2: Aplicamos la fórmula E[T_ii] = 1 / π_i para cada estado i.")
    for i, t in enumerate(tiempos):
        print("  - Estado {}: π_{} = {:.6f}  =>  E[T_{}{}] = {:.6f}".format(i, i, pi[i], i, i, t))

def _imprimir_matriz_aumentada(M, v, nombre="Matriz", decimales=4):
    """Función auxiliar para imprimir la matriz aumentada [M | v]."""
    filas = len(M)
    print("\n{} ({} x {}):".format(nombre, filas, filas + 1))
    ancho = decimales + 4
    spec = "{: " + str(ancho) + "." + str(decimales) + "f}"
    for i in range(filas):
        fila_str = []
        for val in M[i]:
            fila_str.append(spec.format(val))
        
        fila_str.append("|")  # Separador
        fila_str.append(spec.format(v[i]))
        print("  Fila {}: [ {} ]".format(i, "  ".join(fila_str)))

def procedimiento_tiempos_primera_pasad(P):
    print("\n=== Cálculo de tiempos esperados de primera pasada m_ij ===")
    print("Definición: m_ij = E[T_ij] es el tiempo esperado para llegar POR PRIMERA VEZ")
    print("al estado j, comenzando en el estado i (con i ≠ j).")
    print("Para i = j, m_jj se define como 0 (ya estás en j en el tiempo 0).")
    print("\nPara un destino j fijo, se cumple la ecuación de primer paso:")
    print("  m_ij = 1 + sum_{k != j} P[i][k] * m_kj,   para i ≠ j")
    print("Llevando todo al lado izquierdo, obtenemos un sistema lineal que resolvemos con Gauss.\n")
    print("Resolveremos N sistemas lineales, uno para cada estado destino j=0..N-1.")

    # AÑADIMOS verbose=True
    M = matriz_tiempos_primera_pasad(P, verbose=True)
    
    print("\n-----------------------------------------------------")
    print("--- Resultado Final (Matriz m_ij) ---")
    print("-----------------------------------------------------")
    imprimir_matriz(M, nombre="Matriz de tiempos de primera pasada m_ij")

    print("\nInterpretación:")
    print("  - Cada entrada m_ij (i != j) es el tiempo esperado (en número de pasos)")
    print("    para llegar por primera vez al estado j comenzando en i.")
    print("  - Las entradas m_jj se han fijado en 0 por definición de 'tiempo para llegar a j desde j'.")


def procedimiento_completo_markov(P):
    """
    Para problemas como el 1 y 2 del portafolio:
    - Distribución estacionaria
    - Tiempos de recurrencia
    - Tiempos de primera pasada
    """
    procedimiento_distribucion_estacionaria(P)
    procedimiento_tiempos_recurrencia(P)
    procedimiento_tiempos_primera_pasad(P)


# ============================
# Menú principal
# ============================

def menu():
    P = None

    while True:
        print("\n================ MENÚ PRINCIPAL CADENAS DE MARKOV ================")
        print("1) Ingresar / cambiar matriz de transición P")
        print("2) Calcular P^n (probabilidades de transición en n pasos)")
        print("3) Calcular distribución estacionaria π")
        print("4) Calcular tiempos de recurrencia E[T_ii]")
        print("5) Calcular matriz de tiempos de primera pasada m_ij")
        print("6) Ejecutar análisis completo (π, recurrencia, primera pasada)")
        print("0) Salir")
        print("==================================================================")

        opcion = input("Seleccione una opción: \n").strip()

        if opcion == "0":
            print("Saliendo del programa. ¡Hasta luego!")
            break

        if opcion == "1":
            P = leer_matriz_transicion()

        else:
            if P is None:
                print("\n*** Primero debe ingresar una matriz de transición P (opción 1). ***")
                continue

            if opcion == "2":
                procedimiento_potencia(P)
            elif opcion == "3":
                procedimiento_distribucion_estacionaria(P)
            elif opcion == "4":
                procedimiento_tiempos_recurrencia(P)
            elif opcion == "5":
                procedimiento_tiempos_primera_pasad(P)
            elif opcion == "6":
                procedimiento_completo_markov(P)
            else:
                print("Opción no válida. Intente de nuevo.")


# ============================
# Ejecución del script
# ============================

if __name__ == "__main__":
    menu()