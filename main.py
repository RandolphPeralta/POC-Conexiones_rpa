from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from services.login_service import login
from services.autorizacion_service import check_authorization
from services.control_entregas_service import manage_delivery_control
import time
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# Agregar al inicio del script para suprimir logs no deseados
from selenium.webdriver.remote.remote_connection import LOGGER
import logging

# Configurar nivel de logging
LOGGER.setLevel(logging.WARNING)
logging.basicConfig(level=logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

numeros_autorizacion = [
    "29766906",
    "29766636",
    "29766521",
    "29820829", #ANULADA, 
    "29799161", #ANULADA,
    "29809259",
    "29809115",
    "29808833",
    "29808738"

]

def process_authorization(driver, wait, numero, tiempo_limite_minutos=2):
    inicio = datetime.now()
    tiempo_limite = timedelta(minutes=tiempo_limite_minutos)
    
    print(f"\n🔁 Consultando autorización: {numero}\n")
    
    try:
        # Volver a la página inicial para asegurar estado consistente
        time.sleep(0.5)
        #driver.get("https://conexiones.saviasaludeps.com/savia/home.faces")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
        
        # Nuevo: obtener estado junto con éxito
        exito = check_authorization(driver, wait, numero)

        if not exito:
            print(f"❌ Falló consulta para {numero}")
            return False

        #if estado.lower() != "autorizada":
        #    print(f"⛔ Estado no autorizado ({estado}) para {numero}. Saltando...")
        #    return True  # No es error crítico, simplemente lo salta        
        
        
        # Consultar autorización
        #if not check_authorization(driver, wait, numero):
        #    print(f"❌ Falló consulta para {numero}")
        #    return False
            
        if datetime.now() - inicio > tiempo_limite:
            print(f"⏰ Tiempo límite excedido para {numero}")
            return False
            
        # Volver a cargar página antes de control de entregas
        #driver.get("https://conexiones.saviasaludeps.com/savia/home.faces")
        time.sleep(0.5)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
        
        # Gestionar control de entregas
        if not manage_delivery_control(driver, wait, numero):
            print(f"❌ Falló control de entregas para {numero}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Error crítico al procesar {numero}: {str(e)}")
        return False
    
    except Exception as e:
        print(f"❌ Error al procesar autorización {numero}: {str(e)}")
        return False

if __name__ == "__main__":
    driver = None
    
    try:
        # En la parte donde inicias el navegador, agregar opciones para suprimir logs:
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--log-level=3')
        options.add_argument('--disable-logging')

        # Iniciar navegador con las opciones
        driver = webdriver.Chrome(options=options)
        # Iniciar sesión una sola vez al principio
        #driver = webdriver.Chrome()
        wait = WebDriverWait(driver, 15)
        login(driver, wait)
        
        for numero in numeros_autorizacion:
            exito = process_authorization(driver, wait, numero)
            
            if not exito:
                # Si falló o se excedió el tiempo, reiniciar el navegador
                print("🔄 Reiniciando navegador...")
                driver.quit()
                time.sleep(2)
                
                driver = webdriver.Chrome()
                wait = WebDriverWait(driver, 15)
                login(driver, wait)

                
    finally:
        if driver:
            driver.quit()