
import csv  # Imports the csv module to work with CSV files.


def save_to_csv(
    filename: str, x_values: list, y_values: list, x_label: str, y_label: str
) -> None:
    """Saves data to a CSV file.

    Args:
        filename (str): Name of the CSV file.
        x_values (list): List of X-axis values.
        y_values (list): List of Y-axis values.
        x_label (str): Label for the first column.
        y_label (str): Label for the second column.
    """
    try:
        # Opens the file in write mode ("w"), with UTF-8 support
        # and without additional blank lines.
        with open(
            filename, mode="w", newline="", encoding="utf-8"
        ) as file:
            writer = csv.writer(file)  # Creates a writer object to handle the file
            # Writes the header row (column names).
            writer.writerow([x_label, y_label])
            # Combines the x_values and y_values lists and writes the data rows.
            writer.writerows(zip(x_values, y_values))
        # Confirmation message when data is saved.
        print(f"Data saved to: {filename}")
    except OSError as e:
        # Catches errors related to the file system (such as permissions
        # or invalid paths).
        print(f"Error writing the file {filename}: {e}")
