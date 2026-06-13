"""
Módulo de simulación del algoritmo LRU (Least Recently Used).

Contiene la lógica pura del algoritmo de reemplazo de páginas,
sin dependencia de interfaz gráfica.
"""


def simular_lru(referencias, cantidad_marcos):
    """
    Ejecuta la simulación LRU sobre una secuencia de referencias a páginas.

    Retorna una lista de pasos (columnas), el total de hits y el total de fallos.
    Cada paso contiene la página referenciada, si fue fallo o hit, y el estado
    actual de los marcos (solo en fallos).
    """
    marcos = []
    ultima_referencia = {}
    pasos = []
    hits = 0
    fallos = 0

    for turno, pagina in enumerate(referencias):
        if pagina in marcos:
            hits += 1
            ultima_referencia[pagina] = turno
            pasos.append({
                "turno": turno,
                "pagina": pagina,
                "es_fallo": False,
            })
        else:
            fallos += 1

            if len(marcos) < cantidad_marcos:
                marcos.insert(0, pagina)
            else:
                victima = _encontrar_victima(marcos, ultima_referencia, turno)
                idx = marcos.index(victima)
                marcos = [pagina] + marcos[:idx] + marcos[idx + 1:]

            ultima_referencia[pagina] = turno
            pasos.append({
                "turno": turno,
                "pagina": pagina,
                "marcos": list(marcos),
                "es_fallo": True,
            })

    _calcular_distancias(pasos, referencias, cantidad_marcos)
    return pasos, hits, fallos


def _encontrar_victima(marcos, ultima_referencia, turno_actual):
    """Encuentra la página menos recientemente usada entre los marcos."""
    mayor_distancia = -1
    victima = None

    for pagina in marcos:
        distancia = turno_actual - ultima_referencia[pagina]
        if distancia > mayor_distancia:
            mayor_distancia = distancia
            victima = pagina

    return victima


def _calcular_distancias(pasos, referencias, cantidad_marcos):
    """
    Calcula los subcuadraditos de distancia para cada columna de fallo.

    Para cada fallo (excepto el último), se mide cuántos turnos han pasado
    desde la última referencia de cada página en el marco, evaluado justo
    antes del siguiente fallo. Esto muestra visualmente por qué se elige
    esa víctima.
    """
    columnas_fallo = [p for p in pasos if p["es_fallo"]]

    for i, columna in enumerate(columnas_fallo):
        if i < len(columnas_fallo) - 1 and len(columna["marcos"]) == cantidad_marcos:
            turno_proximo_fallo = columnas_fallo[i + 1]["turno"]
            distancias = []

            for pagina_marco in columna["marcos"]:
                ultima_pos = _buscar_ultima_posicion(
                    referencias, pagina_marco, turno_proximo_fallo - 1
                )
                distancias.append(turno_proximo_fallo - ultima_pos)

            columna["distancias"] = distancias
        else:
            columna["distancias"] = []


def _buscar_ultima_posicion(referencias, pagina, hasta_turno):
    """Busca la última posición de una página en la secuencia hasta un turno dado."""
    for j in range(hasta_turno, -1, -1):
        if referencias[j] == pagina:
            return j
    return 0
