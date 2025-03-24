
import argparse

from t8_client.functions.subcommands import (
    get_spectrum,
    get_wave,
    list_spectra,
    list_waves,
    plot_spectrum,
    plot_wave,
)


def add_subcommand(subparsers, name, help_text, func, include_datetime=False) -> None:
    """Añade un subcomando al parser."""
    parser = subparsers.add_parser(name, help=help_text)
    parser.add_argument(
        "--machine", "-M", required=True, help="Identificador de la máquina"
    )
    parser.add_argument("--point", "-p", required=True, help="Punto de medición")
    parser.add_argument("--pmode", "-m", required=True, help="Modo de procesamiento")

    if include_datetime:
        parser.add_argument(
            "--datetime", "-t", required=True, help="Fecha del espectro (timestamp)"
        )

    parser.set_defaults(func=func)

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Cliente T8 para gestionar datos de espectro y ondas"
    )
    subparsers = parser.add_subparsers(dest="command", help="Subcomandos disponibles")

    # Lista de subcomandos con sus funciones asociadas
    commands = [
        ("list-waves", "Lista las formas de onda", list_waves, False),
        ("list-spectra", "Lista los espectros", list_spectra, False),
        ("get-wave", "Obtiene una forma de onda específica", get_wave, True),
        ("get-spectrum", "Obtiene un espectro específico", get_spectrum, True),
        ("plot-wave", "Representa una forma de onda específica", plot_wave, True),
        ("plot-spectrum", "Representa un espectro específico", plot_spectrum, True)
    ]

    # Agregar los subcomandos dinámicamente
    for name, help_text, func, include_datetime in commands:
        add_subcommand(subparsers, name, help_text, func, include_datetime)

    # Parsear argumentos y ejecutar la función correspondiente
    args = parser.parse_args()
    if args.command:
        if hasattr(args, "datetime"):
            args.func(args.machine, args.point, args.pmode, args.datetime)
        else:
            args.func(args.machine, args.point, args.pmode)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
