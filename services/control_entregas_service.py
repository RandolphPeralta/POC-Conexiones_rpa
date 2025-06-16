from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from utils.file_utils import save_delivery_control_json

def manage_delivery_control(driver, wait, authorization_number):
    """
    Gestiona el proceso de control y registro de entregas para una autorización
    
    Args:
        driver: Instancia del navegador
        wait: Instancia de WebDriverWait
        authorization_number: Número de autorización a consultar
        
    Returns:
        dict: Diccionario con los datos del control de entregas
    """

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

    #try:
    # Solo colapsar si está colapsado
    #    panel = wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[a[text()='Autorizaciones']]")))
    #    if "collapsed" in panel.get_attribute("class"):  # o cualquier validación del estado
    #        panel.click()
    #        time.sleep(1)
    #except Exception as e:
    #    print("⚠️ No se pudo verificar o expandir 'Autorizaciones':", e)

    #try:
    #    wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Autorizaciones']/parent::a"))).click()
    #    print("✅ Entraste al módulo de 'Autorizaciones'")
    #except Exception as e:
    #    print("❌ No se pudo acceder al enlace de 'Autorizaciones':", e)
    #    return


    try:
        input_search = wait.until(EC.presence_of_element_located(
            (By.ID, "frmAutorizaciones:tablaRegistros:j_idt78")))
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
    
    time.sleep(0.5)

    try:
        # Esperar a que al menos una row con la columna "Estado" esté visible
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//td[span[@class="ui-column-title" and text()="Estado"]]'))
        )
 
        # Obtener la primera celda con columna "Estado"
        cell = driver.find_element(By.XPATH, '(//td[span[@class="ui-column-title" and text()="Estado"]])[1]')
        full_text = cell.text.strip()
 
        # Remover el encabezado si viene incluido
        if full_text.startswith("Estado"):
            text=full_text.replace("Estado", "").strip()
        else:
            text=full_text
        print(f"Estado {text}")

        estado = text
        if estado != "Autorizada":
                print("⚠️ El estado no es 'Autorizada'. Se detiene el proceso.")
                return None, estado
                #return
        else:
            print("✅ El estado es 'Autorizada'. Se procederá con el clic en 'Ver'.")
            pass
            #except Exception as e:
            #    print("❌ Error al verificar el estado de la tabla:", e)
            #return
    except Exception as e:
        print(f"❌ No se pudo obtener el estado de la primera row: {e}")
        return False
    
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

        # 2. Esperar y extraer información del diálogo
        try:
            # Esperar a que el diálogo esté visible
            wait.until(EC.visibility_of_element_located((By.ID, "j_idt281")))
            
            control_data = {
                "informacion_autorizacion": {},
                "tecnologias": []
            }
            
            # Extraer información de autorización
            control_data["informacion_autorizacion"] = {
                "autorizacion": driver.find_element(By.ID, "frmGestionar:j_idt286").text,
                #"origen": driver.find_element(By.ID, "frmGestionar:j_idt288").text,
                #"anexo_3": driver.find_element(By.ID, "frmGestionar:j_idt292").text,
                #"cantidad_entregas": driver.find_element(By.ID, "frmGestionar:j_idt294").text,
                #"fecha_inicio": driver.find_element(By.ID, "frmGestionar:j_idt296").text,
                #"fecha_fin": driver.find_element(By.ID, "frmGestionar:j_idt298").text,
                #"dias_vigencia": driver.find_element(By.ID, "frmGestionar:j_idt300").text,
                #"posfechada": driver.find_element(By.ID, "frmGestionar:j_idt302").text,
                #"fecha_autorizacion": driver.find_element(By.ID, "frmGestionar:j_idt304").text,
                #"impresiones": driver.find_element(By.ID, "frmGestionar:j_idt306").text
            }
            
            # Extraer tecnologías con estado de entrega
            try:
                rows_technologies = driver.find_elements(
                    By.XPATH, "//div[@id='frmGestionar:pTecnologiasGestionar_content']//tbody[@id='frmGestionar:tablaTecnologiasGestionar_data']/tr")
                
                for row in rows_technologies:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    technology = {
                        #"tipo": cells[0].text,
                        "codigo": cells[1].text,
                        #"descripcion": cells[2].text,
                        #"cantidad": cells[3].text,
                        #"tipo_entrega": cells[4].text
                    }
                    control_data["tecnologias"].append(technology)
            except Exception as e:
                print(f"⚠️ No se pudieron extraer las tecnologías: {e}")

            # Guardar en JSON usando la función modularizada
            #ruta_archivo = save_delivery_control_json(authorization_number, control_data)
            #print(control_data)

            results['success'] = True
            results['data'] = control_data
            #results['filepath'] = ruta_archivo

        except Exception as e:
            error_msg = f"Error al extraer datos del diálogo de control: {str(e)}"
            print(f"❌ {error_msg}")
            results['error'] = error_msg

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
                try:
                    exit_button = wait.until(EC.element_to_be_clickable(
                        (By.XPATH, "//div[@id='j_idt281']//button[contains(text(), 'Salir')]")
                    ))
                    exit_button.click()
                    print("✅ Diálogo de control cerrado con el botón Salir")
                except Exception as e:
                    print(f"⚠️ No se pudo cerrar con botón Salir (intentando JavaScript): {str(e)}")
                    
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

        return results

    except Exception as e:
        error_msg = f"Error inesperado en gestionar_control_entregas: {str(e)}"
        print(f"❌ {error_msg}")
        results['error'] = error_msg
        return results