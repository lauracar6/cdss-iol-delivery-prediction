import mlflow.pyfunc
from models.multimodal_medvit.final_architecture.model_wrapper import MultimodalMedvitModelWrapper

class MultimodalMedvitPyfuncModel(mlflow.pyfunc.PythonModel):

    def load_context(self, context):
        self.wrapper = MultimodalMedvitModelWrapper(
            model_name="bAI-CDV-multimodal-medvit"
        )

        self.wrapper.model_path = context.artifacts["weights"]
        self.wrapper.pipeline_path = context.artifacts["pipeline"]

        with open(context.artifacts["columns"], "r") as f:
            self.wrapper.cols_config = json.load(f)
    
    def predict(self, context, model_input):
        return self.wrapper.predict(model_input)