from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from services.login_service import login
from services.autorizacion_service import check_authorization
from services.control_entregas_service import manage_delivery_control
from services.process_autorization import process_authorization
import time
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.webdriver.remote.remote_connection import LOGGER
import logging

# Configurar nivel de logging
LOGGER.setLevel(logging.WARNING)
logging.basicConfig(level=logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

authorization_numbers = [
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
        
        for number in authorization_numbers:
            exito = process_authorization(driver, wait, number)
            
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