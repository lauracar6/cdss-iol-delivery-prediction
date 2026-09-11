from utils.paths import DATA_DIR
from models.rf_13_tabular.model_specs import RF_13_SPECS
from models.multimodal_medvit.final_architecture.model_specs import MULTIMODAL_MEDVIT_SPECS
from models.base_wrappers import ModelSpec

MODEL_REGISTRY = {
    RF_13_SPECS.key: RF_13_SPECS,
    MULTIMODAL_MEDVIT_SPECS.key: MULTIMODAL_MEDVIT_SPECS,
}

def get_model_specs(key: str) -> ModelSpec:
    return MODEL_REGISTRY[key]