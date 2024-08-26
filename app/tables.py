import duckdb
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Get file path from environment variables
file_path = os.getenv('file_path')



# Check if the file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")

# Connect to the DuckDB file
con = duckdb.connect(file_path)

# Query the database to list all tables
tables_df = con.execute("SHOW TABLES").df()

# Print the table names
print("Tables in the DuckDB file:")
print(tables_df)

'''

# Optionally, check if the file contains some data
if not tables_df.empty:
    # Load data from the first table (if tables are found)
    first_table_name = tables_df['name'].iloc[0]
    data_df = con.execute(f"SELECT * FROM {first_table_name} LIMIT 10").df()
    print("\nSample data from the first table:")
    print(data_df)
else:
    print("No tables found in the DuckDB file.")
'''