import datetime
import streamlit as st
from src.model_registry import get_model_specs
from utils.data_logging.logging_schemas import INTERFACE_VERSION

"""
SESSION_DATA = {
    "session_start": None,
    "model": None,
    "patient_id": None,
    "raw_input": {
        "tabular": {},
        "images": {}
    },
    "result": None
}
"""
DEFAULT_MODEL = "rf_13_tabular"

def initialize_session():

    if "sessao" in st.session_state:
        return

    model_specs = get_model_specs(DEFAULT_MODEL)

    st.session_state["sessao"] = {
        
        "metadata": {
            "request_id": None, # definir isto no momneto em que se clica no botão de prever
            "patient_id": None,
            "session_start" : datetime.datetime.now(),
            "model" : model_specs.key,
            "model_name": model_specs.mlflow_model_name,
            "model_version": model_specs.version, #somehow get the model version defined in model specs
            "migrated_session": False,
            "interface_version": INTERFACE_VERSION, # para já fica esta
        },    

        "raw_input" : { #patient id esta dentro do raw input (definido com um ui input tabular)
            "tabular" : {
                k: None 
                for k in model_specs.ui_inputs["tabular"].keys()
                },
            "images": {
                k: None 
                for k in model_specs.ui_inputs["images"].keys()
                }
        },

        "result": None
}


def migrate_model_session(new_model: str):
    """
    Safely changes the active prediction model, migrating any already
    filled inputs to the new model's session state structure.
    """
    session = st.session_state["sessao"]
    current_model = session["metadata"]["model"]
    
    # If the model is the same, do nothing
    if current_model == new_model:
        return
        
    # Get specifications for both models
    new_specs = get_model_specs(new_model)
    
    old_tabular = session["raw_input"]["tabular"]
    old_images = session["raw_input"]["images"]
    
    # Initialize the new state structure with None values
    new_tabular = {k: None for k in new_specs.ui_inputs["tabular"].keys()}
    new_images = {k: None for k in new_specs.ui_inputs.get("images", {}).keys()}
    
    # Migrate overlapping tabular keys (e.g. "idade", "altura", "paridade")
    for key in new_tabular:
        if key in old_tabular:
            new_tabular[key] = old_tabular[key]
            
    # Migrate overlapping image keys
    for key in new_images:
        if key in old_images:
            new_images[key] = old_images[key]
            
    # Save the migrated structures back to session state
    session["metadata"]["model"] = new_model
    session["metadata"]["model_name"] = new_specs.mlflow_model_name
    session["metadata"]["model_version"] = new_specs.version
    session["metadata"]["migrated_session"] = True
    session["raw_input"]["tabular"] = new_tabular
    session["raw_input"]["images"] = new_images
    
    # Force Streamlit to immediately redraw the page using the new model UI widgets
    #st.rerun()
    st.switch_page("main_page.py")