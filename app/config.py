import os
from dotenv import load_dotenv

load_dotenv()

# Get file path from environment variables
file_path = os.getenv('file_path')
table_name = os.getenv('table_name')