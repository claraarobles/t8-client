"""
This module contains the implementations of the subcommands used by the
T8 client.

It provides functions to interact with a remote server, list available data,
retrieve specific data (waves and spectra), and plot or save this data to
CSV files.

Main functions:
- `list_waves`: Lists available waves and displays their timestamps.
- `list_spectra`: Lists available spectra and displays their timestamps.
- `get_wave`: Downloads a specific wave, decodes it, and saves it to a CSV file.
- `get_spectrum`: Downloads a specific spectrum, decodes it, and saves it to a
    CSV file.
- `plot_wave`: Downloads and plots a specific wave.
- `plot_spectrum`: Downloads and plots a specific spectrum.

Dependencies:
- This module uses environment variables (`T8_HOST`, `T8_USER`, `T8_PASSWORD`)
    to connect to the server.
- Requires the `save_to_csv` and `utc_to_timestamp` functions from other
    project modules.
"""
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

# Load environment variables
load_dotenv()

# Define connection variables
HOST = os.getenv("T8_HOST")
USER = os.getenv("T8_USER")
PASSWORD = os.getenv("T8_PASSWORD")
FORMAT = "zint"

# Function to decode compressed data in zint format
def zint_to_float(raw_: str) -> np.ndarray:
    """
    Decodes compressed data in zint format to a float array.

    Args:
        raw_ (str): The compressed data as a base64 encoded string.

    Returns:
        np.array: The decompressed data as a float array.
    """
    # Decode base64 and decompress the data
    d = decompress(b64decode(raw_.encode()))
    # Convert the decompressed data into a float array
    return np.array(
        [unpack("h", d[i * 2 : (i + 1) * 2])[0] for i in range(int(len(d) / 2))],
        dtype="f",
    )

# Dictionary to select the appropriate decoding function
decode_format = {
    "zint": zint_to_float,
}

# Function to list available waveforms and display their timestamps
def list_waves(machine: str, point: str, pmode: str) -> None:
    """
    Lists available waveforms and displays their timestamps.

    Args:
        machine (str): Machine identifier.
        point (str): Measurement point identifier.
        pmode (str): Mode of operation.
    """
    url = f"http://{HOST}/rest/waves/{machine}/{point}/{pmode}/?array_fmt={FORMAT}"

    try:
        # Send a GET request to the API
        response = requests.get(url, auth=(USER, PASSWORD), timeout=10)
        response.raise_for_status()

        data = response.json()

        if "_items" not in data:
            print("No waveforms found in the response.")
            return

        timestamps = []

        for item in data["_items"]:
            if "_links" in item and "self" in item["_links"]:
                url_self = item["_links"]["self"]
                # Extract the timestamp from the URL
                timestamp = int(url_self.split("/")[-1])

                if timestamp != 0:
                    # Format the timestamp into a readable string
                    formatted_time = datetime.fromtimestamp(timestamp, tz=UTC).strftime(
                        "%Y-%m-%dT%H:%M:%S"
                    )
                    timestamps.append(formatted_time)

        if timestamps:
            # Display all timestamps in separate lines
            print("\n".join(timestamps))
        else:
            print("No valid timestamps found.")

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with the API: {e}")

# Function to list available spectra and display their timestamps
def list_spectra(machine: str, point: str, pmode: str) -> None:
    """
    Lists available spectra and displays their timestamps.

    Args:
        machine (str): Machine identifier.
        point (str): Measurement point identifier.
        pmode (str): Mode of operation.
    """
    url = f"http://{HOST}/rest/spectra/{machine}/{point}/{pmode}/?array_fmt={FORMAT}"

    try:
        # Send a GET request to the API
        response = requests.get(url, auth=(USER, PASSWORD), timeout=10)
        response.raise_for_status()

        data = response.json()

        if "_items" not in data:
            print("No spectra found in the response.")
            return

        timestamps = []

        for item in data["_items"]:
            if "_links" in item and "self" in item["_links"]:
                url_self = item["_links"]["self"]
                # Extract the timestamp from the URL
                timestamp = int(url_self.split("/")[-1])

                if timestamp != 0:
                    # Format the timestamp into a readable string
                    formatted_time = datetime.fromtimestamp(timestamp, tz=UTC).strftime(
                        "%Y-%m-%dT%H:%M:%S"
                    )
                    timestamps.append(formatted_time)

        if timestamps:
            # Display all timestamps in separate lines
            print("\n".join(timestamps))
        else:
            print("No valid timestamps found.")

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with the API: {e}")

# Function to retrieve a specific waveform given a timestamp
def get_wave(machine: str, point: str, pmode: str, date: str) -> None:
    """
    Retrieves a specific waveform given a timestamp.

    Args:
        machine (str): Machine identifier.
        point (str): Measurement point identifier.
        pmode (str): Mode of operation.
        date (str): Timestamp in UTC format.
    """
    # Convert the date to a timestamp
    date = utc_to_timestamp(date)

    url = (
        f"http://{HOST}/rest/waves/{machine}/{point}/{pmode}/{date}/?array_fmt={FORMAT}"
    )

    try:
        # Send a GET request to the API
        response = requests.get(url, auth=(USER, PASSWORD), timeout=10)
        response.raise_for_status()

        data = response.json()

        # Extract relevant fields from the JSON response
        srate = float(data["sample_rate"])
        factor = float(data.get("factor", 1))
        raw = data["data"]

        # Decode the raw data using the specified format
        wave = decode_format[FORMAT](raw)

        # Apply the numeric factor to the data
        wave *= factor

        # Generate the time axis
        t = pylab.linspace(0, (len(wave) / srate) * 1000, len(wave))

        # Generate the filename
        filename = f"{machine}_{point}_{pmode}_{date}.csv"

        # Save the data to a CSV file
        save_to_csv(filename, t, wave, "Time (ms)", "Amplitude")

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with the API: {e}")

