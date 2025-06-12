import json
from pathlib import Path

def save_authorization_json(numero_autorizacion, datos):
    """
    Guarda las autorizacions en un archivo JSON dentro de la carpeta data/autorizaciones
    
    Args:
        numero_autorizacion: Número de autorización para nombrar el archivo
        datos: Diccionario con los datos a guardar
        
    Returns:
        str: Ruta del archivo guardado
    """
    folder = Path("data/autorizaciones")
    folder.mkdir(parents=True, exist_ok=True)

    path = folder / f'datos_autorizacion_{numero_autorizacion}.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
    
    print(f"✅ Datos de autorización guardados en '{path}'")

def save_delivery_control_json(numero_autorizacion, datos):
    """
    Guarda los datos de control de entregas en un archivo JSON dentro de la carpeta data/control_entregas
    
    Args:
        numero_autorizacion: Número de autorización para nombrar el archivo
        datos: Diccionario con los datos a guardar
        
    Returns:
        str: Ruta del archivo guardado
    """
    folder = Path("data/control_entregas")
    folder.mkdir(parents=True, exist_ok=True)

    path = folder / f'control_entregas_{numero_autorizacion}.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
    
    print(f"✅ Datos de control de entregas guardados en '{path}'")
    return str(path)

"""
def guardar_json(numero_autorizacion, datos):
    if folder == autorizaciones:
        folder = Path("data/autorizaciones")
    else folder == control_entregas :
        folder = Path("data/control_entregas")
     
    folder.mkdir(parents=True, exist_ok=True)

    path = folder / f'documento_{numero_autorizacion}.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
    
    print(f"✅ Datos de control de entregas guardados en '{path}'")
    return str(path)
"""
