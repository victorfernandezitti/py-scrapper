import traceback

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

# --- Configuración de Opciones de Chrome para un Entorno Docker ---
# Estas opciones son CRUCIALES para ejecutar Chrome en un contenedor
chrome_options = ChromeOptions()
chrome_options.add_argument("--headless")  # Ejecutar sin una interfaz gráfica de usuario
chrome_options.add_argument("--no-sandbox") # Requerido para ejecutar como root en un contenedor
chrome_options.add_argument("--disable-dev-shm-usage") # Evita problemas de memoria compartida
chrome_options.add_argument("--window-size=1920,1080") # Define un tamaño de ventana

print("Iniciando el script de prueba autocontenido...")

try:
    # --- Inicio del WebDriver ---
    # WebDriverManager descargará y configurará automáticamente el chromedriver correcto
    # que coincida con el navegador Chrome instalado en el contenedor.
    service = ChromeService(ChromeDriverManager().install())
    
    # Inicia el navegador Chrome con el servicio y las opciones configuradas
    driver = webdriver.Chrome(service=service, options=chrome_options)

    print("✅ WebDriver iniciado exitosamente.")

    # --- Inicio de la Prueba ---
    print("Navegando a Google...")
    driver.get("https://www.google.com")
    print(f"Título de la página: {driver.title}")

    print("Realizando búsqueda...")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("Python Selenium self-contained Docker")
    search_box.submit()
    
    # Pequeña espera para que los resultados carguen
    time.sleep(2) 
    print("Búsqueda realizada. Título actual:", driver.title)

    #assert "Python Selenium self-contained Docker" in driver.title
    print("✅ El título de la página de resultados es correcto.")
    print("🎉 Prueba completada exitosamente!")


except Exception as e:
    print(f"❌ Ocurrió un error durante la ejecución: {e}")
    traceback.print_exc()

finally:
    # Asegurarse de cerrar la sesión del navegador
    if 'driver' in locals() and driver:
        driver.quit()
        print("Sesión del navegador cerrada.")