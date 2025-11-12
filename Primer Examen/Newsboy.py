import math

# ============================================================
# MODELO NEWSBOY (Newsvendor) - segun FORMULARIO
# ------------------------------------------------------------
# Definiciones del FORMULARIO:
#   C_menos = p - c         (costo por faltante)
#   C_mas   = c + h         (costo por excedente)
#   alpha   = C_menos / (C_menos + C_mas)   (nivel de servicio critico)
#
# Decision optima:
#   Q* = F^{-1}(alpha)   (cuantil alpha de la demanda)
#
# Este script soporta:
#   1) Demanda Normal(mu, sigma)
#   2) Demanda Discreta: lista de (x_i, prob_i) con sum prob_i = 1
#   3) Demanda Empirica: muestra de observaciones (cuantil empirico)
# ------------------------------------------------------------

# ---- Utilidades numericas ----

def _ndtri(p):
    """
    Aproximacion de la inversa de la CDF normal estandar (Acklam).
    Devuelve z tal que Phi(z) = p.  0 < p < 1.
    """
    if not (0.0 < p < 1.0):
        if p == 0.0:
            return -math.inf
        if p == 1.0:
            return math.inf
        raise ValueError("p debe estar en (0,1)")

    # Coeficientes de Peter John Acklam (2003)
    a = [ -3.969683028665376e+01,  2.209460984245205e+02,
          -2.759285104469687e+02,  1.383577518672690e+02,
          -3.066479806614716e+01,  2.506628277459239e+00 ]
    b = [ -5.447609879822406e+01,  1.615858368580409e+02,
          -1.556989798598866e+02,  6.680131188771972e+01,
          -1.328068155288572e+01 ]
    c = [ -7.784894002430293e-03, -3.223964580411365e-01,
          -2.400758277161838e+00, -2.549732539343734e+00,
           4.374664141464968e+00,  2.938163982698783e+00 ]
    d = [  7.784695709041462e-03,  3.224671290700398e-01,
           2.445134137142996e+00,  3.754408661907416e+00 ]

    plow  = 0.02425
    phigh = 1 - plow

    if p < plow:
        q = math.sqrt(-2*math.log(p))
        return (((((c[0]*q + c[1])*q + c[2])*q + c[3])*q + c[4])*q + c[5]) / \
               ((((d[0]*q + d[1])*q + d[2])*q + d[3])*q + 1)
    if p > phigh:
        q = math.sqrt(-2*math.log(1-p))
        return -(((((c[0]*q + c[1])*q + c[2])*q + c[3])*q + c[4])*q + c[5]) / \
                 ((((d[0]*q + d[1])*q + d[2])*q + d[3])*q + 1)
    q = p - 0.5
    r = q*q
    return (((((a[0]*r + a[1])*r + a[2])*r + a[3])*r + a[4])*r + a[5])*q / \
           (((((b[0]*r + b[1])*r + b[2])*r + b[3])*r + b[4])*r + 1)

def _quantile_discrete(pairs, alpha):
    """
    Cuantil para distribucion discreta.
    Retorna el menor x tal que F(x) >= alpha.
    """
    pairs = sorted(pairs, key=lambda t: t[0])
    total_p = sum(p for _, p in pairs)
    if abs(total_p - 1.0) > 1e-8:
        raise ValueError("Las probabilidades de la distribucion discreta deben sumar 1.")
    acc = 0.0
    for x, p in pairs:
        acc += p
        if acc >= alpha - 1e-12:
            return x
    return pairs[-1][0]

def _quantile_empirical(data, alpha):
    """
    Cuantil empirico tipo 'menor x con F>=alpha' (definicion paso).
    """
    if not data:
        raise ValueError("La muestra empirica no puede estar vacia.")
    xs = sorted(data)
    k = max(0, min(len(xs)-1, int(math.ceil(alpha * len(xs)) - 1)))
    return xs[k]

# ---- Nucleo del modelo ----

def newsboy_alpha(p, c, h):
    """
    Nivel critico del FORMULARIO:
    alpha = (p - c) / ( (p - c) + (c + h) )
    """
    c_menos = p - c         # faltante
    c_mas   = c + h         # excedente
    if c_menos <= 0:
        raise ValueError("Se requiere p > c para que el costo por faltante sea positivo.")
    if c_mas <= 0:
        raise ValueError("Se requiere c + h > 0 para que el costo por excedente sea positivo.")
    return c_menos / (c_menos + c_mas)

def newsboy_normal(mu, sigma, p, c, h, mostrar_procedimiento=True):
    """
    Newsboy con demanda Normal(mu, sigma).
    Q* = mu + z_alpha * sigma, donde z_alpha = Phi^{-1}(alpha).
    """
    if sigma <= 0:
        raise ValueError("sigma debe ser > 0 para la demanda Normal.")
    alpha = newsboy_alpha(p, c, h)
    z = _ndtri(alpha)
    Q_opt = mu + z * sigma

    if mostrar_procedimiento:
        c_menos = p - c
        c_mas = c + h
        print("\nNEWSBOY - Demanda Normal(mu, sigma) - Procedimiento Detallado")
        print("-----------------------------------------------------------")
        print("p = {:.6f}, c = {:.6f}, h = {:.6f}".format(p, c, h))
        print("C_menos = p - c = {:.6f} - {:.6f} = {:.6f}".format(p, c, c_menos))
        print("C_mas   = c + h = {:.6f} + {:.6f} = {:.6f}".format(c, h, c_mas))
        print("alpha = C_menos / (C_menos + C_mas)")
        print("      = {:.6f} / ({:.6f} + {:.6f}) = {:.6f}".format(c_menos, c_menos, c_mas, alpha))
        print("z_alpha = Phi^(-1)({:.6f}) = {:.6f}".format(alpha, z))
        print("Q* = mu + z_alpha * sigma = {:.6f} + {:.6f} * {:.6f} = {:.6f}\n".format(mu, z, sigma, Q_opt))
        print("Notas: Formulas del FORMULARIO para C_menos, C_mas y nivel de servicio critico (alpha).")
        print("      Cuantil normal obtenido por aproximacion numerica.")

    return {"alpha": alpha, "z_alpha": z, "Q*": Q_opt}

