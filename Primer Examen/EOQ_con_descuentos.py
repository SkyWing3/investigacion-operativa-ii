import math

# ============================================================
# EOQ con Descuentos por Cantidad (All-Units)
# ============================================================

def _parse_percent(x):
    """
    Convierte entradas como '0.18' o '18%' a fracción 0.18.
    Si x ya es float, lo devuelve directo.
    """
    if isinstance(x, (int, float)):
        return float(x)
    s = str(x).strip().replace(',', '.')
    if s.endswith('%'):
        return float(s[:-1]) / 100.0
    return float(s)

def eoq_descuentos_all_units(d, K, i, price_breaks, mostrar_procedimiento=True):
    # Validaciones básicas
    if d <= 0:
        raise ValueError("La demanda anual d debe ser > 0.")
    if K < 0:
        raise ValueError("El costo por pedido K no puede ser negativo.")
    i = _parse_percent(i)
    if i <= 0:
        raise ValueError("La tasa de mantenimiento i debe ser > 0 (e.g., 0.20 o '20%').")
    if not price_breaks:
        raise ValueError("Debe proporcionar al menos un tramo de descuentos [(qmin, c)].")

    # Normalizar y ordenar tramos por qmin; agrupar duplicados tomando el menor precio
    _tramos = {}
    for qmin, c in price_breaks:
        if qmin <= 0:
            raise ValueError("Cada qmin debe ser >= 1.")
        if c <= 0:
            raise ValueError("Cada precio unitario c debe ser > 0.")
        qmin = float(qmin)
        c = float(c)
        if qmin not in _tramos or c < _tramos[qmin]:
            _tramos[qmin] = c
    tramos_ordenados = sorted(_tramos.items(), key=lambda x: x[0])

    if mostrar_procedimiento:
        print("\n  EOQ con Descuentos por Cantidad (All-Units) - Procedimiento Detallado")
        print("-----------------------------------------------------------------------")
        print("Demanda anual      d = {:,.4f} unidades/año".format(d))
        print("Costo por pedido   K = ${:,.4f} por orden".format(K))
        print("Tasa de mant.      i = {:.4%} por unidad monetaria*año".format(i))
        print("Tramos (qmin => precio unitario):")
        for qmin, c in tramos_ordenados:
            print("  - Q >= {:,.4f}  =>  c = ${:,.4f}  (h = i*c = {:.4f}*{:.4f})".format(qmin, c, i, c))
        print("\nFórmulas usadas por tramo j:")
        print("  h_j = i * c_j")
        print("  Q*_j = raiz(2 * K * d / h_j)")
        print("  T_j(Q) = (h_j * Q / 2) + (K * d / Q) + (c_j * d)")
        print("  Si Q*_j < qmin_j  =>  usar Q = qmin_j (primera Q factible del tramo).")
        print("-----------------------------------------------------------------------\n")

    candidatos = []
    mejor = None

    for idx, (qmin, c) in enumerate(tramos_ordenados, start=1):
        h = i * c

        # Proteger contra h muy pequeño
        if h <= 0:
            Q_star = float('inf')
            Q = qmin
        else:
            Q_star = math.sqrt(2.0 * K * d / h)
            Q = max(Q_star, qmin)

        CT = (h * Q / 2.0) + (K * d / Q) + (c * d)
        t_ciclo = Q / d
        N = d / Q

        candidato = {
            "tramo": idx,
            "qmin": qmin,
            "c": c,
            "h": h,
            "Q*_sin_restriccion": Q_star,
            "Q_elegida": Q,
            "CT_anual": CT,
            "t_ciclo_anios": t_ciclo,
            "pedidos_por_anio": N
        }
        candidatos.append(candidato)

        if mostrar_procedimiento:
            print("[Tramo {}]   qmin = {:,.4f}  |  c = ${:,.4f}  |  h = i*c = {:.6f}*{:.6f} = {:.6f}".format(
                idx, qmin, c, i, c, h))
            if math.isfinite(Q_star):
                print("  Q*_j = raiz(2*{:.6f}*{:.6f}/{:.6f}) = {:,.6f}".format(K, d, h, Q_star))
                if Q_star < qmin:
                    print("  Q*_j < qmin => se ajusta Q = qmin = {:,.6f}".format(qmin))
                else:
                    print("  Q*_j >= qmin => se usa Q = {:,.6f}".format(Q_star))
            else:
                print("  h ≈ 0 => Q*_j => inf (no hay óptimo finito), se usa Q = qmin = {:,.6f}".format(qmin))

            print("  T_j(Q) = (h*Q/2) + (K*d/Q) + (c*d)")
            print("          = ({:.6f}*{:,.6f}/2) + ({:.6f}*{:.6f}/{:,.6f}) + ({:.6f}*{:.6f})".format(
                h, Q, K, d, Q, c, d))
            print("          = ${:,.6f}  |  t* = {:.6f} años  |  N = {:.6f} órdenes/año\n".format(
                CT, t_ciclo, N))

        if (mejor is None) or (CT < mejor["CT_anual"]):
            mejor = candidato

    if mostrar_procedimiento:
        print("  Mejor alternativa encontrada:")
        print("  Tramo        : {}".format(mejor["tramo"]))
        print("  qmin         : {:,.6f}".format(mejor["qmin"]))
        print("  Precio c     : ${:,.6f}".format(mejor["c"]))
        print("  h = i*c      : {:.6f}".format(mejor["h"]))
        print("  Q* elegida   : {:,.6f} unidades".format(mejor["Q_elegida"]))
        print("  t*           : {:.6f} años  ({:.2f} días)".format(
            mejor["t_ciclo_anios"], mejor["t_ciclo_anios"] * 365))
        print("  N            : {:.6f} órdenes/año".format(mejor["pedidos_por_anio"]))
        print("  CT anual     : ${:,.6f}".format(mejor["CT_anual"]))
        print("-----------------------------------------------------------------------\n")

    return {"mejor": mejor, "candidatos": candidatos}


