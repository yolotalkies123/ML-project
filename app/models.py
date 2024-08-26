from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def train_polynomial_regression(X_train, y_train, degree=2):
    logger.info(f"Starting polynomial regression training with degree {degree}.")
    try:
        poly = PolynomialFeatures(degree=degree)
        X_poly = poly.fit_transform(X_train)
        model = LinearRegression().fit(X_poly, y_train)
        logger.info("Polynomial regression model trained successfully.")
        return model, poly
    except Exception as e:
        logger.error(f"Error during polynomial regression training: {str(e)}")
        raise

def train_decision_tree(X_train, y_train, max_depth=5):
    logger.info(f"Starting decision tree training with max depth {max_depth}.")
    try:
        model = DecisionTreeRegressor(max_depth=max_depth).fit(X_train, y_train)
        logger.info("Decision tree model trained successfully.")
        return model
    except Exception as e:
        logger.error(f"Error during decision tree training: {str(e)}")
        raise
