from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from selenium.webdriver.common.keys import Keys

date = "12/06/2025"

def check_date(driver, wait, authorization_number):
    """
    Gestiona el proceso de control y registro de entregas para una autorización si estos
    ya fueron entregados
    
    Args:
        driver: Instancia del navegador
        wait: Instancia de WebDriverWait
        authorization_number: Número de autorización a consultar
        
    Returns:
        Cambio de date dentro del HTML
    """

    time.sleep(0.5)

    try:
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//h3[a[text()='Autorizaciones']]"))).click().click()
        time.sleep(1)
    except:
        pass

    try:
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[text()='Autorizaciones']/parent::a"))).click()
        print("✅ Entraste al módulo de 'Autorizaciones'")
    except Exception as e:
        print("❌ No se pudo acceder al enlace de 'Autorizaciones':", e)
        return


    try:
        input_search = wait.until(EC.presence_of_element_located(
            (By.ID, "frmAutorizaciones:tablaRegistros:j_idt80")))
        input_search.clear()
        input_search.send_keys(authorization_number)
    except Exception as e:
        print("❌ No se pudo ingresar el número de autorización:", e)
        return

    try:
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(@class, 'ui-icon-refresh')]/ancestor::button"))).click()
    except Exception as e:
        print("❌ No se pudo hacer clic en Refrescar:", e)
        return
    
    
    try:
        # Esperar a que se cierre completamente el diálogo anterior
        time.sleep(2)
        
        # Diccionario para almacenar los results
        results = {
            'success': False,
            'data': None,
            'error': None,
            'filepath': None
        }

        # 1. Hacer clic en "Control y Registro de Entregas"
        try:
            control_button = wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[@title='Control y registro de entregas' and contains(@class, 'ui-button')]"
            )))
            control_button.click()
            print("✅ Se hizo clic en 'Control y registro de entregas' correctamente.")
        except Exception as e:
            error_msg = f"No se pudo hacer clic en el botón de control: {str(e)}"
            print(f"❌ {error_msg}")
            results['error'] = error_msg
            return results

    except Exception as e:
            error_msg = f"Error inesperado en gestionar_control_entregas: {str(e)}"
            print(f"❌ {error_msg}")

    try:
        # Esperar a que al menos una fila con la columna "Tipo Entrega" esté visible
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//td[span[@class="ui-column-title" and text()="Tipo Entrega"]]'))
        )
 
        # Obtener la primera celda con columna "Tipo Entrega"
        cell = driver.find_element(By.XPATH, '(//td[span[@class="ui-column-title" and text()="Tipo Entrega"]])[1]')
        full_text = cell.text.strip()
 
        # Remover el encabezado si viene incluido
        if full_text.startswith("Tipo Entrega"):
            text=full_text.replace("Tipo Entrega", "").strip()
        else:
            text=full_text
            print(f"Tipo Entrega {text}")

        status = text
        if status != "Sin Entrega":
                print(" ✅ El Estado Tipo Entrega 'Autorizada'. Se detiene el proceso.")
                return None
            #return
        elif status == "Sin Entrega":
            print("⚠️ El Tipo Entrega es 'Sin Entrega'. Se procederá con el clic en 'Entrega'.")
            pass
            #except Exception as e:
            #    print("❌ Error al verificar el status de la tabla:", e)
            #return
    except Exception as e:
        print(f"❌ No se pudo obtener el status de la primera fila: {e}")
        #return False


    try:
        # Esperar a que aparezca la tabla con los botones de entrega (ajusta el tiempo si es necesario)
        delivery_button = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[@title='Entregar' and contains(@class, 'ui-button-icon-only')]"
        )))
        delivery_button.click()
        print("✅ Se hizo clic en el botón 'Entregar' correctamente.")
    except Exception as e:
        print(f"❌ No se pudo hacer clic en el botón 'Entregar': {e}")



    

    try:
        # Esperar a que esté presente el campo de date
        input_date = wait.until(EC.presence_of_element_located((
            By.ID, "frmEntrega:fechaEntregaGestionar_input"
        )))

        # Limpiar el campo con .clear() y/o teclas especiales
        input_date.click()
        input_date.send_keys(Keys.CONTROL + "a")  # Seleccionar todo
        input_date.send_keys(Keys.DELETE)         # Borrar contenido

        # Ingresar la nueva date (en el formato que el sistema espera, por ejemplo: dd/mm/yyyy)
        desired_date = date
        input_date.send_keys(desired_date)
        print(f"✅ Fecha ingresada correctamente: {desired_date}")

    except Exception as e:
        print(f"❌ No se pudo ingresar la fecha en el campo: {e}")

    try:
        # Esperar a que el botón de cerrar (ícono X) esté presente y clickeable
        close_button = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//div[contains(@class, 'ui-dialog-titlebar') and .//span[text()='Entregar']]//a[contains(@class, 'ui-dialog-titlebar-close')]"
        )))
        close_button.click()
        print("✅ Se cerró la ventana de 'Entregar' correctamente.")
    except Exception as e:
        print(f"❌ No se pudo cerrar la ventana de 'Entregar': {e}")


    # 3. Cerrar el diálogo de Control y Registro de Entregas (versión mejorada)
    try:
        # Esperar a que el diálogo esté completamente cargado
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.ui-dialog[aria-labelledby='j_idt281_title']")))
            
        # Opción 1: Intentar cerrar con el botón X (versión más específica)
        try:
            close_button = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div.ui-dialog[aria-labelledby='j_idt281_title'] a.ui-dialog-titlebar-close")
            ))
            close_button.click()
            print("✅ Diálogo de control cerrado con el botón X (selector específico)")
        except Exception as e:
            print(f"⚠️ No se pudo cerrar con botón X (intentando alternativa): {str(e)}")
                
        # Opción 2: Intentar con el botón Salir si existe
        #try:
        #    exit_button = wait.until(EC.element_to_be_clickable(
        #        (By.XPATH, "//div[@id='j_idt281']//button[contains(text(), 'Salir')]")
        #    ))
        #    exit_button.click()
        #    print("✅ Diálogo de control cerrado con el botón Salir")
        #except Exception as e:
        #    print(f"⚠️ No se pudo cerrar con botón Salir (intentando JavaScript): {str(e)}")
                    
        # Opción 3: Forzar cierre con JavaScript
        try:
            driver.execute_script("""
            var dialogs = document.querySelectorAll('div.ui-dialog');
            dialogs.forEach(function(dialog) {
            var title = dialog.querySelector('.ui-dialog-title');
            if(title && title.textContent.includes('Control y registro de entregas')) {
            var closeBtn = dialog.querySelector('a.ui-dialog-titlebar-close');
            if(closeBtn) closeBtn.click();
            }
            });
            """)
            print("✅ Diálogo de control cerrado mediante JavaScript")
        except Exception as js_e:
            print(f"⚠️ Fallo al cerrar con JavaScript: {str(js_e)}")
                        
    except Exception as e:
        print(f"❌ Error grave al intentar cerrar el diálogo: {str(e)}")

    return