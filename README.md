# Clinical Decision Support System for Predicting Delivery Mode after Labour Induction
This project presents a CDSS developed alongside CISUC and CHUCH for predicting the delivery mode - Vaginal Delivery (VD) or Cesarian Section (CS) - following Induction of Labour (IOL). 

This CDSS is structured separating the Knowledge Base, Inference Engine and User Interface components which are represented by the folders, models, src and interface respectively.

## Knowledge Base 
Within the models folder are present the Artificial Intelligence (AI) models used by the CDSS to generate the intended clinical support. Currently two models are present:

- A Multimodal model [model](https://github.com/carolinaantunes03/multimodal-prediction-obstetrics).
- A Tabular Random Forest (RF) model developed within an MLOps cicle using MLflow.

