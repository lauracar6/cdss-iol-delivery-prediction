#import config_mlflow
import mlflow
from mlflow.entities import ViewType
from mlflow.tracking import MlflowClient
import os

print("=== SCRIPT register_model.py A EXECUTAR ===")

# antes de começar verificar se a working directory corresponde com a diretoria em que o mlflow está a ser trabalhado (do chat)
print("Working directory:", os.getcwd()) #vai me dizer qual é a diretoria do ficheiro que estou a correr
print("MLflow tracking URI:", mlflow.get_tracking_uri()) #diz-me a diretoria onde as runs do mlflow estão a acontecer (estão a ser loaded?)

experiment_name = "Random_Forest_13_tabular_train" # temos de colocar aqui o nome da experiencia que tens as runs onde vamos procurar o melhor modelo

# codigo do tutorial do artigo
current_experiment = mlflow.get_experiment_by_name(experiment_name)
experiment_id = current_experiment.experiment_id
#print(experiment_id)

best_model_run = mlflow.search_runs(
    experiment_ids=experiment_id, 
    filter_string="", 
    run_view_type=ViewType.ALL,
    max_results=1, 
    order_by=["metrics.val_recall DESC"], # escolhemos a melhor run pela f1 da validation
    output_format="pandas",
)

print("Selected run:")
print(best_model_run["tags.mlflow.runName"].iloc[0])

print("Validation Recall:")
print(best_model_run["metrics.val_recall"].iloc[0])

model_name = "bAI-CDV-random-forest-13-tabular" # It's important to give the model a name that is shell appropiate (no spaces, no reserved characters)

# aqui registamos o modelo que corresponde á melhor run
best_model_run_id = best_model_run["run_id"][0]
best_model_uri = f"runs:/{best_model_run_id}/model"
result = mlflow.register_model(best_model_uri, model_name)

# aqui vamos introduzir aliases aos modelos que registamos para saber quais sao atuais campeoes ou challengers
client = MlflowClient()

# do chat
# Extract the version that was just created
model_version = result.version #extraimos a versão atual que foi registada porque será essa que sera registada como champion, mas podemos alterar a logica

# Assign alias
client.set_registered_model_alias(name=model_name, alias="champion", version=model_version)
# ou entao podemos definri manualemtne a versao que queremos que seja a champion
#client.set_registered_model_alias(name=model_name, alias="champion", version=1) # coloc

print(f"Registered model: {model_name}")
print(f"Version: {result.version}")

