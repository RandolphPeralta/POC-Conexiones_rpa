from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os

def login(driver, wait):
    """
    Realiza el proceso de inicio de sesión en la aplicación Savia Salud.

    Carga las credenciales (usuario y contraseña) desde las variables de entorno
    definidas en un archivo .env, navega a la URL de inicio de sesión,
    y completa los campos de usuario y contraseña para autenticarse.

    Args:
        driver: Instancia de `webdriver` de Selenium, que representa el navegador.
        wait: Instancia de `WebDriverWait` de Selenium, utilizada para esperar
              condiciones específicas de los elementos web.

    Raises:
        TimeoutException: Si algún elemento esperado no se encuentra en el tiempo
                          establecido por la instancia `wait`.
        Exception: Cualquier otra excepción que pueda ocurrir durante el proceso
                   de interacción con los elementos web o la carga de credenciales.
    
    """
    load_dotenv()
    user = os.getenv("USUARIO_SAVIA")
    password = os.getenv("CONTRASENA_SAVIA")

    driver.get("https://conexiones.saviasaludeps.com/savia/home.faces")

    wait.until(EC.presence_of_element_located((By.ID, "login:usuario"))).send_keys(user)
    driver.find_element(By.ID, "login:contrasena").send_keys(password + Keys.RETURN)

    wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
