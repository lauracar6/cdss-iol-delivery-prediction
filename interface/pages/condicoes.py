import streamlit as st
import pandas as pd
from interface.ui_utils.ui_utils import render_widgets_for_group, render_step_tracker, render_sidebar_model_menu
from src.model_registry import get_model_specs
from src.session import initialize_session

initialize_session()

render_step_tracker(current_step=3)
render_sidebar_model_menu()

st.markdown("""
    <style>
    /* Targets the native sidebar navigation container */
    div[data-testid="stSidebarNav"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

left, col, right = st.columns([1,2,1])

with col:  
    
    st.space("small")
    st.subheader("Preparação para indução")
    render_widgets_for_group("inducao")
    
    st.space("small")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Anterior"):
            st.switch_page("pages/historico.py")   

    with col2:
        if st.button("Seguir para previsão"):
            st.switch_page("pages/previsao.py")

#st.session_state