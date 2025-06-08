from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from services.login_service import iniciar_sesion
from services.autorizacion_service import consultar_autorizacion
import time

numeros_autorizacion = [
    "29766906",
    "29766636",
    "29766521"
]

if __name__ == "__main__":
    for numero in numeros_autorizacion:
        print(f"\n🔁 Consultando autorización: {numero}\n")

        driver = webdriver.Chrome()
        wait = WebDriverWait(driver, 15)

        try:
            iniciar_sesion(driver, wait)
            consultar_autorizacion(driver, wait, numero)
        finally:
            driver.quit()
            time.sleep(2)
