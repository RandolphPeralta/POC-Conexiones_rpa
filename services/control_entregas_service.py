from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from utils.file_utils import guardar_control_entregas_json

def gestionar_control_entregas(driver, wait, numero_autorizacion):
    """
    Gestiona el proceso de control y registro de entregas para una autorización
    
    Args:
        driver: Instancia del navegador
        wait: Instancia de WebDriverWait
        numero_autorizacion: Número de autorización a consultar
        
    Returns:
        dict: Diccionario con los datos del control de entregas
    """
    try:
    # Solo colapsar si está colapsado
        panel = wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[a[text()='Autorizaciones']]")))
        if "collapsed" in panel.get_attribute("class"):  # o cualquier validación del estado
            panel.click()
            time.sleep(1)
    except Exception as e:
        print("⚠️ No se pudo verificar o expandir 'Autorizaciones':", e)

    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Autorizaciones']/parent::a"))).click()
        print("✅ Entraste al módulo de 'Autorizaciones'")
    except Exception as e:
        print("❌ No se pudo acceder al enlace de 'Autorizaciones':", e)
        return


    try:
        input_busqueda = wait.until(EC.presence_of_element_located(
            (By.ID, "frmAutorizaciones:tablaRegistros:j_idt80")))
        input_busqueda.clear()
        input_busqueda.send_keys(numero_autorizacion)
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
        
        # Diccionario para almacenar los resultados
        resultados = {
            'success': False,
            'data': None,
            'error': None,
            'filepath': None
        }

        # 1. Hacer clic en "Control y Registro de Entregas"
        try:
            boton_control = wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[@title='Control y registro de entregas' and contains(@class, 'ui-button')]"
            )))
            boton_control.click()
            print("✅ Se hizo clic en 'Control y registro de entregas' correctamente.")
        except Exception as e:
            error_msg = f"No se pudo hacer clic en el botón de control: {str(e)}"
            print(f"❌ {error_msg}")
            resultados['error'] = error_msg
            return resultados

        # 2. Esperar y extraer información del diálogo
        try:
            # Esperar a que el diálogo esté visible
            wait.until(EC.visibility_of_element_located((By.ID, "j_idt281")))
            
            datos_control = {
                "informacion_autorizacion": {},
                "tecnologias": []
            }
            
            # Extraer información de autorización
            datos_control["informacion_autorizacion"] = {
                "autorizacion": driver.find_element(By.ID, "frmGestionar:j_idt286").text,
                "origen": driver.find_element(By.ID, "frmGestionar:j_idt288").text,
                "anexo_3": driver.find_element(By.ID, "frmGestionar:j_idt292").text,
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
                filas_tecnologias = driver.find_elements(
                    By.XPATH, "//div[@id='frmGestionar:pTecnologiasGestionar_content']//tbody[@id='frmGestionar:tablaTecnologiasGestionar_data']/tr")
                
                for fila in filas_tecnologias:
                    celdas = fila.find_elements(By.TAG_NAME, "td")
                    tecnologia = {
                        #"tipo": celdas[0].text,
                        #"codigo": celdas[1].text,
                        #"descripcion": celdas[2].text,
                        #"cantidad": celdas[3].text,
                        "tipo_entrega": celdas[4].text
                    }
                    datos_control["tecnologias"].append(tecnologia)
            except Exception as e:
                print(f"⚠️ No se pudieron extraer las tecnologías: {e}")

            # Guardar en JSON usando la función modularizada
            ruta_archivo = guardar_control_entregas_json(numero_autorizacion, datos_control)
            
            resultados['success'] = True
            resultados['data'] = datos_control
            resultados['filepath'] = ruta_archivo

        except Exception as e:
            error_msg = f"Error al extraer datos del diálogo de control: {str(e)}"
            print(f"❌ {error_msg}")
            resultados['error'] = error_msg

        # 3. Cerrar el diálogo de Control y Registro de Entregas (versión mejorada)
        try:
            # Esperar a que el diálogo esté completamente cargado
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.ui-dialog[aria-labelledby='j_idt281_title']")))
            
            # Opción 1: Intentar cerrar con el botón X (versión más específica)
            try:
                boton_cerrar = wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "div.ui-dialog[aria-labelledby='j_idt281_title'] a.ui-dialog-titlebar-close")
                ))
                boton_cerrar.click()
                print("✅ Diálogo de control cerrado con el botón X (selector específico)")
            except Exception as e:
                print(f"⚠️ No se pudo cerrar con botón X (intentando alternativa): {str(e)}")
                
                # Opción 2: Intentar con el botón Salir si existe
                try:
                    boton_salir = wait.until(EC.element_to_be_clickable(
                        (By.XPATH, "//div[@id='j_idt281']//button[contains(text(), 'Salir')]")
                    ))
                    boton_salir.click()
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

        return resultados

    except Exception as e:
        error_msg = f"Error inesperado en gestionar_control_entregas: {str(e)}"
        print(f"❌ {error_msg}")
        resultados['error'] = error_msg
        return resultados