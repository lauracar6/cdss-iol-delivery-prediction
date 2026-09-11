import json
from utils.paths import MTM_UTILS, MTM_MEDVIT

with open(MTM_UTILS / "columns_config.json", "r") as f:
    COLS_CONFIG = json.load(f)
    
NUM_COLS = COLS_CONFIG["num_cols"]
CAT_COLS = COLS_CONFIG["cat_cols"]
IMG_COLS = COLS_CONFIG["image_cols"]

NUM_CATEGORIES = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
  3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 
  3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 
  3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4]


MULTIMODAL_MODEL_PATH = (MTM_MEDVIT 
/ "multimodal_architecture"
/ "models_prospective"
/ "MedViT2_nopt"
/ "final_model.pth")


PIPELINE_PATH = MTM_UTILS / "final_pipeline_edca.pkl"

with open(MTM_UTILS / "edca_selected_features.json", "r") as f:
    selected_feat = json.load(f)