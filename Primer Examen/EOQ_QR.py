import math

# ============================================================
# MODELO (Q,R) CON DEMANDA PROBABILISTICA - seg. FORMULARIO
# ------------------------------------------------------------
# Del FORMULARIO:
#   T(Q,R) = (K*D / Q) + h[ Q/2 + R - E(X) ] + (p*D*S)/Q
#   S(R)   = E[(X - R)^+] = integral desde R hasta infinito de (x - R) f(x) dx
#   Q*     = sqrt( 2*D*(K - p*S) / h )
#   Cola   : P(X >= R*) = h*Q* / (p*D)
# Donde X = demanda durante el lead time (o periodo correspondiente).
# ============================================================

# ---------- Utilidades Normal ----------
def _phi(z):
    return math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)

def _Phi(z):
    # CDF normal estandar
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))

def _ndtri(p):
    """Inversa de la CDF normal estandar (Acklam). 0<p<1."""
    if not (0.0 < p < 1.0):
        if p == 0.0: 
            return -math.inf
        if p == 1.0: 
            return math.inf
        raise ValueError("p debe estar en (0,1)")
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
          6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [ 7.784695709041462e-03,  3.224671290700398e-01,  2.445134137142996e+00,
          3.754408661907416e+00]
    plow = 0.02425
    phigh = 1 - plow
    if p < plow:
        q = math.sqrt(-2*math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
               ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if p > phigh:
        q = math.sqrt(-2*math.log(1-p))
        return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
                 ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    q = p - 0.5
    r = q*q
    return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / \
           (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)

# ---------- Demanda: utilidades para S(R) y cuantiles ----------
def S_normal(R, mu, sigma):
    """
    S(R) = E[(X-R)^+] para X ~ N(mu, sigma^2)
         = sigma*phi(z) + (mu - R)*(1 - Phi(z)),  z=(R-mu)/sigma
    """
    z = (R - mu) / sigma
    return sigma * _phi(z) + (mu - R) * (1.0 - _Phi(z))

def tail_quantile_normal(tail_prob, mu, sigma):
    """
    Encuentra R tal que P(X >= R) = tail_prob para X ~ N(mu, sigma^2).
    Equivale a R = mu + sigma * Phi^{-1}(1 - tail_prob).
    """
    t = max(min(tail_prob, 1 - 1e-12), 1e-12)  # recorte numerico
    z = _ndtri(1.0 - t)
    return mu + sigma * z

def S_discreta(R, pairs):
    """S(R) empirica para distribucion discreta (x_i, p_i)."""
    s = 0.0
    for x, p in pairs:
        if x > R:
            s += (x - R) * p
    return s

def tail_prob_discreta(R, pairs):
    """P(X >= R) para distribucion discreta."""
    return sum(p for x, p in pairs if x >= R)

def mean_discreta(pairs):
    return sum(x*p for x, p in pairs)

def S_empirica(R, data):
    """S(R) por muestra: promedio de max(x - R, 0)."""
    if not data:
        raise ValueError("La muestra empirica no puede estar vacia.")
    return sum((x - R) for x in data if x > R) / len(data)

def tail_prob_empirica(R, data):
    """P(X >= R) empirica como fraccion de observaciones >= R."""
    return sum(1 for x in data if x >= R) / len(data)

def mean_empirica(data):
    return sum(data) / len(data)

# ---------- Nucleo iterativo (Q,R) ----------
def solve_qr_normal(D, K, h, p, mu, sigma, tol=1e-8, max_iter=100, mostrar_procedimiento=True):
    """
    Resuelve (Q*, R*) para demanda Normal(mu, sigma).
    Iteracion:
      1) Q <- EOQ base: sqrt(2DK/h)
      2) tail = h Q / (p D);  R <- cuantil de cola (Normal)
      3) S <- S_normal(R);    Q <- sqrt( 2D (K - p S)/h )
      4) Repetir hasta convergencia
    """
    # Validaciones
    if any(x <= 0 for x in (D, h, p, sigma)) or K < 0:
        raise ValueError("Parametros invalidos: D,h,p,sigma deben ser >0 y K>=0.")

    Q = math.sqrt(2.0 * D * K / h)  # inicial (EOQ basico)
    if mostrar_procedimiento:
        print("\nModelo (Q,R) - Demanda Normal - Procedimiento Detallado")
        print("-----------------------------------------------------------")
        print("D={:.6f}, K={:.6f}, h={:.6f}, p={:.6f}, mu={:.6f}, sigma={:.6f}".format(D, K, h, p, mu, sigma))
        print("Formulas del FORMULARIO:")
        print("  T(Q,R) = (K*D/Q) + h[Q/2 + R - E(X)] + (p*D*S)/Q")
        print("  Q*     = sqrt( 2*D*(K - p*S) / h )")
        print("  P(X >= R*) = h*Q* / (p*D)\n")
        print("Inicio: Q0 = sqrt(2*{}*{}/{}) = {:.6f}".format(D, K, h, Q))

    for it in range(1, max_iter+1):
        # Paso cola -> R
        tail = (h * Q) / (p * D)
        R = tail_quantile_normal(tail, mu, sigma)
        # S(R)
        S = S_normal(R, mu, sigma)
        # Q nuevo
        K_eff = K - p * S
        if K_eff <= 0:
            # Caso teorico: el optimo empuja Q -> 0. Impone cota inferior.
            Q_new = max(1e-9, math.sqrt(max(0.0, 2.0 * D * K_eff) / h))
        else:
            Q_new = math.sqrt(2.0 * D * K_eff / h)

        if mostrar_procedimiento:
            print("Iter {:02d}:".format(it))
            print("  tail = h*Q/(p*D) = {:.6f}*{:.6f}/({:.6f}*{:.6f}) = {:.6f}".format(h, Q, p, D, tail))
            print("  R  = F_inv_col(tail) = {:.6f}".format(R))
            print("  S  = E[(X-R)^+] = {:.6f}".format(S))
            print("  K - p*S = {:.6f} - {:.6f}*{:.6f} = {:.6f}".format(K, p, S, K_eff))
            print("  Q <- sqrt(2*D*(K - p*S)/h) = {:.6f}".format(Q_new))

        if abs(Q_new - Q) <= tol * max(1.0, Q):
            Q = Q_new
            break
        Q = Q_new

    # Magnitudes finales
    t_ciclo = Q / D
    N = D / Q
    EX = mu
    CT = (K * D / Q) + h * (Q / 2.0 + R - EX) + (p * D * S) / Q

    if mostrar_procedimiento:
        print("\nConvergencia alcanzada.")
        print("Q* = {:.6f}  |  R* = {:.6f}".format(Q, R))
        print("t* = Q*/D = {:.6f} anios  ({:.2f} dias)".format(t_ciclo, t_ciclo*365))
        print("N  = D/Q* = {:.6f} ordenes/anio".format(N))
        print("CT = (K*D/Q*) + h[Q*/2 + R* - E(X)] + (p*D*S)/Q* = {:.6f}\n".format(CT))

    return {"Q*": Q, "R*": R, "t* (anios)": t_ciclo, "Pedidos/anio": N, "CT anual": CT}

def solve_qr_discreta(D, K, h, p, pairs, tol=1e-8, max_iter=100, mostrar_procedimiento=True):
    # Normalizar y validar
    pairs = sorted(pairs, key=lambda t: t[0])
    if abs(sum(pi for _, pi in pairs) - 1.0) > 1e-8:
        raise ValueError("Las probabilidades deben sumar 1.")
    EX = sum(x*pi for x, pi in pairs)
    if any(val <= 0 for val in (D, h, p)) or K < 0:
        raise ValueError("Parametros invalidos: D,h,p>0 y K>=0.")

    Q = math.sqrt(2.0 * D * K / h)
    if mostrar_procedimiento:
        print("\nModelo (Q,R) - Demanda Discreta - Procedimiento Detallado")
        print("------------------------------------------------------------")
        print("D={:.6f}, K={:.6f}, h={:.6f}, p={:.6f}".format(D, K, h, p))
        print("E(X) = {:.6f}".format(EX))
        print("Tabla (x_i, p_i):")
        for x, pi in pairs:
            print("  {:.6f}\t{:.6f}".format(x, pi))
        print("\nFormulas del FORMULARIO y esquema iterativo como en el caso Normal.\n")
        print("Inicio: Q0 = sqrt(2*{}*{}/{}) = {:.6f}".format(D, K, h, Q))

    for it in range(1, max_iter+1):
        tail = (h * Q) / (p * D)
        # hallar R tal que P(X >= R) = tail (cuantil de supervivencia discreta):
        candidates = []
        for x, _ in pairs:
            tp = tail_prob_discreta(x, pairs)
            candidates.append((x, tp, abs(tp - tail)))
        # elige el que minimice la diferencia |tp - tail|
        R, tp_sel, _ = min(candidates, key=lambda t: t[2])

        S = S_discreta(R, pairs)
        K_eff = K - p * S
        if K_eff <= 0:
            Q_new = max(1e-9, math.sqrt(max(0.0, 2.0 * D * K_eff) / h))
        else:
            Q_new = math.sqrt(2.0 * D * K_eff / h)

        if mostrar_procedimiento:
            print("Iter {:02d}: tail obj = {:.6f} | P(X>=R)~{:.6f} con R={:.6f}".format(it, tail, tp_sel, R))
            print("  S(R) = {:.6f}  ->  K - p*S = {:.6f}  ->  Q = {:.6f}".format(S, K_eff, Q_new))

        if abs(Q_new - Q) <= tol * max(1.0, Q):
            Q = Q_new
            break
        Q = Q_new

    t_ciclo = Q / D
    N = D / Q
    CT = (K * D / Q) + h * (Q / 2.0 + R - EX) + (p * D * S) / Q

    if mostrar_procedimiento:
        print("\nConvergencia alcanzada.")
        print("Q* = {:.6f}  |  R* = {:.6f}".format(Q, R))
        print("t* = {:.6f} anios  ({:.2f} dias)".format(t_ciclo, t_ciclo*365))
        print("N  = {:.6f} ordenes/anio".format(N))
        print("CT = {:.6f}\n".format(CT))

    return {"Q*": Q, "R*": R, "t* (anios)": t_ciclo, "Pedidos/anio": N, "CT anual": CT}

def solve_qr_empirica(D, K, h, p, data, tol=1e-8, max_iter=100, mostrar_procedimiento=True):
    if not data:
        raise ValueError("La muestra empirica no puede estar vacia.")
    EX = mean_empirica(data)
    if any(val <= 0 for val in (D, h, p)) or K < 0:
        raise ValueError("Parametros invalidos: D,h,p>0 y K>=0.")

    Q = math.sqrt(2.0 * D * K / h)
    if mostrar_procedimiento:
        print("\nModelo (Q,R) - Demanda Empirica - Procedimiento Detallado")
        print("------------------------------------------------------------")
        print("D={:.6f}, K={:.6f}, h={:.6f}, p={:.6f}".format(D, K, h, p))
        print("E(X)={:.6f}  |  n={} observaciones".format(EX, len(data)))
        print("Formulas del FORMULARIO e iteracion como en los casos anteriores.\n")
        print("Inicio: Q0 = sqrt(2*{}*{}/{}) = {:.6f}".format(D, K, h, Q))

    for it in range(1, max_iter+1):
        tail = (h * Q) / (p * D)
        # cuantil de cola empirico: buscamos R con P(X>=R)~tail
        xs = sorted(set(data))
        candidates = []
        for x in xs:
            tp = tail_prob_empirica(x, data)
            candidates.append((x, tp, abs(tp - tail)))
        R, tp_sel, _ = min(candidates, key=lambda t: t[2])

        S = S_empirica(R, data)
        K_eff = K - p * S
        if K_eff <= 0:
            Q_new = max(1e-9, math.sqrt(max(0.0, 2.0 * D * K_eff) / h))
        else:
            Q_new = math.sqrt(2.0 * D * K_eff / h)

        if mostrar_procedimiento:
            print("Iter {:02d}: tail obj = {:.6f} | P(X>=R)~{:.6f} con R={:.6f}".format(it, tail, tp_sel, R))
            print("  S(R) = {:.6f}  ->  K - p*S = {:.6f}  ->  Q = {:.6f}".format(S, K_eff, Q_new))

        if abs(Q_new - Q) <= tol * max(1.0, Q):
            Q = Q_new
            break
        Q = Q_new

    t_ciclo = Q / D
    N = D / Q
    CT = (K * D / Q) + h * (Q / 2.0 + R - EX) + (p * D * S) / Q

    if mostrar_procedimiento:
        print("\nConvergencia alcanzada.")
        print("Q* = {:.6f}  |  R* = {:.6f}".format(Q, R))
        print("t* = {:.6f} anios  ({:.2f} dias)".format(t_ciclo, t_ciclo*365))
        print("N  = {:.6f} ordenes/anio".format(N))
        print("CT = {:.6f}\n".format(CT))

    return {"Q*": Q, "R*": R, "t* (anios)": t_ciclo, "Pedidos/anio": N, "CT anual": CT}

# ================================
# ENTRADA INTERACTIVA (opcional)
# ================================
def _leer_float(msg):
    while True:
        s = input(msg).strip().replace(",", ".")
        try:
            return float(s)
        except ValueError:
            print("  Valor no valido. Intenta de nuevo.")

def _leer_discreta():
    print("Ingrese pares 'x p' por linea (ej: 100 0.2). Finalice con linea vacia.")
    pares = []
    while True:
        line = input("> ").strip()
        if line == "":
            break
        try:
            xs, ps = line.split()
            x = float(xs.replace(",", "."))
            p = float(ps.replace(",", "."))
            if not (0.0 <= p <= 1.0):
                raise ValueError
            pares.append((x, p))
        except Exception:
            print("  Formato invalido. Use: x p")
    return pares

def _leer_lista_floats(msg):
    while True:
        s = input(msg).strip()
        try:
            vals = [float(x.strip().replace(",", ".")) for x in s.split()]
            if not vals:
                raise ValueError
            return vals
        except Exception:
            print("  Ingresa numeros separados por espacios.")

if __name__ == "__main__":
    print("MODELO (Q,R) con Demanda Probabilistica - Interactivo\n")
    D = _leer_float("Demanda anual D (unidades/anio): \n")
    K = _leer_float("Costo por pedido K ($/orden): \n")
    h = _leer_float("Costo de mantenimiento h ($/unidad*anio): \n")
    p = _leer_float("Costo por faltante p ($/unidad): \n")

    print("\nTipo de demanda durante lead time X:")
    print("  1) Normal(mu, sigma)")
    print("  2) Discreta (x_i, p_i)")
    print("  3) Empirica (muestra)")
    op = input("Opcion [1/2/3]: \n").strip()

    if op == "1":
        mu = _leer_float("mu (media de X): \n")
        sigma = _leer_float("sigma (>0): \n")
        res = solve_qr_normal(D, K, h, p, mu, sigma, mostrar_procedimiento=True)
    elif op == "2":
        pares = _leer_discreta()
        res = solve_qr_discreta(D, K, h, p, pares, mostrar_procedimiento=True)
    elif op == "3":
        data = _leer_lista_floats("Observaciones de X separadas por espacios: \n")
        res = solve_qr_empirica(D, K, h, p, data, mostrar_procedimiento=True)
    else:
        raise SystemExit("Opcion invalida.")
