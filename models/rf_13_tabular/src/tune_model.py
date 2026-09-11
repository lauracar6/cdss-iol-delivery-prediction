from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
import pandas as pd
import json 
import mlflow

pipeline = Pipeline([
    ("model", RandomForestClassifier(random_state=42))
])

# o objetivo da grid search não é produzir o modelo final mas sim encontrar os melhores parametros
# guardamos os parametros portanto

def parameters_search(X_train, y_train, run_name):
    
    param_grid = {
        "model__n_estimators": [50, 100, 150],
        "model__max_depth": [None, 5, 10, 20],
        "model__max_features": ["sqrt", "log2"],
        "model__min_samples_split": [2, 5, 10],
        "model__min_samples_leaf": [1, 2, 5],
        "model__class_weight": [None, "balanced"],
        "model__criterion": ["gini", "entropy"],
    }

    grid_search = GridSearchCV(
        estimator=pipeline,
        param_grid=param_grid,
        cv=5,
        scoring="recall",
        n_jobs=-1
    )

    with mlflow.start_run(run_name=run_name):

        grid_search.fit(X_train, y_train)

        # logar a grelha usada
        mlflow.log_dict(param_grid, "param_grid.json")
        
        # logar info sobre a configuração da gridsearch (nº de folds e scoring usado para definri melhores params)
        mlflow.log_param("cv", 5)
        mlflow.log_param("scoring", "recall")

        # logar melhores parametros encontrados
        mlflow.log_params(grid_search.best_params_)

        # logar f1 do melhor fold
        mlflow.log_metric(
            "best_cv_f1",
            grid_search.best_score_
        )

        # logar os resultados todos num csv
        results = pd.DataFrame(grid_search.cv_results_)

        results.to_csv(
            "grid_search_results.csv",
            index=False
        )

        mlflow.log_artifact(
            "grid_search_results.csv"
        )

        
    return grid_search.best_params_, grid_search.best_score_

X_train = pd.read_csv("models/rf_13_tabular/datasets/tabular_13_train.csv")
y_train = pd.read_csv("models/rf_13_tabular/datasets/y_train.csv").squeeze()
print(y_train.value_counts())

experiment_name = "Random_Forest_13_tabular_GridSearch"
descrição = ("Hyperparameter tuning para o modelo Random Forest com 70 por cento do dataset retrospetivo e com 13 das features vtabulares - obtidas na analise de features mais relevantes para a previsão com SHAP.")
tags = {"mlflow.note.content": descrição}

# verificar se a experiencia ja existe
experiment = mlflow.get_experiment_by_name(experiment_name)
if experiment is None:
    mlflow.create_experiment(
    name=experiment_name, tags=tags
    )

# ativar esta experiencia para o mlflow saber que o que vamos loggar a partir de agora é relativo a esta experiencia
mlflow.set_experiment(experiment_name=experiment_name)

params, best_score = parameters_search(
    X_train,
    y_train,
    run_name="recall_scoring"
)

print("Best parameters:")
print(params)

print(f"Best CV F1-score: {best_score:.4f}")

