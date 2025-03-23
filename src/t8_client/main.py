import os
import argparse
import requests
import json
from dotenv import load_dotenv
from datetime import UTC, datetime

# Cargar variables de entorno
load_dotenv()

# Definir variables de conexión
HOST = os.getenv('T8_HOST')
USER = os.getenv('T8_USER')
PASSWORD = os.getenv('T8_PASSWORD')
FORMAT = 'zint'

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


def main():
    parser = argparse.ArgumentParser(description="Cliente T8 para gestionar datos de espectro y ondas")

    # Subcomandos
    subparsers = parser.add_subparsers(dest="command", help="Subcomandos disponibles")

    # Subcomando list-waves
    waves_parser = subparsers.add_parser("list-waves", help="Lista las formas de onda")
    waves_parser.add_argument("--machine", required=True, help="Identificador de la máquina")
    waves_parser.add_argument("--point", required=True, help="Punto de medición")
    waves_parser.add_argument("--pmode", required=True, help="Modo de procesamiento")
    waves_parser.set_defaults(func=list_waves)


    # Parsear argumentos
    args = parser.parse_args()
    if args.command:
        args.func(args.machine, args.point, args.pmode)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
