import streamlit as st
import time
import pandas as pd
from interface.ui_utils.ui_utils import render_widgets_for_group, use_sample, render_step_tracker,render_sidebar_model_menu
from src.session import initialize_session
from src.model_registry import get_model_specs
initialize_session()

render_step_tracker(current_step=0)
model_specs = get_model_specs(st.session_state["sessao"]["metadata"]["model"])

# Hide page links in the sidebar
st.markdown("""
    <style>
    /* Targets the native sidebar navigation container */
    div[data-testid="stSidebarNav"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

render_sidebar_model_menu()

# Notification message displayed upon model switch 
if st.session_state["sessao"]["metadata"].get("migrated_session", False):

    st.info(
        f"**Modelo alterado para: {model_specs.ui_terminology}**\n\n"
        "Os dados introduzidos anteriormente foram mantidos. "
        "Reveja e complete os dados necessários para obter uma nova previsão."
    )

    st.session_state["sessao"]["metadata"]["migrated_session"] = False

left, col, right = st.columns([1,2,1])

with col: 

    st.space("small")
    st.subheader("Dados maternos")

    st.info("\* Campo obrigatório para obter previsão")
    st.space("small")

    current_id = st.session_state["sessao"]["metadata"]["patient_id"]

    # Patient ID input to save as metadata
    id_paciente = st.number_input(
            "Nº de Processo",
            value= current_id if current_id is not None else None,
            width= 300,
        )
    
    st.session_state["sessao"]["metadata"]["patient_id"] = id_paciente

    render_widgets_for_group("maternos")

    st.space("small")
    
    #st.write("---") # Visual separator
    #if st.button("Carregar exemplos"):

     #   samples = model_specs.samples

      #  st.session_state["sessao"]["samples"] = samples

    #samples = st.session_state.get("sessao", {}).get("samples")

    #if samples:

        #key = st.selectbox(
         #   "Escolha um exemplo",
         #   samples.keys()
        #)

        #st.dataframe(pd.DataFrame([samples[key]]))

        #if st.button("Confirmar Carregamento"):
            #use_sample(samples[key])
            
    st.space("small")
    col1, col2 = st.columns(2)



    with col2:
        if st.button("Seguinte"):
            st.switch_page("pages/gravidez.py")

# For debug, uncomment to see data in session
#st.session_state