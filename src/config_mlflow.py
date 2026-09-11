"""
-> This script serves only to set the directory where mlflow must create and run experiments and register models.
"""

import mlflow
from utils.paths import MLRUNS


mlflow.set_tracking_uri(f"file://{MLRUNS}")

#CONFIG_MLFLOW = mlflow.set_tracking_uri("file:/home/beatrix/Documents/Laura/MLflow_test/mlruns") #im saying that the mlruns folder mlflow should use to create, run experiments and regisetr models is located one level up the folder where the scripts that use mlflow are
#CONFIG_MLFLOW = mlflow.set_tracking_uri("http://10.3.2.112:5000")