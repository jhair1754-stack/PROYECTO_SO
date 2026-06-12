import tkinter as tk
from tkinter import ttk, messagebox


def ejecutar_lru():
    try:
        cantidad_marcos = int(entry_marcos.get())
        referencias = list(map(int, entry_paginas.get().split()))

        marcos = []
        fallos = 0

        resultado.config(state="normal")
        resultado.delete("1.0", tk.END)

        resultado.insert(
            tk.END,
            f"{'PÁGINA':^10}{'ESTADO':^15}{'MARCOS':^30}\n",
            "titulo_tabla"
        )

        resultado.insert(
            tk.END,
            "-" * 60 + "\n"
        )

        for pagina in referencias:

            if pagina in marcos:
                marcos.remove(pagina)
                marcos.append(pagina)
                estado = "HIT"
                tag = "hit"

            else:
                fallos += 1

                if len(marcos) < cantidad_marcos:
                    marcos.append(pagina)
                else:
                    marcos.pop(0)
                    marcos.append(pagina)

                estado = "FAULT"
                tag = "fault"

            resultado.insert(
                tk.END,
                f"{pagina:^10}{estado:^15}{str(marcos):^30}\n",
                tag
            )

        resultado.insert(
            tk.END,
            "\n" + "=" * 60 + "\n",
            "titulo_tabla"
        )

        resultado.insert(
            tk.END,
            f"Total de fallos de página: {fallos}\n",
            "resumen"
        )

        resultado.config(state="disabled")

    except ValueError:
        messagebox.showerror(
            "Error",
            "Ingrese datos válidos."
        )


# ------------------ VENTANA ------------------

ventana = tk.Tk()
ventana.title("Simulador LRU")
ventana.geometry("850x600")
ventana.configure(bg="#F4F6F8")

# Estilo moderno
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Titulo.TLabel",
    font=("Segoe UI", 18, "bold"),
    background="#F4F6F8",
    foreground="#1F2937"
)

style.configure(
    "Texto.TLabel",
    font=("Segoe UI", 11),
    background="#F4F6F8"
)

style.configure(
    "Boton.TButton",
    font=("Segoe UI", 11, "bold"),
    padding=8
)

# Título
ttk.Label(
    ventana,
    text="Simulador de Reemplazo de Página LRU",
    style="Titulo.TLabel"
).pack(pady=15)

# Frame principal
frame = ttk.Frame(ventana, padding=15)
frame.pack(fill="x")

# Marcos
ttk.Label(
    frame,
    text="Cantidad de marcos:",
    style="Texto.TLabel"
).grid(row=0, column=0, sticky="w", pady=5)

entry_marcos = ttk.Entry(frame, width=20)
entry_marcos.grid(row=0, column=1, padx=10)

# Referencias
ttk.Label(
    frame,
    text="Secuencia de páginas:",
    style="Texto.TLabel"
).grid(row=1, column=0, sticky="w", pady=5)

entry_paginas = ttk.Entry(frame, width=50)
entry_paginas.grid(row=1, column=1, padx=10)

# Botón
ttk.Button(
    ventana,
    text="▶ Ejecutar LRU",
    style="Boton.TButton",
    command=ejecutar_lru
).pack(pady=10)

# Frame resultados
frame_resultado = ttk.LabelFrame(
    ventana,
    text=" Resultado de la simulación "
)
frame_resultado.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=10
)

scroll = ttk.Scrollbar(frame_resultado)
scroll.pack(side="right", fill="y")

resultado = tk.Text(
    frame_resultado,
    font=("Consolas", 11),
    bg="#FFFFFF",
    fg="#111827",
    yscrollcommand=scroll.set
)

resultado.pack(fill="both", expand=True)

scroll.config(command=resultado.yview)

# Colores de texto
resultado.tag_config(
    "hit",
    foreground="#16A34A"
)

resultado.tag_config(
    "fault",
    foreground="#DC2626"
)

resultado.tag_config(
    "titulo_tabla",
    foreground="#2563EB",
    font=("Consolas", 11, "bold")
)

resultado.tag_config(
    "resumen",
    foreground="#7C3AED",
    font=("Consolas", 12, "bold")
)

ventana.mainloop()
