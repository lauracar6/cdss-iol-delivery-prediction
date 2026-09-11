from models.base_wrappers import ModelSpec
from models.rf_13_tabular.schema import RF_13_UI_INPUTS, RF_13_SCHEMA, RF_13_UI_INPUTS_TO_MODEL, RF_13_UI_SAMPLES
from models.rf_13_tabular.model_wrapper import RF13ModelWrapper
from utils.paths import DATA_DIR, MLRUNS

from mlflow import MlflowClient

client = MlflowClient()
mlflow_model_name = "bAI-CDV-random-forest-13-tabular"
alias = "champion"
model_version_details = client.get_model_version_by_alias(name=mlflow_model_name, alias=alias)
version = model_version_details.version

RF_13_SPECS = ModelSpec(
    key="rf_13_tabular",
    mlflow_model_name=mlflow_model_name, #tive de alterar o modelo
    ui_terminology = "Dados clínicos",
    version=version, #para ja mas alterar para ir bsuac a versao ao mlflow
    ui_inputs=RF_13_UI_INPUTS,
    model_schema=RF_13_SCHEMA,
    ui_to_model=RF_13_UI_INPUTS_TO_MODEL,
    samples=RF_13_UI_SAMPLES,
    raw_inputs_csv=DATA_DIR / "raw_inputs_RF13.csv",
    preprocessed_inputs_csv=DATA_DIR / "preprocessed_inputs_RF13.csv",
    predictions_csv=DATA_DIR / "predictions_RF13.csv",
    wrapper=RF13ModelWrapper("bAI-CDV-random-forest-13-tabular") 
)