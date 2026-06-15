import tkinter as tk
import os
import sys
from PIL import Image, ImageTk

# Colores del tema
_BG = "#000000"
_DORADO = "#D4B996"
_BLANCO = "#F5F5F5"

def _buscar_logo():
    # Busca el logo (soporta ejecucion normal y como .exe)
    if getattr(sys, '_MEIPASS', None):
        carpeta = sys._MEIPASS
    else:
        carpeta = os.path.dirname(os.path.abspath(__file__))
    for ext in ("jpg", "jpeg", "png", "JPG", "JPEG", "PNG", "gif", "GIF"):
        ruta = os.path.join(carpeta, f"logo.{ext}")
        if os.path.isfile(ruta):
            return ruta
    return None

def mostrar_intro(callback_terminar):
    splash = tk.Tk()
    splash.overrideredirect(True)
    splash.attributes("-topmost", True)
    splash.configure(bg=_BG)

    # Centrar ventana
    ancho, alto = 640, 520
    x = (splash.winfo_screenwidth() - ancho) // 2
    y = (splash.winfo_screenheight() - alto) // 2
    splash.geometry(f"{ancho}x{alto}+{x}+{y}")

    # Fondo degradado
    canvas_bg = tk.Canvas(splash, highlightthickness=0)
    canvas_bg.pack(fill="both", expand=True)

    r1, g1, b1 = 0, 0, 0
    r2, g2, b2 = 0x1A, 0x1F, 0x26
    for y_coord in range(0, alto, 2):
        frac = y_coord / alto
        r = int(r1 + (r2 - r1) * frac)
        g = int(g1 + (g2 - g1) * frac)
        b = int(b1 + (b2 - b1) * frac)
        color_hex = f"#{r:02x}{g:02x}{b:02x}"
        canvas_bg.create_rectangle(0, y_coord, ancho, y_coord + 2, fill=color_hex, outline="")

    _BG_CENTRO = "#0D0F13"

    # Contenedor principal
    main_frame = tk.Frame(splash, bg=_BG_CENTRO)
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Titulos
    tk.Label(
        main_frame,
        text="Sistemas Operativos G2 - Proyecto 1",
        font=("Times New Roman", 16, "bold"),
        fg=_DORADO, bg=_BG_CENTRO
    ).pack(pady=(20, 0))

    tk.Label(
        main_frame,
        text="Algoritmos de Reemplazo de Página",
        font=("Times New Roman", 16, "bold"),
        fg=_DORADO, bg=_BG_CENTRO
    ).pack(pady=(0, 15))

    # Carga el logo
    ruta_logo = _buscar_logo()

    global img_tk
    img_tk = None

    try:
        if not ruta_logo:
            raise FileNotFoundError("No se encontró el archivo 'logo'")

        img_pil = Image.open(ruta_logo)
        w_orig, h_orig = img_pil.size

        # Redimensionar manteniendo proporcion
        max_size = 180
        escala = min(max_size / w_orig, max_size / h_orig)
        nuevo_w = int(w_orig * escala)
        nuevo_h = int(h_orig * escala)

        img_pil = img_pil.resize((nuevo_w, nuevo_h), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img_pil)

        lbl_logo = tk.Label(main_frame, image=img_tk, bg=_BG_CENTRO)
        lbl_logo.image = img_tk
        lbl_logo.pack(pady=(10, 10))

    except Exception:
        # Texto de respaldo si no se encuentra el logo
        tk.Label(
            main_frame,
            text="UNIVERSIDAD NACIONAL MAYOR\nDE SAN MARCOS",
            font=("Times New Roman", 15, "italic", "bold"),
            fg=_DORADO, bg=_BG_CENTRO, justify="center"
        ).pack(pady=(40, 40))

    # Creditos del equipo
    tk.Label(
        main_frame,
        text="Integrantes del Equipo 6:",
        font=("Helvetica", 12, "bold"),
        fg=_BLANCO, bg=_BG_CENTRO
    ).pack(pady=(15, 5))

    tk.Label(
        main_frame,
        text="- Yucra Tintaya, Anthony Josue    (24200043)",
        font=("Courier", 11),
        fg=_BLANCO, bg=_BG_CENTRO
    ).pack()

    tk.Label(
        main_frame,
        text="- Figueroa Estrella, Jhair Alberto (24200013)",
        font=("Courier", 11),
        fg=_BLANCO, bg=_BG_CENTRO
    ).pack()

    tk.Label(
        main_frame,
        text="- Jimenes Trujillo, Jack Bryan     (24200109)",
        font=("Courier", 11),
        fg=_BLANCO, bg=_BG_CENTRO
    ).pack(pady=(0, 20))

    # Cierra el splash despues de 3.25 segundos
    def _cerrar():
        splash.destroy()
        callback_terminar()

    splash.after(3250, _cerrar)
    splash.mainloop()
