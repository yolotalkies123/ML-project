import logging
from sklearn.model_selection import train_test_split

# Initialize logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def preprocess_data(df, feature_col, target_col):
    logger.info("Starting data preprocessing.")
    
    try:
        # Extract features and target
        X = df[[feature_col]]
        y = df[target_col]
        logger.debug(f"Features: {X.head()}")
        logger.debug(f"Target: {y.head()}")
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        logger.info(f"Data split into training and test sets. Training set size: {len(X_train)}, Test set size: {len(X_test)}")
        
        return X_train, X_test, y_train, y_test
    
    except Exception as e:
        logger.error(f"Error during data preprocessing: {str(e)}")
        raise

