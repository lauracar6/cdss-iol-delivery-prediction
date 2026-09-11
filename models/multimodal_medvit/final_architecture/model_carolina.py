import sys
import os
import json
import random
from pathlib import Path
import io

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader
from PIL import Image

from models.multimodal_medvit.multimodal_architecture import models
from models.multimodal_medvit.multimodal_architecture.data import get_val_image_transform
from models.multimodal_medvit.final_architecture.model_config import NUM_CATEGORIES
from utils.paths import MTM_UTILS#, PROSPECTIVE_DATASET, RETROSPECTIVE_DATASET
#from src.data.model_schema import FULL_MODEL_SCHEMA_TABULAR


import joblib

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#vou ter de fazer uma alteração a esta função (passar a configuração toda de cols em ves de numericas e ceteg separadas)
def load_multimodal_model(multimodal_model_path, cols_config): 
    
    num_cols = cols_config["num_cols"]
    num_numerical = len(num_cols)
    #num_categories = [train_df[col].nunique() + 1 for col in cat_col
    num_categories = NUM_CATEGORIES #isto esta adaptado ao do medvit, muito atenção a isto

    multimodal_model = models.build_multimodal_model(
        num_numerical=num_numerical,
        num_categories=num_categories,
        tabular_token_dim=192,
        tabular_hidden_dim=192
    ).to(DEVICE)

    multimodal_model.load_state_dict(torch.load(multimodal_model_path, map_location=DEVICE))
    multimodal_model.eval()

    return multimodal_model

image_transform = get_val_image_transform()


def load_image(img_input, root_dir=None):
    """
    Carrega uma imagem a partir de um caminho (str) ou de bytes diretamente.
    Retorna o tensor transformado e um indicador de sucesso (1) ou falha (0).
    """
    # 1. Caso Base: Se a entrada for nula ou inválida
    if img_input is None or pd.isna(img_input):
        return torch.zeros(3, 224, 224), 0
        
    img = None

    # 2. Cenário A: A entrada são BYTES diretamente
    if isinstance(img_input, (bytes, bytearray)):
        try:
            img = Image.open(io.BytesIO(img_input)).convert("RGB")
        except Exception as e:
            print(f"[ERROR] Could not load image from bytes: {e}")
            return torch.zeros(3, 224, 224), 0

    # 3. Cenário B: A entrada é um CAMINHO (String)
    elif isinstance(img_input, str):
        # Tratar o caminho com o diretório raiz, se fornecido
        if root_dir and not os.path.isabs(img_input):
            img_input = os.path.join(root_dir, img_input)
        
        # Verificar se o ficheiro existe no disco
        if not os.path.exists(img_input):
            print(f"[WARN] Missing image path: {img_input}")
            return torch.zeros(3, 224, 224), 0
            
        try:
            img = Image.open(img_input).convert("RGB")
        except Exception as e:
            print(f"[ERROR] Could not open {img_input}: {e}")
            return torch.zeros(3, 224, 224), 0
            
    # 4. Cenário C: Tipo de dados não suportado
    else:
        print(f"[ERROR] Unsupported image input type: {type(img_input)}")
        return torch.zeros(3, 224, 224), 0

    # 5. Sucesso: Aplica as transformações e retorna
    return image_transform(img), 1



@torch.no_grad()
def extract_image_embeddings (model, image, valid):

    model.eval()

 
    image = image.unsqueeze(0)
    image = image.unsqueeze(0)

    image = image.to(DEVICE)

    emb,_ = model.image_encoder(
            image,
            image_valid_num=torch.tensor([1]).to(DEVICE),
            return_feature = True
            )  
    
    emb = F.layer_norm (emb, emb.shape[1:]) #the embedding is normalized (to stabilize values)
    
    return emb.cpu().numpy().flatten()   #flattened into a 1D vector
   


def get_tabular_features(data, num_cols, cat_cols):
    features = []
    
    # 1. Identificar as chaves/índices disponíveis
    # Se for uma Series do Pandas, olhamos para o .index. Se for dicionário, olhamos para as chaves.
    if isinstance(data, pd.Series):
        keys = data.index
    elif isinstance(data, dict):
        keys = data.keys()
    else:
        raise TypeError("O argumento 'data' deve ser um pandas.Series ou um dicionário.")
    
    # 2. Definir as colunas a ignorar (remover da extração)
    cols_to_drop = {"Processo", "Class"}
    
    # 3. Iterar pelas colunas desejadas
    for col in num_cols + cat_cols:
        if col in cols_to_drop:
            continue  # Salta se for uma das colunas que queremos ignorar
            
        if col in keys:
            features.append(data[col])
        else:
            features.append(np.nan)
            
    return np.array(features, dtype=float)

def concatenate_embeddings (head_emb, femur_emb, abdomen_emb, tabular_features): 

    multimodal_vector = np.concatenate ([head_emb, abdomen_emb, femur_emb, tabular_features])

    return multimodal_vector

