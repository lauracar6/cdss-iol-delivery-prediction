from utils.paths import IMG_DIR
from utils.data_logging.logging_schemas import LOG_SCHEMAS
import os
import pandas as pd
from pathlib import Path


def log_inference_data_to_csv(csv_path, session_data, stage, tabular=None, images=None, prediction=None):

    """
    Save inference information to a CSV file.

    Parameters
    ----------
    csv_path : str | Path
        Destination CSV.
    session_data : dict
        Current inference session.
    stage : {"raw_input", "processed_input", "predictions"}
        Logging stage.
    tabular : dict, optional
        Tabular data to log (raw or processed).
    images : dict, optional
        Images to save. Keys correspond to the image names.
    prediction : dict, optional
        Prediction returned by the model wrapper.
    """

    log_schema = LOG_SCHEMAS[stage]
    row = {}

    for key in log_schema["metadata"]:
            row[key] = session_data["metadata"][key] # preenche a linha dos dados de metadata segundo as keys definidad no schema
    
    # tabular (raw ou processado)
    if tabular is not None:
        for key in tabular.keys():
            row[key] = tabular[key]
    
    os.makedirs(IMG_DIR, exist_ok=True)

    if images is not None: # se não existirem imagens
        for key, image in images.items(): #vai aos labels que estao ou no raw input ou nos dados processados

            if image is None:
                row[f"{key}_path"] = None
                continue

            img_path = os.path.join(
                    IMG_DIR,
                    f"{session_data['metadata']['session_start']}_{key}.png"
                )

            with open(img_path, "wb") as f:
                f.write(image)

            row[f"{key}_path"] = img_path

    
    if prediction is not None:
        for key in log_schema.get("prediction", []):
            row[key] = prediction.get(key)


    # Assegurar ordem correta de colunas
    columns = []

    # metadata
    columns.extend(log_schema["metadata"])

    # tabular
    if tabular is not None:
        columns.extend(tabular.keys())

    # image paths
    if images is not None:
        columns.extend(f"{key}_path" for key in images.keys())

    # prediction
    if prediction is not None:
        columns.extend(log_schema["prediction"])

    df = pd.DataFrame([row])
    df = df.reindex(columns=columns)

    if not Path(csv_path).exists():
        df.to_csv(csv_path, index=False)
    else:
        df.to_csv(csv_path, mode="a", header=False, index=False)
