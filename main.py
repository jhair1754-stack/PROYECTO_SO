import tkinter as tk
from tkinter import ttk, messagebox


def ejecutar_lru():

    try:

        cantidad_marcos = int(entry_marcos.get())

        referencias = list(
            map(
                int,
                entry_paginas.get().split()
            )
        )

        # ---------------------------
        # Limpiar tabla anterior
        # ---------------------------

        for item in tabla.get_children():
            tabla.delete(item)

        columnas = ["Marco"]

        for i in range(len(referencias)):
            columnas.append(str(i + 1))

        tabla["columns"] = columnas

        tabla.column("#0", width=0, stretch=False)

        for col in columnas:

            if col == "Marco":

                tabla.heading(
                    col,
                    text="Marco"
                )

                tabla.column(
                    col,
                    width=90,
                    anchor="center"
                )

            else:

                indice = int(col) - 1

                tabla.heading(
                    col,
                    text=str(referencias[indice])
                )

                tabla.column(
                    col,
                    width=60,
                    anchor="center"
                )

        # ---------------------------
        # Simulación LRU
        # ---------------------------

        marcos = []
        historial = []

        hits = 0
        fallos = 0

        for pagina in referencias:

            if pagina in marcos:

                marcos.remove(pagina)
                marcos.append(pagina)

                hits += 1

            else:

                fallos += 1

                if len(marcos) < cantidad_marcos:

                    marcos.append(pagina)

                else:

                    marcos.pop(0)
                    marcos.append(pagina)

            estado = marcos.copy()

            while len(estado) < cantidad_marcos:
                estado.insert(0, "")

            historial.append(estado.copy())

        # ---------------------------
        # Construcción de la matriz
        # ---------------------------

        for fila in range(cantidad_marcos):

            valores = [f"Marco {fila}"]

            for instante in historial:
                valores.append(instante[fila])

            tabla.insert(
                "",
                "end",
                values=valores
            )

        # ---------------------------
        # Estadísticas
        # ---------------------------

        porcentaje_fallos = (
            fallos / len(referencias)
        ) * 100

        porcentaje_hits = (
            hits / len(referencias)
        ) * 100

        lbl_hits.config(
            text=f"✅ Hits: {hits} ({porcentaje_hits:.2f}%)"
        )

        lbl_fallos.config(
            text=f"❌ Fallos: {fallos} ({porcentaje_fallos:.2f}%)"
        )

        lbl_total.config(
            text=f"📄 Referencias procesadas: {len(referencias)}"
        )

    except ValueError:

        messagebox.showerror(
            "Error",
            "Ingrese valores válidos."
        )


# =====================================================
# VENTANA PRINCIPAL
# =====================================================

ventana = tk.Tk()

ventana.title(
    "Simulador LRU - Least Recently Used"
)

ventana.geometry("1200x700")

ventana.configure(
    bg="#F4F6F8"
)

# =====================================================
# ESTILOS
# =====================================================

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Titulo.TLabel",
    font=("Segoe UI", 20, "bold"),
)

style.configure(
    "Texto.TLabel",
    font=("Segoe UI", 11),
)

style.configure(
    "Boton.TButton",
    font=("Segoe UI", 11, "bold"),
    padding=8
)

# =====================================================
# TITULO
# =====================================================

ttk.Label(
    ventana,
    text="Simulador de Reemplazo de Página LRU",
    style="Titulo.TLabel"
).pack(
    pady=15
)

# =====================================================
# PANEL DE ENTRADA
# =====================================================

frame_entrada = ttk.LabelFrame(
    ventana,
    text=" Datos de Entrada "
)

frame_entrada.pack(
    fill="x",
    padx=15,
    pady=10
)

# Marcos

ttk.Label(
    frame_entrada,
    text="Cantidad de marcos:",
    style="Texto.TLabel"
).grid(
    row=0,
    column=0,
    padx=10,
    pady=10,
    sticky="w"
)

entry_marcos = ttk.Entry(
    frame_entrada,
    width=20
)

entry_marcos.grid(
    row=0,
    column=1,
    padx=10
)

entry_marcos.insert(
    0,
    "3"
)

# Secuencia

ttk.Label(
    frame_entrada,
    text="Secuencia de páginas:",
    style="Texto.TLabel"
).grid(
    row=1,
    column=0,
    padx=10,
    pady=10,
    sticky="w"
)

entry_paginas = ttk.Entry(
    frame_entrada,
    width=80
)

entry_paginas.grid(
    row=1,
    column=1,
    padx=10
)

entry_paginas.insert(
    0,
    "1 2 3 4 2 5 1 3 4 5"
)

# Botón

ttk.Button(
    frame_entrada,
    text="▶ Ejecutar Simulación LRU",
    style="Boton.TButton",
    command=ejecutar_lru
).grid(
    row=2,
    column=0,
    columnspan=2,
    pady=15
)

# =====================================================
# RESULTADOS
# =====================================================

frame_resultado = ttk.LabelFrame(
    ventana,
    text=" Evolución de los Marcos de Memoria "
)

frame_resultado.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=10
)

# Scrolls

scroll_y = ttk.Scrollbar(
    frame_resultado,
    orient="vertical"
)

scroll_x = ttk.Scrollbar(
    frame_resultado,
    orient="horizontal"
)

tabla = ttk.Treeview(
    frame_resultado,
    show="headings",
    yscrollcommand=scroll_y.set,
    xscrollcommand=scroll_x.set
)

scroll_y.config(
    command=tabla.yview
)

scroll_x.config(
    command=tabla.xview
)

scroll_y.pack(
    side="right",
    fill="y"
)

scroll_x.pack(
    side="bottom",
    fill="x"
)

tabla.pack(
    fill="both",
    expand=True
)

# =====================================================
# ESTADÍSTICAS
# =====================================================

frame_estadisticas = ttk.LabelFrame(
    ventana,
    text=" Estadísticas "
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
    padx=20,
    pady=10
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
    text="📄 Referencias procesadas: 0",
    font=("Segoe UI", 11, "bold")
)

lbl_total.pack(
    side="left",
    padx=20
)

# =====================================================
# EJECUTAR EJEMPLO AL INICIO
# =====================================================

ejecutar_lru()

ventana.mainloop()