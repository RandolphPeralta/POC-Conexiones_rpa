
from services.autorizacion_service import check_authorization
from services.control_entregas_service import manage_delivery_control
from services.check_date_authorizations import check_date
import time
from datetime import datetime, timedelta
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.webdriver.remote.remote_connection import LOGGER
import logging

# Configurar nivel de logging
LOGGER.setLevel(logging.WARNING)
logging.basicConfig(level=logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)


def process_authorization(driver, wait, number, time_limit_minutes=3):
    """
    Procesa una autorización específica, incluyendo su consulta y la gestión de entregas.

    La función navega al módulo de autorizaciones, busca la autorización por su número,
    verifica que su estado sea 'Autorizada' y, si es así, procede con el control de entregas.
    Incorpora un límite de tiempo para cada procesamiento y reinicia el navegador
    si la autorización no está 'Autorizada' o si ocurre un error.

    Args:
        driver: Instancia de `webdriver` de Selenium, que representa el navegador.
        wait: Instancia de `WebDriverWait` de Selenium, utilizada para esperar
              condiciones específicas de los elementos web.
        number (str): El número de autorización a procesar.
        time_limit_minutes (int, optional): El tiempo máximo en minutos permitido
                                            para procesar una autorización.
                                            Por defecto es 2 minutos.

    Returns:
        bool: Retorna `True` si la autorización fue procesada exitosamente (es decir,
              se encontró como 'Autorizada' y se gestionó el control de entregas).
              Retorna `False` si la autorización no está 'Autorizada', si excede
              el tiempo límite, o si ocurre cualquier otro error durante el proceso.

    Raises:
        TimeoutException: Propagada desde las funciones internas de Selenium si un
                          elemento no se encuentra en el tiempo esperado.
        Exception: Captura y maneja cualquier otro error inesperado que pueda ocurrir
                   durante la ejecución, imprimiendo un mensaje y retornando `False`.
    """
    start = datetime.now()
    time_limit = timedelta(minutes=time_limit_minutes)
    
    print(f"\n🔁 Consultando autorización: {number}\n")
    
    try:
        # Volver a la página inicial para asegurar estado consistente
        time.sleep(0.5)
        #driver.get("https://conexiones.saviasaludeps.com/savia/home.faces")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
        
        # Nuevo: obtener estado junto con éxito
        #exito = check_authorization(driver, wait, number)

        #if not exito:
        #    print(f"❌ Falló consulta para {number}")
        #    return False

        auth_data = check_authorization(driver, wait, number)

        if not auth_data:
            print(f"Falló consulta para {number}")
            return False
        
        
        #if estado.lower() != "autorizada":
        #    print(f"⛔ Estado no autorizado ({estado}) para {number}. Saltando...")
        #    return True  # No es error crítico, simplemente lo salta        
        
        
        # Consultar autorización
        #if not check_authorization(driver, wait, number):
        #    print(f"❌ Falló consulta para {number}")
        #    return False
            
        if datetime.now() - start > time_limit:
            print(f"⏰ Tiempo límite excedido para {number}")
            return False
            
        # Volver a cargar página antes de control de entregas
        #driver.get("https://conexiones.saviasaludeps.com/savia/home.faces")
        time.sleep(0.5)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
        
        # Gestionar control de entregas
        #if not manage_delivery_control(driver, wait, number):
        #    print(f"❌ Falló control de entregas para {number}")
        #    return False

        control_result = manage_delivery_control(driver, wait, number)
        if not control_result or not control_result.get("success"):
            return None
        
        time.sleep(0.5)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
        # Gestionar las fechas de control de entregas
        if not check_date(driver, wait, number):
            print(f"⚙️ Revision de control de fechas de entregas para {number} terminado")
            return True

        control_data = control_result.get("data", {})
        tecnologias = control_data.get("tecnology", [])
        technology_code = tecnologias[0]["code"] if tecnologias else None

        # ✅ Consolidar JSON final
        result_json = {
            "authorization_code": auth_data["autorizacion"]["numero"],
            "document": auth_data["paciente"]["documento"],
            "patient_name": auth_data["paciente"]["nombre"],
            "government": auth_data["paciente"]["regimen"],
            "gender": auth_data["paciente"]["genero"],
            "cups_code": technology_code
        }
        
        return result_json, print(result_json)        

            
        return True
        
    except Exception as e:
        print(f"❌ Error crítico al procesar {number}: {str(e)}")
        return False
    
    except Exception as e:
        print(f"❌ Error al procesar autorización {number}: {str(e)}")
        return False

