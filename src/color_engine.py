import re
import numpy as np
from PIL import Image

def extraer_paleta_jerarquica(ruta_svg):
    """
    Extrae los colores del SVG ignorando los encabezados decorativos (width=200),
    excepto en el Grupo 1 donde el negro es un pincel real.
    """
    try:
        with open(ruta_svg, 'r', encoding='utf-8') as f:
            svg_text = f.read()

        grupos = {}
        # Buscamos los bloques de cada columna (Color-1-Group, etc.)
        bloques_grupos = re.findall(r'<g id="Color-(\d+)-Group">(.*?)</g>', svg_text, re.DOTALL)

        for g_num, contenido_bloque in bloques_grupos:
            g_id = int(g_num)
            
            # Capturamos el ancho para distinguir entre botones de 100 (pinceles) y 200 (cabeceras)
            rects = re.findall(r'<rect width="(\d+)"[^>]*fill="(#[a-fA-F0-9]{6})"', contenido_bloque)
            
            if rects:
                grupos[g_id] = {'main': None, 'variaciones': {}}
                v_idx = 0
                
                for width, hex_val in rects:
                    color = hex_val.upper()
                    if width == "200":
                        # Guardamos el color de cabecera (como el Rosa #EA696D o el Negro #000000)
                        grupos[g_id]['main'] = color
                    else:
                        # Es un pincel de 100x100
                        grupos[g_id]['variaciones'][v_idx] = color
                        v_idx += 1

        # --- CONSTRUCCIÓN DE LA PALETA PLANA ---
        paleta_plana = []
        for g_id in sorted(grupos.keys()):
            # CASO ESPECIAL: En el Grupo 1, el Negro (#000000) tiene width 200 pero ES un pincel.
            # Lo añadimos al inicio de la columna si no está ya en las variaciones.
            if g_id == 1 and grupos[g_id]['main'] not in grupos[g_id]['variaciones'].values():
                paleta_plana.append(grupos[g_id]['main'])

            # Añadimos los pinceles estándar (width 100)
            for v_id in sorted(grupos[g_id]['variaciones'].keys()):
                paleta_plana.append(grupos[g_id]['variaciones'][v_id])

        print(f"✅ Sincronización exitosa. Total colores usables: {len(paleta_plana)}")
        return paleta_plana, grupos

    except Exception as e:
        print(f"❌ Error en SVG: {e}")
        return ["#000000"], {1: {'main': "#000000", 'variaciones': {0: "#000000"}}}

def hex_to_rgb(hex_str):
    """Convierte HEX a tupla RGB para cálculos matemáticos."""
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def procesar_imagen_a_matriz(ruta_img, paleta_hex, size=(150, 150)):
    """
    Mapea la imagen a los IDs de la paleta. 
    Usa NEAREST para evitar que se creen colores "fantasma" en los bordes.
    """
    img = Image.open(ruta_img).convert('RGB')
    
    # NEAREST es ideal para pixel art porque no mezcla colores al redimensionar
    img = img.resize(size, Image.Resampling.NEAREST)
    pixeles = np.array(img)
    
    # Convertimos la paleta filtrada a RGB
    paleta_rgb = np.array([hex_to_rgb(h) for h in paleta_hex])
    
    alto, ancho, _ = pixeles.shape
    matriz_ids = np.zeros((alto, ancho), dtype=int)

    # Optimizamos con NumPy: calculamos la distancia de cada píxel a cada color de la paleta
    for y in range(alto):
        for x in range(ancho):
            pixel = pixeles[y, x]
            # Norma vectorial para hallar el color más cercano (Distancia Euclidiana)
            distancias = np.linalg.norm(paleta_rgb - pixel, axis=1)
            matriz_ids[y, x] = np.argmin(distancias)
            
    return matriz_ids