from src import config_mlflow #só import config_mflow se estiver a correr a interface de uma página

#from src.models_specs import MODEL_SPECS
import mlflow.pyfunc
import pandas as pd
import streamlit as st
import os
import datetime
import copy
import streamlit as st

#from src.features.feature_engineering import save_to_csv
from src.features.validation import validate_raw_input 
from utils.data_logging.logger import log_inference_data_to_csv
from src.model_registry import get_model_specs


def validate_raw_input(session_data: dict) -> dict:

    raw_input = session_data["raw_input"]
    model_specs = get_model_specs(session_data["metadata"]["model"])
    tabular_metadata = model_specs.ui_inputs.get("tabular", {})
    images_metadata = model_specs.ui_inputs.get("images", {})
    missing = [] # missing values
    invalid = [] # clinically unplausible values (out of the admissible range)

    if tabular_metadata:
        for key, metadata in tabular_metadata.items():
            
            value = raw_input["tabular"].get(key)
            label = metadata["label"]

            # Verify firts if for required values they have a value
            if metadata.get("required", False) and value is None:
                missing.append(label)
                continue

            if value is None:
                continue

            # Second, verify if the input with a admissible range the inserted value is within bonds 
            range_values = metadata.get("range_values")

            if range_values is not None:
                min_value, max_value = metadata["range_values"]

                if (
                    (min_value is not None and value < min_value)
                    or
                    (max_value is not None and value > max_value)
                ):
                    invalid.append(
                        f"{label} (valor: {value}; permitido: {min_value}–{max_value})"
                    )
    
    if images_metadata:
        for key, metadata in images_metadata.items():
            
            value = raw_input["images"].get(key)
            label = metadata["label"]

            if metadata.get("required", False) and value is None:
                missing.append(label)
                continue

            if value is None:
                continue

    messages = []

    if missing:
        missing_str = "".join(f"\n- **{item}**" for item in missing)
        messages.append(
            f"A previsão não pode ser feita sem os seguintes dados: {missing_str}.\n")

    if invalid:
        invalid_str = "\n".join(f"- **{item}**" for item in invalid)
        messages.append(
            f"Os seguintes campos contêm valores inválidos:\n\n {invalid_str}."
        )

    if messages:
        messages.append(
            "Pode editar os campos mencionados acima ou volte aos respetivos campos e introduza os valores solicitados."
        )

        return {
            "success": False,
            "message": "\n\n".join(messages)
        }

    return {
        "success": True,
        "message": "Raw input is valid."
        }



def predict(session_data: dict) -> dict:

    raw_input = session_data["raw_input"]
    model_specs = get_model_specs(session_data["metadata"]["model"])
    
    df = pd.DataFrame([raw_input["tabular"]])
    pd.set_option('display.max_columns', None)
    print("raw input\n", df.head())

    # saving raw data (thi is just for debug)
    if model_specs.raw_inputs_csv:
        
        log_inference_data_to_csv(
            model_specs.raw_inputs_csv,
            session_data,
            stage="raw_input",
            tabular=raw_input["tabular"],
            images=raw_input.get("images", {})
        ) # no prediction to save yet


    # Dos valores já introduzidos passar para a payload aquilo que nao precisa de ser processado
    tabular_data = raw_input["tabular"]

    tabular_to_process = {
        feature: None 
        for feature in model_specs.model_schema["tabular"] 
        }

    # passar ja aqui os valores que podem seguir diretamente para o modelo
    for ui_key, feature in model_specs.ui_to_model["tabular"].items():
        tabular_to_process[feature] = tabular_data[ui_key]

    if model_specs.ui_inputs["images"]: #se o modelo receber imagens, a mesma logica
        
        images = raw_input["images"]

        images_to_process = {
            feature: None 
            for feature in model_specs.model_schema["images"] 
            }

        for ui_key, feature in model_specs.ui_to_model["images"].items():
            images_to_process[feature] = images[ui_key]

        input_to_process = {
            "tabular": tabular_to_process,
            "images": images_to_process
        }

    else:

        input_to_process = {
            "tabular": tabular_to_process,
            "images": None
        }

    # Construir o model input
    model_input = model_specs.wrapper.preprocess(raw_input, input_to_process)
    df = pd.DataFrame([model_input["tabular"]])
    pd.set_option('display.max_columns', None)
    print("model input\n", df.head())

    print("model input", model_input["tabular"])

    # saving preprocessed data (thi is just for debug)
    if model_specs.preprocessed_inputs_csv:
    
        log_inference_data_to_csv(
            model_specs.preprocessed_inputs_csv,
            session_data,
            stage="processed_input",
            tabular=model_input["tabular"],
            images=model_input.get("images", {})
        ) # no prediction to save yet

    # Correr inferencia
    prediction = model_specs.wrapper.predict(model_input)

    # Gerar explicação

    explanation = model_specs.wrapper.explain(model_input, prediction)


    # save prediction with corresponding sample
    if model_specs.predictions_csv:
        log_inference_data_to_csv(
            model_specs.predictions_csv,
            session_data,
            stage="predictions",
            tabular=model_input["tabular"],
            images=model_input.get("images", {}),
            prediction=prediction
        )


    return {
        "success": True,
        "prediction": prediction,
        "explanation": explanation,
        "message": "Inference successful.",
    }

