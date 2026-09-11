import streamlit as st
from src.session import initialize_session

initialize_session()

st.switch_page("pages/dados_paciente.py")

#_, col, _ = st.columns([1,2,1])

#with col:

    # as opções devem estar a vista!
    #selected_mode = st.radio("Modo de previsão", ["Rápido", "Avançado"])
    #mapping = {
     #   "Rápido": "rf_13_tabular",
      #  "Avançado": "multimodal_medvit"
    #}
    #model = mapping[selected_mode]
    
    #if st.button ("Seguinte"): # so aqui é que as coisas entram em sessao
     #   st.session_state["sessao"]["model"] = model
      #  model_specs = get_model_specs(model)
       # st.session_state["sessao"]["raw_input"]["tabular"] = {k: None for k in model_specs.ui_inputs["tabular"].keys()}
        #st.session_state["sessao"]["raw_input"]["images"] = {k: None for k in model_specs.ui_inputs["images"].keys()}
        #st.switch_page("pages/automatic_render.py")