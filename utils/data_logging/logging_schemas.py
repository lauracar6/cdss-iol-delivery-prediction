"""
This file serves to set the structure of 3 things this tool will log:
 - raw inputs
 - processed inputs
 - processed inputs with the corresponding predictions

 In each schema you can find what the interface expects to log 

"""
INTERFACE_VERSION = "1.4"

RAW_INPUT_LOG_SCHEMA = {
    "metadata": [
        "request_id",
        "patient_id",
        "session_start",
        "interface_version",
        "model_name",
        "model_version",
    ],
    "tabular": [],
    "images": [],
}

PREPROCESSED_INPUT_LOG_SCHEMA = {
    "metadata": [
        "request_id",
        "patient_id",
        "session_start",
        "interface_version",
        "model_name",
        "model_version",
    ],
    "tabular": [],
    "images": [],
}

PREDICTIONS_LOG_SCHEMA = {    
    "metadata": [
        "request_id",
        "patient_id",
        "session_start",
        "interface_version",
        "model",
        "model_version",
    ],
    "tabular": [],
    "images": [],
    "prediction": [
        "predicted_class",
        "class_0_proba",
        "class_1_proba",
    ],
    }

LOG_SCHEMAS = {
    "raw_input" : RAW_INPUT_LOG_SCHEMA,
    "processed_input": PREPROCESSED_INPUT_LOG_SCHEMA,
    "predictions": PREDICTIONS_LOG_SCHEMA
}