import duckdb  
import pandas as pd
import logging
from config import file_path,table_name



# Initialize logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_data(file_path: str, table_name: str) -> pd.DataFrame:
    logger.info(f"Starting to load data from table '{table_name}' in file '{file_path}'")
    try:
        # Establish connection
        con = duckdb.connect(file_path)
        logger.debug("Database connection established.")
        
        # Execute query
        query = f"SELECT * FROM {table_name}"
        df = con.execute(query).df()
        logger.info(f"Data loaded successfully from table '{table_name}'.")
        
        return df
    except Exception as e:
        logger.error(f"Error loading data from table '{table_name}': {str(e)}")
        raise
