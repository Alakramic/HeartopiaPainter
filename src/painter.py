import pyautogui
import time
import random
import numpy as np
import keyboard  # <--- Nueva librería

def pintar_capa(matriz, color_id, coords_cal, ancho_g, alto_g):
    x_off, y_off, w_total, h_total = coords_cal
    dx = w_total / ancho_g
    dy = h_total / alto_g

    puntos = np.argwhere(matriz == color_id)
    print(f"Pintando {len(puntos)} píxeles. PRESIONA 'ESC' PARA CANCELAR.")

    for fila, col in puntos:
        # --- VERIFICACIÓN DE EMERGENCIA ---
        if keyboard.is_pressed('esc'):
            print("!!! PINTADO CANCELADO POR EL USUARIO !!!")
            break 
        # ----------------------------------

        px = x_off + (col * dx) + (dx / 2)
        py = y_off + (fila * dy) + (dy / 2)
        
        pyautogui.moveTo(px, py, _pause=False)
        
        pyautogui.mouseDown(button='left')
        time.sleep(0.02) 
        pyautogui.mouseUp(button='left')
        
        time.sleep(random.uniform(0.015, 0.045))
    
    print("Proceso finalizado o detenido.")