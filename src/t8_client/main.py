"""
This module defines the command-line interface for the T8 client.

It provides subcommands to list, retrieve, and plot data for spectra and waves.
Each subcommand is dynamically configured and executes specific functions
based on the arguments provided by the user.
"""
import argparse
from argparse import _SubParsersAction
from typing import Callable

# Importing functions for subcommands from the module
from t8_client.functions.subcommands import (
    get_spectrum,
    get_wave,
    list_spectra,
    list_waves,
    plot_spectrum,
    plot_wave,
)


def add_subcommand(
    subparsers: _SubParsersAction,
    name: str,
    help_text: str,
    func: Callable,
    include_datetime: bool = False
) -> None:
    """
    Adds a subcommand to the parser.

    Args:
        subparsers (_SubParsersAction): The subparsers object to add the subcommand to.
        name (str): The name of the subcommand.
        help_text (str): The help text for the subcommand.
        func (Callable): The function to execute for the subcommand.
        include_datetime (bool): Whether the subcommand requires a datetime argument.
    """
    # Create a new subparser for the subcommand
    parser = subparsers.add_parser(name, help=help_text)

    # Add required arguments for the subcommand
    parser.add_argument(
        "--machine", "-M", required=True, help="Machine identifier"
    )
    parser.add_argument("--point", "-p", required=True, help="Measurement point")
    parser.add_argument("--pmode", "-m", required=True, help="Processing mode")

    # Optionally add a datetime argument if required
    if include_datetime:
        parser.add_argument(
            "--datetime", "-t", required=True, help="Spectrum date (timestamp)"
        )

    # Set the default function to execute when this subcommand is called
    parser.set_defaults(func=func)

def main() -> None:
    """
    Main function to parse arguments and execute the corresponding subcommand.
    """
    # Create the main argument parser
    parser = argparse.ArgumentParser(
        description="T8 client to manage spectrum and wave data"
    )
    # Create subparsers for the available subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # List of subcommands with their associated functions
    commands = [
        ("list-waves", "Lists waveforms", list_waves, False),
        ("list-spectra", "Lists spectra", list_spectra, False),
        ("get-wave", "Gets a specific waveform", get_wave, True),
        ("get-spectrum", "Gets a specific spectrum", get_spectrum, True),
        ("plot-wave", "Plots a specific waveform", plot_wave, True),
        ("plot-spectrum", "Plots a specific spectrum", plot_spectrum, True)
    ]

    # Dynamically add the subcommands to the parser
    for name, help_text, func, include_datetime in commands:
        add_subcommand(subparsers, name, help_text, func, include_datetime)

    # Parse the command-line arguments
    args = parser.parse_args()
    if args.command:
        # Execute the corresponding function for the subcommand
        if hasattr(args, "datetime"):
            args.func(args.machine, args.point, args.pmode, args.datetime)
        else:
            args.func(args.machine, args.point, args.pmode)
    else:
        # If no subcommand is provided, display the help message
        parser.print_help()

if __name__ == "__main__":
    main()
