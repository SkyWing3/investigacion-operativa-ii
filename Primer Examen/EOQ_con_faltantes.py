import math

# ============================================================
# EOQ con Faltantes Planeados (Backorders) - segun FORMULARIO
# ------------------------------------------------------------
# Variables:
#   d : demanda anual (unidades/anio)
#   K : costo por pedido (USD/orden)
#   h : costo de mantenimiento (USD/unidad*anio)
#   p : costo anual por unidad faltante (USD/unidad*anio)
#   c : costo de adquisicion (USD/unidad)
#
# Formulas:
#   Q* = raiz( (2*K*d / h) * (p + h)/p )
#   S* = raiz( (2*K*d / h) * p/(p + h) )
#   CT(Q,S) = (K*d / Q) + (c*d) + [h*S^2 / (2*Q)] + [p*(Q-S)^2 / (2*Q)]
# ============================================================

def eoq_con_faltantes(d, K, h, p, c=0.0, mostrar_procedimiento=True):
    if d <= 0:
        raise ValueError("La demanda anual d debe ser mayor que 0.")
    if K < 0:
        raise ValueError("El costo por pedido K no puede ser negativo.")
    if h <= 0:
        raise ValueError("El costo de mantenimiento h debe ser mayor que 0.")
    if p <= 0:
        raise ValueError("El costo por faltante p debe ser mayor que 0.")
    if c < 0:
        raise ValueError("El costo de adquisicion c no puede ser negativo.")

    Q_opt = math.sqrt((2.0 * K * d / h) * ((p + h) / p))
    S_opt = math.sqrt((2.0 * K * d / h) * (p / (p + h)))

    Bmax = Q_opt - S_opt
    t_ciclo = Q_opt / d
    N = d / Q_opt

    CT = (K * d / Q_opt) + (c * d) + (h * S_opt**2) / (2.0 * Q_opt) + (p * (Q_opt - S_opt)**2) / (2.0 * Q_opt)

    if mostrar_procedimiento:
        print("\nEOQ con Faltantes Planeados - Procedimiento Detallado")
        print("--------------------------------------------------------")
        print("d = {:,.6f}  (unid/anio)".format(d))
        print("K = ${:,.6f}  (por orden)".format(K))
        print("h = ${:,.6f}  (por unid/anio)".format(h))
        print("p = ${:,.6f}  (por unid faltante/anio)".format(p))
        print("c = ${:,.6f}  (por unidad)\n".format(c))
        print("Formulas usadas:")
        print("  Q* = raiz( (2*K*d / h) * (p + h)/p )")
        print("  S* = raiz( (2*K*d / h) * p/(p + h) )")
        print("  CT = (K*d / Q) + (c*d) + [h*S^2 / (2*Q)] + [p*(Q-S)^2 / (2*Q)]")
        print("  t* = Q*/d,   N = d / Q*\n")

        print("Sustitucion numerica:")
        print("  Q* = raiz( (2*{:.6f}*{:.6f} / {:.6f}) * ({:.6f}+{:.6f})/{:.6f} ) = {:,.6f}".format(
            K, d, h, p, h, p, Q_opt))
        print("  S* = raiz( (2*{:.6f}*{:.6f} / {:.6f}) * {:.6f}/({:.6f}+{:.6f}) ) = {:,.6f}".format(
            K, d, h, p, p, h, S_opt))
        print("  Bmax = Q* - S* = {:,.6f} - {:,.6f} = {:,.6f}".format(Q_opt, S_opt, Bmax))
        print("  t* = Q*/d = {:,.6f}/{:.6f} = {:.6f} años ({:.2f} dias)".format(
            Q_opt, d, t_ciclo, t_ciclo * 365))
        print("  N = d/Q* = {:.6f}/{:,.6f} = {:.6f} ordenes/año\n".format(d, Q_opt, N))

        print("Costo total anual:")
        CT_desg = (
            (K * d / Q_opt),
            (c * d),
            (h * S_opt**2) / (2.0 * Q_opt),
            (p * (Q_opt - S_opt)**2) / (2.0 * Q_opt),
        )
        print("     = ({:.6f}) + ({:.6f}) + ({:.6f}) + ({:.6f})".format(
            CT_desg[0], CT_desg[1], CT_desg[2], CT_desg[3]))
        print("     = ${:,.6f}\n".format(CT))

        print("Resultados:")
        print("  Q* (cantidad optima)     : {:,.6f} unidades".format(Q_opt))
        print("  S* (inventario maximo)   : {:,.6f} unidades".format(S_opt))
        print("  Bmax (faltante maximo)   : {:,.6f} unidades".format(Bmax))
        print("  t* (tiempo entre pedidos): {:.6f} años ({:.2f} dias)".format(
            t_ciclo, t_ciclo * 365))
        print("  N  (ordenes por año)     : {:.6f}".format(N))
        print("  CT (costo anual total)   : ${:,.6f}".format(CT))
        print("--------------------------------------------------------\n")

    return {
        "Q*": Q_opt,
        "S* (inventario maximo)": S_opt,
        "Bmax (faltante maximo)": Bmax,
        "t* (años)": t_ciclo,
        "Pedidos/año": N,
        "CT anual": CT
    }


def _leer_float(msg):
    while True:
        s = input(msg).strip().replace(",", ".")
        try:
            return float(s)
        except ValueError:
            print("  Valor no valido. Intentalo de nuevo (usa numeros, ej. 24000, 50, 2.5).")


if __name__ == "__main__":
    print("EOQ con Faltantes Planeados (Backorders)\n")
    d = _leer_float("Demanda anual d (unidades/año): \n")
    K = _leer_float("Costo por pedido K ($/orden): \n")
    h = _leer_float("Costo de mantenimiento h ($/unidad*año): \n")
    p = _leer_float("Costo por faltante p ($/unidad*año): \n")
    c = _leer_float("Costo de adquisicion c ($/unidad) [0 si no se considera]: \n")

    res = eoq_con_faltantes(d, K, h, p, c, mostrar_procedimiento=True)
