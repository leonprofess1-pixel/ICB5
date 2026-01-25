import pandas as pd
import os

data_dir = 'P2/data'
files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]

report = ""

for file in files:
    file_path = os.path.join(data_dir, file)
    try:
        df = pd.read_csv(file_path)
        report += f"--- {file} ---\n"
        report += f"Shape: {df.shape}\n"
        report += f"Columns: {list(df.columns)}\n"
        report += f"Head:\n{df.head(3).to_markdown(index=False)}\n\n"
        
        # Basic info akin to df.info() but stringified
        buffer = []
        df.info(buf=buffer)
        # report += "".join(buffer) # df.info() output can be verbose/messy to parse programmatically sometimes, skipping for now to save tokens
        
    except Exception as e:
        report += f"Error reading {file}: {e}\n\n"

print(report)
