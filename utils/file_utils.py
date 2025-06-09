import json
from pathlib import Path

def guardar_autorizacion_json(numero_autorizacion, datos):
    carpeta = Path("data/autorizaciones")
    carpeta.mkdir(parents=True, exist_ok=True)

    ruta = carpeta / f'datos_autorizacion_{numero_autorizacion}.json'
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
    
    print(f"✅ Datos de autorización guardados en '{ruta}'")

def guardar_control_entregas_json(numero_autorizacion, datos):
    """
    Guarda los datos de control de entregas en un archivo JSON dentro de la carpeta data/control_entregas
    
    Args:
        numero_autorizacion: Número de autorización para nombrar el archivo
        datos: Diccionario con los datos a guardar
        
    Returns:
        str: Ruta del archivo guardado
    """
    carpeta = Path("data/control_entregas")
    carpeta.mkdir(parents=True, exist_ok=True)

    ruta = carpeta / f'control_entregas_{numero_autorizacion}.json'
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
    
    print(f"✅ Datos de control de entregas guardados en '{ruta}'")
    return str(ruta)

"""
def guardar_json(numero_autorizacion, datos):
    if carpeta == autorizaciones:
        carpeta = Path("data/autorizaciones")
    else carpeta == control_entregas :
        carpeta = Path("data/control_entregas")
     
    carpeta.mkdir(parents=True, exist_ok=True)

    ruta = carpeta / f'documento_{numero_autorizacion}.json'
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
    
    print(f"✅ Datos de control de entregas guardados en '{ruta}'")
    return str(ruta)
"""
