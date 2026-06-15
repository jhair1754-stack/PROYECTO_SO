# Paleta de colores
COLORES = {
    "fondo_canvas":      "#1A1F26",
    "borde_celda":       "#C5A880",
    "relleno_celda":     "#1E2530",
    "texto_pagina":      "#E8DCC8",
    "texto_numero":      "#E0D6C2",
    "fallo_circulo":     "#E74C3C",
    "fallo_relleno":     "#3B1A1A",
    "hit_linea":         "#2ECC71",
    "hit_relleno":       "#1A3B2A",
    "subcuadro_borde":   "#C5A880",
    "subcuadro_relleno": "#2A2418",
    "subcuadro_texto":   "#FFD700",
    "etiqueta_mru":      "#5DADE2",
    "etiqueta_lru":      "#E74C3C",
    "separador":         "#C5A880",
    "titulo_secuencia":  "#8A7D6B",
    "reemplazo_triangulo": "#FFD700",
}

# Dimensiones de la tabla
ANCHO_CELDA = 65
ALTO_CELDA = 55
MARGEN_X = 90
MARGEN_Y = 110
ESPACIO_SECUENCIA = 42


class LRURenderer:

    def __init__(self, canvas, root):
        self.canvas = canvas
        self.root = root
        self._animacion_id = None

    def cancelar_animacion(self):
        if self._animacion_id is not None:
            self.root.after_cancel(self._animacion_id)
            self._animacion_id = None

    def iniciar_animacion(self, pasos, referencias, cantidad_marcos, al_terminar):
        self.cancelar_animacion()
        self.canvas.delete("all")
        self.canvas.configure(bg=COLORES["fondo_canvas"])

        self._dibujar_etiquetas_laterales(cantidad_marcos)
        self._dibujar_titulo_secuencia(pasos)

        columna_fallo = [0]

        def animar(paso_idx):
            if paso_idx >= len(pasos):
                self.canvas.config(scrollregion=self.canvas.bbox("all"))
                al_terminar()
                self._animacion_id = None
                return

            paso = pasos[paso_idx]
            self._dibujar_referencia_superior(paso, paso_idx)

            if paso["es_fallo"]:
                self._dibujar_columna_marcos(paso, columna_fallo[0], cantidad_marcos)
                columna_fallo[0] += 1

            self.canvas.config(scrollregion=self.canvas.bbox("all"))

            # Auto-scroll para ver el paso actual
            bbox = self.canvas.bbox("all")
            if bbox:
                self.canvas.config(scrollregion=bbox)
                x_visible = MARGEN_X + paso_idx * ESPACIO_SECUENCIA + 50
                total_w = bbox[2] - bbox[0]
                if total_w > 0:
                    self.canvas.xview_moveto(max(0, (x_visible - 300) / total_w))

            velocidad = 350 if paso["es_fallo"] else 200
            self._animacion_id = self.root.after(velocidad, animar, paso_idx + 1)

        animar(0)

    def _dibujar_etiquetas_laterales(self, cantidad_marcos):
        # Etiquetas MRU y LRU a la izquierda
        y_inicio = MARGEN_Y
        y_fin = MARGEN_Y + cantidad_marcos * ALTO_CELDA

        self.canvas.create_text(
            40, y_inicio + 15,
            text="MRU", font=("Consolas", 13, "bold"),
            fill=COLORES["etiqueta_mru"], anchor="w"
        )

        self.canvas.create_text(
            40, y_fin - 15,
            text="LRU", font=("Consolas", 13, "bold"),
            fill=COLORES["etiqueta_lru"], anchor="w"
        )

        # Flecha MRU -> LRU
        flecha_x = 50
        self.canvas.create_line(
            flecha_x, y_inicio + 30,
            flecha_x, y_fin - 30,
            fill=COLORES["separador"], width=2,
            arrow="last", arrowshape=(10, 12, 5)
        )

    def _dibujar_titulo_secuencia(self, pasos):
        self.canvas.create_text(
            MARGEN_X, 15,
            text="Secuencia de Referencias",
            font=("Segoe UI", 12, "bold"), fill=COLORES["titulo_secuencia"],
            anchor="w"
        )

    def _dibujar_referencia_superior(self, paso, paso_idx):
        # Dibuja la referencia arriba con circulo rojo (fallo) o linea verde (hit)
        x = MARGEN_X + paso_idx * ESPACIO_SECUENCIA
        y = 45

        if paso["es_fallo"]:
            self.canvas.create_oval(
                x - 16, y - 16, x + 16, y + 16,
                outline=COLORES["fallo_circulo"], width=2,
                fill=COLORES["fallo_relleno"]
            )
            color_texto = COLORES["fallo_circulo"]
        else:
            self.canvas.create_line(
                x - 12, y + 14, x + 12, y + 14,
                fill=COLORES["hit_linea"], width=3, capstyle="round"
            )
            color_texto = COLORES["hit_linea"]

        self.canvas.create_text(
            x, y,
            text=str(paso["pagina"]),
            font=("Consolas", 13, "bold"),
            fill=color_texto
        )

        # Mini etiqueta F o H debajo
        y_label = y + 28
        if paso["es_fallo"]:
            self.canvas.create_text(
                x, y_label, text="F",
                font=("Consolas", 8, "bold"),
                fill=COLORES["fallo_circulo"]
            )
            # Triangulo de reemplazo
            if paso.get("es_reemplazo"):
                ty = y_label + 12
                self.canvas.create_polygon(
                    x - 6, ty, x + 6, ty, x, ty + 8,
                    fill=COLORES["reemplazo_triangulo"],
                    outline=COLORES["reemplazo_triangulo"]
                )
        else:
            self.canvas.create_text(
                x, y_label, text="H",
                font=("Consolas", 8, "bold"),
                fill=COLORES["hit_linea"]
            )

    def _dibujar_columna_marcos(self, paso, columna_fallo, cantidad_marcos):
        # Dibuja una columna de marcos con los valores
        x = MARGEN_X + columna_fallo * ANCHO_CELDA

        for fila in range(cantidad_marcos):
            y = MARGEN_Y + fila * ALTO_CELDA

            # Celda
            self.canvas.create_rectangle(
                x + 1, y + 1,
                x + ANCHO_CELDA - 1, y + ALTO_CELDA - 1,
                outline=COLORES["borde_celda"], width=1,
                fill=COLORES["relleno_celda"]
            )

            if fila < len(paso.get("marcos", [])):
                valor = paso["marcos"][fila]

                # Resaltar la pagina nueva
                if fila == 0:
                    self.canvas.create_rectangle(
                        x + 2, y + 2,
                        x + ANCHO_CELDA - 2, y + ALTO_CELDA - 2,
                        outline=COLORES["fallo_circulo"], width=2,
                        fill="#2A1A1A"
                    )
                    color_num = "#FFD700"
                else:
                    color_num = COLORES["texto_numero"]

                self.canvas.create_text(
                    x + ANCHO_CELDA / 2, y + ALTO_CELDA / 2,
                    text=str(valor),
                    font=("Consolas", 16, "bold"),
                    fill=color_num
                )

                # Subcuadradito de distancia
                distancias = paso.get("distancias", [])
                if distancias and fila < len(distancias):
                    self._dibujar_subcuadro(x, y, distancias[fila])

    def _dibujar_subcuadro(self, x_celda, y_celda, valor):
        # Dibuja el numerito de distancia en la esquina de la celda
        sub_w = 22
        sub_h = 20
        sx = x_celda + ANCHO_CELDA - sub_w - 1
        sy = y_celda + ALTO_CELDA - sub_h - 1

        self.canvas.create_rectangle(
            sx, sy, sx + sub_w, sy + sub_h,
            outline=COLORES["subcuadro_borde"], width=1,
            fill=COLORES["subcuadro_relleno"]
        )
        self.canvas.create_text(
            sx + sub_w / 2, sy + sub_h / 2,
            text=str(valor),
            font=("Consolas", 9, "bold"),
            fill=COLORES["subcuadro_texto"]
        )
