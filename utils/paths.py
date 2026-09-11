from pathlib import Path

# Root of the entire project
PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODELS = PROJECT_ROOT / "models"
MLRUNS = PROJECT_ROOT / "mlruns"

# Paths related to MV_MULTIMODAL MODEL
MTM_MEDVIT = MODELS / "multimodal_medvit"
DATASETS = MTM_MEDVIT / "datasets"
PROSPECTIVE_DATASET = DATASETS / "prospective-dataset" / "all_prospective_data.csv"
RETROSPECTIVE_DATASET  = DATASETS / "retrospective-dataset" / "all_retrospective_data.csv"
MTM_UTILS = MTM_MEDVIT / "final_architecture" / "utils" 
RESULTS = MTM_MEDVIT / "final_architecture" / "results" / "edca_selected_data"


DATA_DIR = PROJECT_ROOT / "data"
IMG_DIR = DATA_DIR / "images"
INTERFACE_PREDICTIONS = PROJECT_ROOT / "final_architecture" / "results" / "interface_predictions"
