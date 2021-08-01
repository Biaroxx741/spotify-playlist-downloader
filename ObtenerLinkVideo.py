from time import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os, time, glob, requests
from webdriver_manager.chrome import ChromeDriverManager

driver = None
DOWNLOAD_PATH = os.path.join(os.environ['USERPROFILE'], 'Downloads')
def PrevConfigs():
    '''
    Inicializa el webdriver. Es usado en una funcion con el fin de solo ejecutarse una vez obtenido los datos
    necesarios del usuario.
    '''
    opts = Options()
    opts.add_argument("--headless")
    opts.add_experimental_option("excludeSwitches", ["enable-logging"])
    global driver 
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)
    # driver = webdriver.Chrome(r'C:\SeleniumChromeDriver\chromedriver.exe')
    os.system('cls')

def CheckExtraTabs():
    '''
    Detecta si hay mas de un tab abierto, y en caso afirmativo, los cierra dejando solo la primer tab.\n
    Esto mas que nada para evitar la apertura de tabs debido a ads.
    '''
    driver_len = len(driver.window_handles) 
    if driver_len > 1: 
        for i in range(driver_len - 1, 0, -1):
            driver.switch_to.window(driver.window_handles[i]) 
            driver.close()
        driver.switch_to.window(driver.window_handles[0]) 

def CheckIfDownloadFinished():
    '''
    Verifica si en el directorio de descargas existe almenos un archivo siendo descargado,
    si lo encuentra espera 5 segundos y vuelve a chequear.
    '''
    while True:
        checkExt = []
        checkExt.extend(glob.glob(os.path.join(DOWNLOAD_PATH,'*.crdownload')))
        if len(checkExt) == 0:
            break
        time.sleep(5)

def DownloadVid(videoID, nombreCancion):
    '''
    Usa la web \'y2mate.com\' para convertir y descargar la version .mp3 del tema.\n
    :param videoID: el ID del video a descargar\n
    :param nombreCancion: nombre usado al momento de guardar la cancion como archivo
    '''
    driver.get(f'https://www.y2mate.com/youtube-mp3/{videoID}')
    time.sleep(5)
    while True:
        try:
            driver.find_element_by_id('process_mp3').click()
            time.sleep(5)
            urlDescarga = driver.find_element_by_id('process-result').find_element_by_class_name('has-success').find_element_by_class_name('btn-success').get_attribute("href")
            # driver.get(urlDescarga)
            r = requests.get(urlDescarga)
            nombreCancion += '.mp3'
            rutaArchivo = os.path.join(DOWNLOAD_PATH, nombreCancion)
            with open(rutaArchivo, 'wb') as outfile:
                outfile.write(r.content)
            CheckIfDownloadFinished()
            CheckExtraTabs()
            break
        except Exception as e:
            print(e)
            driver.refresh()
            time.sleep(5)
            pass

def PrepareName2Query(nombre):
    '''
    Elimina potenciales caracteres no deseados.\n
    Reemplaza los espacios por \'+\' para poder usarlo como query en la URL de Youtube.\n
    Le adheciona la palabra \'+letra\' para obtener los videos con lyrics (y asi evitar clips de videos con intros no deseadas).\n
    :return texto: el texto con todas las modificaciones aplicadas.
    '''
    texto = nombre.replace('-', '').replace(' ', '+').replace(',', '').replace('++', '+')
    texto += '+letra'
    return texto

def GetVideoID(nombre):
    '''
    Devuelve el ID del video obteniendolo del primer resultado de busqueda de Youtube.\n
    :param nombre: nombre de la cancion y (opcionalmente) del artista
    :return videoID: ID del video
    '''
    nombreListo = PrepareName2Query(nombre)
    driver.get(f'https://www.youtube.com/results?search_query={nombreListo}')
    time.sleep(2)
    while True:
        try:
            VideoID = driver.find_element_by_id("video-title").get_attribute("href")
            VideoID = VideoID.split('=')[1]
            break
        except:
            driver.refresh()
            pass
    return VideoID
    # DownloadVid(VideoID)

def CloseWin():
    driver.quit()
    
