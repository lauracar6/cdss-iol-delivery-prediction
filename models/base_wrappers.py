from dataclasses import dataclass
from typing import Dict, List, Any
from pathlib import Path
from abc import ABC, abstractmethod

class ModelWrapper(ABC):
    
    @abstractmethod
    def preprocess(self, raw_input: dict, input_to_process: dict) -> dict:
        """
        Feature engineering of model-specific features that are not directly collected by the UI.

        Transforms the raw input dictionary containing all the UI collected values into the model 
        payload containing all expected features and their corresponding values.

        :param dict raw_input: Dictionary containing all raw values collected by the UI
        :param dict input_to_process: Dictionary containing all inputs that require
        """

        
        pass

    @abstractmethod
    def predict(self, model_input: dict) -> dict:
        """Runs inference on the preprocessed inputs."""
        pass

    def explain(self, model_input: dict, prediction: dict) -> dict | None:
        """Generates XAI explanation (SHAP, etc.) if supported, else returns None."""
        return None


@dataclass
class ModelSpec:
    key: str                             
    mlflow_model_name: str
    ui_terminology: str
    version: str                            
    
    # Ui inputs e model schema
    ui_inputs: Dict[str, Any]            
    model_schema: List[str]  
    ui_to_model: Dict[str, Any]           
    
    # csv paths for data storing
    raw_inputs_csv: Path
    preprocessed_inputs_csv: Path
    predictions_csv: Path
    
    # testing and demo data
    samples: Dict[str, Dict[str, Any]]
    
    # execution engine
    wrapper: ModelWrapper

    # Derived raw input contract for validation
    def get_raw_input_contract(self) -> Dict[str, Any]:
        """Automatically builds the validation contract directly from the UI inputs."""
        contract = {
            "tabular": {},
            "images": {}
        }

        for key, metadata in self.ui_inputs.get("tabular", {}).items():
            contract["tabular"][key] = metadata["label"]
        
        for key, metadata in self.ui_inputs.get("images", {}).items():
            contract["images"][key] = metadata["label"]


        """for key, metadata in self.ui_inputs.get("tabular", {}).items():
            if metadata["type"] == "numeric":
                    contract["tabular"][key] = (int, float)
            else: #we step into categorical type of inputs
                # Check what widget style is used to render this categorical input
                widget = metadata.get("widget_type", metadata.get("widget"))
                if widget == "multiselect":
                    contract["tabular"][key] = list  # Accepts a list of strings
                else:
                    contract["tabular"][key] = str   # Accepts a single string (selectbox/radio)"""
            # 2. Map Image Inputs (Images are validated as raw bytes)
        """for key, metadata in self.ui_inputs.get("images", {}).items():
            if key is not None:
                contract["images"][key] = bytes
            else:
                contract["images"][key] = None"""

        return contract

