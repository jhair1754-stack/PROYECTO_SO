import tkinter as tk
from tkinter import ttk, messagebox


def ejecutar_lru():
    try:
        cantidad_marcos = int(entry_marcos.get())
        referencias = list(map(int, entry_paginas.get().split()))

        marcos = []
        fallos = 0

        resultado.delete("1.0", tk.END)

        resultado.insert(tk.END, f"Marcos: {cantidad_marcos}\n")
        resultado.insert(tk.END, f"Referencias: {referencias}\n\n")

        for pagina in referencias:

            if pagina in marcos:
                marcos.remove(pagina)
                marcos.append(pagina)
                estado = "HIT"

            else:
                fallos += 1

                if len(marcos) < cantidad_marcos:
                    marcos.append(pagina)
                else:
                    marcos.pop(0)
                    marcos.append(pagina)

                estado = "FAULT"

            resultado.insert(
                tk.END,
                f"Página: {pagina:>3} | {estado:>5} | Marcos: {marcos}\n"
            )

        resultado.insert(
            tk.END,
            f"\nTotal de fallos de página: {fallos}"
        )

    except ValueError:
        messagebox.showerror(
            "Error",
            "Ingrese datos válidos."
        )


# Ventana principal
ventana = tk.Tk()
ventana.title("Simulador LRU")
ventana.geometry("700x500")

# Cantidad de marcos
ttk.Label(
    ventana,
    text="Cantidad de marcos:"
).pack(pady=5)

entry_marcos = ttk.Entry(ventana)
entry_marcos.pack()

# Secuencia de páginas
ttk.Label(
    ventana,
    text="Secuencia de páginas (separadas por espacios):"
).pack(pady=5)

entry_paginas = ttk.Entry(ventana, width=50)
entry_paginas.pack()

# Botón
ttk.Button(
    ventana,
    text="Ejecutar LRU",
    command=ejecutar_lru
).pack(pady=10)

# Área de resultados
resultado = tk.Text(
    ventana,
    width=80,
    height=20
)
resultado.pack(pady=10)

ventana.mainloop()
