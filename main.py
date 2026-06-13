import tkinter as tk
from tkinter import ttk, messagebox


# =====================================================
# ALGORITMO LRU TIPO PILA (STACK)
# =====================================================

def ejecutar_lru():

    try:

        cantidad_marcos = int(entry_marcos.get())

        referencias = list(
            map(
                int,
                entry_paginas.get().split()
            )
        )

        # Limpiar dibujo anterior
        canvas.delete("all")

        pila = []

        historial = []

        hits = 0
        fallos = 0

        # ----------------------------------
        # Simulación LRU estilo profesor
        # ----------------------------------

        for pagina in referencias:

            eliminado = ""

            if pagina in pila:

                hits += 1

                pila.remove(pagina)

                pila.insert(0, pagina)

                estado = "HIT"

            else:

                fallos += 1

                estado = "FAULT"

                if len(pila) == cantidad_marcos:

                    eliminado = pila.pop(-1)

                pila.insert(0, pagina)

            snapshot = pila.copy()

            while len(snapshot) < cantidad_marcos:
                snapshot.append("")

            historial.append(
                {
                    "pila": snapshot,
                    "estado": estado,
                    "pagina": pagina,
                    "eliminado": eliminado
                }
            )

        # ----------------------------------
        # DIBUJO
        # ----------------------------------

        ancho_celda = 60
        alto_celda = 50

        margen_x = 80
        margen_y = 70

        # Título MRU
        canvas.create_text(
            40,
            margen_y,
            text="MRU",
            font=("Segoe UI", 12, "bold"),
            fill="#2563EB"
        )

        # Dibujar columnas
        for col, paso in enumerate(historial):

            x = margen_x + col * ancho_celda

            # Página referenciada
            canvas.create_text(
                x + ancho_celda / 2,
                25,
                text=str(paso["pagina"]),
                font=("Segoe UI", 14, "bold")
            )

            # HIT o FAULT
            color = "#16A34A" if paso["estado"] == "HIT" else "#DC2626"

            canvas.create_text(
                x + ancho_celda / 2,
                50,
                text="H" if paso["estado"] == "HIT" else "F",
                fill=color,
                font=("Segoe UI", 10, "bold")
            )

            for fila in range(cantidad_marcos):

                y = margen_y + fila * alto_celda

                valor = paso["pila"][fila]

                canvas.create_rectangle(
                    x,
                    y,
                    x + ancho_celda,
                    y + alto_celda,
                    outline="#CBD5E1",
                    width=1
                )

                if valor != "":

                    canvas.create_text(
                        x + ancho_celda / 2,
                        y + alto_celda / 2,
                        text=str(valor),
                        font=("Consolas", 16, "bold")
                    )

        # Etiqueta LRU
        canvas.create_text(
            40,
            margen_y + cantidad_marcos * alto_celda - 10,
            text="LRU",
            font=("Segoe UI", 12, "bold"),
            fill="#DC2626"
        )

        # ----------------------------------
        # RESUMEN
        # ----------------------------------

        porcentaje_hits = hits * 100 / len(referencias)
        porcentaje_fallos = fallos * 100 / len(referencias)

        lbl_hits.config(
            text=f"✅ Hits: {hits} ({porcentaje_hits:.2f}%)"
        )

        lbl_fallos.config(
            text=f"❌ Fallos: {fallos} ({porcentaje_fallos:.2f}%)"
        )

        lbl_total.config(
            text=f"📄 Referencias: {len(referencias)}"
        )

        canvas.config(
            scrollregion=canvas.bbox("all")
        )

    except ValueError:

        messagebox.showerror(
            "Error",
            "Ingrese datos válidos."
        )


# =====================================================
# VENTANA
# =====================================================

ventana = tk.Tk()

ventana.title(
    "Simulador LRU - Método del Profesor"
)

ventana.geometry("1400x800")

ventana.configure(bg="#F4F6F8")

# =====================================================
# ESTILOS
# =====================================================

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Titulo.TLabel",
    font=("Segoe UI", 20, "bold")
)

# =====================================================
# TÍTULO
# =====================================================

ttk.Label(
    ventana,
    text="Simulador LRU (Pila de Recencia)",
    style="Titulo.TLabel"
).pack(pady=15)

# =====================================================
# DATOS
# =====================================================

frame_datos = ttk.LabelFrame(
    ventana,
    text="Datos de Entrada"
)

frame_datos.pack(
    fill="x",
    padx=15,
    pady=10
)

ttk.Label(
    frame_datos,
    text="Cantidad de marcos:"
).grid(
    row=0,
    column=0,
    padx=10,
    pady=10
)

entry_marcos = ttk.Entry(
    frame_datos,
    width=15
)

entry_marcos.grid(
    row=0,
    column=1
)

entry_marcos.insert(
    0,
    "4"
)

ttk.Label(
    frame_datos,
    text="Secuencia:"
).grid(
    row=1,
    column=0,
    padx=10,
    pady=10
)

entry_paginas = ttk.Entry(
    frame_datos,
    width=90
)

entry_paginas.grid(
    row=1,
    column=1
)

entry_paginas.insert(
    0,
    "0 1 3 4 5 0 1 3 4 2 8 3 2"
)

ttk.Button(
    frame_datos,
    text="▶ Ejecutar LRU",
    command=ejecutar_lru
).grid(
    row=2,
    column=0,
    columnspan=2,
    pady=10
)

# =====================================================
# RESULTADO
# =====================================================

frame_resultado = ttk.LabelFrame(
    ventana,
    text="Visualización MRU → LRU"
)

frame_resultado.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=10
)

scroll_x = ttk.Scrollbar(
    frame_resultado,
    orient="horizontal"
)

scroll_y = ttk.Scrollbar(
    frame_resultado,
    orient="vertical"
)

canvas = tk.Canvas(
    frame_resultado,
    bg="white",
    xscrollcommand=scroll_x.set,
    yscrollcommand=scroll_y.set
)

scroll_x.config(command=canvas.xview)
scroll_y.config(command=canvas.yview)

scroll_x.pack(side="bottom", fill="x")
scroll_y.pack(side="right", fill="y")

canvas.pack(
    fill="both",
    expand=True
)

# =====================================================
# ESTADÍSTICAS
# =====================================================

frame_estadisticas = ttk.LabelFrame(
    ventana,
    text="Estadísticas"
)

frame_estadisticas.pack(
    fill="x",
    padx=15,
    pady=10
)

lbl_hits = ttk.Label(
    frame_estadisticas,
    text="✅ Hits: 0",
    font=("Segoe UI", 11, "bold")
)

lbl_hits.pack(
    side="left",
    padx=20
)

lbl_fallos = ttk.Label(
    frame_estadisticas,
    text="❌ Fallos: 0",
    font=("Segoe UI", 11, "bold")
)

lbl_fallos.pack(
    side="left",
    padx=20
)

lbl_total = ttk.Label(
    frame_estadisticas,
    text="📄 Referencias: 0",
    font=("Segoe UI", 11, "bold")
)

lbl_total.pack(
    side="left",
    padx=20
)

# Ejecutar ejemplo inicial
ejecutar_lru()

ventana.mainloop()