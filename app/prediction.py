import logging
import numpy as np

# Initialize logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def make_prediction(model, input_data, polynomial=None):
    logger.info("Starting prediction.")
    
    try:
        # Ensure input_data is a numpy array for reshaping
        input_data = np.asarray(input_data)
        
        # Check for dimensionality and reshape if necessary
        if input_data.ndim > 2:
            logger.debug("Input data has more than 2 dimensions. Reshaping to 2D.")
            input_data = input_data.reshape(-1, input_data.shape[-1])
        
        if polynomial:
            logger.debug("Applying polynomial transformation to input data.")
            transformed_data = polynomial.transform(input_data)
            predictions = model.predict(transformed_data)
        else:
            predictions = model.predict(input_data)
        
        # Convert predictions to standard Python types
        if isinstance(predictions, np.ndarray):
            predictions = predictions.tolist()
        
        logger.info(f"Prediction completed successfully. Predictions: {predictions}")
        return predictions
    
    except Exception as e:
        logger.error(f"Error making prediction: {str(e)}")
        raise
