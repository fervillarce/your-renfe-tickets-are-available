# your-renfe-tickets-are-available

## Goal

Estaba harto de tener que acceder todos los días a la web de Renfe para ver si sacaban los billetes para Navidad (este año están tardando más de lo normal), así que hice este script que comprueba si han publicado los billetes para un trayecto y fecha concreto, y envía un email en caso afirmativo.


## Files

* **main.py**. Este script extrae la información del elememento donde se encuentran los billetes publicados y envía un email cuando ya están disponibles.
* **chromedriver**. Es necesario tener el driver de Chrome en la misma carpeta. Este driver se puede descargar de [aquí](https://chromedriver.chromium.org/).
* **gmail_credentials.py**. Este archivo es necesario para indicar el sender_email, la password de gmail y el receiver_email. Esta aparte por seguridad. No está en este repositorio ya que se encuentra en el .gitignore.


## Pipeline description

El proceso es el siguiente:
1. Se abre el navegador (Chrome) de forma headless, para que no se abra el front del navegador y únicamente corra en el back. Si comentamos las líneas de headless, se podrá ver todo el proceso desde el front.
2. Navega a la homepage de [Renfe](http://www.renfe.com/).
3. Introduce los parámetros (origen, destino y fecha de ida) en el formulario de la página y clica en submit.
4. Extrae el contenido del elemento en el que en algún momento se encontrarán los billetes publicados.
5. Si el mensaje es distinto de "El trayecto consultado no se encuentra disponible para la venta en estos momentos o bien no existe conexión directa, por favor inténtelo más adelante y disculpe las molestias.", se loguea a gmail y se envía a la cuenta establecida un email informando de la disponibilidad de los billetes para el trayecto y fecha indicados. El protocolo SSL permite encriptar la conexión SMTP y hacer que la conexión sea segura. Más información en este [artículo](https://realpython.com/python-send-email/).


## How to use it

1. Instalar selenium.
2. Descargar archivos del repo en la misma carpeta.
3. Introducir los parámetros de trayecto y fecha en el propio script.
4. Programar el cronjob (ver cómo en el siguiente apartado).
5. Para que gmail permita la conexión hay que activar "Permitir el acceso de aplicaciones poco seguras" en esta [página](https://myaccount.google.com/u/1/lesssecureapps?pageId=none).
6. El correo llegará a la cuenta receiver_email cuando Renfe publique billetes para el trayecto y la fecha introducidos en el script (se encuentran como parámetros en la parte superior).


### How to run a file automatically by setting a cronjob

En la terminal:
1. `crontab -e` para abrir crontab (el archivo que contiene los cronjobs). Se abre el archivo con un editor (vim o nano, el que esté por defecto). Si lo queremos abrir con nano hay que ejecutar antes en la terminal el comando `export EDITOR=nano`.
2. Metemos el cronjob en el archivo mediante el texto `* * * * * command`. Los asteriscos significan la frecuencia u hora de ejecución del comando (esta [página](https://crontab.guru/) es de gran ayuda). A continuación se introduce el comando de ejecución que, en nuestro caso, estará formado por la ruta donde se encuentra instalado python (o python3) y la ruta donde se encuentra el archivo. Yo lo he configurado para que se ejecute cada hora de la siguiente forma:\
`*/60 * * * * /usr/local/bin/python3 /Users/gr/Ironhack/your-renfe-tickets-are-available/main.py`\
Para saber dónde se encuentra python, ejecutamos `which python` en la terminal.
3. Guardamos y salimos del editor. En nano, hacemos ctrl+o y enter (para guardar) y ctrl+x (para salir).
4. `crontab -l` para ver los cronjobs activos. Debería estar nuestro cronjob.
5. `crontab -r` para eliminar todos los cronjobs más adelante, cuando hayamos conseguido nuestro objetivo.