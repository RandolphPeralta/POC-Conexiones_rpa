from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from services.login_service import iniciar_sesion
from services.autorizacion_service import consultar_autorizacion
from services.control_entregas_service import gestionar_control_entregas
import time
from threading import Thread
import sys

numeros_autorizacion = [
    "29766906",
    "29766636",
    "29766521"
]

def ejecutar_consulta(driver, wait, numero, tiempo_limite):
    """
    Función que ejecuta la consulta con un tiempo límite
    """
    try:
        # Configurar el temporizador
        def temporizador():
            time.sleep(tiempo_limite)
            sys.exit(1)  # Forzar la terminación del hilo
        
        timer_thread = Thread(target=temporizador)
        timer_thread.daemon = True
        timer_thread.start()
        
        # Ejecutar las consultas
        consultar_autorizacion(driver, wait, numero)
        gestionar_control_entregas(driver, wait, numero)
        
    except SystemExit:
        print(f"⏰ Tiempo límite alcanzado ({tiempo_limite} segundos) para la autorización {numero}")
    except Exception as e:
        print(f"❌ Error durante la consulta de {numero}: {str(e)}")

if __name__ == "__main__":
    tiempo_limite = 120  # 2 minutos en segundos
    
    for numero in numeros_autorizacion:
        print(f"\n🔁 Consultando autorización: {numero}\n")
        
        driver = None
        intentos = 0
        max_intentos = 3
        exito = False
        
        while intentos < max_intentos and not exito:
            intentos += 1
            try:
                driver = webdriver.Chrome()
                wait = WebDriverWait(driver, 15)
                
                # Iniciar sesión solo si es el primer intento o si falló la consulta anterior
                if intentos == 1:
                    iniciar_sesion(driver, wait)
                
                # Ejecutar la consulta con tiempo límite
                ejecutar_consulta(driver, wait, numero, tiempo_limite)
                exito = True
                
            except Exception as e:
                print(f"⚠️ Intento {intentos} fallido para {numero}: {str(e)}")
                if driver:
                    driver.quit()
                time.sleep(5)  # Esperar antes de reintentar
            finally:
                if driver:
                    driver.quit()
                time.sleep(2)  # Espera corta entre cierre y nueva instancia
        
        if not exito:
            print(f"❌ No se pudo completar la consulta para {numero} después de {max_intentos} intentos")