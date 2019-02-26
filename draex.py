
from webbot import Browser
from bs4 import BeautifulSoup
import time, timeit, sys, json, pprint, os, datetime, codecs

web = Browser(showWindow = False)

"""
TODO: Add redirection and notFound manager
"""
log_levels = {4: "NFO", 3: "DBG", 2: "DNG", 1: "CRT" }

global global_level
global_level = 4

global idleTime # Tiempo de espera en segundos
idleTime = 30

global logFile
logFile = open("log", "w+")

global baseUrl 
baseUrl = "http://dle.rae.es/"

global pp
pp = pprint.PrettyPrinter(indent=4)

global creaDict
creaDict = {}

def currentTimeString():
    now = datetime.datetime.now()
    return now.strftime("%Y%m%d-%H%M%S")

def log(text, level):
	if level <= global_level:
	    logFile.write(f"[{currentTimeString()}] | {text}\n")
	    print(f"[{log_levels[level]}] {text}")

def extractDefinition(paragraph):
    try:
        # Buscar el numero de definicion correspondiente al párrafo
        # recibido como parámetro
        definitionOrder = paragraph.find("span", class_= "n_acep").get_text()
        definitionOrder = definitionOrder.split(".")[0] # Eliminar el punto final

        if definitionOrder != None: # Si existe...
            debug("")
            definitionText = paragraph.get_text()
            # Devulve una tupla con el orden de la definición y la propia definición   
            return (int(definitionOrder), definitionText[ 3: ].rstrip())
        else:
            log("Error extrayendo la definición, el parrafo no existe", 1)
            log("Saliendo...", 2)
            system.exit(0)

    except Exception as exc:
        log(f"Error extrayendo los datos semánticos del párrafo: {paragraph}", 3)
        log(f"Excepción: {str(exc)}", 3)

def getDefinitionData(word):
    """
    Receives an string representing a word in the DRAE dictionary
    Then uses Selenium and Firefox Web Driver to run the JS challenge
    and obtain the HTML source code of the Web containing the definitions
    """
    # Call WebDriver and GET the URL with the desired word
    web.go_to(f"{baseUrl}?w={word}")

    # Sleep in order to avoid weird behaviour
    # NOTE: DO NOT CHANGE
    #time.sleep(idleTime)

    # Get page source
    source = web.get_page_source()
    log("HTML obtenido", 3)

    # Identificar el tipo de pagina recibida (redirección, definición o error)
    # Para ello contar el numero de article que contiene
    redirectionPage = isRedirectionPage(source)
    log(f"La página recibida [{baseUrl}?w={word}] es una página de redirección: {redirectionPage}", 3)
    return (BeautifulSoup(source , features="html.parser"), redirectionPage)

def processWordInRedirectionPage(wordRedirectionPage, lastIndex, lastDict):
    completeDefinitions = lastDict
    currentWord = wordRedirectionPage
    
    log("Procesando página de redirección", 3)

    try:
        pageData = getDefinitionData(currentWord.rstrip())
        soup = pageData[0]

        log("Analizando el HTML para obtener los párrafos...", 4)
        paragraphs = soup.find_all("p")
        print(paragraphs)
        # Loop over every single paragraph in the definition page
        log("Extrayendo definiciones de los párrafos", 4)
        maxRef = 0

        for paragraph in paragraphs:

            # Extraer la definición del párrafo
            defResult = extractDefinition(paragraph)
            defNum, defText = defResult
                
            # El numero de la definicion actual es mayor que
            # el máximo previo
            if defNum > maxRef:
                maxRef = defNum
                print(f"[NORM] {defNum}:{defText}")  # Tenemos una definición!
                
                try:
                    # Intentar añadir las definiciones al diccionario
                    completeDefinitions["usoNormal"][defNum] = defText
                
                except Exception as exc:
                    log("Error añadiendo claves al diccionario (NORMAL)", 3)
                    log(f"Excepción: {str(exc)}", 3)

                    #raise exc     
            
            elif defNum <= maxRef:
                print(f"[ESPC] {defNum}:{defText}")
                try:
                    completeDefinitions["usoEspecial"][defNum] = defText
                except Exception as exc:
                    log("Error añadiendo claves al diccionario (ESPECIAL)", 3)
                    log(f"Excepción: {str(exc)}", 3)
                    #raise exc

        return completeDefinitions

    except Exception as exc:
        log("Error extrayendo definiciones de las palabras en la página de redirección", 3)
        log(f"Excepción: {str(exc)}", 3)
        #raise exc

