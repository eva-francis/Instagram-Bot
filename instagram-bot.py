from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import sys

# Función para manejo de la consola de comandos
def ImprimirLinea(text):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()

# Clase actual del robot
class InstagramBot:

    def __init__(self, usuario, clave):
        self.usuario = usuario
        self.clave = clave
        self.driver = webdriver.Firefox()

    def CerrarNavegador(self):
        self.driver.close()

    # Función para la localización de elementos por xpath y autorización de credenciales
    def InicioSesion(self):
        driver = self.driver
        driver.get("https://www.instagram.com/")
        time.sleep(2)
        login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        login_button.click()
        time.sleep(2)
        usuario_elem = driver.find_element_by_xpath("//input[@name='username']")
        usuario_elem.clear()
        usuario_elem.send_keys(self.usuario)
        clave_elem = driver.find_element_by_xpath("//input[@name='password']")
        clave_elem.clear()
        clave_elem.send_keys(self.clave)
        clave_elem.send_keys(Keys.RETURN)
        time.sleep(2)

    # Función para la subida e iteración de imágenes
    def Fotos(self, etiqueta):
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + etiqueta + "/")
        time.sleep(2)

        # Reuniendo fotos
        referencias = []
        for i in range(1, 7):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                # Tomar etiquetas
                hrefs_in_view = driver.find_elements_by_tag_name('a')
                # Encontrar nuevas etiquetas relevantes
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if '.com/p/' in elem.get_attribute('href')]
                # Armar una lista de fotos únicas
                [referencias.append(href) for href in hrefs_in_view if href not in referencias]
                # print("Comprobar: largo de referencias de las fotos " + str(len(pic_hrefs)))
            except Exception:
                continue

        # Realizar acciones con las fotos
        fotos_unicas = len(referencias)
        for ref in referencias:
            driver.get(ref)
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                time.sleep(random.randint(2, 4))
                like_button = lambda: driver.find_element_by_xpath('//span[@aria-label="Me gusta"]').click()
                like_button().click()
                for segundos in reversed(range(0, random.randint(18, 28))):
                    ImprimirLinea("#" + etiqueta + ': fotos únicas restantes: ' + str(fotos_unicas)
                                    + " | Temporizador " + str(segundos))
                    time.sleep(1)
            except Exception as e:
                time.sleep(2)
            fotos_unicas -= 1

# Credenciales actuales
usuario = "USERNAME"
clave = "PASSWORD"

instagramBot = InstagramBot(usuario, clave)
instagramBot.InicioSesion()

etiquetas = []

while True:
    try:
        # Elegir una etiqueta al azar de la lista
        etiqueta = random.choice(etiquetas)
        instagramBot.Fotos(etiqueta)
    except Exception:
        instagramBot.CerrarNavegador()
        time.sleep(60)
        instagramBot = InstagramBot(usuario, clave)

instagramBot.InicioSesion()