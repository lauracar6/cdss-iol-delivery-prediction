from sklearn.model_selection import train_test_split
from src.paths import RETROSPECTIVE_DATASET
from models.rf_13_tabular.src.schema import RF_13_SCHEMA
from pathlib import Path
import pandas as pd

df = pd.read_csv(RETROSPECTIVE_DATASET)

FEATURES = RF_13_SCHEMA["tabular"]

X = df[FEATURES]
y = df["Class"]

# Data spliting and saving
X_train, X_temp, y_train, y_temp = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp,
    y_temp,
    test_size=0.50,
    random_state=42,
    stratify=y_temp
)

output_dir = Path("models/rf_13_tabular/datasets")
output_dir.mkdir(parents=True, exist_ok=True)

X_train = pd.read_csv("models/rf_13_tabular/datasets/tabular_13_train.csv")
y_train = pd.read_csv("models/rf_13_tabular/datasets/y_train.csv").squeeze()

# Datasets validação
X_val = pd.read_csv("models/rf_13_tabular/datasets/tabular_13_val.csv")
y_val = pd.read_csv("models/rf_13_tabular/datasets/y_val.csv").squeeze()

X_test = pd.read_csv("models/rf_13_tabular/datasets/tabular_13_test.csv")
y_test = pd.read_csv("models/rf_13_tabular/datasets/y_test.csv").squeeze()

print(X_train.shape)
print(X_val.shape)
print(X_test.shape)

print(y_train.value_counts())
print(y_val.value_counts())
print(y_test.value_counts())