# ================================
# MODO INTERACTIVO (opcional)
# ================================
def _leer_breaks_interactivo():
    """
    Pide al usuario la cantidad de tramos y cada (qmin, c).
    Devuelve la lista de tuplas [(qmin, c), ...].
    """
    print("\nIngrese los tramos de descuentos (All-Units).")
    print("Ejemplo: si hay 3 tramos: (1, 10.0), (200, 9.5), (500, 9.0)")
    while True:
        try:
            n = int(input("¿Cuántos tramos de precio hay? (>=1): ").strip())
            if n >= 1:
                break
            print("Debe ser un entero >= 1.")
        except ValueError:
            print("Entrada no válida. Intente de nuevo.")
    tramos = []
    for k in range(1, n + 1):
        while True:
            try:
                qmin = float(input("  Tramo {} - qmin (cantidad mínima): ".format(k)).strip().replace(",", "."))
                c = float(input("  Tramo {} - precio unitario c ($/unidad): ".format(k)).strip().replace(",", "."))
                if qmin <= 0 or c <= 0:
                    print("  qmin y c deben ser > 0. Intente nuevamente.")
                    continue
                tramos.append((qmin, c))
                break
            except ValueError:
                print("  Entrada no válida. Intente nuevamente.")
    return tramos


if __name__ == "__main__":
    print("  EOQ con Descuentos por Cantidad (All-Units)\n")

    def _leer_float(msg):
        while True:
            s = input(msg).strip()
            try:
                return float(s.replace(",", "."))
            except ValueError:
                try:
                    return _parse_percent(s)
                except Exception:
                    print("  Valor no válido. Intente nuevamente (acepta '0.18' o '18%').")

    d = _leer_float("Demanda anual d (unidades/año): \n")
    K = _leer_float("Costo por pedido K ($/orden): \n")
    i = _leer_float("Tasa de mantenimiento i (ej. 0.20 o 20%): \n")
    tramos = _leer_breaks_interactivo()

    resultado = eoq_descuentos_all_units(d, K, i, tramos, mostrar_procedimiento=True)