CAMELOT 2 logger
================

Programa en linea de comandos para crear un log de imagenes de CAMELOT2.

Lee una lista de directorios base (`/camelot2p/data_raw` y `/camelot2q/data_processed`, por ejemplo) y busca en ellos subdirectorios con formato `YYMmmdd`, donde crea los logs en texto plano y html, demás de un índice `index.html` en cada directorio base.

Por defecto busca imagenes nuevas en cada subdirectorio, por lo que si hay algún cambio o borrado debe usarse el parametro `-a` para que haga una búsqueda desde cero.

Instalación
-----------

Descargar el codigo de git y entrar en el directorio. Después instalar:

    pip3 install . --user

Esto instala el ejecutable ``camelot-log``. Para instalarlo globalmente debe usarse `sudo`.


Requisitos
----------

* Python 3.4 (mejor 3.6)
* astropy

Uso básico
----------

Ver ayuda

    $ camelot-log --help

Hacer el log de todos los directorios base, actualizando solo los nuevos FITS.

    $ camelot-log 
