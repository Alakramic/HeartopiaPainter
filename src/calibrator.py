import tkinter as tk
from PIL import ImageGrab
import numpy as np

class CalibradorArea:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("CALIBRADOR: Ajusta el cuadro rojo sobre el lienzo")
        
        # Opacidad para ver el juego detrás
        self.top.attributes('-alpha', 0.3)
        self.top.attributes('-topmost', True)
        
        # El área roja visual que estirarás sobre el juego
        self.canvas = tk.Canvas(self.top, bg='red', highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.coords = None
        
        # Botón de confirmación
        self.btn = tk.Button(
            self.top, 
            text="CONFIRMAR Y AJUSTAR AL BLANCO", 
            font=('Arial', 10, 'bold'),
            bg="#4CAF50",
            fg="white",
            command=self.confirmar
        )
        self.btn.pack(side="bottom", pady=10)

    def auto_ajuste_magnetico(self, x, y, w, h):
        """
        Analiza el área confirmada (con un margen extra) para encontrar
        el recuadro blanco exacto del juego.
        """
        margen = 20  # Miramos 20px extra hacia afuera por si el usuario se quedó corto
        
        # Definimos la caja de captura (x1, y1, x2, y2)
        bbox = (x - margen, y - margen, x + w + margen, y + h + margen)
        
        try:
            # Captura de pantalla silenciosa para procesar píxeles
            cap = ImageGrab.grab(bbox=bbox)
            img_np = np.array(cap)
            
            # Buscamos el blanco puro (Heartopia usa 255 o muy cerca)
            mask = np.all(img_np >= 250, axis=-1)
            coords_blancas = np.column_stack(np.where(mask))
            
            if coords_blancas.size > 0:
                # Encontramos límites en la imagen capturada
                min_y, min_x = coords_blancas.min(axis=0)
                max_y, max_x = coords_blancas.max(axis=0)
                
                # Traducimos a coordenadas reales de la pantalla
                real_x = (x - margen) + min_x
                real_y = (y - margen) + min_y
                real_w = max_x - min_x
                real_h = max_y - min_y
                
                print(f"✨ Ajuste Magnético: ¡Blanco detectado con precisión!")
                return (real_x, real_y, real_w, real_h)
            
        except Exception as e:
            print(f"❌ Error en el auto-ajuste: {e}")
            
        print("⚠️ No se detectó blanco puro. Usando coordenadas manuales del cuadro rojo.")
        return (x, y, w, h)

    def confirmar(self):
        """
        Calcula el área roja y aplica el ajuste fino.
        """
        self.top.update()
        
        # 1. Posición bruta del cuadro rojo en pantalla
        raw_x = self.canvas.winfo_rootx()
        raw_y = self.canvas.winfo_rooty()
        raw_w = self.canvas.winfo_width()
        raw_h = self.canvas.winfo_height()
        
        # 2. Aplicar el imán al blanco
        self.coords = self.auto_ajuste_magnetico(raw_x, raw_y, raw_w, raw_h)
        
        print(f"✅ Calibración final: {self.coords}")
        self.top.destroy()