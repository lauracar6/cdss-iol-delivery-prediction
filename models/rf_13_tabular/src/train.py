import json
import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.base import BaseEstimator
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
)

def get_rf_params(experiment_name: str, run_name: str | None = None) -> dict:
    """
    Retrieve Logistic Regression hyperparameters from a Grid Search
    MLflow experiment.

    If run_name is provided, parameters are retrieved from that run.
    Otherwise, the run with the highest best_cv_f1 metric is selected.

    Parameters
    ----------
    experiment_name : str
        Name of the MLflow Grid Search experiment.

    run_name : str | None
        Name of the run to retrieve parameters from.
        If None, the run with the highest best_cv_f1 is used.

    Returns
    -------
    dict
        Dictionary of LogisticRegression hyperparameters.
    """
    experiment = mlflow.get_experiment_by_name(experiment_name)

    if experiment is None:
        raise ValueError(
            f"Experiment '{experiment_name}' was not found."
        )

    runs = mlflow.search_runs(
        experiment_ids=[experiment.experiment_id]
    )

    if runs.empty:
        raise ValueError(
            "No runs found for the Grid Search experiment."
        )

    if run_name is None:

        selected_run = runs.sort_values(
            by="metrics.best_cv_recall",
            ascending=False
        ).iloc[0]

    else:

        selected_runs = runs[
            runs["tags.mlflow.runName"] == run_name
        ]

        if selected_runs.empty:
            raise ValueError(
                f"Run '{run_name}' was not found."
            )

        selected_run = selected_runs.iloc[0]

    print("\nSelected Grid Search run:")
    print(selected_run["tags.mlflow.runName"])

    print("Best CV F1:")
    print(selected_run["metrics.best_cv_recall"])

    rf_params = {
        "n_estimators": int(selected_run["params.model__n_estimators"]),
        "max_depth": int(selected_run["params.model__max_depth"]),
        "max_features": selected_run["params.model__max_features"],
        "min_samples_split": int(selected_run["params.model__min_samples_split"]),
        "min_samples_leaf": int(selected_run["params.model__min_samples_split"]),
        "class_weight": selected_run["params.model__class_weight"],
        "criterion": selected_run["params.model__criterion"]
    }

    return rf_params


rf_params = get_rf_params(
    experiment_name="Random_Forest_13_tabular_GridSearch",
    run_name="recall_scoring"
)

print("Random Forest parametros usados:", rf_params)

pipeline = Pipeline([
    ("model", RandomForestClassifier(
        random_state=42,
        **rf_params))
])


def train_rf(
    model: BaseEstimator,
    run_name: str,
    X_train: pd.DataFrame,
    X_val: pd.DataFrame,
    y_train: pd.Series,
    y_val: pd.Series,
) -> str:

    with mlflow.start_run(run_name=run_name):

        # Treino
        model.fit(X_train, y_train)

        # Validação
        y_pred = model.predict(X_val)
        y_prob = model.predict_proba(X_val)[:, 1]

        # logging of validation metrics
        mlflow.log_metric(
            "val_accuracy",
            accuracy_score(y_val, y_pred)
        )

        mlflow.log_metric(
            "val_precision",
            precision_score(y_val, y_pred)
        )

        mlflow.log_metric(
            "val_recall",
            recall_score(y_val, y_pred)
        )

        mlflow.log_metric(
            "val_f1",
            f1_score(y_val, y_pred)
        )

        mlflow.log_metric(
            "val_auc",
            roc_auc_score(y_val, y_prob)
        )

        # Matriz de confusão

        cm = confusion_matrix(y_val, y_pred)

        disp = ConfusionMatrixDisplay(confusion_matrix=cm)

        disp.plot()

        cm_path = "validation_confusion_matrix.png"

        plt.savefig(cm_path, bbox_inches="tight")

        plt.close()

        mlflow.log_artifact(cm_path)

        run_id = mlflow.active_run().info.run_id

    return run_id

# Datasets treino
X_train = pd.read_csv("models/rf_13_tabular/datasets/tabular_13_train.csv")
y_train = pd.read_csv("models/rf_13_tabular/datasets/y_train.csv").squeeze()

# Datasets validação
X_val = pd.read_csv("models/rf_13_tabular/datasets/tabular_13_val.csv")
y_val = pd.read_csv("models/rf_13_tabular/datasets/y_val.csv").squeeze()

experiment_name = "Random_Forest_13_tabular_train"
descrição = ("Experiência para treinar o modelo Random Forest com 70 por cento do dataset retrospetivo e com 13 das features vtabulares - obtidas na analise de features mais relevantes para a previsão com SHAP.")
tags = {"mlflow.note.content": descrição}

# verificar se a experiencia ja existe
experiment = mlflow.get_experiment_by_name(experiment_name)
if experiment is None:
    mlflow.create_experiment(
    name=experiment_name, tags=tags
    )

# ativar esta experiencia para o mlflow saber que o que vamos loggar a partir de agora é relativo a esta experiencia
mlflow.set_experiment(experiment_name=experiment_name)

# Permitir o autolog do MLflow para logar metricas de treino
mlflow.sklearn.autolog() 

run_name = "RandomForest_train_RecallParams"

run_id = train_rf(
    model=pipeline,
    run_name=run_name,
    X_train=X_train,
    X_val=X_val,
    y_train=y_train,
    y_val=y_val,
)

print(f"Run ID: {run_id}")