def processWordPage(currentWord):
    completeDefinitions = {
        "usoNormal": {},
        "usoEspecial": {}
    }

    log(f"Buscando: '{currentWord.rstrip()}' ...", 4)
    
    try:
        # Obtener los datos de la pagina
        soup, isRedirection = getDefinitionData(currentWord.rstrip())
        # Si no es una pagina de redireccion, comprobarlo de nuevo
        if not(isRedirection):

            log("Analizando el HTML para obtener los párrafos...", 4)
            paragraphs = soup.find_all("p")
            # Loop over every single paragraph in the definition page
            log("Extrayendo definiciones de los párrafos", 4)

            maxRef = 0

            print(f"TIPO: {len(paragraphs)}\n\n")

            for paragraph in paragraphs:

                # Extraer la definición del párrafo
                defResult = extractDefinition(paragraph)
                defNum, defText = defResult

                # El numero de la definicion actual es mayor que
                # el máximo previo
                if defNum > maxRef:
                    maxRef = defNum
                    print(f"[NORM] {defNum}:{defText}")  # Tenemos una definición!
                    
                    try:
                        # Intentar añadir las definiciones al diccionario
                        completeDefinitions["usoNormal"][defNum] = defText
                    
                    except Exception as exc:
                        log("Error añadiendo claves al diccionario (NORMAL)", 3) 
                        log(f"Excepción: {str(exc)}", 3)
                        ##raise exc     
                
                elif defNum <= maxRef:
                    print(f"[ESPC] {defNum}:{defText}")
                    try:
                        completeDefinitions["usoEspecial"][defNum] = defText
                    except Exception as exc:
                        log("Error añadiendo claves al diccionario (ESPECIAL)", 3)
                        log(f"Excepción: {str(exc)}", 3)
                        ##raise exc

        else:
            log("Procesando página de redirección...", 4)

            # Obtener los links de la página
            log("Obteniendo links en la pagina de redireccion...", 4)
            links = soup.find_all("a")
            
            log(f"Número de links en la página: {len(links)}", 3)

            redirectedWordsIds = []

            # Iterar sobre cada uno
            for link in links:
                log(f"Iterando sobre el link {link}", 3)
                try:
                    # Obtener el href de cada uno
                    currentLink = link["href"]
                    if currentLink not in ["", " ", None]:
                       #log(f"Trabajando sobre el link: {currentLink}", 3)

                        # Las definiciones comienzan con ?id, así las 
                        # podemos aislar para tratarlas indiviualmente
                        if currentLink.startswith("?id"):
                            log("El link es válido, continuando...", 3)
                            # Existe la posibilidad de que haya varios id
                            # en cada href, separados por un |, así que
                            # comprobamos si hay o no
                            if "|" in currentLink: # Hay varios id en un href
                                log("Hay varios ids en el link, separandolos", 3)
                                for individualId in currentLink[:3].split("|"): # Eliminar el ?id y separar los id
                                    redirectedWordsIds.append(individualId)
                            
                            else: # si no, procesarlos tal cual
                                log("No hay varios id en cada link, procesando de forma normal...", 3)
                                individualId = currentLink[:3]
                                redirectedWordsIds.append(individualId)
                                processWordPage(f"{baseUrl}?id={individualId}")

                except Exception as exc:
                    log("Error obteniendo link['href']", 3)
                    log(f"Excepción: {str(exc)}", 3)

            # Ahora, iterar sobre los ids y procesarlos
            idCounter = 0
            for redirectedWordId in redirectedWordsIds:
                fullWordUrl = f"{baseUrl}?id={redirectedWordId}"
                completeDefinitions = processWordInRedirectionPage(fullWordUrl, idCounter, completeDefinitions)
                idCounter += 1

    except Exception as exc:
        log(f"Error obteniendo los datos de la palabra: {currentWord.rstrip()}", 3)
        log(f"Excepción: {str(exc)}", 3)
        #raise exc

    try:
        pp.pprint(completeDefinitions)
        log("Abriendo JSON para guardar las definiciones...", 4)
        log("Convirtiendo dict a JSON y guardando en archivo", 3)

        with codecs.open(f"{currentWord.rstrip()}.json", 'w', encoding='utf-8') as f:
            json.dump(completeDefinitions , f, ensure_ascii=False, indent=4, sort_keys=False)

        log("Completadas todas las operaciones anteriores con éxito", 4)
        log("Archivo de JSON cerrado y listo!", 4)

    except Exception as exc:
        log("Error mostrando y guardando los resultados", 3)
        log(f"Excepción: {str(exc)}", 3)
        #raise exc

    try:
        creaDict[currentWord.rstrip()] = completeDefinitions
    except Exception as exc:
        log(f"No se ha podido guardar la palabra {currentWord.rstrip()} en el diccionario general", 3)
        log(f"Excepción: {str(exc)}", 3)
        #raise exc

    log("Hecho!", 4)

