from sklearn.metrics import mean_squared_error
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def evaluate_model(model, X_test, y_test, polynomial=None) -> float:
    logger.info("Starting model evaluation.")
    if polynomial:
        try:
            X_test = polynomial.transform(X_test)
            logger.debug("Data transformed using polynomial features.")
        except Exception as e:
            logger.error(f"Error during polynomial transformation: {str(e)}")
            raise
    
    try:
        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        logger.info(f"Model evaluation completed. Mean Squared Error: {mse:.4f}")
        return mse
    except Exception as e:
        logger.error(f"Error during model evaluation: {str(e)}")
        raise
