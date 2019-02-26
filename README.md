# DRAEX - Extractor del Diccionario de la Real Academia Española

### DRAEX elimina las limitaciones de la página web del DRAE permitiendo la descarga en formato JSON todas las definiciones asociadas a una palabra (o a un conjunto de ellas) para su posterior consulta.

#### Página oficial del DRAE: [ Diccionario Online de la Real Academia Española ](http://dle.rae.es/)

# Instalación

DRAEX necesita Python 3.6 o superior para funcionar correctamente. 

## Instalación rápida

Con diferencia, la manera más simple y rápida de instalar _DRAEX_ es utilizando _pip_:

```shell
pip3 install draex
```

## Instalación manual

Si eso no funciona, una solución podría ser instalar las dependencias de forma manual.

Las siguientes librerías (**externas**) son necesarias para ejecutar _DRAEX_:

1. WebBot
2. BeautifulSoup

Para instalarlas, simplemente utiliza pip3:

```shell
pip3 install -r requirements.txt
```

Si por algún motivo eso no funcionase, instálalas individualmente con:

```shell
pip3 install webbot
pip3 install BeautifulSoup
```

Clona este repositorio:

```bash
git clone http://github.com/rmon-vfer/draex.git
```

Una vez clonado, muevete al directorio del repositorio:

```bash
cd ./draex/
```

Para ejecutar el programa, lee la siguiente sección

# Uso

Por el momento, DRAEX solo cuenta con una interfaz interactiva, existen planes para extender la interfaz actual e implementar un modo _avanzado_, si quieres colaborar, haz un _fork_, haz los cambios que creas convenientes y despues haz un _pull request_ a este repositorio.

Para usar el modo interactivo de DRAEX, simplemente escribe:

```shell
python3 draex.py
```

# Implementación

La implementetación de DRAEX es bastante simple si atendemos al problema que la originó, la página web del [ Diccionario Online de la Real Academia Española ](http://dle.rae.es/), que impide mediante un _challenge_ (reto) de JavaScript acceder a la página si no es mediante un navegador con un motor capaz de resolverlo, (_por ejemplo, V8 de Google_)

En la mayoría de los casos es bastante tedioso hacerle ingeniería inversa a un JS Challenge, así que en lugar de hacer eso, decidí renderizar la página web con el WebDriver de Chromium en modo Headless para así resolverlo y obtener el código fuente de la página.
Una vez obtenido es bastante sencillo emplear el HTML para obtener las definiciones y demás datos.

# Resultados

## Logs

El programa genera un archivo log que puede servir posteriormente para su depuración:

#### _main.log_

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

## Definiciones

Las definiciones de almacenan por duplicado, una copia se almacena en un archivo JSON ```general.json``` y otra copia en un archivo cuyo nombre es la palabra definida.

El archivo de definición individual, está estructurado en dos secciones, de acuerdo al uso que recibe cada significado de la palabra:

1. Uso Normal (_denominado_ ```[UNORM]``` en el log)
2. Uso Especial (_denominado_ ```[USPEC]``` en el log)

Las diferentes definiciones presentan el mismo orden que en la página web original.

Un ejemplo de ```<palabra>.json``` es el siguiente

#### _diccionario.json_

```JSON
{
    "usoNormal" : {
        1 : "Definicion1",
        2 : "Definición2",
        3 : "Definición3
    },
    "usoEspecial" : {
        1 : "Definicion1",
        2 : "Definición2",
        3 : "Definición3
    }
}
```

# Notas

## Aviso **legal** (muy importante)

Ni yo ni ninguna de las personas que han colaborado conmigo en el desarrollo de esta herramienta deseamos dañar en modo alguno a la _Real Academia Española_, el presente software es liberado bajo la licencia MIT, y su única finalidad es servir de ejemplo para el aprendizaje de las tecnologías y la seguridad web.

> Si utilizas este programa asumes las condiciones de la licencia MIT y estás de acuerdo en que **no lo utilizarás para obtener ningún beneficio** más allá del puro conocimiento.

## Aviso de desarrollo

**Este software está en desarrollo**, lo que implica que las cosas pueden cambiar de un día para otro sin previo aviso, pueden dejar de funcionar o directamente desaparecer entre una versión y otra.

# Colaboración

Si quieres colaborar, **haz un fork** y completa alguno de los (muchos) ```TODO```'s que pueblan el código, intenta solucionar algún bug o implementa alguna característica interesante.

Una vez que tengas la nueva característica/bug..., haz una _pull request_ a la _main branch_ de este repo ~~(quizá estaría bien abrir una _development branch_)~~.

