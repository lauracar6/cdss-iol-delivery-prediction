import base64
import streamlit as st
import pandas as pd
import numpy as np
import cv2
import os
from utils.paths import IMG_DIR


def apply_categorical_mapping(ui_data: dict, mappings: dict, model_input: dict) -> dict:
    """
    Applies one-hot encoding mappings to categorical inputs.

    Args:
    > ui_data: dictionary with UI inputs
    > mappings: categorical mappings
    > model_input: final model input dict initialized with all columns

    Returns:
    -> updated model_input
    """

    # going over every input and respective value
    for feature, options_mapping in mappings.items():

        for column in options_mapping.values():
            model_input[column] = 0

        selected = ui_data.get(feature) # so vai a procura das features categoricas

        if selected is None:
            continue

        if isinstance(selected, str):
            if selected in options_mapping:
                column = options_mapping[selected]
                model_input[column] = 1
        
        elif isinstance(selected,list):
            for option in selected:
                if option in options_mapping:
                    column = options_mapping[option]
                model_input[column] = 1
       
    return model_input



def imc(height, weight):
    
    if height > 0:
        imc = round(weight/((height/100)**2),1)
    else:
        imc = 0

    if imc < 15 or imc > 60:
        st.markdown(f"<p style='font-size:14px;'><b>IMC inicial tem de ser um valor entre 15 e 60</b> </p>", unsafe_allow_html=True)
    
    return imc

def aumento_ponderal(initial_weight, final_weight):
    return final_weight - initial_weight



def hadlock_formula(dpb,ac,hc,fl):

    dpb_cm = dpb/10
    hc_cm = hc/10
    ac_cm = ac/10
    fl_cm = fl/10
    log_epf = (1.3596 - 0.00386 * (ac_cm * fl_cm) + 0.0064 * hc_cm + 0.00061 * (dpb_cm * ac_cm) + 0.0424 * ac_cm + 0.174 * fl_cm)
    epf = round(10 ** log_epf,2)
    
    return epf
            

def save_to_csv(data, tabular_keys, image_keys, csv_path):
    os.makedirs(IMG_DIR, exist_ok=True)

    row = {}

    # timestamp
    row["timestamp"] = data["timestamp"]

    # tabulares
    tabular = data["tabular"]
    for k in tabular_keys:
        row[k] = tabular.get(k, None)

    # imagens (optional)
    images = data.get("images")
    if image_keys and images:
        for img_name in image_keys:
            if img_name in images and images.get(img_name) is not None:
                img_path = os.path.join(
                    IMG_DIR,
                    f"{data['timestamp']}_{img_name}.png"
                )

                with open(img_path, "wb") as f:
                    f.write(images[img_name])

                row[f"{img_name}_image_path"] = img_path
            else:
                row[f"{img_name}_image_path"] = None

    df = pd.DataFrame([row])

    # FORÇA ordem fixa de colunas
    # Build columns: include image path columns only if image_keys provided
    columns = ["timestamp"] + tabular_keys
    if image_keys:
        columns += [f"{k}_image_path" for k in image_keys]

    df = df.reindex(columns=columns)

    if "prediction" in data:
        df["predicted_class"] = data["prediction"]["predicted_class"]
        df["class_0_proba"] = data["prediction"]["class_0_proba"]
        df["class_1_proba"] = data["prediction"]["class_1_proba"]

    # write
    if not os.path.exists(csv_path):
        df.to_csv(csv_path, index=False)
    else:
        df.to_csv(csv_path, mode="a", header=False, index=False)