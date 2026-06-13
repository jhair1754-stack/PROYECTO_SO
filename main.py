import tkinter as tk
from tkinter import ttk, messagebox

class LRUSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador LRU - Método del Profesor")
        self.root.geometry("1400x800")
        self.root.configure(bg="#F4F6F8")
        
        self.setup_styles()
        self.build_ui()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Titulo.TLabel", font=("Segoe UI", 20, "bold"), background="#F4F6F8")
        style.configure("TLabelFrame", background="#F4F6F8")
        style.configure("TLabel", background="#F4F6F8")
        style.configure("TButton", font=("Segoe UI", 10, "bold"))

    def build_ui(self):
        ttk.Label(self.root, text="Simulador LRU (Método del Profesor)", style="Titulo.TLabel").pack(pady=15)
        
        # Datos de Entrada
        frame_datos = ttk.LabelFrame(self.root, text="Datos de Entrada")
        frame_datos.pack(fill="x", padx=15, pady=10)
        
        ttk.Label(frame_datos, text="Cantidad de marcos:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_marcos = ttk.Entry(frame_datos, width=15)
        self.entry_marcos.grid(row=0, column=1)
        self.entry_marcos.insert(0, "4")
        
        ttk.Label(frame_datos, text="Secuencia:").grid(row=1, column=0, padx=10, pady=10)
        self.entry_paginas = ttk.Entry(frame_datos, width=90)
        self.entry_paginas.grid(row=1, column=1)
        self.entry_paginas.insert(0, "0 1 3 2 1 5 0 3 4 6 4 1 2 5 3 2")
        
        self.btn_ejecutar = ttk.Button(frame_datos, text="▶ Ejecutar LRU", command=self.ejecutar_lru)
        self.btn_ejecutar.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Canvas
        frame_resultado = ttk.LabelFrame(self.root, text="Visualización Animada")
        frame_resultado.pack(fill="both", expand=True, padx=15, pady=10)
        
        scroll_x = ttk.Scrollbar(frame_resultado, orient="horizontal")
        scroll_y = ttk.Scrollbar(frame_resultado, orient="vertical")
        self.canvas = tk.Canvas(frame_resultado, bg="white", xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        
        scroll_x.config(command=self.canvas.xview)
        scroll_y.config(command=self.canvas.yview)
        scroll_x.pack(side="bottom", fill="x")
        scroll_y.pack(side="right", fill="y")
        self.canvas.pack(fill="both", expand=True)
        
        # Estadísticas
        frame_stats = ttk.LabelFrame(self.root, text="Estadísticas")
        frame_stats.pack(fill="x", padx=15, pady=10)
        
        self.lbl_hits = ttk.Label(frame_stats, text="✅ Hits: 0", font=("Segoe UI", 11, "bold"))
        self.lbl_hits.pack(side="left", padx=20)
        
        self.lbl_fallos = ttk.Label(frame_stats, text="❌ Fallos: 0", font=("Segoe UI", 11, "bold"))
        self.lbl_fallos.pack(side="left", padx=20)
        
        self.lbl_total = ttk.Label(frame_stats, text="📄 Referencias: 0", font=("Segoe UI", 11, "bold"))
        self.lbl_total.pack(side="left", padx=20)
        
    def ejecutar_lru(self):
        try:
            cantidad_marcos = int(self.entry_marcos.get())
            referencias = list(map(int, self.entry_paginas.get().split()))
        except ValueError:
            messagebox.showerror("Error", "Ingrese datos válidos.")
            return

        self.canvas.delete("all")
        self.btn_ejecutar.config(state="disabled")
        
        self.lbl_hits.config(text="✅ Hits: ...")
        self.lbl_fallos.config(text="❌ Fallos: ...")
        self.lbl_total.config(text="📄 Referencias: ...")
        
        cols, hits, fallos = self.simular_lru(referencias, cantidad_marcos)
        self.animar_solucion(cols, referencias, hits, fallos, cantidad_marcos)
        
    def simular_lru(self, referencias, cantidad_marcos):
        frames = []
        last_seen = {}
        cols = []
        hits = fallos = 0
        
        for t, p in enumerate(referencias):
            if p in frames:
                hits += 1
                last_seen[p] = t
                cols.append({"time": t, "page": p, "is_fault": False})
            else:
                fallos += 1
                if len(frames) < cantidad_marcos:
                    frames.insert(0, p)
                else:
                    max_dist = -1
                    p_remove = None
                    for fp in frames:
                        dist = t - last_seen[fp]
                        if dist > max_dist:
                            max_dist = dist
                            p_remove = fp
                    idx = frames.index(p_remove)
                    frames = [p] + frames[:idx] + frames[idx+1:]
                
                last_seen[p] = t
                cols.append({
                    "time": t,
                    "page": p,
                    "frames": list(frames),
                    "is_fault": True
                })

        # Calcular las distancias hacia atrás desde el próximo fallo
        fault_cols = [c for c in cols if c["is_fault"]]
        for i in range(len(fault_cols)):
            if i < len(fault_cols) - 1:
                next_fault_time = fault_cols[i+1]["time"]
                # Solo calcular los cuadraditos si el marco está lleno y necesitamos reemplazar
                if len(fault_cols[i]["frames"]) == cantidad_marcos:
                    subboxes = []
                    for fp in fault_cols[i]["frames"]:
                        last_idx = -1
                        for j in range(next_fault_time - 1, -1, -1):
                            if referencias[j] == fp:
                                last_idx = j
                                break
                        dist = next_fault_time - last_idx
                        subboxes.append(dist)
                    fault_cols[i]["subboxes"] = subboxes
                else:
                    fault_cols[i]["subboxes"] = []
            else:
                fault_cols[i]["subboxes"] = []
                
        # Inyectar los cuadraditos de vuelta a la lista general
        for fc in fault_cols:
            for c in cols:
                if c["is_fault"] and c["time"] == fc["time"]:
                    c["subboxes"] = fc["subboxes"]
                    
        return cols, hits, fallos

    def animar_solucion(self, cols, referencias, hits, fallos, cantidad_marcos):
        ancho_celda = 60
        alto_celda = 50
        margen_x = 80
        margen_y = 100
        
        def dibujar_paso(paso_idx, current_fault_col):
            if paso_idx >= len(cols):
                porcentaje_hits = hits * 100 / len(referencias)
                porcentaje_fallos = fallos * 100 / len(referencias)
                self.lbl_hits.config(text=f"✅ Hits: {hits} ({porcentaje_hits:.2f}%)")
                self.lbl_fallos.config(text=f"❌ Fallos: {fallos} ({porcentaje_fallos:.2f}%)")
                self.lbl_total.config(text=f"📄 Referencias: {len(referencias)}")
                self.canvas.config(scrollregion=self.canvas.bbox("all"))
                self.btn_ejecutar.config(state="normal")
                return

            c = cols[paso_idx]
            x_seq = margen_x + paso_idx * 40
            y_seq = 40
            
            # Dibujar referencia en la parte superior
            if c["is_fault"]:
                # Circulo para fallos
                self.canvas.create_oval(x_seq - 15, y_seq - 15, x_seq + 15, y_seq + 15, outline="#DC2626", width=2)
            else:
                # Subrayado para hits
                self.canvas.create_line(x_seq - 10, y_seq + 15, x_seq + 10, y_seq + 15, fill="#16A34A", width=3)
            
            self.canvas.create_text(x_seq, y_seq, text=str(c["page"]), font=("Segoe UI", 12, "bold"))

            next_fault_col = current_fault_col
            
            # Si es un fallo, se dibuja la columna en los marcos
            if c["is_fault"]:
                x = margen_x + current_fault_col * ancho_celda
                for fila in range(cantidad_marcos):
                    y = margen_y + fila * alto_celda
                    self.canvas.create_rectangle(x, y, x + ancho_celda, y + alto_celda, outline="black", width=1)
                    
                    if fila < len(c["frames"]):
                        valor = c["frames"][fila]
                        self.canvas.create_text(x + ancho_celda / 2, y + alto_celda / 2, text=str(valor), font=("Consolas", 16))
                        
                        # Dibujar el subcuadrado si existe (distancia al próximo fallo)
                        if c.get("subboxes") and fila < len(c["subboxes"]):
                            sub_val = c["subboxes"][fila]
                            sub_w = 20
                            sub_h = 20
                            self.canvas.create_rectangle(x + ancho_celda - sub_w, y + alto_celda - sub_h, x + ancho_celda, y + alto_celda, outline="black", width=1)
                            self.canvas.create_text(x + ancho_celda - sub_w / 2, y + alto_celda - sub_h / 2, text=str(sub_val), font=("Consolas", 10))
                
                next_fault_col += 1
                
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
            
            # Continuar con el siguiente paso en 500ms
            self.root.after(500, dibujar_paso, paso_idx + 1, next_fault_col)
            
        # Iniciar animación
        dibujar_paso(0, 0)

if __name__ == "__main__":
    root = tk.Tk()
    app = LRUSimulatorApp(root)
    # Ejecutar la animación por defecto al inicio
    root.after(500, app.ejecutar_lru)
    root.mainloop()