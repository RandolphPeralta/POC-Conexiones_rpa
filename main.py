from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from services.login_service import iniciar_sesion
from services.autorizacion_service import consultar_autorizacion
from services.control_entregas_service import gestionar_control_entregas
import time
from datetime import datetime, timedelta

numeros_autorizacion = [
    "29766906",
    "29766636",
    "29766521"
]

def procesar_autorizacion(driver, wait, numero, tiempo_limite_minutos=2):
    inicio = datetime.now()
    tiempo_limite = timedelta(minutes=tiempo_limite_minutos)
    
    print(f"\n🔁 Consultando autorización: {numero}\n")
    
    try:
        # Consultar autorización con manejo de tiempo
        consultar_autorizacion(driver, wait, numero)
        
        # Verificar si se ha excedido el tiempo límite
        if datetime.now() - inicio > tiempo_limite:
            print(f"⏰ Tiempo límite excedido para la autorización {numero}")
            return False
        
        # Gestionar control de entregas con manejo de tiempo
        gestionar_control_entregas(driver, wait, numero)
        
        # Verificar tiempo nuevamente
        if datetime.now() - inicio > tiempo_limite:
            print(f"⏰ Tiempo límite excedido para la autorización {numero}")
            return False
        
        return True
    
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
        iniciar_sesion(driver, wait)
        
        for numero in numeros_autorizacion:
            exito = procesar_autorizacion(driver, wait, numero)
            
            if not exito:
                # Si falló o se excedió el tiempo, reiniciar el navegador
                print("🔄 Reiniciando navegador...")
                driver.quit()
                time.sleep(2)
                
                driver = webdriver.Chrome()
                wait = WebDriverWait(driver, 15)
                iniciar_sesion(driver, wait)
                
    finally:
        if driver:
            driver.quit()