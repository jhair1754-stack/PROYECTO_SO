"""
Módulo de pantalla de bienvenida (Splash Screen).

Muestra una presentación animada estilo PS2 de 2 segundos antes
de iniciar la interfaz principal del simulador LRU.
"""

import tkinter as tk
import os
from PIL import Image, ImageTk

# Colores del tema Premium
_BG = "#000000"
_DORADO = "#D4B996"
_BLANCO = "#F5F5F5"

def _buscar_logo():
    """Busca el archivo de imagen 'logo' en la carpeta raíz."""
    carpeta = os.path.dirname(os.path.abspath(__file__))
    # Intentar extensiones comunes
    for ext in ("jpg", "jpeg", "png", "JPG", "JPEG", "PNG", "gif", "GIF"):
        ruta = os.path.join(carpeta, f"logo.{ext}")
        if os.path.isfile(ruta):
            return ruta
    return None

def mostrar_intro(callback_terminar):
    """
    Crea una ventana temporal sin bordes, muestra el logo con su relación de
    aspecto original preservada, y tras 2 segundos se destruye
    e inicia la aplicación principal.
    """
    splash = tk.Tk()
    splash.overrideredirect(True)
    splash.configure(bg=_BG)

    # ── Dimensiones y Centrado en Pantalla ─────────────────────────────────
    ancho, alto = 640, 520
    x = (splash.winfo_screenwidth() - ancho) // 2
    y = (splash.winfo_screenheight() - alto) // 2
    splash.geometry(f"{ancho}x{alto}+{x}+{y}")

    # ── Títulos ────────────────────────────────────────────────────────────
    tk.Label(
        splash,
        text="Sistemas Operativos G2 - Proyecto 1",
        font=("Times New Roman", 16, "bold"),
        fg=_DORADO, bg=_BG
    ).pack(pady=(20, 0))

    tk.Label(
        splash,
        text="Algoritmos de Reemplazo de Página",
        font=("Times New Roman", 16, "bold"),
        fg=_DORADO, bg=_BG
    ).pack(pady=(0, 15))

    # ── Carga y Redimensionamiento del Logo ────────────────────────────────
    ruta_logo = _buscar_logo()
    
    # Referencia global para evitar recolección de basura en Tkinter
    global img_tk
    img_tk = None

    try:
        if not ruta_logo:
            raise FileNotFoundError("No se encontró el archivo 'logo'")

        # Abrir imagen original
        img_pil = Image.open(ruta_logo)
        w_orig, h_orig = img_pil.size

        # Ajustar preservando la relación de aspecto original (caja de 180x180 max)
        max_size = 180
        escala = min(max_size / w_orig, max_size / h_orig)
        nuevo_w = int(w_orig * escala)
        nuevo_h = int(h_orig * escala)

        img_pil = img_pil.resize((nuevo_w, nuevo_h), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img_pil)

        lbl_logo = tk.Label(splash, image=img_tk, bg=_BG)
        lbl_logo.image = img_tk
        lbl_logo.pack(pady=(10, 10))

    except Exception:
        # Fallback de texto si el logo no está o falla la lectura
        tk.Label(
            splash,
            text="UNIVERSIDAD NACIONAL MAYOR\nDE SAN MARCOS",
            font=("Times New Roman", 15, "italic", "bold"),
            fg=_DORADO, bg=_BG, justify="center"
        ).pack(pady=(40, 40))

    # ── Créditos ───────────────────────────────────────────────────────────
    tk.Label(
        splash,
        text="Integrantes del Equipo 6:",
        font=("Helvetica", 12, "bold"),
        fg=_BLANCO, bg=_BG
    ).pack(pady=(15, 5))

    tk.Label(
        splash,
        text="- Yucra Tintaya, Anthony Josue    (24200043)",
        font=("Courier", 11),
        fg=_BLANCO, bg=_BG
    ).pack()

    tk.Label(
        splash,
        text="- Figueroa Estrella, Jhair Alberto (24200013)",
        font=("Courier", 11),
        fg=_BLANCO, bg=_BG
    ).pack()

    tk.Label(
        splash,
        text="- Jimenes Trujillo, Jack Bryan     (24200109)",
        font=("Courier", 11),
        fg=_BLANCO, bg=_BG
    ).pack(pady=(0, 20))

    # ── Temporizador de Cierre (2 Segundos) ────────────────────────────────
    def _cerrar():
        splash.destroy()
        callback_terminar()

    splash.after(3000, _cerrar)
    splash.mainloop()
