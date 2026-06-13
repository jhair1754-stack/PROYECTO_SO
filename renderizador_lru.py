"""
Módulo de renderizado y animación para la tabla LRU.

Se encarga de dibujar paso a paso la tabla de reemplazo de páginas
sobre un Canvas de Tkinter, con animaciones suaves y visualización
clara de fallos de página, hits, marcos y subcuadraditos de distancia.
"""

# Paleta de colores para un estilo moderno y tecnológico
COLORES = {
    "fondo_canvas": "#0F172A",
    "borde_celda": "#334155",
    "relleno_celda": "#1E293B",
    "texto_pagina": "#F8FAFC",
    "texto_numero": "#E2E8F0",
    "fallo_circulo": "#EF4444",
    "fallo_relleno": "#7F1D1D",
    "hit_linea": "#22C55E",
    "hit_relleno": "#14532D",
    "subcuadro_borde": "#F59E0B",
    "subcuadro_relleno": "#78350F",
    "subcuadro_texto": "#FDE68A",
    "etiqueta_mru": "#3B82F6",
    "etiqueta_lru": "#EF4444",
    "separador": "#475569",
    "titulo_secuencia": "#94A3B8",
}

# Dimensiones de la tabla
ANCHO_CELDA = 65
ALTO_CELDA = 55
MARGEN_X = 90
MARGEN_Y = 110
ESPACIO_SECUENCIA = 42


class LRURenderer:
    """Renderiza y anima la simulación LRU en un Canvas de Tkinter."""

    def __init__(self, canvas, root):
        self.canvas = canvas
        self.root = root
        self._animacion_id = None

    def cancelar_animacion(self):
        """Cancela cualquier animación en progreso."""
        if self._animacion_id is not None:
            self.root.after_cancel(self._animacion_id)
            self._animacion_id = None

    def iniciar_animacion(self, pasos, referencias, cantidad_marcos, al_terminar):
        """
        Inicia la animación paso a paso de la simulación LRU.

        Parámetros:
            pasos: lista de columnas generada por simular_lru
            referencias: secuencia original de páginas
            cantidad_marcos: número de marcos de página
            al_terminar: callback que se llama al finalizar la animación
        """
        self.cancelar_animacion()
        self.canvas.delete("all")
        self.canvas.configure(bg=COLORES["fondo_canvas"])

        self._dibujar_etiquetas_laterales(cantidad_marcos)
        self._dibujar_titulo_secuencia(pasos)

        columna_fallo = [0]  # mutable counter

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

            # Auto-scroll para que se vea el paso actual
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
        """Dibuja las etiquetas MRU y LRU a la izquierda de la tabla."""
        y_inicio = MARGEN_Y
        y_fin = MARGEN_Y + cantidad_marcos * ALTO_CELDA

        # Etiqueta MRU (arriba)
        self.canvas.create_text(
            40, y_inicio + 15,
            text="MRU", font=("Consolas", 11, "bold"),
            fill=COLORES["etiqueta_mru"], anchor="w"
        )

        # Etiqueta LRU (abajo)
        self.canvas.create_text(
            40, y_fin - 15,
            text="LRU", font=("Consolas", 11, "bold"),
            fill=COLORES["etiqueta_lru"], anchor="w"
        )

        # Flecha decorativa MRU → LRU
        flecha_x = 50
        self.canvas.create_line(
            flecha_x, y_inicio + 30,
            flecha_x, y_fin - 30,
            fill=COLORES["separador"], width=2,
            arrow="last", arrowshape=(10, 12, 5)
        )

    def _dibujar_titulo_secuencia(self, pasos):
        """Dibuja un título sutil encima de la secuencia de referencias."""
        self.canvas.create_text(
            MARGEN_X, 15,
            text="Secuencia de Referencias",
            font=("Segoe UI", 9), fill=COLORES["titulo_secuencia"],
            anchor="w"
        )

    def _dibujar_referencia_superior(self, paso, paso_idx):
        """Dibuja la referencia de página en la parte superior con indicador visual."""
        x = MARGEN_X + paso_idx * ESPACIO_SECUENCIA
        y = 45

        if paso["es_fallo"]:
            # Círculo rojo con relleno semitransparente para fallo
            self.canvas.create_oval(
                x - 16, y - 16, x + 16, y + 16,
                outline=COLORES["fallo_circulo"], width=2,
                fill=COLORES["fallo_relleno"]
            )
            color_texto = COLORES["fallo_circulo"]
        else:
            # Subrayado verde para hit
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

        # Mini etiqueta F / H debajo
        y_label = y + 28
        if paso["es_fallo"]:
            self.canvas.create_text(
                x, y_label, text="F",
                font=("Consolas", 8, "bold"),
                fill=COLORES["fallo_circulo"]
            )
        else:
            self.canvas.create_text(
                x, y_label, text="H",
                font=("Consolas", 8, "bold"),
                fill=COLORES["hit_linea"]
            )

    def _dibujar_columna_marcos(self, paso, columna_fallo, cantidad_marcos):
        """Dibuja una columna de marcos con sus valores y subcuadraditos."""
        x = MARGEN_X + columna_fallo * ANCHO_CELDA

        for fila in range(cantidad_marcos):
            y = MARGEN_Y + fila * ALTO_CELDA

            # Celda con bordes redondeados simulados
            self.canvas.create_rectangle(
                x + 1, y + 1,
                x + ANCHO_CELDA - 1, y + ALTO_CELDA - 1,
                outline=COLORES["borde_celda"], width=1,
                fill=COLORES["relleno_celda"]
            )

            if fila < len(paso.get("marcos", [])):
                valor = paso["marcos"][fila]

                # Resaltar la página nueva que acaba de entrar
                if fila == 0:
                    self.canvas.create_rectangle(
                        x + 2, y + 2,
                        x + ANCHO_CELDA - 2, y + ALTO_CELDA - 2,
                        outline=COLORES["fallo_circulo"], width=2,
                        fill="#1C1917"
                    )
                    color_num = "#FBBF24"
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
        """Dibuja el subcuadradito de distancia dentro de una celda."""
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
