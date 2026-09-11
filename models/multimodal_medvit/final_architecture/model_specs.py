from models.base_wrappers import ModelSpec
from models.multimodal_medvit.final_architecture.schema import MULTIMODAL_MEDVIT_UI_INPUTS, MULTIMODAL_MEDVIT_SCHEMA, MULTIMODAL_MEDVIT_UI_INPUTS_TO_MODEL, MULTIMODAL_MEDVIT_UI_SAMPLES
from models.multimodal_medvit.final_architecture.model_wrapper import MultimodalMedvitModelWrapper
from utils.paths import DATA_DIR

MULTIMODAL_MEDVIT_SPECS = ModelSpec(
    key="multimodal_medvit",
    mlflow_model_name="bAI-CDV-multimodal-medvit",
    ui_terminology = "Dados clínicos e ultrasons",
    version="1.0", #para já
    ui_inputs=MULTIMODAL_MEDVIT_UI_INPUTS,
    model_schema=MULTIMODAL_MEDVIT_SCHEMA,
    ui_to_model=MULTIMODAL_MEDVIT_UI_INPUTS_TO_MODEL,
    samples=MULTIMODAL_MEDVIT_UI_SAMPLES,
    raw_inputs_csv=DATA_DIR / "raw_inputs_MTM_MEDVIT.csv",
    preprocessed_inputs_csv=DATA_DIR / "preprocessed_inputs_MTM_MEDVIT.csv",
    predictions_csv=DATA_DIR / "predictions_inputs_MTM_MEDVIT.csv",
    wrapper=MultimodalMedvitModelWrapper("bAI-CDV-multimodal-medvit") 
)