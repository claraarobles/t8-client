# T8 Client

## Descripción

T8 Client es una herramienta de línea de comandos diseñada para interactuar con un servidor que proporciona datos de espectros y ondas. Permite listar, obtener y visualizar estos datos de manera sencilla mediante subcomandos de la interfaz de línea de comandos.

## Objetivo del Proyecto

Este proyecto ha sido desarrollado para facilitar la consulta y análisis de datos espectrales y de ondas desde un servidor remoto. A través de una interfaz de línea de comandos, los usuarios pueden listar registros disponibles, obtener datos específicos y generar gráficos o archivos CSV para su posterior análisis.

## Estructura del Proyecto

### 1. `main.py`

Este script es el punto de entrada del cliente. Define la interfaz de línea de comandos utilizando `argparse`, una biblioteca estándar de Python para analizar argumentos de línea de comandos, configurando los subcomandos disponibles:

- `list-waves`: Lista las ondas disponibles.
- `list-spectra`: Lista los espectros disponibles.
- `get-wave`: Obtiene una onda específica.
- `get-spectrum`: Obtiene un espectro específico.
- `plot-wave`: Grafica una onda específica.
- `plot-spectrum`: Grafica un espectro específico.

Cada subcomando requiere parámetros como el identificador de la máquina, el punto de medición, el modo de procesamiento y, en algunos casos, un timestamp. Por ejemplo:

```bash
t8-client get-wave -M LP_Turbine -MAD31CY005 A -m AM1 -t "2019-04-11T18:25:54"
```

### 2. `save_to_csv.py`

Este módulo contiene la función `save_to_csv()`, que permite guardar datos en un archivo CSV. Recibe listas de valores de los ejes X e Y, así como los nombres de las columnas.

### 3. `subcommands.py`

Contiene la implementación de cada uno de los subcomandos definidos en `main.py`. Realiza solicitudes HTTP al servidor para obtener los datos, los procesa y genera archivos CSV o gráficos según corresponda.

- `list_waves()`: Lista las ondas disponibles y muestra sus timestamps.
- `list_spectra()`: Lista los espectros disponibles y muestra sus timestamps.
- `get_wave()`: Descarga una onda específica, la decodifica y la guarda en CSV.
- `get_spectrum()`: Descarga un espectro específico, lo decodifica y lo guarda en CSV.
- `plot_wave()`: Descarga y grafica una onda específica.
- `plot_spectrum()`: Descarga y grafica un espectro específico.

### 4. `timestamp.py`

Proporciona la función `utc_to_timestamp()`, que convierte fechas en formato UTC (`YYYY-MM-DDTHH:MM:SS`) a timestamps para su uso en consultas al servidor.

Por ejemplo:
- Entrada: `"2023-01-01T12:00:00"`
- Salida: `1672574400` (timestamp en segundos)
