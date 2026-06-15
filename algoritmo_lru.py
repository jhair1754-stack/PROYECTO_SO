def simular_lru(referencias, cantidad_marcos):
    # Simula el algoritmo LRU y retorna pasos, hits, fallos y reemplazos
    marcos = []
    ultima_referencia = {}
    pasos = []
    hits = 0
    fallos = 0
    reemplazos = 0

    for turno, pagina in enumerate(referencias):
        if pagina in marcos:
            # Hit: la pagina ya esta en memoria
            hits += 1
            ultima_referencia[pagina] = turno
            pasos.append({
                "turno": turno,
                "pagina": pagina,
                "es_fallo": False,
                "es_reemplazo": False,
            })
        else:
            # Fallo: la pagina no esta en memoria
            fallos += 1

            if len(marcos) < cantidad_marcos:
                marcos.insert(0, pagina)
                hubo_reemplazo = False
            else:
                # Reemplazo: se saca la victima (la menos reciente)
                victima = _encontrar_victima(marcos, ultima_referencia, turno)
                idx = marcos.index(victima)
                marcos = [pagina] + marcos[:idx] + marcos[idx + 1:]
                hubo_reemplazo = True
                reemplazos += 1

            ultima_referencia[pagina] = turno
            pasos.append({
                "turno": turno,
                "pagina": pagina,
                "marcos": list(marcos),
                "es_fallo": True,
                "es_reemplazo": hubo_reemplazo,
            })

    _calcular_distancias(pasos, referencias, cantidad_marcos)
    return pasos, hits, fallos, reemplazos


def _encontrar_victima(marcos, ultima_referencia, turno_actual):
    # Busca la pagina menos recientemente usada
    mayor_distancia = -1
    victima = None

    for pagina in marcos:
        distancia = turno_actual - ultima_referencia[pagina]
        if distancia > mayor_distancia:
            mayor_distancia = distancia
            victima = pagina

    return victima


def _calcular_distancias(pasos, referencias, cantidad_marcos):
    # Calcula las distancias para los subcuadraditos de cada columna
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
    # Busca la ultima vez que aparecio la pagina antes de cierto turno
    for j in range(hasta_turno, -1, -1):
        if referencias[j] == pagina:
            return j
    return 0
