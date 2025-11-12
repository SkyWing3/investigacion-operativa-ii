import math

# ============================================================
# EOQ con Punto de Reorden — según FORMULARIO
# ------------------------------------------------------------
# Variables:
#   d : demanda anual (unidades/año)
#   K : costo por pedido ($/orden)
#   h : costo de mantenimiento ($/unidad·año)
#   c : costo de adquisición ($/unidad)
#   L : tiempo de entrega (lead time)
#   unidades_L : 'anios', 'dias', 'semanas', 'meses'
#   dias_por_ano : conversión (por defecto 365)
#
# Fórmulas:
#   Q*  = sqrt( 2·K·d / h )
#   t*  = Q*/d
#   n   = floor( L / t* )
#   Le  = L - n·t*
#   PR  = Le·d
#   CT  = (K·d/Q*) + (c·d) + (h·Q*/2)
# ============================================================

def _L_a_anios(L, unidades_L, dias_por_ano=365.0):
    unidades_L = unidades_L.lower()
    if unidades_L in ("anio", "anios", "años", "año"):
        return float(L)
    if unidades_L in ("dia", "dias", "día", "días"):
        return float(L) / dias_por_ano
    if unidades_L in ("semana", "semanas"):
        return float(L) * 7.0 / dias_por_ano
    if unidades_L in ("mes", "meses"):
        # Aproximación estándar de 30.4167 días/mes ≈ 365/12
        return float(L) * (365.0 / 12.0) / dias_por_ano
    raise ValueError("unidades_L debe ser 'anios', 'dias', 'semanas' o 'meses'.")

def eoq_punto_reorden(
    d,
    K,
    h,
    c=0.0,
    L=0.0,
    unidades_L="dias",
    dias_por_ano=365.0,
    mostrar_procedimiento=True
):
    # Validaciones básicas
    if d <= 0:
        raise ValueError("La demanda anual d debe ser > 0.")
    if K < 0:
        raise ValueError("El costo por pedido K no puede ser negativo.")
    if h <= 0:
        raise ValueError("El costo de mantenimiento h debe ser > 0.")
    if c < 0:
        raise ValueError("El costo unitario c no puede ser negativo.")
    if L < 0:
        raise ValueError("El tiempo de entrega L no puede ser negativo.")

    # 1) EOQ del formulario
    Q_opt = math.sqrt(2.0 * K * d / h)
    t_c = Q_opt / d
    N = d / Q_opt
    CT = (K * d / Q_opt) + (c * d) + (h * Q_opt / 2.0)

    # 2) Convertir L a años y aplicar PR
    L_anios = _L_a_anios(L, unidades_L, dias_por_ano)
    n = math.floor(L_anios / t_c) if t_c > 0 else 0
    Le = L_anios - n * t_c
    PR = Le * d

    if mostrar_procedimiento:
        print("\nEOQ con Punto de Reorden — Procedimiento Detallado")
        print("------------------------------------------------------")
        print("d = {:,.6f}  (unid/año)".format(d))
        print("K = ${:,.6f}  (por orden)".format(K))
        print("h = ${:,.6f}  (por unid·año)".format(h))
        print("c = ${:,.6f}  (por unidad)".format(c))
        print("L = {:,.6f}  ({})  →  {:.6f} años\n".format(L, unidades_L, L_anios))

        print("Fórmulas (FORMULARIO):")
        print("  Q*  = √(2·K·d / h)")
        print("  t*  = Q*/d")
        print("  n   = ⌊ L / t* ⌋")
        print("  Le  = L − n·t*")
        print("  PR  = Le·d")
        print("  CT  = (K·d/Q*) + (c·d) + (h·Q*/2)\n")

        print("Sustitución numérica:")
        print("  Q* = √(2·{:.6f}·{:.6f}/{:.6f}) = {:,.6f}".format(K, d, h, Q_opt))
        print("  t* = Q*/d = {:,.6f}/{:.6f} = {:.6f} años  ({:.2f} días)".format(Q_opt, d, t_c, t_c * 365))
        print("  n  = ⌊ L/t* ⌋ = ⌊ {:.6f}/{:.6f} ⌋ = {}".format(L_anios, t_c, n))
        print("  Le = L − n·t* = {:.6f} − {}·{:.6f} = {:.6f} años  ({:.2f} días)".format(L_anios, n, t_c, Le, Le * 365))
        print("  PR = Le·d = {:.6f}·{:.6f} = {:,.6f} unidades\n".format(Le, d, PR))

        parte1 = (K * d / Q_opt)
        parte2 = (c * d)
        parte3 = (h * Q_opt / 2.0)
        print("Costo total anual (opcional, como EOQ básico):")
        print("  CT = (K·d/Q*) + (c·d) + (h·Q*/2)")
        print("     = ({:.6f}) + ({:.6f}) + ({:.6f}) = ${:,.6f}\n".format(parte1, parte2, parte3, CT))

        print("Resultados:")
        print("  Q* (lote óptimo)         : {:,.6f} unidades".format(Q_opt))
        print("  t* (tiempo entre pedidos): {:.6f} años  ({:.2f} días)".format(t_c, t_c * 365))
        print("  N  (órdenes por año)     : {:.6f}".format(N))
        print("  n  (ciclos enteros en L) : {}".format(n))
        print("  Le (lead time efectivo)  : {:.6f} años  ({:.2f} días)".format(Le, Le * 365))
        print("  PR (punto de reorden)    : {:,.6f} unidades".format(PR))
        print("  CT (costo anual)         : ${:,.6f}".format(CT))
        print("------------------------------------------------------\n")

    return {
        "Q*": Q_opt,
        "t* (años)": t_c,
        "Pedidos/año": N,
        "n (ciclos enteros en L)": n,
        "Le (años)": Le,
        "PR (unidades)": PR,
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
            print("  Valor no válido. Intenta de nuevo.")

if __name__ == "__main__":
    print("EOQ con Punto de Reorden\n")
    d = _leer_float("Demanda anual d (unidades/año): \n")
    K = _leer_float("Costo por pedido K ($/orden): \n")
    h = _leer_float("Costo de mantenimiento h ($/unidad·año): \n")
    c = _leer_float("Costo de adquisición c ($/unidad) [0 si no se considera]: \n")

    print("\nUnidad de L (lead time): [anios|dias|semanas|meses]")
    unidades = input("Unidad de L: \n").strip().lower()
    L = _leer_float("Valor de L en la unidad elegida: \n")

    res = eoq_punto_reorden(d, K, h, c, L, unidades_L=unidades, mostrar_procedimiento=True)
