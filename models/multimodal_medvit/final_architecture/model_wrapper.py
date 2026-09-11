from models.base_wrappers import ModelWrapper
from models.multimodal_medvit.final_architecture.schema import MULTIMODAL_MEDVIT_CATEGORICAL_MAPPINGS
from src.features.feature_engineering import apply_categorical_mapping, imc, aumento_ponderal, hadlock_formula
import mlflow
import os
import re
import numpy as np
import pandas as pd
import torch
import joblib
import json
from utils.paths import MTM_UTILS, MTM_MEDVIT, DATA_DIR, RESULTS

from models.multimodal_medvit.final_architecture.model_carolina import (load_multimodal_model,
                            load_image,
                            extract_image_embeddings,
                            get_tabular_features,
                            concatenate_embeddings,
                            
                        )

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

from models.multimodal_medvit.final_architecture.model_config import MULTIMODAL_MODEL_PATH, PIPELINE_PATH, COLS_CONFIG
#from models.multimodal_medvit2.final_architecture.explainability import UnifiedClinicalProxy
from pytorch_grad_cam import HiResCAM
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from PIL import Image
import io
import cv2

class MultimodalMedvitModelWrapper(ModelWrapper):
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model = None
        self.pipeline = None
        self.model_path = MULTIMODAL_MODEL_PATH #temporariamente
        self.pipeline_path = PIPELINE_PATH
        self.cols_config = COLS_CONFIG

    
    def _load_model(self):

        # contruir o modelo e a pipeline caso nao tenham sido ainda 
        # o path dos pesos do medvit, da pipeline do edca e da configuração de colunas tem de ser atributos internos (nao pdoem ser paths fixos)
        if self.model is None:
            self.model = load_multimodal_model(
                self.model_path,
                self.cols_config
            )

        if self.pipeline is None:
            self.pipeline = joblib.load(self.pipeline_path)
            
        return self.model, self.pipeline

    
    def preprocess(self, raw_input: dict, input_to_process: dict) -> dict:

        """
        Feature engineering of multimodal_medvit model-specific features that are not directly collected by the UI.

        Computed features for this model include:
        - IMCs (initial/final)
        - PartoTermoAnterior
        - PatologiasPrevias_19-obesidade
        - AumentoPonderal
        - EPF(pesoemg)
        - CSAAnt 
        """

        tabular_raw = raw_input["tabular"]
        tabular_processed = input_to_process["tabular"]
        images_processed = input_to_process["images"]

        # Get collected values that will be used to compte the remaining features
        altura = tabular_raw["altura"]
        peso_i = tabular_raw["pesoInicial"]
        peso_f = tabular_raw["pesoFinal"]
        dpb = tabular_raw["dpb"]
        pAB = tabular_raw["pAB"]
        pc = tabular_raw["pc"]
        fl = tabular_raw["fl"]
        paridade = tabular_raw["paridade"]
        partos_pre_termo = tabular_raw["partoPreTermoAnt"]
        tipo_parto_ant = tabular_raw["tipoPartoAnt"]


        # BMI derivation
        imc_i = imc(altura, peso_i)
        tabular_processed["IMCInicial"] = imc_i

        imc_f = imc(altura, peso_f)
        tabular_processed["IMCfinal"] = imc_f

        # Parto Termo Anterior derivation
        if paridade != 0:
            tabular_processed["PartoTermoAnterior"] = paridade - partos_pre_termo
        else:
            tabular_processed["PartoTermoAnterior"] = 0

        # Previous pathologies - obesidade derivation
        if imc_f > 30:
            tabular_processed["PatologiasPrevias_19-obesidade"] = 1
        else:
            tabular_processed["PatologiasPrevias_19-obesidade"] = 0

        # Weight gain derivation
        aument_pond = aumento_ponderal(peso_i, peso_f)
        tabular_processed["AumentoPonderal"] = aument_pond

        # Estimated fetal weight
        epf = hadlock_formula(dpb,pAB,pc,fl)
        tabular_processed["EPF(pesoemg)"] = epf
                
        # CSAAnt derivation
        if tipo_parto_ant == "Cesariana":
            tabular_processed["CSAAnt"] = 1
        else: 
            tabular_processed["CSAAnt"] = 0

        # One-hot encoding for categorical variables
        tabular_processed = apply_categorical_mapping(tabular_raw, MULTIMODAL_MEDVIT_CATEGORICAL_MAPPINGS, tabular_processed)

        print("TABULAR PROCESSED:")
        for k, v in tabular_processed.items():
            print(f"{k}: {v!r} | type={type(v)}")

        # Turn all processed inputs in float format
        tabular_processed = {k: float(v) for k, v in tabular_processed.items()}

        # Build model payload
        return {
            "tabular": tabular_processed,
            "images": images_processed
        }

    
    def predict(self, 
        model_input: dict | pd.DataFrame,
        device = DEVICE, 
        cols_config = COLS_CONFIG,
        root_dir = None) -> dict:

        model, pipeline = self._load_model()

        num_cols = COLS_CONFIG["num_cols"] 
        cat_cols = COLS_CONFIG["cat_cols"] 
        img_cols = COLS_CONFIG["image_cols"]

        # Adaptation to different formats
        if isinstance(model_input, pd.DataFrame):
            # Se for um DataFrame inteiro, extraímos apenas a primeira linha como Series
            row = model_input.iloc[0]
            tabular_data = row
            # No DataFrame original, as imagens estão nas colunas indicadas por img_cols
            abdomen_img_input = row[img_cols[0]]
            head_img_input = row[img_cols[1]]
            femur_img_input = row[img_cols[2]]

        elif isinstance(model_input, pd.Series):
            row = model_input
            tabular_data = row
            head_img_input = row[img_cols[1]]
            femur_img_input = row[img_cols[2]]
            abdomen_img_input = row[img_cols[0]]

        elif isinstance(model_input, dict):
            # Se for o dicionário estruturado que definiu anteriormente:
            tabular_data = model_input["tabular"]
            images = model_input["images"]
            #print("images from model input", images)
            abdomen_img_input = images[img_cols[0]]
            head_img_input = images[img_cols[1]]
            femur_img_input = images[img_cols[2]]
            
        else:
            raise TypeError("O 'model_input' deve ser um DataFrame, uma Series ou um Dicionário estruturado.")

        # 2. Carregar as imagens (A nossa função load_image agora aceita bytes ou caminhos str!)
        head_img, head_valid = load_image(head_img_input, root_dir)
        femur_img, femur_valid = load_image(femur_img_input, root_dir)
        abdomen_img, abdomen_valid = load_image(abdomen_img_input, root_dir)
        
        # Mover tensores para o dispositivo correto (GPU/CPU)
        head_img = head_img.to(device)
        femur_img = femur_img.to(device)
        abdomen_img = abdomen_img.to(device)

        # 3. Extrair as características tabulares (A função aceita dict ou Series perfeitamente)
        tabular_features = get_tabular_features(tabular_data, num_cols, cat_cols)

        # 4. Extração de Embeddings (Rede Neuronal)
        with torch.no_grad():
            head_emb = extract_image_embeddings(model, head_img, head_valid)
            femur_emb = extract_image_embeddings(model, femur_img, femur_valid)
            abdomen_emb = extract_image_embeddings(model, abdomen_img, abdomen_valid)

        # 5. Concatenar tudo num único vetor
        embedding_vector = concatenate_embeddings(head_emb, femur_emb, abdomen_emb, tabular_features)

        # Reconstruir os nomes das colunas para o pipeline do Scikit-Learn
        head_cols    = [f"image_head_emb{i+1}"    for i in range(head_emb.shape[0])]
        abdomen_cols = [f"image_abdomen_emb{i+1}" for i in range(abdomen_emb.shape[0])]
        femur_cols   = [f"image_femur_emb{i+1}"   for i in range(femur_emb.shape[0])]
        tabular_cols = num_cols + cat_cols

        all_cols = head_cols + abdomen_cols + femur_cols + tabular_cols

        # Criar o DataFrame de uma linha que o pipeline (Scikit-learn/XGBoost) exige
        embedding_df = pd.DataFrame([embedding_vector], columns=all_cols)
        
        # 6. Inferência Final do Pipeline
        y_proba = pipeline.predict_proba(embedding_df)[:, 1]
        y_pred = (y_proba >= 0.5).astype(int)

        # Retornar o dicionário de previsão limpo
        prediction = {
            "predicted_class": int(y_pred[0]),
            "class_0_proba": float(1 - y_proba[0]),
            "class_1_proba": float(y_proba[0]),
        }

        return prediction

    def explain(self, model_input: dict, prediction: dict):

        return {
            "success": False, # manter false enquanto não existir explicabilidade
            "predicted_class": int(prediction["predicted_class"]),
        }

