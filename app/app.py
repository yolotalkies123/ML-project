import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import pandas as pd
from data_loader import load_data
from config import file_path, table_name
from preprocessing import preprocess_data
from models import train_polynomial_regression, train_decision_tree
from evaluation import evaluate_model
from prediction import make_prediction
import logging
import numpy as np

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Load and preprocess data
try:
    df = load_data(file_path, table_name)  # Ensure this function returns a DataFrame
    X_train, X_test, y_train, y_test = preprocess_data(df, 'network_in', 'cpu')
    logger.info("Data loaded and preprocessed successfully.")
except Exception as e:
    logger.error(f"Error loading or preprocessing data: {str(e)}")
    raise HTTPException(status_code=500, detail="Error loading or preprocessing data")

# Train models
try:
    poly_model, poly = train_polynomial_regression(X_train, y_train, degree=2)
    tree_model = train_decision_tree(X_train, y_train, max_depth=5)
    logger.info("Models trained successfully.")
except Exception as e:
    logger.error(f"Error training models: {str(e)}")
    raise HTTPException(status_code=500, detail="Error training models")

# Evaluate models
try:
    poly_mse = evaluate_model(poly_model, X_test, y_test, poly)
    tree_mse = evaluate_model(tree_model, X_test, y_test)
    logger.info(f"Polynomial Regression MSE: {poly_mse}")
    logger.info(f"Decision Tree MSE: {tree_mse}")
except Exception as e:
    logger.error(f"Error evaluating models: {str(e)}")
    raise HTTPException(status_code=500, detail="Error evaluating models")

# Define the FastAPI route for predictions
class PredictionRequest(BaseModel):
    network_in: float

@app.post("/predict")
def predict(request: PredictionRequest):
    try:
        logger.info("Starting prediction.")
        
        # Prepare input data
        input_data = [[request.network_in]]
        
        # Make predictions
        poly_pred = make_prediction(poly_model, input_data, poly)
        tree_pred = make_prediction(tree_model, input_data)
        
        # Convert numpy.float32 to float
        poly_pred = float(poly_pred[0])
        tree_pred = float(tree_pred[0])
        
        # Interpolation and Extrapolation predictions
        interp_value = [[X_train.mean()]]
        extrap_value = [[X_train.max() + 10]]
        
        interp_poly_pred = make_prediction(poly_model, interp_value, poly)
        interp_tree_pred = make_prediction(tree_model, interp_value)
        extrap_poly_pred = make_prediction(poly_model, extrap_value, poly)
        extrap_tree_pred = make_prediction(tree_model, extrap_value)
        
        # Convert numpy.float32 to float
        interp_poly_pred = float(interp_poly_pred[0])
        interp_tree_pred = float(interp_tree_pred[0])
        extrap_poly_pred = float(extrap_poly_pred[0])
        extrap_tree_pred = float(extrap_tree_pred[0])
        
        # Prepare response
        response = {
            'Polynomial Regression MSE': float(poly_mse),
            'Decision Tree MSE': float(tree_mse),
            'Polynomial Prediction': poly_pred,
            'Decision Tree Prediction': tree_pred,
            'Interpolation Prediction (Polynomial)': interp_poly_pred,
            'Interpolation Prediction (Decision Tree)': interp_tree_pred,
            'Extrapolation Prediction (Polynomial)': extrap_poly_pred,
            'Extrapolation Prediction (Decision Tree)': extrap_tree_pred
        }
        
        logger.info(f"Prediction completed successfully. Predictions: {response}")
        return response
    
    except Exception as e:
        logger.error(f"Error making prediction: {str(e)}")
        raise HTTPException(status_code=500, detail="Error making prediction")


