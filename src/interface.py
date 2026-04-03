import tkinter as tk
from tkinter import messagebox
import numpy as np
from .color_engine import extraer_paleta_jerarquica, procesar_imagen_a_matriz
from .calibrator import CalibradorArea
from .painter import pintar_capa

class HeartopiaDashboard:
    def __init__(self, ruta_svg, ruta_img, ancho_g, alto_g):
        self.root = tk.Tk()
        self.root.title("Heartopia Dashboard")
        self.root.geometry("1100x850")
        self.root.attributes('-topmost', True)

        self.ancho_g = ancho_g
        self.alto_g = alto_g
        self.ruta_svg = ruta_svg 
        
        # 1. Cargamos paleta y procesamos matriz
        self.paleta, self.dict_grupos = extraer_paleta_jerarquica(ruta_svg)
        self.matriz = procesar_imagen_a_matriz(ruta_img, self.paleta, (ancho_g, alto_g))
        
        self.color_idx = None
        self.coords = None
        self.botones_colores = {} 

        self.setup_ui()

    def setup_ui(self):
        colores_usados = np.unique(self.matriz)
        main_container = tk.Frame(self.root)
        main_container.pack(fill="both", expand=True)

        # --- PANEL IZQUIERDO ---
        left_panel = tk.Frame(main_container, width=550, padx=10, pady=10)
        left_panel.pack(side="left", fill="y")

        tk.Label(left_panel, text="1. CONFIGURACIÓN", font=("Arial", 10, "bold")).pack()
        tk.Button(left_panel, text="Calibrar Área", command=self.calibrar).pack(pady=5)
        self.status_cal = tk.Label(left_panel, text="Área: Pendiente", fg="red")
        self.status_cal.pack()

        tk.Label(left_panel, text="2. PALETA", font=("Arial", 10, "bold")).pack(pady=10)

        palette_frame = tk.Frame(left_panel, bg="#2b2b2b", padx=5, pady=5)
        palette_frame.pack(fill="both", expand=True)

        row, col = 0, 0
        max_grupos_por_fila = 4

        for g_id in sorted(self.dict_grupos.keys()):
            grupo = self.dict_grupos[g_id]
            grupo_container = tk.Frame(palette_frame, bg="#2b2b2b", padx=4, pady=4)
            grupo_container.grid(row=row, column=col, sticky="nw")

            cols_wrapper = tk.Frame(grupo_container, bg="#2b2b2b")
            cols_wrapper.pack()

            col_izq = tk.Frame(cols_wrapper, bg="#2b2b2b")
            col_izq.pack(side="left", padx=1)
            col_der = tk.Frame(cols_wrapper, bg="#2b2b2b")
            col_der.pack(side="left", padx=1)

            v_items = list(sorted(grupo['variaciones'].items()))
            
            if len(v_items) >= 10:
                # 0-4 es la derecha, 5-9 es la izquierda
                parte_derecha_juego = v_items[:5]  
                parte_izquierda_juego = v_items[5:10] 

                # --- COLUMNA IZQUIERDA (5-9): AHORA INVERTIDA ---
                for _, hex_val in reversed(parte_izquierda_juego):
                    self.crear_boton_color(col_izq, hex_val, colores_usados).pack(pady=1)

                # --- COLUMNA DERECHA (0-4): SE QUEDA INVERTIDA (como estaba bien) ---
                for _, hex_val in reversed(parte_derecha_juego):
                    self.crear_boton_color(col_der, hex_val, colores_usados).pack(pady=1)
            else:
                for _, hex_val in v_items:
                    self.crear_boton_color(col_izq, hex_val, colores_usados).pack(pady=1)

            col += 1
            if col >= max_grupos_por_fila:
                col = 0
                row += 1

        # --- CONTROLES INFERIORES ---
        bottom_info = tk.Frame(left_panel, pady=10)
        bottom_info.pack(side="bottom", fill="x")

        self.current_color_label = tk.Label(bottom_info, text="Color: Ninguno")
        self.current_color_label.pack()
        self.color_sample = tk.Frame(bottom_info, width=100, height=25, bg="gray", relief="ridge", bd=2)
        self.color_sample.pack(pady=5)

        self.btn_go = tk.Button(bottom_info, text="¡PINTAR CAPA!", bg="green", fg="white", 
                                font=("Arial", 11, "bold"), height=2, state="disabled", command=self.go)
        self.btn_go.pack(fill="x")

        # --- PANEL DERECHO ---
        right_panel = tk.Frame(main_container, bg="#222", padx=10, pady=10)
        right_panel.pack(side="right", fill="both", expand=True)
        self.preview_canvas = tk.Canvas(right_panel, width=500, height=500, bg="black", highlightthickness=0)
        self.preview_canvas.pack(pady=10)
        self.dibujar_matriz_completa()

    def crear_boton_color(self, parent, hex_val, usados):
        idx = self.paleta.index(hex_val)
        btn = tk.Button(parent, bg=hex_val, text="●" if idx in usados else "",
                        fg="white" if hex_val.lower() != "#feffff" else "black", 
                        font=("Arial", 7, "bold"), width=3, height=1, relief="flat",
                        command=lambda i=idx: self.set_color(i))
        self.botones_colores[idx] = btn
        return btn

    def set_color(self, idx):
        for b in self.botones_colores.values(): b.config(relief="flat", bd=1)
        self.botones_colores[idx].config(relief="sunken", bd=3)
        self.color_idx = idx
        self.color_sample.config(bg=self.paleta[idx])
        self.actualizar_vista_capa(idx)
        self.check_ready()

    def calibrar(self):
        cal = CalibradorArea(self.root)
        self.root.wait_window(cal.top)
        if cal.coords:
            self.coords = cal.coords
            self.status_cal.config(text="Área: OK", fg="green")
            self.check_ready()

    def check_ready(self):
        if self.coords and self.color_idx is not None:
            self.btn_go.config(state="normal")

    def go(self):
        # 1. Minimizar el Dashboard para no estorbar
        self.root.iconify()
        
        # 2. Esperar 3 segundos (3000 milisegundos)
        # Esto te da tiempo de posicionar el mouse o verificar el juego
        print("Iniciando cuenta regresiva de 3 segundos...")
        self.root.after(3000, self.ejecutar_pintado)

    def ejecutar_pintado(self):
        # 3. Iniciar el proceso de pintado real
        pintar_capa(self.matriz, self.color_idx, self.coords, self.ancho_g, self.alto_g)
        
        # 4. Restaurar y avisar al terminar
        self.root.deiconify()
        self.root.attributes('-topmost', True)
        self.root.lift()
        messagebox.showinfo("Bot", "Capa finalizada. ¿Siguiente color?")

    def dibujar_matriz_completa(self):
        self.preview_canvas.delete("all")
        escala = 500 / max(self.ancho_g, self.alto_g)
        for y in range(self.alto_g):
            for x in range(self.ancho_g):
                self.preview_canvas.create_rectangle(x*escala, y*escala, (x+1)*escala, (y+1)*escala, 
                                                    fill=self.paleta[self.matriz[y][x]], outline="")

    def actualizar_vista_capa(self, idx):
        self.preview_canvas.delete("all")
        escala = 500 / max(self.ancho_g, self.alto_g)
        puntos = np.argwhere(self.matriz == idx)
        for fila, col in puntos:
            self.preview_canvas.create_rectangle(col*escala, fila*escala, (col+1)*escala, (fila+1)*escala,
                                                fill=self.paleta[idx], outline="")

    def start(self):
        self.root.mainloop()