import sys
from src.interface import HeartopiaDashboard

def iniciar_configuracion():
    # Diccionario con las dimensiones exactas extraídas de canvas.js
    DIMENSIONES = {
        '1': {'nombre': '16:9', 'niveles': [[30, 18], [50, 28], [100, 56], [150, 84]]},
        '2': {'nombre': '4:3',  'niveles': [[30, 24], [50, 38], [100, 76], [150, 114]]},
        '3': {'nombre': '1:1',  'niveles': [[30, 30], [50, 50], [100, 100], [150, 150]]},
        '4': {'nombre': '3:4',  'niveles': [[24, 30], [38, 50], [76, 100], [114, 150]]},
        '5': {'nombre': '9:16', 'niveles': [[18, 30], [28, 50], [56, 100], [84, 150]]}
    }

    print("--- CONFIGURACIÓN DE LIENZO HEARTOPIA ---")
    print("Selecciona la Relación de Aspecto:")
    for k, v in DIMENSIONES.items():
        print(f"{k}. {v['nombre']}")
    
    rel_opcion = input("Opción (1-5): ")
    if rel_opcion not in DIMENSIONES:
        print("Opción inválida. Usando 1:1 por defecto.")
        rel_opcion = '3'

    print("\nSelecciona el Nivel de Detalle (Iconos de cuadrícula):")
    print("1. Nivel 1 (Bajo)")
    print("2. Nivel 2")
    print("3. Nivel 3")
    print("4. Nivel 4 (Máximo)")
    
    lvl_opcion = input("Nivel (1-4): ")
    try:
        idx_lvl = int(lvl_opcion) - 1
        if not (0 <= idx_lvl <= 3): raise ValueError
    except:
        print("Nivel inválido. Usando Nivel 4 por defecto.")
        idx_lvl = 3

    # Extraer ancho y alto finales
    config_elegida = DIMENSIONES[rel_opcion]
    ancho, alto = config_elegida['niveles'][idx_lvl]
    
    print(f"\n[!] Configuración lista: {config_elegida['nombre']} | Tamaño: {ancho}x{alto}")
    return ancho, alto

if __name__ == "__main__":
    # 1. Pedir configuración al usuario
    ancho_final, alto_final = iniciar_configuracion()

    # 2. Iniciar la interfaz con las dimensiones elegidas
    # Asegúrate de que tu clase en interface.py reciba (ancho_g, alto_g)
    app = HeartopiaDashboard(
        ruta_svg="data/paleta.svg", 
        ruta_img="data/imagen.jpg", 
        ancho_g=ancho_final,
        alto_g=alto_final
    )
    app.start()