# Function to retrieve a specific spectrum given a timestamp
def get_spectrum(machine: str, point: str, pmode: str, date: str) -> None:
    """
    Retrieves a specific spectrum given a timestamp.

    Args:
        machine (str): Machine identifier.
        point (str): Measurement point identifier.
        pmode (str): Mode of operation.
        date (str): Timestamp in UTC format.
    """
    # Convert the date to a timestamp
    date = utc_to_timestamp(date)

    url = (
        f"http://{HOST}/rest/spectra/{machine}/{point}/{pmode}/{date}/"
        f"?array_fmt={FORMAT}"
    )

    try:
        # Send a GET request to the API
        response = requests.get(url, auth=(USER, PASSWORD), timeout=10)
        response.raise_for_status()

        data = response.json()

        # Extract relevant fields from the JSON response
        fmin = data.get("min_freq", 0)
        fmax = data["max_freq"]
        factor = data["factor"]
        raw = data["data"]

        # Decode the raw data using the specified format
        sp = decode_format[FORMAT](raw)

        # Apply the numeric factor to the data
        sp *= factor

        # Generate the frequency axis
        freq = pylab.linspace(fmin, fmax, len(sp))

        # Generate the filename
        filename = f"{machine}_{point}_{pmode}_{date}.csv"

        # Save the data to a CSV file
        save_to_csv(filename, freq, sp, "Frequency (Hz)", "Amplitude")

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with the API: {e}")

# Function to plot a specific waveform given a timestamp
def plot_wave(machine: str, point: str, pmode: str, date: str) -> None:
    """
    Plots a specific waveform given a timestamp.

    Args:
        machine (str): Machine identifier.
        point (str): Measurement point identifier.
        pmode (str): Mode of operation.
        date (str): Timestamp in UTC format.
    """
    # Convert the date to a timestamp
    date = utc_to_timestamp(date)

    url = (
        f"http://{HOST}/rest/waves/{machine}/{point}/{pmode}/{date}/?array_fmt={FORMAT}"
    )

    try:
        # Send a GET request to the API
        response = requests.get(url, auth=(USER, PASSWORD), timeout=10)
        response.raise_for_status()

        data = response.json()

        # Extract relevant fields from the JSON response
        srate = float(data["sample_rate"])
        factor = float(data.get("factor", 1))
        raw = data["data"]

        # Decode the raw data using the specified format
        wave = decode_format[FORMAT](raw)

        # Apply the numeric factor to the data
        wave *= factor

        # Generate the time axis
        t = pylab.linspace(0, (len(wave) / srate) * 1000, len(wave))

        # Plot the waveform
        pylab.figure()
        pylab.title(
            f"Waveform - Machine: {machine}, Point: {point}, Mode: {pmode}"
        )
        pylab.xlabel("Time (ms)")
        pylab.ylabel("Amplitude")
        pylab.plot(t, wave)
        pylab.grid(True)
        pylab.show()

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with the API: {e}")

# Function to plot a specific spectrum given a timestamp
def plot_spectrum(machine: str, point: str, pmode: str, date: str) -> None:
    """
    Plots a specific spectrum given a timestamp.

    Args:
        machine (str): Machine identifier.
        point (str): Measurement point identifier.
        pmode (str): Mode of operation.
        date (str): Timestamp in UTC format.
    """
    # Convert the date to a timestamp
    date = utc_to_timestamp(date)

    url = (
        f"http://{HOST}/rest/spectra/{machine}/{point}/{pmode}/{date}/"
        f"?array_fmt={FORMAT}"
    )

    try:
        # Send a GET request to the API
        response = requests.get(url, auth=(USER, PASSWORD), timeout=10)
        response.raise_for_status()

        data = response.json()

        # Extract relevant fields from the JSON response
        fmin = data.get("min_freq", 0)
        fmax = data["max_freq"]
        factor = data["factor"]
        raw = data["data"]

        # Decode the raw data using the specified format
        sp = decode_format[FORMAT](raw)

        # Apply the numeric factor to the data
        sp *= factor

        # Generate the frequency axis
        freq = pylab.linspace(fmin, fmax, len(sp))

        # Plot the spectrum
        pylab.figure()
        pylab.title(
            f"Spectrum - Machine: {machine}, Point: {point}, Mode: {pmode}"
        )
        pylab.xlabel("Frequency (Hz)")
        pylab.ylabel("Amplitude")
        pylab.plot(freq, sp)
        pylab.grid(True)
        pylab.show()

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with the API: {e}")
