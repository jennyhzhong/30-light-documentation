import os                      # Used for working with folders and file paths
import pandas as pd            # Used to read CSV files into tables (DataFrames)
import matplotlib.pyplot as plt  # Used to create and save graphs

# =========================
# Folder Setup
# =========================

# Find the folder where this Python script is located
base_folder = os.path.dirname(os.path.abspath(__file__))

# Build the path to the data folder
data_folder = os.path.join(base_folder, "data")

# Build the path to the graphs folder
graphs_folder = os.path.join(base_folder, "graphs")

# Create the graphs folder if it does not already exist
os.makedirs(graphs_folder, exist_ok=True)

# =========================
# Loop through all CSV files in the data folder
# =========================
for filename in os.listdir(data_folder):
    # Only process files that end in .csv
    if filename.endswith(".csv"):
        # Build the full path to the current CSV file
        csv_path = os.path.join(data_folder, filename)

        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_path)

        # =========================
        # Create a flipped light column
        # =========================
        # Arduino analog readings range from 0 to 1023.
        # If your circuit gives LOWER values for brighter light,
        # then 1023 - value flips it so brighter light appears HIGHER on the graph.
        df["flipped_light"] = 1023 - df["light_level"]

        # =========================
        # Create the graph
        # =========================
        plt.figure(figsize=(10, 5))

        # X-axis: elapsed time in seconds
        # Y-axis: flipped light value
        plt.plot(df["elapsed_s"], df["flipped_light"])

        # Add labels and title
        plt.xlabel("Time Since Start (s)")
        plt.ylabel("Light Intensity (Higher = Brighter)")
        plt.title(f"Light Intensity Over Time - {filename}")

        # Tight layout prevents labels from getting cut off
        plt.tight_layout()

        # =========================
        # Save the graph as a PNG
        # =========================
        # Replace .csv with .png in the file name
        output_name = filename.replace(".csv", ".png")

        # Build the full output path
        output_path = os.path.join(graphs_folder, output_name)

        # Save the graph image
        plt.savefig(output_path)

        # Close the figure so memory is cleared before the next file
        plt.close()

        # Print the saved file path in Command Prompt
        print(f"Saved graph: {output_path}")