def newsboy_discreta(pairs, p_, c, h, mostrar_procedimiento=True):
    """
    Newsboy con distribucion discreta de demanda.
    pairs: [(x_i, prob_i)] con sum prob_i = 1.
    Q* = menor x con F(x) >= alpha.
    """
    alpha = newsboy_alpha(p_, c, h)
    Q_opt = _quantile_discrete(pairs, alpha)

    if mostrar_procedimiento:
        c_menos = p_ - c
        c_mas = c + h
        print("\nNEWSBOY - Demanda Discreta - Procedimiento Detallado")
        print("------------------------------------------------------")
        print("p = {:.6f}, c = {:.6f}, h = {:.6f}".format(p_, c, h))
        print("C_menos = p - c = {:.6f}".format(c_menos))
        print("C_mas   = c + h = {:.6f}".format(c_mas))
        print("alpha = {:.6f}".format(alpha))
        print("Distribucion discreta (x_i, p_i) ordenada por x:")
        for x, pr in sorted(pairs, key=lambda t: t[0]):
            print("  x={:.6f}, p={:.6f}".format(x, pr))
        print("=> Q* = F^(-1)({:.6f}) = {:.6f}\n".format(alpha, Q_opt))

    return {"alpha": alpha, "Q*": Q_opt}

def newsboy_empirica(muestra, p_, c, h, mostrar_procedimiento=True):
    """
    Newsboy con demanda empirica (observaciones).
    Q* = cuantil empirico de orden alpha.
    """
    alpha = newsboy_alpha(p_, c, h)
    Q_opt = _quantile_empirical(muestra, alpha)

    if mostrar_procedimiento:
        c_menos = p_ - c
        c_mas = c + h
        print("\nNEWSBOY - Demanda Empirica - Procedimiento Detallado")
        print("------------------------------------------------------")
        print("p = {:.6f}, c = {:.6f}, h = {:.6f}".format(p_, c, h))
        print("C_menos = p - c = {:.6f}".format(c_menos))
        print("C_mas   = c + h = {:.6f}".format(c_mas))
        print("alpha = {:.6f}".format(alpha))
        print("muestra (n={}), Q* = cuantil empirico({:.6f}) = {:.6f}\n".format(len(muestra), alpha, Q_opt))

    return {"alpha": alpha, "Q*": Q_opt}

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

def _leer_lista_floats(msg):
    while True:
        s = input(msg).strip()
        try:
            vals = [float(x.strip().replace(",", ".")) for x in s.split()]
            if not vals:
                raise ValueError
            return vals
        except Exception:
            print("  Ingresa numeros separados por espacios, ej: 100 120 90 110")

def _leer_discreta():
    print("Ingrese pares 'x p' por linea. Finalice con una linea vacia.")
    pares = []
    while True:
        line = input("> ").strip()
        if line == "":
            break
        try:
            x_s, p_s = line.split()
            x = float(x_s.replace(",", "."))
            pr = float(p_s.replace(",", "."))
            if pr < 0 or pr > 1:
                print("  La probabilidad debe estar en [0,1].")
                continue
            pares.append((x, pr))
        except Exception:
            print("  Formato invalido. Use: x p  (ej: 100 0.25)")
    return pares

if __name__ == "__main__":
    print("MODELO NEWSBOY (Newsvendor) - Interactivo\n")
    print("Selecciona el tipo de demanda:")
    print("  1) Normal(mu, sigma)")
    print("  2) Discreta (x_i, p_i)")
    print("  3) Empirica (muestra de observaciones)")
    tipo = input("Opcion [1/2/3]: ").strip()

    p = _leer_float("Precio de venta p ($/unidad): ")
    c = _leer_float("Costo de adquisicion c ($/unidad): ")
    h = _leer_float("Costo de mantener excedente h ($/unidad*periodo): ")

    if tipo == "1":
        mu = _leer_float("Media mu de la demanda: ")
        sigma = _leer_float("Desviacion estandar sigma de la demanda (>0): ")
        res = newsboy_normal(mu, sigma, p, c, h, mostrar_procedimiento=True)

    elif tipo == "2":
        print("\nDistribucion discreta:")
        pares = _leer_discreta()
        res = newsboy_discreta(pares, p, c, h, mostrar_procedimiento=True)

    elif tipo == "3":
        print("\nIngresa la muestra empirica (demanda historica).")
        datos = _leer_lista_floats("Observaciones separadas por espacios: ")
        res = newsboy_empirica(datos, p, c, h, mostrar_procedimiento=True)

    else:
        raise SystemExit("Opcion no valida.")
