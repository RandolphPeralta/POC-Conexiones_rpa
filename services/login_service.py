from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os

def iniciar_sesion(driver, wait):
    load_dotenv()
    usuario = os.getenv("USUARIO_SAVIA")
    contrasena = os.getenv("CONTRASENA_SAVIA")

    driver.get("https://conexiones.saviasaludeps.com/savia/home.faces")

    wait.until(EC.presence_of_element_located((By.ID, "login:usuario"))).send_keys(usuario)
    driver.find_element(By.ID, "login:contrasena").send_keys(contrasena + Keys.RETURN)

    wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
