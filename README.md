# DRAEX - Dump the Royal Spanish Academy's dictionary

DRAEX allows you to bypass the restrictions on the [ Royal Spanish Academy's online dictionary ](http://dle.rae.es/) 
and download word definitions for offline usage.

## Getting started

Clone this repository and cd into it:

```bash
git clone http://github.com/rmonvfer/draex && cd draex
```

Then install the required dependencies:

```shell
pip3 install -r requirements.txt
```

Now you are ready to go!

## Usage

Fire the script with `python3 draex.py` and follow the on-screen instructions.

## Why?

That's a good question actually.

Royal Spanish Academy's online dictionary implementation just sucks, it uses weird and outdated hacks to prevent bots from scrapping the word definitions but instead of adding a simple captcha-like mechanism they went with a broken javascript challenge and an even more broken rendering system that only prevents human usage.

tl;dr, they throwing public money away instead of using simpler and cheaper systems, so this project was born to take advantage of those flaws and (maybe) help policy makers and other entities become aware of them.

### Ok, but how?

Just use a headless Chrome/Firefox (selenium or whatever you like) to bypass the JS challenge and then beautifulsoup (or any other DOM/XML parser) to scrap the page content. Then add some logic to parse, structure and save the information and there you go!

There are some minor details that I won't explain here because I dont't really like being sued but you'll hopefuly find a way around them.


## Output

DRAEX outputs several files, let's review them one by one

### The debug log

This ~~mess~~ script generates an output log file (the one you **MUST** use when reporting bugs) that looks like the following:

```
[20190226-085731] | 
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
    
[20190226-085731] | Iniciando...
[20190226-085731] | No he podido crear un directorio especial para almacenar las palabras guardadas, ejecútame como administrador.
[20190226-085731] | Almacenaré las definiciones en este mismo directorio
[20190226-085731] | 
--------------------------------------------------------
    1) Extraer todas las definiciones de cada
       palabra contenida en un archivo de texto
    2) Extraer todas las definiciones del diccionario
       de prueba (test_.txt)
    3) Extraer definiciones individualmente
--------------------------------------------------------
    
[20190226-085800] | Procesando archivo de prueba...
[20190226-085800] | Buscando: 'de' ...
[20190226-085805] | HTML obtenido
[20190226-085805] | Hay 0 definiciones en la pagina recibida
[20190226-085805] | La página recibida [http://dle.rae.es/?w=de] es una página de redirección: True
[20190226-085805] | Procesando página de redirección...
[20190226-085805] | Obteniendo links en la pagina de redireccion...
[20190226-085805] | Número de links en la página: 86
[20190226-085805] | Iterando sobre el link <a href="index.html" title="Versión electrónica de la 23.ª edición del «Diccionario de la lengua española» («DLE» 23.2: actualización, diciembre 2018)">Diccionario de la lengua española </a>
[20190226-085805] | Iterando sobre el link <a href="http://www.rae.es/obras-academicas/diccionarios/diccionario-de-la-lengua-espanola" target="_blank" title="«Diccionario de la lengua española» - Edición del Tricentenario">Edición del Tricentenario</a>
[20190226-085805] | Iterando sobre el link <a class="text" href="/?t=/docs/aviso.html" id="avisoh" title="AVISO IMPORTANTE"><span style="color:rgb(0, 255, 126)">Actualización 2018</span></a>
[20190226-085805] | Iterando sobre el link <a class="icon fa-angle-down" href="http://www.rae.es/" target="_blank">RAE.es</a>
[20190226-085805] | Iterando sobre el link <a href="http://www.rae.es/recursos" style="display: block;" target="_blank">Recursos</a>
[20190226-085805] | Iterando sobre el link <a href="http://www.rae.es/formulario/unidrae" style="display: block;" target="_blank" title="Unidad Interactiva del Diccionario de la lengua española">UNIDRAE</a>
[20190226-085805] | Iterando sobre el link <a href="http://www.rae.es/consultas-linguisticas" style="display: block;" target="_blank">Consultas lingüísticas</a>
[20190226-085805] | Iterando sobre el link <a href="http://www.rae.es/recursos/gramatica/nueva-gramatica" style="display: block;" target="_blank">Gramática</a>
[20190226-085805] | Iterando sobre el link <a href="http://www.rae.es/recursos/ortografia/ortografia-2010" style="display: block;" target="_blank">Ortografía</a>
[20190226-085805] | Iterando sobre el link <a href="http://www.rae.es/recursos/banco-de-datos/corpes-xxi" style="display: block;" target="_blank" title="Corpus del Español del Siglo XXI">CORPES XXI</a>
[20190226-085805] | Iterando sobre el link <a href="http://www.rae.es/recursos/diccionarios/nuevo-diccionario-historico" style="display: block;" target="_blank" title="Nuevo diccionario histórico del español">NDHE</a>
[20190226-085805] | Iterando sobre el link <a href="http://archivo.rae.es" style="display: block;" target="_blank" title="Archivo de la Real Academia Española">Archivo</a>
[20190226-085805] | Iterando sobre el link <a href="https://letras.rae.es" style="display: block;" target="_blank" title="Letras de la Real Academia Española">Tienda de la RAE</a>
```

(And yeah I know it's in spanish bc I am lazy and translation takes time)

### The definitions

Definitions are saved twice:
 - One goes to a JSON file named `general.json`, which contains all scraped definitions.
 - The other one goes to another JSON with the same name as the defined word.


For example, if you defined the word _"diccionario"_:

```javascript
{
    'usoNormal' : {
        1 : 'Definicion1',
        2 : 'Definición2',
        3 : 'Definición3'
    },
    'usoEspecial' : {
        1 : 'Definicion1',
        2 : 'Definición2',
        3 : 'Definición3'
    }
}
```

Note how the definition object is splitted into 2 sections based on the definition's usage.

## Legal notice
This software is released under the terms expressed in the MIT License. Please, refer to the LICENSE file for more information.
