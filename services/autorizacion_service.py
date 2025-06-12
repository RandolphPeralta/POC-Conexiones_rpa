from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import json
from utils.file_utils import guardar_autorizacion_json

# Agregar al inicio del script para suprimir logs no deseados
from selenium.webdriver.remote.remote_connection import LOGGER
import logging

# Configurar nivel de logging
LOGGER.setLevel(logging.WARNING)
logging.basicConfig(level=logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)


def check_authorization(driver, wait, numero_autorizacion):
    """
    Gestiona las autorizaciones
    
    Args:
        driver: Instancia del navegador
        wait: Instancia de WebDriverWait
        numero_autorizacion: Número de autorización a consultar
        
    Returns:
        datos: Diccionario con los datos de la autorizacion
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
    
    time.sleep(0.5)

    try:
        # Esperar a que al menos una fila con la columna "Estado" esté visible
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

        if text != "Autorizada":
                print("⚠️ El estado no es 'Autorizada'. Se detiene el proceso.")
                #return
        else:
            print("✅ El estado es 'Autorizada'. Se procederá con el clic en 'Ver'.")
            #except Exception as e:
            #    print("❌ Error al verificar el estado de la tabla:", e)
            #return
    except Exception as e:
        print(f"❌ No se pudo obtener el estado de la primera fila: {e}")
    

    try:
        time.sleep(2)
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@title='Ver' and contains(@class, 'ui-button')]"))).click()
    except Exception as e:
        print("❌ No se pudo hacer clic en el botón 'Ver':", e)
        return

    try:
        wait.until(EC.visibility_of_element_located((By.ID, "dialogoVerId")))

        def obtener(id): return driver.find_element(By.ID, id).text

        datos = {
            "autorizacion": {
                "numero": obtener("frmVer:j_idt130"),
                "origen": obtener("frmVer:j_idt132"),
                "solicitud": obtener("frmVer:j_idt137"),
                #"cantidad_entregas": obtener("frmVer:j_idt139"),
                #"fecha_inicio": obtener("frmVer:j_idt141"),
                #"fecha_fin": obtener("frmVer:j_idt143"),
                #"dias_vigencia": obtener("frmVer:j_idt145"),
                #"posfechada": obtener("frmVer:j_idt147"),
                #"fecha_autorizacion": obtener("frmVer:j_idt149"),
                #"impresiones": obtener("frmVer:j_idt151"),
                #"ambito": obtener("frmVer:j_idt153"),
                #"contrato_anticipado": obtener("frmVer:j_idt155")
            },
            "prestador": {
                "tipo_documento": obtener("frmVer:j_idt161"),
                "numero_documento": obtener("frmVer:j_idt163"),
                "razon_social": obtener("frmVer:razonSocialAuditar"),
                #"departamento": obtener("frmVer:departamentoIpsAuditar"),
                #"sede_prestador": obtener("frmVer:j_idt167"),
                #"telefono1": obtener("frmVer:j_idt169"),
                #"telefono2": obtener("frmVer:j_idt173"),
                #"correo": obtener("frmVer:j_idt171"),
                #"municipio": obtener("frmVer:j_idt175"),
                #"direccion": obtener("frmVer:j_idt177")
            },
            "paciente": {
                "nombre": obtener("frmVer:j_idt181"),
                "documento": obtener("frmVer:j_idt183"),
                "contrato": obtener("frmVer:j_idt185"),
                "regimen": obtener("frmVer:j_idt187"),
                "tipo_documento": obtener("frmVer:j_idt191"),
                "fecha_nacimiento": obtener("frmVer:j_idt193"),
                "direccion": obtener("frmVer:j_idt195"),
                "genero": obtener("frmVer:j_idt197"),
                "nivel_sisben": obtener("frmVer:j_idt199"),
                "servicio": obtener("frmVer:j_idt201"),
                "diagnostico_principal": obtener("frmVer:j_idt203")
            },
            #"tecnologias": [],
            #"pagos_compartidos": {
            #    "cuota_moderadora": obtener("frmVer:j_idt232"),
            #    "cuota_recuperacion": obtener("frmVer:j_idt234"),
            #    "copago": obtener("frmVer:j_idt236"),
            #    "tope_afiliado": obtener("frmVer:j_idt238"),
            #    "valor": obtener("frmVer:j_idt240"),
            #    "porcentaje": obtener("frmVer:j_idt242"),
            #    "nombre_autorizador": obtener("frmVer:j_idt244"),
            #    "cargo": obtener("frmVer:j_idt246")
            #},
            #"observaciones": ""
        }

        #try:
        #    datos["observaciones"] = driver.find_element(By.ID, "frmVer:j_idt257").text.strip()
        #except:
        #    datos["observaciones"] = ""

        #try:
        #    filas = driver.find_elements(By.XPATH, "//tbody[@id='frmVer:tablaTecnologiasVer_data']/tr")
        #    for fila in filas:
        #        celdas = fila.find_elements(By.TAG_NAME, "td")
        #        datos["tecnologias"].append({
        #            "tipo": celdas[0].text,
        #            "codigo": celdas[1].text,
        #            "descripcion": celdas[2].text,
        #            "cantidad": celdas[3].text,
        #            "valor": celdas[4].text
        #        })
        #except Exception as e:
        #    print(f"⚠️ No se pudieron extraer tecnologías: {e}")

        guardar_autorizacion_json(numero_autorizacion, datos)
        
        # 7. Cerrar el diálogo de visualización (versión mejorada para Autorizaciones)
        try:
            # Esperar a que el diálogo esté completamente cargado
            wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "div.ui-dialog[aria-labelledby='dialogoVerId_title']")
            ))
            
            # Opción 1: Intentar cerrar con el botón X (selector específico para Autorizaciones)
            try:
                boton_cerrar = wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "div.ui-dialog[aria-labelledby='dialogoVerId_title'] a.ui-dialog-titlebar-close")
                ))
                boton_cerrar.click()
                print("✅ Diálogo de Autorizaciones cerrado con el botón X")
            except Exception as e:
                print(f"⚠️ No se pudo cerrar Autorizaciones con botón X (intentando alternativa): {str(e)}")
                
                # Opción 2: Intentar con el botón "Salir" si existe
                try:
                    boton_salir = wait.until(EC.element_to_be_clickable(
                        (By.XPATH, "//div[@id='dialogoVerId']//button[contains(text(), 'Salir')]")
                    ))
                    boton_salir.click()
                    print("✅ Diálogo de Autorizaciones cerrado con el botón Salir")
                except Exception as e:
                    print(f"⚠️ No se pudo cerrar Autorizaciones con botón Salir (intentando JavaScript): {str(e)}")
                    
                    # Opción 3: Forzar cierre con JavaScript específico para Autorizaciones
                    try:
                        driver.execute_script("""
                            var dialogs = document.querySelectorAll('div.ui-dialog');
                            dialogs.forEach(function(dialog) {
                                var closeBtn = dialog.querySelector('a.ui-dialog-titlebar-close');
                                if(closeBtn) closeBtn.click();
                            });
                        """)
                        print("✅ Diálogo de Autorizaciones cerrado mediante JavaScript")
                    except Exception as js_e:
                        print(f"⚠️ Fallo al cerrar Autorizaciones con JavaScript: {str(js_e)}")
                        
        except Exception as e:
            print(f"❌ Error grave al intentar cerrar el diálogo de Autorizaciones: {str(e)}")
        
        # Esperar a que se cierre completamente el diálogo
        time.sleep(2)
        
    except Exception as e:
        print("❌ Error al extraer datos del diálogo:", e)
        return None
        
    return datos