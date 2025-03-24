
import argparse

from t8_client.functions.subcommands import (
    get_spectrum,
    get_wave,
    list_spectra,
    list_waves,
    plot_spectrum,
    plot_wave,
)


def main():
    
    parser = argparse.ArgumentParser(description="Cliente T8 para gestionar datos de espectro y ondas")

    # Subcomandos
    subparsers = parser.add_subparsers(dest="command", help="Subcomandos disponibles")

    # Subcomando list-waves
    waves_parser = subparsers.add_parser("list-waves", help="Lista las formas de onda")
    waves_parser.add_argument("--machine", "-M", required=True, help="Identificador de la máquina", dest="machine")
    waves_parser.add_argument("--point", "-p", required=True, help="Punto de medición", dest="point")
    waves_parser.add_argument("--pmode", "-m", required=True, help="Modo de procesamiento", dest="pmode")
    waves_parser.set_defaults(func=list_waves)

    # Subcomando list-spectra
    spectra_parser = subparsers.add_parser("list-spectra", help="Lista los espectros")
    spectra_parser.add_argument("--machine", "-M", required=True, help="Identificador de la máquina")
    spectra_parser.add_argument("--point", "-p", required=True, help="Punto de medición")
    spectra_parser.add_argument("--pmode", "-m", required=True, help="Modo de procesamiento")
    spectra_parser.set_defaults(func=list_spectra)

    # Subcomando get-wave
    wave_parser = subparsers.add_parser("get-spectrum", help="Obtiene un espectro específico")
    wave_parser.add_argument("--machine", "-M", required=True, help="Identificador de la máquina")
    wave_parser.add_argument("--point", "-p", required=True, help="Punto de medición")
    wave_parser.add_argument("--pmode", "-m", required=True, help="Modo de procesamiento")
    wave_parser.add_argument("--datetime", "-t", required=True, help="Fecha del espectro (timestamp)")
    wave_parser.set_defaults(func=get_wave)

    # Subcomando get-spectrum
    spectrum_parser = subparsers.add_parser("get-spectrum", help="Obtiene un espectro específico")
    spectrum_parser.add_argument("--machine", "-M", required=True, help="Identificador de la máquina")
    spectrum_parser.add_argument("--point", "-p", required=True, help="Punto de medición")
    spectrum_parser.add_argument("--pmode", "-m", required=True, help="Modo de procesamiento")
    spectrum_parser.add_argument("--datetime", "-t", required=True, help="Fecha del espectro (timestamp)")
    spectrum_parser.set_defaults(func=get_spectrum)

    # Subcomando plot-wave
    plot_wave_parser = subparsers.add_parser("plot-wave", help="Representa una forma de onda específica")
    plot_wave_parser.add_argument("--machine", "-M", required=True, help="Identificador de la máquina")
    plot_wave_parser.add_argument("--point", "-p", required=True, help="Punto de medición")
    plot_wave_parser.add_argument("--pmode", "-m", required=True, help="Modo de procesamiento")
    plot_wave_parser.add_argument("--datetime", "-t", required=True, help="Fecha de la forma de onda (timestamp)")
    plot_wave_parser.set_defaults(func=plot_wave)

    # Subcomando plot-spectrum
    plot_spectrum_parser = subparsers.add_parser("plot-spectrum", help="Representa un espectro específico")
    plot_spectrum_parser.add_argument("--machine", "-M", required=True, help="Identificador de la máquina")
    plot_spectrum_parser.add_argument("--point", "-p", required=True, help="Punto de medición")
    plot_spectrum_parser.add_argument("--pmode", "-m", required=True, help="Modo de procesamiento")
    plot_spectrum_parser.add_argument("--datetime", "-t", required=True, help="Fecha del espectro (timestamp)")
    plot_spectrum_parser.set_defaults(func=plot_spectrum)

    # Parsear argumentos
    args = parser.parse_args()
    if args.command:
        if args.command in ["get-wave", "get-spectrum", "plot-wave", "plot-spectrum"]:
            args.func(args.machine, args.point, args.pmode, args.datetime)
        else:
            args.func(args.machine, args.point, args.pmode)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
