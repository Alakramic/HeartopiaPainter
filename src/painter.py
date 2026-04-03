import pyautogui
import time
import random
import numpy as np
import keyboard

def pintar_capa(matriz, color_id, coords_cal, ancho_g, alto_g):
    """
    Pinta con Triple Clic de Anclaje en el primer píxel para 
    evitar el fallo de sincronización inicial.
    """
    x_off, y_off, w_total, h_total = coords_cal
    
    pyautogui.PAUSE = 0.001 

    puntos = np.argwhere(matriz == color_id)
    print(f"🎨 Capa {color_id}: {len(puntos)} píxeles.")

    step_x = w_total / ancho_g
    step_y = h_total / alto_g

    es_el_primer_punto = True

    for fila, col in puntos:
        if keyboard.is_pressed('esc'): break 

        px = x_off + (col * step_x) + (step_x / 2)
        py = y_off + (fila * step_y) + (step_y / 2)
        
        pyautogui.moveTo(px, py, _pause=False)
        
        # --- TÉCNICA DE TRIPLE CLIC DE ANCLAJE ---
        if es_el_primer_punto:
            print("⚓ Triple clic de seguridad en el inicio...")
            for _ in range(3):
                pyautogui.mouseDown(button='left')
                time.sleep(0.015) # Un poco más de tiempo para el anclaje
                pyautogui.mouseUp(button='left')
                time.sleep(0.02)
            es_el_primer_punto = False
        else:
            # --- ESCRITURA NORMAL ---
            pyautogui.mouseDown(button='left')
            time.sleep(0.012) 
            pyautogui.mouseUp(button='left')
        
        time.sleep(0.015)
    
    print("✅ Capa finalizada.")