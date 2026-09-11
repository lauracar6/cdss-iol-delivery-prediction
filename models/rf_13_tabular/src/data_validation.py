import pandas as pd
from models.rf_13_tabular.schema import RF_13_SCHEMA
from utils.paths import RETROSPECTIVE_DATASET


def validate_dataset(df: pd.DataFrame):

    # Dataset vazio
    if df.empty:
        raise ValueError("Dataset is empty.")

    # Colunas
    missing = set(RF_13_SCHEMA["tabular"]) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    # Missing values
    if df.isnull().sum().sum() > 0:
        raise ValueError("Dataset contains missing values.")

    # Duplicados
    if df.duplicated().sum() > 0:
        raise ValueError("Dataset contains duplicated rows.")

    # Target binário
    if df["Class"].nunique() != 2:
        raise ValueError("Target is not binary.")

    return True

retrospective_df = pd.read_csv(RETROSPECTIVE_DATASET)
y = retrospective_df["Class"]
print(y.value_counts())

print(validate_dataset(retrospective_df))