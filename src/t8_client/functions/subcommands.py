
import os
from base64 import b64decode
from datetime import UTC, datetime
from struct import unpack
from zlib import decompress

import numpy as np
import requests
from dotenv import load_dotenv
from matplotlib import pylab

from t8_client.functions.save_to_csv import save_to_csv
from t8_client.functions.timestamp import utc_to_timestamp

# Cargar variables de entorno
load_dotenv()

# Definir variables de conexión
HOST = os.getenv("T8_HOST")
USER = os.getenv("T8_USER")
PASSWORD = os.getenv("T8_PASSWORD")
FORMAT = "zint"


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
    return np.array(
        [unpack("h", d[i * 2 : (i + 1) * 2])[0] for i in range(int(len(d) / 2))],
        dtype="f",
    )


# Diccionario para seleccionar la función de decodificación adecuada
decode_format = {
    "zint": zint_to_float,
}


def list_waves(machine, point, pmode) -> None:
    """Lista las formas de onda disponibles y muestra los valores de 'snap'."""
    url = f"http://{HOST}/rest/waves/{machine}/{point}/{pmode}/?array_fmt={FORMAT}"

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
                timestamp = int(
                    url_self.split("/")[-1]
                )

                if timestamp != 0:
                    formatted_time = datetime.fromtimestamp(timestamp, tz=UTC).strftime(
                        "%Y-%m-%dT%H:%M:%S"
                    )
                    timestamps.append(formatted_time)

        if timestamps:
            print(
                "\n".join(timestamps)
            )  # Mostrar todos los timestamps en líneas separadas
        else:
            print("No se encontraron timestamps válidos.")

    except requests.exceptions.RequestException as e:
        print(f"Error al comunicarse con la API: {e}")


def list_spectra(machine, point, pmode) -> None:
    """Lista los espectros disponibles y muestra los valores de 'snap'."""
    url = f"http://{HOST}/rest/spectra/{machine}/{point}/{pmode}/?array_fmt={FORMAT}"

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
                timestamp = int(
                    url_self.split("/")[-1]
                )  # Extraer número final de la URL

                if timestamp != 0:
                    formatted_time = datetime.fromtimestamp(timestamp, tz=UTC).strftime(
                        "%Y-%m-%dT%H:%M:%S"
                    )
                    timestamps.append(formatted_time)

        if timestamps:
            print(
                "\n".join(timestamps)
            )  # Mostrar todos los timestamps en líneas separadas
        else:
            print("No se encontraron timestamps válidos.")

    except requests.exceptions.RequestException as e:
        print(f"Error al comunicarse con la API: {e}")


def get_wave(machine, point, pmode, date):
    """Obtiene una forma de onda específica dado un timestamp."""

    date = utc_to_timestamp(date)

    url = (
        f"http://{HOST}/rest/waves/{machine}/{point}/{pmode}/{date}/?array_fmt={FORMAT}"
    )

    try:
        response = requests.get(url, auth=(USER, PASSWORD), timeout=10)
        response.raise_for_status()

        data = response.json()

        # Extraer campos del JSON
        srate = float(data["sample_rate"])
        factor = float(data.get("factor", 1))
        raw = data["data"]

        # Decodificar los datos crudos usando el formato especificado
        wave = decode_format[FORMAT](raw)

        # Aplicar el factor numérico a los datos
        wave *= factor

        # Obtener el eje de tiempo
        t = pylab.linspace(0, (len(wave) / srate) * 1000, len(wave))

        # Nombre del archivo
        filename = f"{machine}_{point}_{pmode}_{date}.csv"

        # Guardar en CSV 
        save_to_csv(filename, t, wave, "Tiempo (ms)", "Amplitud")

    except requests.exceptions.RequestException as e:
        print(f"Error al comunicarse con la API: {e}")




def get_spectrum(machine, point, pmode, date):
    """Obtiene un espectro específico dado un timestamp."""

    date = utc_to_timestamp(date)

    url = (
        f"http://{HOST}/rest/spectra/{machine}/{point}/{pmode}/{date}/"
        f"?array_fmt={FORMAT}"
    )

    try:
        response = requests.get(url, auth=(USER, PASSWORD), timeout=10)
        response.raise_for_status()

        data = response.json()

        # Extraer campos relevantes de la respuesta JSON
        fmin = data.get("min_freq", 0)
        fmax = data["max_freq"]
        factor = data["factor"]
        raw = data["data"]

        # Decodificar los datos en bruto usando el formato especificado
        sp = decode_format[FORMAT](raw)

        # Aplicar el factor numérico a los datos
        sp *= factor

        # Generar el eje de frecuencia
        freq = pylab.linspace(fmin, fmax, len(sp))

        # Nombre del archivo
        filename = f"{machine}_{point}_{pmode}_{date}.csv"

        # Guardar en CSV
        save_to_csv(filename, freq, sp, "Frecuencia (Hz)", "Amplitud")

    except requests.exceptions.RequestException as e:
        print(f"Error al comunicarse con la API: {e}")



def plot_wave(machine, point, pmode, date):
    """Representa una forma de onda específica dado un timestamp."""

    date = utc_to_timestamp(date)

    url = (
        f"http://{HOST}/rest/waves/{machine}/{point}/{pmode}/{date}/?array_fmt={FORMAT}"
    )

    try:
        response = requests.get(url, auth=(USER, PASSWORD), timeout=10)
        response.raise_for_status()

        data = response.json()

        # Extraer campos del JSON
        srate = float(data["sample_rate"])
        factor = float(data.get("factor", 1))
        raw = data["data"]

        # Decodificar los datos crudos usando el formato especificado
        wave = decode_format[FORMAT](raw)

        # Aplicar el factor numérico a los datos
        wave *= factor

        # Obtener el eje de tiempo
        t = pylab.linspace(0, (len(wave) / srate) * 1000, len(wave))

        # Graficar la onda
        pylab.figure()
        pylab.title(
            f"Forma de Onda - Máquina: {machine}, Punto: {point}, Modo: {pmode}"
        )
        pylab.xlabel("Tiempo (ms)")
        pylab.ylabel("Amplitud")
        pylab.plot(t, wave)
        pylab.grid(True)
        pylab.show()

    except requests.exceptions.RequestException as e:
        print(f"Error al comunicarse con la API: {e}")


def plot_spectrum(machine, point, pmode, date):
    """Representa una forma de espectro específica dado un timestamp."""

    date = utc_to_timestamp(date)

    url = (
        f"http://{HOST}/rest/spectra/{machine}/{point}/{pmode}/{date}/"
        f"?array_fmt={FORMAT}"
    )

    try:
        response = requests.get(url, auth=(USER, PASSWORD), timeout=10)
        response.raise_for_status()

        data = response.json()

        # Extraer campos relevantes de la respuesta JSON
        fmin = data.get("min_freq", 0)
        fmax = data["max_freq"]
        factor = data["factor"]
        raw = data["data"]

        # Decodificar los datos en bruto usando el formato especificado
        sp = decode_format[FORMAT](raw)

        # Aplicar el factor numérico a los datos
        sp *= factor

        # Generar el eje de frecuencia
        freq = pylab.linspace(fmin, fmax, len(sp))

        # Graficar el espectro
        pylab.figure()
        pylab.title(
            f"Forma de Espectro - Máquina: {machine}, Punto: {point}, Modo: {pmode}"
        )
        pylab.xlabel("Frecuencia (Hz)")
        pylab.ylabel("Amplitud")
        pylab.plot(freq, sp)
        pylab.grid(True)
        pylab.show()

    except requests.exceptions.RequestException as e:
        print(f"Error al comunicarse con la API: {e}")
