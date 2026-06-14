"""
Simulador LRU — Punto de entrada principal.

Construye la ventana con un diseño Premium Dark & Gold,
conecta los datos de entrada con el algoritmo LRU y el renderizador
de animación.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from algoritmo_lru import simular_lru
from renderizador_lru import LRURenderer, COLORES


# ─── Colores de la interfaz ──────────────────────────────────────────────────

BG_PRINCIPAL = "#0D0D0D"
BG_PANEL     = "#121212"
FG_TEXTO     = "#D4B996"
FG_TITULO    = "#C5A880"
FG_ACENTO    = "#C5A880"
FG_BOTON     = "#B8963E"
FG_HIT       = "#2ECC71"
FG_FALLO     = "#E74C3C"


class LRUSimulatorApp:
    """Aplicación principal del simulador LRU."""

    def __init__(self, root):
        self.root = root
        self.root.title("Simulador LRU — Reemplazo de Páginas")
        self.root.geometry("1400x820")
        self.root.configure(bg=BG_PRINCIPAL)
        self.root.minsize(900, 600)

        self._configurar_estilos()
        self._construir_interfaz()

        self.renderer = LRURenderer(self.canvas, self.root)

    # ── Estilos ──────────────────────────────────────────────────────────────

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(".", background=BG_PRINCIPAL, foreground=FG_TEXTO)
        style.configure("Titulo.TLabel",
                         font=("Segoe UI", 22, "bold"),
                         foreground=FG_TITULO,
                         background=BG_PRINCIPAL)
        style.configure("Subtitulo.TLabel",
                         font=("Segoe UI", 10),
                         foreground="#8A7D6B",
                         background=BG_PRINCIPAL)
        style.configure("TLabelFrame",
                         background=BG_PANEL,
                         foreground=FG_TEXTO,
                         borderwidth=2,
                         relief="groove")
        style.configure("TLabelFrame.Label",
                         background=BG_PANEL,
                         foreground=FG_ACENTO,
                         font=("Segoe UI", 13, "bold"))
        style.configure("TLabel",
                         background=BG_PANEL,
                         foreground=FG_TEXTO,
                         font=("Segoe UI", 11))
        style.configure("TEntry",
                         fieldbackground="#252A34",
                         foreground="#E0D6C2",
                         insertcolor="#E0D6C2",
                         font=("Consolas", 11))
        style.configure("Ejecutar.TButton",
                         font=("Segoe UI", 11, "bold"),
                         background=FG_BOTON,
                         foreground="#0D0D0D",
                         padding=(20, 18))
        style.map("Ejecutar.TButton",
                   background=[("active", "#D4AA4F"), ("disabled", "#3A3A3A")])
        style.configure("Stats.TLabel",
                         background="#0A0A0A",
                         foreground="#E0D6C2",
                         font=("Consolas", 12, "bold"))
        # Scrollbar oscuro
        style.configure("TScrollbar",
                         background="#1A1F26",
                         troughcolor="#0D0D0D",
                         arrowcolor="#C5A880")
        # Panel de estadísticas oscuro
        style.configure("Stats.TLabelframe",
                         background="#0A0A0A",
                         foreground="#D4B996",
                         borderwidth=2,
                         relief="groove")
        style.configure("Stats.TLabelframe.Label",
                         background="#0A0A0A",
                         foreground="#C5A880",
                         font=("Segoe UI", 13, "bold"))

    # ── Construcción de la interfaz ──────────────────────────────────────────

    def _construir_interfaz(self):
        # Título
        ttk.Label(
            self.root,
            text="⚙  Simulador LRU",
            style="Titulo.TLabel"
        ).pack(pady=(18, 2))

        ttk.Label(
            self.root,
            text="Algoritmo de Reemplazo de Páginas — Least Recently Used",
            style="Subtitulo.TLabel"
        ).pack(pady=(0, 12))

        # Panel de datos de entrada
        frame_datos = ttk.LabelFrame(self.root, text="  Datos de Entrada  ")
        frame_datos.pack(fill="x", padx=20, pady=(0, 8))

        ttk.Label(frame_datos, text="Marcos de página:").grid(
            row=0, column=0, padx=(15, 8), pady=10, sticky="e")
        self.entry_marcos = ttk.Entry(frame_datos, width=10)
        self.entry_marcos.grid(row=0, column=1, padx=(0, 30), pady=10, sticky="w")
        self.entry_marcos.insert(0, "4")

        ttk.Label(frame_datos, text="Secuencia de referencias:").grid(
            row=0, column=2, padx=(0, 8), pady=10, sticky="e")
        self.entry_paginas = ttk.Entry(frame_datos, width=60)
        self.entry_paginas.grid(row=0, column=3, padx=(0, 15), pady=10, sticky="w")
        self.entry_paginas.insert(0, "0 1 3 2 1 5 0 3 4 6 4 1 2 5 3 2")

        self.btn_ejecutar = ttk.Button(
            frame_datos,
            text="▶  Ejecutar LRU",
            style="Ejecutar.TButton",
            command=self._ejecutar
        )
        self.btn_ejecutar.grid(row=0, column=4, padx=(15, 10), pady=10, sticky="ns")

        # Sub-contenedor vertical para indicadores de resultado
        frame_indicadores = tk.Frame(frame_datos, bg=BG_PANEL)
        frame_indicadores.grid(row=0, column=5, padx=(5, 15), pady=8, sticky="w")

        # Fila superior: Fallos de Página
        row_fallos = tk.Frame(frame_indicadores, bg=BG_PANEL)
        row_fallos.pack(anchor="w", pady=(0, 4))

        tk.Label(
            row_fallos, text="Fallos de Página:",
            font=("Segoe UI", 9, "bold"), fg="#C5A880", bg=BG_PANEL
        ).pack(side="left", padx=(0, 6))

        self.entry_fallos_resultado = tk.Entry(
            row_fallos, width=6, state="readonly",
            font=("Consolas", 14, "bold"), justify="center",
            readonlybackground="#121212", fg="#FFE600",
            highlightthickness=1, highlightcolor="#C5A880",
            relief="flat", bd=2
        )
        self.entry_fallos_resultado.pack(side="left")

        # Fila inferior: Reemplazos de Página
        row_reemplazos = tk.Frame(frame_indicadores, bg=BG_PANEL)
        row_reemplazos.pack(anchor="w", pady=(0, 0))

        tk.Label(
            row_reemplazos, text="Reemplazos de Página:",
            font=("Segoe UI", 9, "bold"), fg="#C5A880", bg=BG_PANEL
        ).pack(side="left", padx=(0, 6))

        self.entry_reemplazos_resultado = tk.Entry(
            row_reemplazos, width=6, state="readonly",
            font=("Consolas", 14, "bold"), justify="center",
            readonlybackground="#121212", fg="#FFE600",
            highlightthickness=1, highlightcolor="#C5A880",
            relief="flat", bd=2
        )
        self.entry_reemplazos_resultado.pack(side="left")

        # Canvas de visualización
        frame_visual = ttk.LabelFrame(self.root, text="  Visualización Animada  ")
        frame_visual.pack(fill="both", expand=True, padx=20, pady=(0, 8))

        scroll_x = ttk.Scrollbar(frame_visual, orient="horizontal")
        scroll_y = ttk.Scrollbar(frame_visual, orient="vertical")

        self.canvas = tk.Canvas(
            frame_visual,
            bg=COLORES["fondo_canvas"],
            highlightthickness=0,
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        scroll_x.config(command=self.canvas.xview)
        scroll_y.config(command=self.canvas.yview)
        scroll_x.pack(side="bottom", fill="x")
        scroll_y.pack(side="right", fill="y")
        self.canvas.pack(fill="both", expand=True)

        # Panel de estadísticas
        frame_stats = ttk.LabelFrame(self.root, text="  Estadísticas  ",
                                      style="Stats.TLabelframe")
        frame_stats.pack(fill="x", padx=20, pady=(0, 12))

        self.lbl_hits = ttk.Label(frame_stats, text="✅  Hits: —", style="Stats.TLabel")
        self.lbl_hits.pack(side="left", padx=25, pady=8)

        self.lbl_fallos = ttk.Label(frame_stats, text="❌  Fallos: —", style="Stats.TLabel")
        self.lbl_fallos.pack(side="left", padx=25, pady=8)

        self.lbl_total = ttk.Label(frame_stats, text="📄  Total: —", style="Stats.TLabel")
        self.lbl_total.pack(side="left", padx=25, pady=8)

    # ── Lógica de ejecución ──────────────────────────────────────────────────

    def _ejecutar(self):
        try:
            cantidad_marcos = int(self.entry_marcos.get())
            referencias = list(map(int, self.entry_paginas.get().split()))
        except ValueError:
            messagebox.showerror(
                "Datos inválidos",
                "Ingrese números enteros separados por espacios en la secuencia "
                "y un número válido para los marcos."
            )
            return

        if cantidad_marcos < 1:
            messagebox.showerror("Error", "La cantidad de marcos debe ser al menos 1.")
            return

        if not referencias:
            messagebox.showerror("Error", "La secuencia de referencias no puede estar vacía.")
            return

        self.btn_ejecutar.config(state="disabled")
        self._actualizar_estadisticas_cargando()

        pasos, hits, fallos, reemplazos = simular_lru(referencias, cantidad_marcos)

        def al_terminar():
            self._actualizar_estadisticas(hits, fallos, len(referencias))
            self._mostrar_resultados_entrada(fallos, reemplazos)
            self.btn_ejecutar.config(state="normal")

        self.renderer.iniciar_animacion(pasos, referencias, cantidad_marcos, al_terminar)

    def _actualizar_estadisticas_cargando(self):
        self.lbl_hits.config(text="✅  Hits: ...")
        self.lbl_fallos.config(text="❌  Fallos: ...")
        self.lbl_total.config(text="📄  Total: ...")
        # Limpiar cuadros de resultado
        self._escribir_entry_readonly(self.entry_fallos_resultado, "...")
        self._escribir_entry_readonly(self.entry_reemplazos_resultado, "...")

    def _actualizar_estadisticas(self, hits, fallos, total):
        pct_hits = hits * 100 / total if total else 0
        pct_fallos = fallos * 100 / total if total else 0
        self.lbl_hits.config(text=f"✅  Hits: {hits}  ({pct_hits:.1f}%)")
        self.lbl_fallos.config(text=f"❌  Fallos: {fallos}  ({pct_fallos:.1f}%)")
        self.lbl_total.config(text=f"📄  Total: {total} referencias")

    def _mostrar_resultados_entrada(self, fallos, reemplazos):
        """Escribe los resultados finales en los cuadros readonly."""
        self._escribir_entry_readonly(self.entry_fallos_resultado, str(fallos))
        self._escribir_entry_readonly(self.entry_reemplazos_resultado, str(reemplazos))

    @staticmethod
    def _escribir_entry_readonly(entry, texto):
        """Escribe texto en un Entry readonly de forma segura."""
        entry.config(state="normal")
        entry.delete(0, "end")
        entry.insert(0, texto)
        entry.config(state="readonly")


# ─── Punto de entrada ────────────────────────────────────────────────────────

if __name__ == "__main__":
    from integrantes import mostrar_intro

    def iniciar_simulador():
        root = tk.Tk()
        app = LRUSimulatorApp(root)
        root.after(600, app._ejecutar)
        root.mainloop()

    mostrar_intro(iniciar_simulador)