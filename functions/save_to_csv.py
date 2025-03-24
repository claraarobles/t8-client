import csv


def save_to_csv(filename, x_values, y_values, x_label, y_label) -> None:
    """Guarda datos en un archivo CSV.

    Args:
        filename (str): Nombre del archivo CSV.
        x_values (list): Lista de valores del eje X.
        y_values (list): Lista de valores del eje Y.
        x_label (str): Etiqueta de la primera columna.
        y_label (str): Etiqueta de la segunda columna.
    """
    try:
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([x_label, y_label])  # Escribir encabezado
            writer.writerows(zip(x_values, y_values))  # Escribir datos
        print(f"Datos guardados en: {filename}")
    except IOError as e:  # noqa: UP024
        print(f"Error al escribir el archivo {filename}: {e}")
