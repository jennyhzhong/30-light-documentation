import os
import pandas as pd
import matplotlib.pyplot as plt


# ===== Folder Setup =====
base_folder = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(base_folder, "data")
graphs_folder = os.path.join(base_folder, "graphs")


# Create graphs folder if it doesn't exist
os.makedirs(graphs_folder, exist_ok=True)


# ===== Process Each CSV File =====
for filename in os.listdir(data_folder):
    if filename.endswith(".csv"):
        csv_path = os.path.join(data_folder, filename)


        # Read CSV data
        df = pd.read_csv(csv_path)


        # ===== Plot Graph =====
        plt.figure(figsize=(10, 5))
        plt.plot(df["elapsed_s"], df["light_level"])


        plt.xlabel("Time Since Start (s)")
        plt.ylabel("Light Level")
        plt.title(f"Light Level Over Time - {filename}")
        plt.tight_layout()


        # ===== Save Graph =====
        output_name = filename.replace(".csv", ".png")
        output_path = os.path.join(graphs_folder, output_name)


        plt.savefig(output_path)
        plt.close()


        print(f"Saved graph: {output_path}")
