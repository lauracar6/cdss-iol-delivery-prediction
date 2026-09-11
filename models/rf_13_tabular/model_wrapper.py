from models.base_wrappers import ModelWrapper
from models.rf_13_tabular.schema import RF_13_CATEGORICAL_MAPPINGS, YES_NO_MAPPING
from models.rf_13_tabular.explainability import explain_rf_tabular
from src.features.feature_engineering import imc
import mlflow
import pandas as pd

class RF13ModelWrapper(ModelWrapper):
    
    def __init__(self, model_name: str): # quando chamar o wrapper deste modelo so tenho de indicar o nome do modelo registado no mflow
        self.model_name = model_name
        self.pyfunc_model = None
        self.sklearn_model = None
        self.expected_features = None

    
    def _load_model(self):
        
        if self.pyfunc_model is None or self.sklearn_model is None:
            # 1. Load PyFunc model to read metadata schema
            self.pyfunc_model = mlflow.pyfunc.load_model(
                model_uri=f"models:/{self.model_name}@champion"
            )
            
            # 2. Load sklearn model for probability inference
            self.sklearn_model = mlflow.sklearn.load_model(
                model_uri=f"models:/{self.model_name}@champion"
            )
            
            # 3. Read and cache the expected features from MLflow schema
            schema = self.pyfunc_model.metadata.get_input_schema()
            self.expected_features = [f.name for f in schema.inputs]
            
        return self.pyfunc_model, self.sklearn_model, self.expected_features

    
    def preprocess(self, raw_input: dict, input_to_process: dict) -> dict:
        
        # aqui so acontece processamento especifico ao modelo. passar os valores introduzidos para  a estrtura que o modelo recebe é feito antes
      
        tabular_raw = raw_input["tabular"]
        tabular_processed = input_to_process["tabular"] #aqui ainda pode estar em categorica

        paridade = tabular_raw["paridade"]
        partos_pre_termo = tabular_raw["partoPreTermoAnt"]

        if paridade is not 0:

            tabular_processed["PartoTermoAnterior"] = paridade - partos_pre_termo

        else:

            tabular_processed["PartoTermoAnterior"] = 0

        if tabular_raw["altura"] is not 0:
            imc_final = imc(tabular_raw["altura"], tabular_raw["pesoFinal"])
        else:
            imc_final = 0
        
        if imc_final > 30:
            tabular_processed["PatologiasPrevias_19-obesidade"] = 1
        else:
            tabular_processed["PatologiasPrevias_19-obesidade"] = 0


        for ui_key, feature in RF_13_CATEGORICAL_MAPPINGS.items():
            
            selected = tabular_raw.get(ui_key)
            tabular_processed[feature] = YES_NO_MAPPING[selected]
    
        # converting preprocessed tabular data to float types
        tabular_processed = {k: float(v) for k, v in tabular_processed.items()}

        return {
            "tabular": tabular_processed
        }

    
    def predict(self, model_input: dict | pd.DataFrame) -> dict:

        """
        Runs Random Forest inference on the preprocessed tabular input.
        """

        _, sklearn_model, expected_features = self._load_model()

        # Verificamos primeiro o tipo de input (pode ser um dataframe pandas ou um dicionario)

        if isinstance (model_input, dict):
            #vou alterar so poruq estou a criar um dicionario sem "tabular"
            tabular_input = model_input.get("tabular", model_input)
            received_features = tabular_input.keys()
        
        elif isinstance(model_input, pd.DataFrame):
            received_features = model_input.columns
        
        missing_features = set(expected_features) - set(received_features) #set() permite fazer operações entre conjuntos. 
        # neste caso estamos a verificar que features estão a faltar nas introduzidas na interface -input.keys()
        if missing_features:
            raise ValueError(f"Erro de Schema: Faltam as seguintes features no input: {missing_features}")
        
        #tive de adicionar aqui para o caso de nao ter a key "tabular"
        model_input = model_input.get("tabular", model_input)

        if isinstance(model_input, pd.DataFrame):
            df = model_input[expected_features].copy()
        else:
            #alterei aqui pata model input em vez de model_input["tabular"]
            df = pd.DataFrame([model_input])[expected_features]

        # Garantir a ordem correta de colunas
        df = df[expected_features] # reordena  segundo o schema esperado pelo modelo

        # Fazer previsão (uso o modelo sklearn)
        predicted_class = int(sklearn_model.predict(df)[0]) # o resultado vem em float # fazemos [0] porque o resultado vem num array e a previsao esta no primeiro indice
        probabilidades = sklearn_model.predict_proba(df)[0]

        return {
            "predicted_class": predicted_class, 
            "class_0_proba": probabilidades[0],
            "class_1_proba": probabilidades[1]           
        }


    def explain(self, model_input: dict, prediction: dict) -> dict | None:
         
         """Generates explanations as table and waterfall plot"""
        
         _, sklearn_model, expected_features = self._load_model()

         predicted_class = prediction["predicted_class"]

        # tenho de adicionar isto aqui so para o caso do model inptu nao ter tabular
         model_input = model_input.get("tabular", model_input)

         explanation = explain_rf_tabular(
            model = sklearn_model,
            expected_features = expected_features,
            input = model_input, #["tabular"],
            predicted_class = predicted_class
         )

         return explanation
         
