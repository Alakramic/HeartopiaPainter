import tkinter as tk
from PIL import ImageGrab
import numpy as np
import ctypes

# DPI Awareness para que Windows no escale la captura
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    ctypes.windll.user32.SetProcessDPIAware()

class CalibradorArea:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("CALIBRADOR: Detectando Borde Negro")
        self.top.attributes('-alpha', 0.3)
        self.top.attributes('-topmost', True)
        
        self.canvas = tk.Canvas(self.top, bg='red', highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.coords = None
        self.btn = tk.Button(
            self.top, text="CONFIRMAR Y AJUSTAR AL BORDE NEGRO", 
            font=('Arial', 10, 'bold'), bg="#4CAF50", fg="white",
            command=self.confirmar
        )
        self.btn.pack(side="bottom", pady=10)

    def auto_ajuste_por_borde(self, x, y, w, h):
        margen = 40 
        bbox = (x - margen, y - margen, x + w + margen, y + h + margen)
        
        try:
            # Captura en escala de grises para detectar el negro fácilmente
            cap = ImageGrab.grab(bbox=bbox, all_screens=True).convert("L")
            img_np = np.array(cap)
            
            # Buscamos el NEGRO (valor cercano a 0)
            # Ponemos < 30 por si el motor del juego lo aclara un poquito
            mask = img_np < 30 
            
            coords_negro = np.column_stack(np.where(mask))
            
            if coords_negro.size > 50: # Si encontramos suficientes píxeles negros
                min_y, min_x = coords_negro.min(axis=0)
                max_y, max_x = coords_negro.max(axis=0)
                
                # --- LÓGICA DE BORDE EXTERIOR ---
                # Como el borde negro es parte del marco, tomamos desde
                # el exterior del mismo para no perder ese píxel de dibujo.
                real_x = (x - margen) + min_x
                real_y = (y - margen) + min_y
                real_w = max_x - min_x
                real_h = max_y - min_y
                
                print(f"🎯 Borde Negro detectado: {real_w}x{real_h} px")
                return (real_x, real_y, real_w, real_h)

            print("⚠️ No se detectó el borde negro. Usando manual.")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            
        return (x, y, w, h)

    def confirmar(self):
        self.top.update()
        c_x = self.canvas.winfo_rootx()
        c_y = self.canvas.winfo_rooty()
        c_w = self.canvas.winfo_width()
        c_h = self.canvas.winfo_height()
        
        # El resultado se guarda como (x, y, ancho, alto)
        res = self.auto_ajuste_por_borde(c_x, c_y, c_w, c_h)
        self.coords = res
        self.top.destroy()