import os
import argparse
import requests
from dotenv import load_dotenv
from datetime import datetime

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Formato de decodificación de los datos
FORMAT = 'zint'

HOST = os.getenv('T8_HOST')
USER = os.getenv('T8_USER')
PASSWORD = os.getenv('T8_PASSWORD')

print(f"T8_USER: {USER}")
print(f"T8_PASSWORD: {PASSWORD}")

def list_waves(machine, point, pmode):
    print(f"Listando formas de onda para MACHINE={machine}, POINT={point}, PMODE={pmode}")

    url = f"http://{HOST}/rest/waves/{machine}/{point}/{pmode}/?array_fmt={FORMAT}"
    print(f"Solicitando formas de onda desde: {url}")

    try:
        response = requests.get(url, auth=(USER, PASSWORD), timeout=10)
        response.raise_for_status()  # Lanza una excepción si el código de estado no es 200

        # Depuración: imprime el código de estado y la respuesta completa
        print(f"Código de estado: {response.status_code}")
        data = response.json()
        print("Respuesta completa de la API:", data)

        # Procesar las entradas con "waves"
        waves = data.get("waves", [])
        if not waves:
            print("No se encontraron formas de onda.")
            return

        print("Lista de snap_t disponibles:")
        for wave in waves:
            snap_t = wave.get('snap_t')  # Accede al campo 'snap_t' de cada entrada
            if snap_t:
                # Si snap_t es un timestamp, conviértelo a un formato legible
                snap_t_date = datetime.utcfromtimestamp(snap_t).strftime('%Y-%m-%dT%H:%M:%S')
                print(snap_t_date)

    except requests.exceptions.RequestException as e:
        print(f"Error al comunicarse con la URL: {e}")


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