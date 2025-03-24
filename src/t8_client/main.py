import os
import argparse
import requests
import json
from dotenv import load_dotenv
from datetime import UTC, datetime
from matplotlib import pylab
import numpy as np
from base64 import b64decode
from struct import unpack
from zlib import decompress


# Cargar variables de entorno
load_dotenv()

# Definir variables de conexión
HOST = os.getenv('T8_HOST')
USER = os.getenv('T8_USER')
PASSWORD = os.getenv('T8_PASSWORD')
FORMAT = 'zint'

# Función para decodificar datos comprimidos en formato zint
def zint_to_float(raw_):
    """
    Decodes compressed data in zint format to a float array.

    Args:
        raw_ (str): The compressed data as a base64 encoded string.

    Returns:
        np.array: The decompressed data as a float array.
    """
    d = decompress(b64decode(raw_.encode()))
    return np.array([unpack('h', d[i*2:(i+1)*2])[0] for i in range(int(len(d)/2))],
                    dtype='f')


# Diccionario para seleccionar la función de decodificación adecuada
decode_format = {
    'zint': zint_to_float,
}

def list_waves(machine, point, pmode):
    """ Lista las formas de onda disponibles y muestra los valores de 'snap'. """
    url = f"http://{HOST}/rest/waves/{machine}/{point}/{pmode}/"f"?array_fmt={FORMAT}"
    print(f"Solicitando datos desde: {url}")  # Para depuración

    try:
        response = requests.get(url, auth=(USER, PASSWORD), timeout=10)
        response.raise_for_status()

        data = response.json()
        
        if "_items" not in data:
            print("No se encontraron formas de onda en la respuesta.")
            return

        timestamps = []

        for item in data["_items"]:
            if "_links" in item and "self" in item["_links"]:
                url_self = item["_links"]["self"]
                timestamp = int(url_self.split("/")[-1])  # Extraer número final de la URL
                
                if timestamp != 0:
                    formatted_time = datetime.fromtimestamp(timestamp, tz=UTC).strftime("%Y-%m-%dT%H:%M:%S")
                    timestamps.append(formatted_time)

        if timestamps:
            print("\n".join(timestamps))  # Mostrar todos los timestamps en líneas separadas
        else:
            print("No se encontraron timestamps válidos.")
            
    except requests.exceptions.RequestException as e:
        print(f"Error al comunicarse con la API: {e}")


def list_spectra(machine, point, pmode):
    """ Lista los espectros disponibles y muestra los valores de 'snap'. """
    url = f"http://{HOST}/rest/spectra/{machine}/{point}/{pmode}/"f"?array_fmt={FORMAT}"
    print(f"Solicitando datos desde: {url}")  # Para depuración

    try:
        response = requests.get(url, auth=(USER, PASSWORD), timeout=10)
        response.raise_for_status()

        data = response.json()
        
        if "_items" not in data:
            print("No se encontraron espectros en la respuesta.")
            return

        timestamps = []

        for item in data["_items"]:
            if "_links" in item and "self" in item["_links"]:
                url_self = item["_links"]["self"]
                timestamp = int(url_self.split("/")[-1])  # Extraer número final de la URL
                
                if timestamp != 0:
                    formatted_time = datetime.fromtimestamp(timestamp, tz=UTC).strftime("%Y-%m-%dT%H:%M:%S")
                    timestamps.append(formatted_time)

        if timestamps:
            print("\n".join(timestamps))  # Mostrar todos los timestamps en líneas separadas
        else:
            print("No se encontraron timestamps válidos.")
            
    except requests.exceptions.RequestException as e:
        print(f"Error al comunicarse con la API: {e}")


def get_wave(machine, point, pmode, date):
    """ Obtiene una forma de onda específica dado un timestamp. """
    try:
        # Convertir la fecha UTC en formato ISO 8601 a timestamp
        date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=UTC)
        date = str(int(date.timestamp()))

    except ValueError as e:
        print(f"Error al convertir la fecha: {e}")
        return

    url = f"http://{HOST}/rest/waves/{machine}/{point}/{pmode}/{date}/"f"?array_fmt={FORMAT}"
    print(f"Solicitando datos desde: {url}")  # Para depuración

    try:
        response = requests.get(url, auth=(USER, PASSWORD), timeout=10)
        response.raise_for_status()

        data = response.json()
        print(json.dumps(data, indent=4))  # Mostrar la forma de onda en formato JSON
        
    except requests.exceptions.RequestException as e:
        print(f"Error al comunicarse con la API: {e}")


