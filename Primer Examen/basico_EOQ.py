import math

def eoq_basico(d, K, h, c):
    """
    MODELO EOQ BÁSICO - FORMULARIO OFICIAL
    ------------------------------------------------
    d : demanda anual (unidades/año)
    K : costo de preparación o pedido ($/orden)
    h : costo de mantenimiento ($/unidad*año)
    c : costo de adquisición ($/unidad)
    ------------------------------------------------
    Fórmulas según el FORMULARIO DE MODELOS DE INVENTARIOS:
    
    Cantidad óptima:
        Q* = raiz(2*K*d / h)

    Tiempo de ciclo:
        t* = Q* / d

    Costo total por unidad de tiempo:
        T(Q) = (h*Q/2) + (c*d) + (K*d / Q)
    """

    # Calcular cantidad óptima Q*
    Q_opt = math.sqrt((2 * K * d) / h)

    # Calcular tiempo de ciclo
    t_opt = Q_opt / d

    # Calcular número de pedidos por año
    N = d / Q_opt

    # Calcular costo total anual (CT)
    CT = (h * Q_opt / 2) + (c * d) + (K * d / Q_opt)

    # Mostrar procedimiento paso a paso
    print("\n===== PROCEDIMIENTO DETALLADO - EOQ BÁSICO =====")
    print("Demanda anual (d) = {:,.2f} unidades/año".format(d))
    print("Costo por pedido (K) = ${:,.2f} por orden".format(K))
    print("Costo de mantenimiento (h) = ${:,.2f} por unidad*año".format(h))
    print("Costo de adquisición (c) = ${:,.2f} por unidad\n".format(c))

    print("Fórmulas utilizadas:")
    print("  Q* = raiz(2*K*d / h)")
    print("  t* = Q* / d")
    print("  CT = (h*Q/2) + (c*d) + (K*d / Q)\n")

    print("Sustituyendo valores:")
    print("  Q* = raiz(2*{}*{} / {}) = {:,.2f}".format(K, d, h, Q_opt))
    print("  t* = {:,.2f} / {} = {:.5f} años".format(Q_opt, d, t_opt))
    print("  N  = {} / {:,.2f} = {:.2f} órdenes/año".format(d, Q_opt, N))
    print("  CT = ({}*{:,.2f}/2) + ({}*{}) + ({}*{}/{:,.2f}) = ${:,.2f}\n".format(
        h, Q_opt, c, d, K, d, Q_opt, CT))

    print("===== RESULTADOS =====")
    print("Cantidad óptima a pedir (Q*)       = {:,.2f} unidades".format(Q_opt))
    print("Tiempo entre pedidos (t*)          = {:.5f} años ({:.2f} días)".format(t_opt, t_opt * 365))
    print("Número de pedidos por año (N)      = {:.2f}".format(N))
    print("Costo total anual estimado (CT)    = ${:,.2f}".format(CT))
    print("===============================================\n")

    # Retorno de valores clave
    return {"Q*": Q_opt, "t* (años)": t_opt, "Pedidos/año": N, "Costo total anual": CT}


# === ENTRADA INTERACTIVA ===
if __name__ == "__main__":
    print("  MODELO EOQ BÁSICO - FORMULARIO DE INVENTARIOS  \n")
    d = float(input("Ingrese la demanda anual (d) en unidades/año: \n"))
    K = float(input("Ingrese el costo por pedido (K) en $/orden: \n"))
    h = float(input("Ingrese el costo de mantenimiento (h) en $/unidad*año: \n"))
    c = float(input("Ingrese el costo de adquisición (c) en $/unidad: \n"))

    resultados = eoq_basico(d, K, h, c)