def isRedirectionPage(pageSource):
    pageObject = BeautifulSoup(pageSource , features="html.parser")

    # Contar el numero de "articles" (definiciones) que contiene la pagina recibida
    articles = pageObject.find_all("article")
    log(f"Hay {len(articles)} definiciones en la pagina recibida", 3)
    return len(articles) == 0

def single_extract():
    word = input("[INP] Palabra a buscar? ")
    try:
        processWordPage(word)

    except Exception as exc:
        log(f"No se ha podido procesar la palabra: {word}", 4)
        log(f"Excepción: {str(exc)}", 3)

def read_and_extract():
    file_ = input("[INP] Archivo? ")
    if os.path.exists(file_):
        with open(file_) as fl:
            for word in fl.readlines():
                word = word.strip().lower()
                processWordPage(word)
    else:
        log("La ruta especificada no es válida, comprueba que el archivo exista\nen la ruta especificada en intentalo de nuevo")
        log(f"""
    1) Volver a intentarlo
    2) Volver al menú principal
    3) Salir del programa
    --------------------------------------------------------
        """, 4)
        option = int(input("[INP] Opción? "))
        if option == 2:
            main()
        elif option == 3:
            sys.exit()
        else:
            read_and_extract()

def test_extract():
    log("Procesando archivo de prueba...", 4)
    with open("dicts/test_.txt") as fl:
            for word in fl.readlines():
                word = word.strip().lower()
                processWordPage(word)

def main():
    log(f"""
     ___                                           
    (   )                                          
  .-.| |   ___ .-.      .---.    .--.    ___  ___  
 /   \ |  (   )   \    / .-, \  /    \  (   )(   ) 
|  .-. |   | ' .-. ;  (__) ; | |  .-. ;  | |  | |  
| |  | |   |  / (___)   .'`  | |  | | |   \ `' /   
| |  | |   | |         / .'| | |  |/  |   / ,. \   
| |  | |   | |        | /  | | |  ' _.'  ' .  ; .  
| '  | |   | |        ; |  ; | |  .'.-.  | |  | |  
' `-'  /   | |        ' `-'  | '  `-' /  | |  | |  
 `.__,'   (___)       `.__.'_.  `.__.'  (___)(___) 
--------------------------------------------------
     Extractor del Diccionario de la Real 
         Academia Española (DRAE)
--------------------------------------------------
           | @ramon_vfer - 2019 |
           ----------------------
    """, 4)

    log("Iniciando...", 4)

    try:
        os.mkdir("palabras_definidas")
        os.chdir("palabras_definidas")
        def_sav = os.join(os.getcwd(), "palabras_definidas")
        log(f"Las definiciones se guardarán como un archivo JSON en {def_sav}", 4)

    except Exception as exc:
        log("No he podido crear un directorio especial para almacenar las palabras guardadas, ejecútame como administrador.", 4)
        log("Almacenaré las definiciones en este mismo directorio", 4)

    log(f"""
--------------------------------------------------------
    1) Extraer todas las definiciones de cada
       palabra contenida en un archivo de texto
    2) Extraer todas las definiciones del diccionario
       de prueba (test_.txt)
    3) Extraer definiciones individualmente
--------------------------------------------------------
    """, 4)

    selected_option = int(input("[INP] Selecciona una opción:  "))

    if selected_option == 1:
        read_and_extract()

    elif selected_option == 2:
        test_extract()
    
    elif selected_option == 3:
        single_extract()

    log("Guardando el JSON principal...", 3)
    with codecs.open("general.json", 'w', encoding='utf-8') as sf:
        json.dump(creaDict , sf, ensure_ascii=False, indent=4, sort_keys=False)
    
    log("Hecho!", 4)

    log("Cerrando todos los procesos abiertos...", 4)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        log("KeyboardInterrupt se ha lanzado, interrumpiendo aplicacion...", 2)