def get_spectrum(machine, point, pmode, date):
    """ Obtiene un espectro específico dado un timestamp. """
    try:
        # Convertir la fecha UTC en formato ISO 8601 a timestamp
        date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=UTC)
        date = str(int(date.timestamp()))

    except ValueError as e:
        print(f"Error al convertir la fecha: {e}")
        return

    url = f"http://{HOST}/rest/spectra/{machine}/{point}/{pmode}/{date}/"f"?array_fmt={FORMAT}"
    print(f"Solicitando datos desde: {url}")  # Para depuración

    try:
        response = requests.get(url, auth=(USER, PASSWORD), timeout=10)
        response.raise_for_status()

        data = response.json()
        print(json.dumps(data, indent=4))  # Mostrar el espectro en formato JSON
        
    except requests.exceptions.RequestException as e:
        print(f"Error al comunicarse con la API: {e}")


def plot_wave(machine, point, pmode, date):
    """ Representa una forma de onda específica dado un timestamp. """
    try:
        # Convertir la fecha UTC en formato ISO 8601 a timestamp
        date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=UTC)
        date = str(int(date.timestamp()))

    except ValueError as e:
        print(f"Error al convertir la fecha: {e}")
        return

    url = f"http://{HOST}/rest/waves/{machine}/{point}/{pmode}/{date}/"f"?array_fmt={FORMAT}"
    print(f"Solicitando datos desde: {url}")  # Para depuración

    try:
        response = requests.get(url, auth=(USER, PASSWORD), timeout=10)
        response.raise_for_status()

        data = response.json()

        # Extraer campos del JSON
        srate = float(data['sample_rate'])
        factor = float(data.get('factor', 1))
        raw = data['data']

        # Decodificar los datos crudos usando el formato especificado
        wave = decode_format[FORMAT](raw)

        # Aplicar el factor numérico a los datos
        wave *= factor

        # Obtener el eje de tiempo
        t = pylab.linspace(0, (len(wave)/srate)*1000, len(wave))

        # Graficar la onda
        pylab.figure()
        pylab.title(f"Forma de Onda - Máquina: {machine}, Punto: {point}, Modo: {pmode}")
        pylab.xlabel("Tiempo (ms)")
        pylab.ylabel("Amplitud")
        pylab.plot(t, wave)
        pylab.grid(True)
        pylab.show()

    except requests.exceptions.RequestException as e:
        print(f"Error al comunicarse con la API: {e}")

def main():
    parser = argparse.ArgumentParser(description="Cliente T8 para gestionar datos de espectro y ondas")

    # Subcomandos
    subparsers = parser.add_subparsers(dest="command", help="Subcomandos disponibles")

    # Subcomando list-waves
    waves_parser = subparsers.add_parser("list-waves", help="Lista las formas de onda")
    waves_parser.add_argument("--machine","-M", required=True, help="Identificador de la máquina")
    waves_parser.add_argument("--point","-p", required=True, help="Punto de medición")
    waves_parser.add_argument("--pmode","-m", required=True, help="Modo de procesamiento")
    waves_parser.set_defaults(func=list_waves)

    # Subcomando list-spectra
    spectra_parser = subparsers.add_parser("list-spectra", help="Lista los espectros")
    spectra_parser.add_argument("--machine","-M", required=True, help="Identificador de la máquina")
    spectra_parser.add_argument("--point","-p", required=True, help="Punto de medición")
    spectra_parser.add_argument("--pmode","-m", required=True, help="Modo de procesamiento")
    spectra_parser.set_defaults(func=list_spectra)

    # Subcomando get-spectrum
    spectrum_parser = subparsers.add_parser("get-spectrum", help="Obtiene un espectro específico")
    spectrum_parser.add_argument("--machine","-M", required=True, help="Identificador de la máquina")
    spectrum_parser.add_argument("--point","-p", required=True, help="Punto de medición")
    spectrum_parser.add_argument("--pmode","-m", required=True, help="Modo de procesamiento")
    spectrum_parser.add_argument("--datetime","-t", required=True, help="Fecha del espectro (timestamp)")
    spectrum_parser.set_defaults(func=get_spectrum)

    # Subcomando plot-wave
    plot_wave_parser = subparsers.add_parser("plot-wave", help="Representa una forma de onda específica")
    plot_wave_parser.add_argument("--machine","-M", required=True, help="Identificador de la máquina")
    plot_wave_parser.add_argument("--point","-p", required=True, help="Punto de medición")
    plot_wave_parser.add_argument("--pmode","-m", required=True, help="Modo de procesamiento")
    plot_wave_parser.add_argument("--datetime","-t", required=True, help="Fecha de la forma de onda (timestamp)")
    plot_wave_parser.set_defaults(func=plot_wave)

    # Parsear argumentos
    args = parser.parse_args()
    if args.command:
        if args.command in ["get-wave", "get-spectrum", "plot-wave"]:
            args.func(args.machine, args.point, args.pmode, args.datetime)
        else:
            args.func(args.machine, args.point, args.pmode)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
