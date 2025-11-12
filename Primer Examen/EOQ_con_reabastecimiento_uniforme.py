import math

# ============================================================
# EOQ con Reabastecimiento Uniforme (Producción Finita)
# ------------------------------------------------------------
# Variables:
#   d : demanda anual (unidades/año)
#   a : tasa de producción (unidades/año)  [a > d]
#   K : costo por pedido ($/orden)
#   h : costo de mantenimiento ($/unidad·año)
#   c : costo de adquisición ($/unidad)
#
# Fórmulas:
#   T(Q)  = (K·d / Q) + (c·d) + (h/2)·(1 - d/a)·Q
#   Q*    = √( 2·K·d / [ h·(1 - d/a) ] )
#   IMAX  = Q·(1 - d/a)
#   t*    = Q*/d
#   N     = d/Q*
# ============================================================

def eoq_reabastecimiento_uniforme(d, a, K, h, c=0.0, mostrar_procedimiento=True):
    # Validaciones
    if d <= 0:
        raise ValueError("La demanda anual d debe ser > 0.")
    if a <= 0:
        raise ValueError("La tasa de producción a debe ser > 0.")
    if a <= d:
        raise ValueError("La tasa de producción a debe ser mayor que la demanda d (a > d).")
    if K < 0:
        raise ValueError("El costo por pedido K no puede ser negativo.")
    if h <= 0:
        raise ValueError("El costo de mantenimiento h debe ser > 0.")
    if c < 0:
        raise ValueError("El costo de adquisición c no puede ser negativo.")

    factor = 1.0 - (d / a)
    denom = h * factor

    Q_opt = math.sqrt((2.0 * K * d) / denom)
    IMAX = Q_opt * factor
    t_c = Q_opt / d
    N = d / Q_opt

    CT = (K * d / Q_opt) + (c * d) + (h * factor * Q_opt / 2.0)

    if mostrar_procedimiento:
        print("\nEOQ con Reabastecimiento Uniforme — Procedimiento Detallado")
        print("----------------------------------------------------------------")
        print("d = {:,.6f}  (unid/año)".format(d))
        print("a = {:,.6f}  (unid/año)   [tasa de producción]".format(a))
        print("K = ${:,.6f}  (por orden)".format(K))
        print("h = ${:,.6f}  (por unid·año)".format(h))
        print("c = ${:,.6f}  (por unidad)\n".format(c))

        print("Fórmulas (FORMULARIO):")
        print("  T(Q)  = (K·d / Q) + (c·d) + (h/2)·(1 - d/a)·Q")
        print("  Q*    = √( 2·K·d / [ h·(1 - d/a) ] )")
        print("  IMAX  = Q·(1 - d/a)")
        print("  t*    = Q*/d,     N = d/Q*\n")

        print("Sustitución numérica:")
        print("  (1 - d/a) = 1 - {:.6f}/{:.6f} = {:.6f}".format(d, a, factor))
        print("  Q* = √( 2·{:.6f}·{:.6f} / ({:.6f}·{:.6f}) ) = {:,.6f}".format(K, d, h, factor, Q_opt))
        print("  IMAX = {:,.6f}·{:.6f} = {:,.6f}".format(Q_opt, factor, IMAX))
        print("  t* = Q*/d = {:,.6f}/{:.6f} = {:.6f} años  ({:.2f} días)".format(Q_opt, d, t_c, t_c * 365))
        print("  N  = d/Q* = {:.6f}/{:,.6f} = {:.6f} órdenes/año\n".format(d, Q_opt, N))

        print("Costo total anual:")
        print("  T(Q*) = (K·d / Q*) + (c·d) + (h/2)·(1 - d/a)·Q*")
        parte1 = (K * d / Q_opt)
        parte2 = (c * d)
        parte3 = (h * factor * Q_opt / 2.0)
        print("        = ({:.6f}) + ({:.6f}) + ({:.6f})".format(parte1, parte2, parte3))
        print("        = ${:,.6f}\n".format(CT))

        print("Resultados:")
        print("  Q* (lote óptimo)         : {:,.6f} unidades".format(Q_opt))
        print("  IMAX (inventario máximo) : {:,.6f} unidades".format(IMAX))
        print("  t* (tiempo entre pedidos): {:.6f} años  ({:.2f} días)".format(t_c, t_c * 365))
        print("  N  (pedidos por año)     : {:.6f}".format(N))
        print("  CT (costo anual total)   : ${:,.6f}".format(CT))
        print("----------------------------------------------------------------\n")

    return {
        "Q*": Q_opt,
        "IMAX": IMAX,
        "t* (años)": t_c,
        "Pedidos/año": N,
        "CT anual": CT
    }


# ================================
# ENTRADA INTERACTIVA (opcional)
# ================================
def _leer_float(msg):
    while True:
        s = input(msg).strip().replace(",", ".")
        try:
            return float(s)
        except ValueError:
            print("  Valor no válido. Intenta de nuevo (usa números, ej. 26000, 36500, 20, 7.3).")

if __name__ == "__main__":
    print("EOQ con Reabastecimiento Uniforme (Producción Finita)\n")
    d = _leer_float("Demanda anual d (unidades/año): \n")
    a = _leer_float("Tasa de producción a (unidades/año): \n")
    K = _leer_float("Costo por pedido K ($/orden): \n")
    h = _leer_float("Costo de mantenimiento h ($/unidad·año): \n")
    c = _leer_float("Costo de adquisición c ($/unidad) [0 si no se considera]: \n")

    _ = eoq_reabastecimiento_uniforme(d, a, K, h, c, mostrar_procedimiento=True)
