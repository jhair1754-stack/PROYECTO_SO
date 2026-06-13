import tkinter as tk
from tkinter import ttk, messagebox


def ejecutar_lru():

    try:

        cantidad_marcos = int(entry_marcos.get())
        referencias = list(map(int, entry_paginas.get().split()))

        # Limpiar simulación anterior
        for widget in frame_matriz.winfo_children():
            widget.destroy()

        marcos = []
        historial = []

        hits = 0
        fallos = 0

        # -------------------------
        # Simulación LRU
        # -------------------------

        for pagina in referencias:

            hit = False

            pila_lru = []

            if pagina in pila_lru:

                # HIT
                pila_lru.remove(pagina)
                pila_lru.insert(0, pagina)

            else:

                # FAULT

                if len(pila_lru) == cantidad_marcos:
                    pagina_eliminada = pila_lru.pop(-1)

                pila_lru.insert(0, pagina)

            estado = marcos.copy()

            while len(estado) < cantidad_marcos:
                estado.insert(0, "")

            historial.append(
                {
                    "marcos": estado.copy(),
                    "hit": hit
                }
            )

        # -------------------------
        # Dibujar matriz
        # -------------------------

        ancho = 45
        alto = 40

        for fila in range(cantidad_marcos):

            for columna in range(len(historial)):

                valor = historial[columna]["marcos"][fila]

                color = "#FFFFFF"

                if valor != "":
                    color = "#F8FAFC"

                lbl = tk.Label(
                    frame_matriz,
                    text=str(valor),
                    width=3,
                    height=1,
                    font=("Consolas", 18, "bold"),
                    bg=color,
                    relief="flat"
                )

                lbl.grid(
                    row=fila,
                    column=columna,
                    padx=2,
                    pady=2
                )

        # -------------------------
        # Estadísticas
        # -------------------------

        porcentaje_fallos = (fallos / len(referencias)) * 100
        porcentaje_hits = (hits / len(referencias)) * 100

        lbl_hits.config(
            text=f"✅ Hits: {hits} ({porcentaje_hits:.2f}%)"
        )

        lbl_fallos.config(
            text=f"❌ Fallos: {fallos} ({porcentaje_fallos:.2f}%)"
        )

        lbl_total.config(
            text=f"📄 Referencias: {len(referencias)}"
        )

    except ValueError:

        messagebox.showerror(
            "Error",
            "Ingrese valores válidos."
        )


# ==================================================
# VENTANA
# ==================================================

ventana = tk.Tk()

ventana.title(
    "Simulador LRU"
)

ventana.geometry("1400x700")

ventana.configure(
    bg="#F4F6F8"
)

# ==================================================
# ESTILOS
# ==================================================

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Titulo.TLabel",
    font=("Segoe UI", 20, "bold")
)

style.configure(
    "Boton.TButton",
    font=("Segoe UI", 11, "bold")
)

# ==================================================
# TITULO
# ==================================================

ttk.Label(
    ventana,
    text="Simulador de Reemplazo de Página LRU",
    style="Titulo.TLabel"
).pack(
    pady=15
)

# ==================================================
# ENTRADA
# ==================================================

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
    "3"
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
    width=80
)

entry_paginas.grid(
    row=1,
    column=1
)

entry_paginas.insert(
    0,
    "1 2 3 1 4 2 5 1 2 3 4 5"
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

# ==================================================
# RESULTADO
# ==================================================

frame_resultado = ttk.LabelFrame(
    ventana,
    text="Visualización Tipo Escalera"
)

frame_resultado.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=10
)

canvas = tk.Canvas(
    frame_resultado,
    bg="white"
)

scroll_x = ttk.Scrollbar(
    frame_resultado,
    orient="horizontal",
    command=canvas.xview
)

canvas.configure(
    xscrollcommand=scroll_x.set
)

scroll_x.pack(
    side="bottom",
    fill="x"
)

canvas.pack(
    fill="both",
    expand=True
)

frame_matriz = tk.Frame(
    canvas,
    bg="white"
)

canvas.create_window(
    (0, 0),
    window=frame_matriz,
    anchor="nw"
)

frame_matriz.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

# ==================================================
# ESTADÍSTICAS
# ==================================================

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