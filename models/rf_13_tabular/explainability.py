"""
SHAP explainability for the Random Forest (fast / tabular) model.
"""

from pathlib import Path

import mlflow.sklearn
import pandas as pd
import shap
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter
from sklearn.pipeline import Pipeline
from utils.paths import RETROSPECTIVE_DATASET

# Defaults for feature ranking on the Streamlit page
SHAP_TOP_N = 3
SHAP_MIN_VALUE = 0.0

PREDICTION_MAPPING = {
    0: "vaginal",
    1: "cesariana",
}

CLINICAL_LABEL_MAP = {
    "Paridade":"Paridade",
    "PartoTermoAnterior": "Nº de partos termo anteriores",
    "Idade":"Idade",
    "PesoInicial": "Peso inicial",
    "PesoFinal": "Peso final",
    "Altura": "Altura",
    "IG": "Idade gestacional",
    "Bishop": "índice de bishop",
    "MetodoInd_1-misoprostol": "Método de indução (misoprostol)", 
    "ComplicGravidez_2-DG": "Diabetes gestacionais", 
    "PatologiasPrevias_19-obesidade": "Imc superior a 30", 
    "MotivoInd_11-patologiafetal": "Motivo de indução (patologia fetal)", 
    "CSAAnt": "Cesariana anterior"
}


@st.cache_resource
def load_shap_background(features: tuple):
    """ 
    Loads and caches background dataset (the same used during training) to be used by SHAP Explainer.
    """
    
    # Features must be passed as a tuple so they are hashable for st.cache_resource
    if RETROSPECTIVE_DATASET.exists():
        df = pd.read_csv(RETROSPECTIVE_DATASET)
        background = df[list(features)]
        if len(background) > 100:
            return shap.sample(background, 100, random_state=42)
        return background
    raise FileNotFoundError(
        "Background dataset not found. Expected retrospective_dataset.csv "
        "in the project root or one level above."
    )


@st.cache_resource
def get_rf_explainer(_model, features: tuple):
    """
    Creates SHAP Explainer object once and caches it in memory.

    :param model: Sklearn model thet generated predictions
    :param tuple features: Expected features schema 
    """
    background = load_shap_background(features)
    return shap.Explainer(_model, background)



def input_to_dataframe(input: dict | pd.DataFrame, feature_order: list | dict) -> pd.DataFrame:
    """
    Converte dados tabulares para DataFrame e ordena as colunas 
    com base nas chaves de um dicionário ou elementos de uma lista.
    """
    if isinstance(input, pd.DataFrame):
        df = input.copy()
    else:
        df = pd.DataFrame([input])
    
    # Se feature_order for um dicionário, extrai as chaves como uma lista
    if isinstance(feature_order, dict):
        feature_order = list(feature_order.keys())
    else:
        feature_order = feature_order

    return df[feature_order]

def extract_top_positive_features(
    shap_values,
    sample_df: pd.DataFrame,
    predicted_class: int,
    top_n: int = SHAP_TOP_N,
    min_shap: float = SHAP_MIN_VALUE,
) -> list[dict]:
    """
    Rank features by positive SHAP contribution toward the predicted class.

    Returns a list of dicts: feature name, shap_value, input_value.
    """
    class_idx = int(predicted_class)
    contributions = shap_values.values[0, :, class_idx] # sample index = 0; feature index = all features; class index = the predicted one -> this gets shap values for the first sample (and the only, we are passing one sample at a time), all features and for the predcited class
    feature_names = list(sample_df.columns)

    ranked = []
    for name, shap_val in zip(feature_names, contributions):
        shap_val = float(shap_val)
        if shap_val >= min_shap:
            ranked.append(
                {
                    "feature": name,
                    "shap_value": round(shap_val, 4),
                    "input_value": sample_df[name].iloc[0],
                }
            )

    ranked.sort(key=lambda item: item["shap_value"], reverse=True)
    return ranked[:top_n]



def ordered_feature_contributions(
    shap_values,
    sample_df: pd.DataFrame,
    predicted_class: int,
    feature_mapping: dict = None,  # Added mapping dictionary parameter
) -> list[dict]:
    """
    Rank features by greatest SHAP contribution (absolute shap value) given the predicted class.
    Returns a list of dicts: feature name, clinical label, shap_value, input_value.
    """
    if feature_mapping is None:
        feature_mapping = {}

    class_idx = int(predicted_class)
    contributions = shap_values.values[0, :, class_idx] 
    feature_names = list(sample_df.columns)
    
    ranked = []
    for name, shap_val in zip(feature_names, contributions):
        shap_val = float(shap_val) 
        
        # Look up the clean medical label, fallback to auto-formatting if missing
        clean_label = feature_mapping.get(
            name, 
            name.replace("_", " ").title()
        )
        
        ranked.append(
            {
                "feature": name,
                "feature_label": clean_label,  # New display column
                "shap_value": round(shap_val, 4),
                "shap_abs_value": abs(shap_val),
                "input_value": sample_df[name].iloc[0],
                "direction": "increase" if shap_val > 0 else "decrease",
            }
        )

    # Sort everything by maximum absolute impact
    ranked.sort(key=lambda item: item["shap_abs_value"], reverse=True)

    return ranked


def explain_rf_tabular(
    model,
    expected_features: list,
    input: dict | pd.DataFrame,
    predicted_class: int,

) -> dict:
    """
    Compute SHAP values for one RF prediction and return top contributing features
    for the predicted class.
    """
    
    # Here we convert the input the model received as a pandas dataframe to get the shap values with the explainer
    sample_df = input_to_dataframe(input, expected_features)

    if isinstance(model, Pipeline):
        model = model.named_steps["model"]

    explainer = get_rf_explainer(model, tuple(expected_features)) # returns the explainer given the model used for prediction
    shap_values = explainer(sample_df)

    # creating needed values for watterfall plot
    class_idx = int(predicted_class)

    # SHAP VALUES
    if shap_values.values.ndim == 3:
        values = shap_values.values[0, :, class_idx]
    else:
        values = shap_values.values[0, :]

    # BASE VALUE
    base_vals = shap_values.base_values
    if np.array(base_vals).ndim == 2:
        base_value = base_vals[0, class_idx]
    else:
        base_value = base_vals[0]

    # SAMPLE
    data = sample_df.iloc[0].values
    feature_names = list(sample_df.columns)

    # SHAP VALUES, BASE VALUE, DATA e FEATURE NAMES
    explanation = shap.Explanation(
        values=values, 
        base_values=base_value, 
        data=data, 
        feature_names=feature_names
    )

    #waterfall = shap.plots.waterfall(explanation)
    fig, ax = plt.subplots(figsize=(8, 4))

    shap.plots.waterfall(
        explanation,
        show=False
    )

    fig = plt.gcf()

    ordered_feature_contributions = ordered_feature_contributions(shap_values, sample_df, predicted_class, feature_mapping=CLINICAL_LABEL_MAP)

    return {
        "success": True, # just to signal an explanation was generated so the interface knows it can display
        "predicted_class": int(predicted_class),
        "base_value": base_value,
        "shap_raw_explanation": explanation,
        "top_features": ordered_feature_contributions,
    }

