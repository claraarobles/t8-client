
import os
import argparse
import requests
from dotenv import load_dotenv


# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Formato de decodificación de los datos
FORMAT = 'zint'

HOST = os.getenv('T8_HOST')
USER = os.getenv('T8_USER')
PASSWORD = os.getenv('T8_PASSWORD')



def list_waves(machine, point, pmode):
    print(f"Listando formas de onda para MACHINE={machine}, POINT={point}, PMODE={pmode}")

    url = f"http://{HOST}/rest/waves/{machine}/{point}/{pmode}/0/"f"?array_fmt={FORMAT}"
    print(f"Solicitando formas de onda desde: {url}")

    try:
        response = requests.get(url,auth=(USER, PASSWORD), timeout=10)
        response.raise_for_status()  # Lanza una excepción si el código de estado no es 200
        data = response.json()  # Asume que la respuesta es JSON
        print("Formas de onda disponibles:")
        for wave in data.get("waves", []):
            print(f"- {wave}")
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
