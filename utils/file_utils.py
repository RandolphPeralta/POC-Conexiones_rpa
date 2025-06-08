import json
from pathlib import Path

def guardar_autorizacion_json(numero_autorizacion, datos):
    carpeta = Path("data/autorizaciones")
    carpeta.mkdir(parents=True, exist_ok=True)

    ruta = carpeta / f'datos_autorizacion_{numero_autorizacion}.json'
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
    
    print(f"✅ Datos de autorización guardados en '{ruta}'")
