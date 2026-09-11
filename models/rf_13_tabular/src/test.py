import mlflow
from mlflow.tracking import MlflowClient
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.base import BaseEstimator
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    roc_curve,
)

def test_rf(
    model: BaseEstimator,
    model_name: str,
    model_alias: str,
    run_name: str,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> str:

    """
    Evaluate the registered Logistic Regression model on the test set.

    Parameters
    ----------
    model : BaseEstimator
        Registered model loaded from MLflow Model Registry.

    model_name : str
        Name of the registered model.

    model_alias : str
        Alias of the registered model (e.g. champion).

    run_name : str
        Name of the MLflow run.

    X_test : pd.DataFrame
        Test features.

    y_test : pd.Series
        Test labels.

    Returns
    -------
    str
        MLflow run ID.
    """

    client = MlflowClient()

    model_version = client.get_model_version_by_alias(
        name=model_name,
        alias=model_alias
    ).version

    with mlflow.start_run(run_name=run_name):

        # Teste
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]

        # logging of validation metrics
        mlflow.log_metric(
            "test_accuracy",
            accuracy_score(y_test, y_pred)
        )

        mlflow.log_metric(
            "test_precision",
            precision_score(y_test, y_pred)
        )

        mlflow.log_metric(
            "test_recall",
            recall_score(y_test, y_pred)
        )

        mlflow.log_metric(
            "test_f1",
            f1_score(y_test, y_pred)
        )

        mlflow.log_metric(
            "test_auc",
            roc_auc_score(y_test, y_prob)
        )

        # logar model info
        mlflow.log_param(
            "registered_model",
            model_name
        )

        mlflow.log_param(
            "model_alias",
            model_alias
        )

        mlflow.log_param(
            "model_version",
            model_version
        )


        # Matriz de confusão
        cm = confusion_matrix(y_test, y_pred)

        disp = ConfusionMatrixDisplay(confusion_matrix=cm)

        disp.plot()

        cm_path = "test_confusion_matrix.png"

        plt.savefig(cm_path, bbox_inches="tight")

        plt.close()

        mlflow.log_artifact(cm_path)

        # ROC curve
        fpr, tpr, _ = roc_curve(
            y_test,
            y_prob
        )

        plt.figure()

        plt.plot(fpr, tpr, label="Logistic Regression")

        plt.plot(
            [0, 1],
            [0, 1],
            linestyle="--"
        )

        plt.xlabel("False Positive Rate")

        plt.ylabel("True Positive Rate")

        plt.title("ROC Curve")

        plt.legend()

        roc_path = "roc_curve.png"

        plt.savefig(
            roc_path,
            bbox_inches="tight"
        )

        plt.close()

        mlflow.log_artifact(roc_path)

        run_id = mlflow.active_run().info.run_id

    return run_id

# Datasets teste
X_test = pd.read_csv("models/lr_13_tabular/datasets/tabular_13_test.csv")
y_test = pd.read_csv("models/lr_13_tabular/datasets/y_test.csv").squeeze()

experiment_name = "Random_Forest_13_tabular_test"
descrição = ("Experiência para testar o modelo Random Forest com o modelo resgistado correspondente a melhpr run do treino.")
tags = {"mlflow.note.content": descrição}

# verificar se a experiencia ja existe
experiment = mlflow.get_experiment_by_name(experiment_name)
if experiment is None:
    mlflow.create_experiment(
    name=experiment_name, tags=tags
    )

# ativar esta experiencia para o mlflow saber que o que vamos loggar a partir de agora é relativo a esta experiencia
mlflow.set_experiment(experiment_name=experiment_name)

MODEL_NAME = "bAI-CDV-random-forest-13-tabular"
MODEL_ALIAS = "champion"

model = mlflow.sklearn.load_model(
    f"models:/{MODEL_NAME}@{MODEL_ALIAS}"
)

run_id = test_rf(
    model=model,
    model_name=MODEL_NAME,
    model_alias=MODEL_ALIAS,
    run_name="same_test_data_as_lr",
    X_test=X_test,
    y_test=y_test,
)

print(run_id)