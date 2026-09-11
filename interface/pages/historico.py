import streamlit as st
from interface.ui_utils.ui_utils import render_widgets_for_group, render_step_tracker,render_sidebar_model_menu
from src.model_registry import get_model_specs
from src.session import initialize_session

initialize_session()

# Hide page links on the sidebar
st.markdown("""
    <style>
    /* Targets the native sidebar navigation container */
    div[data-testid="stSidebarNav"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

render_step_tracker(current_step=2)
render_sidebar_model_menu()

left, col, right = st.columns([1,2,1])

with col:  
    
    st.space("small")
    st.subheader("Antecedentes obstétricos")
    render_widgets_for_group("historico")
    
    st.space("small")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Anterior"):
            st.switch_page("pages/gravidez.py")   

    with col2:
        if st.button("Seguinte"):
            st.switch_page("pages/condicoes.py")


# For debug, uncomment to see data in session
st.session_state