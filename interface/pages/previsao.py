import streamlit as st
import copy
import pandas as pd
import uuid

from src.inference_engine import validate_raw_input, predict
from interface.ui_utils.ui_utils import (
    display_prediction,
    display_explanation,
    render_sidebar_model_menu,
    migrate_model_session,
    get_model_options
)
from src.session import initialize_session
from src.model_registry import get_model_specs


initialize_session()

# Hide page links on the side bar
st.markdown("""
    <style>
    /* Targets the native sidebar navigation container */
    div[data-testid="stSidebarNav"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

render_sidebar_model_menu()


input_data = st.session_state["sessao"]["raw_input"]
result = st.session_state["sessao"].get("result")

has_prediction = result is not None
is_expanded = not has_prediction

# Validation pipeline from inference engine is called for data validation
session_data = copy.deepcopy(st.session_state["sessao"])
validation = validate_raw_input(session_data)

# Confirmation panel
with st.expander("Confimar dados da paciente para previsão",expanded=is_expanded):

    tabular_data = pd.DataFrame([input_data.get("tabular", {})])

    st.markdown("##### Variáveis tabulares")

    # Editable dataframe for displaying tabular values
    edited_df = st.data_editor(tabular_data,use_container_width=True,hide_index=True)

    # Validation feedback is shown in the panel before the user hits predict
    if not validation["success"]:
        st.markdown(validation["message"])

    # If valued are edited on the table, update raw input payload
    edited_dict = edited_df.iloc[0].to_dict()

    # Make sure the edited value's type is according to what its expected for that input
    model = st.session_state["sessao"]["metadata"]["model"]
    model_specs = get_model_specs(model)

    for key, value in edited_dict.items():

        if key not in model_specs.ui_inputs.get("tabular", {}):
            continue

        metadata = model_specs.ui_inputs["tabular"][key]

        if metadata.get("type") == "numeric" and value is not None:
            try:
                step = metadata.get("step")

                if step:
                    edited_dict[key] = float(value)
                else:
                    edited_dict[key] = int(value)

            except (ValueError, TypeError):
                # Keeps the original value in case it can not convert to the expected type
                pass

    # If the table is edited  the raw input payload in session is updated and prior predictions are cleared from session          
    if edited_dict != input_data.get("tabular", {}):
        st.session_state["sessao"]["raw_input"]["tabular"] = edited_dict
        st.session_state["sessao"]["result"] = None
        st.session_state["sessao"]["metadata"]["request_id"] = None
        st.rerun()

    requires_images = model_specs.ui_inputs.get("images", {})

    if requires_images:
        # Display of uploaded images on the confirmation panel
        images = input_data.get("images", {})
        valid_images = {k: v for k, v in images.items() if v is not None}
        images = input_data.get("images", {})
        valid_images = {k: v for k, v in images.items() if v is not None}

        if valid_images:
            st.markdown("##### Ecografias")
            cols = st.columns(3)
            for i, img in enumerate(valid_images.values()):
                with cols[i % 3]:
                    st.image(img, use_container_width=True)
        else:
            st.markdown("##### Ecografias")
            st.write("Não introduziu imagens.")

    # add logic to allow to change images in the confirmation panel

    st.space("small")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Voltar ao formulário completo",use_container_width=True):
            st.switch_page("pages/dados_paciente.py")

    with col2:
        if st.button("Confirmar e prever",type="primary",use_container_width=True):

            # Data is validated again upon prediction request
            session_data = copy.deepcopy(st.session_state["sessao"])
            validation = validate_raw_input(session_data)

            if not validation["success"]:
                st.markdown(validation["message"])
                st.rerun()

            # Only upon valid data, the inference pipeline is triggered
            novo_request_id = str(uuid.uuid4())
            st.session_state["sessao"]["metadata"]["request_id"] = novo_request_id
            session_data["metadata"]["request_id"] = novo_request_id # update session data copy that will has the data that will be persisted
            result = predict(session_data)
            st.session_state["sessao"]["result"] = result
            st.rerun()


if result:
    st.divider()

    with st.container(width=700,border=True):
        st.subheader("Previsão")
        st.space("small")
        display_prediction(result["prediction"])
        explanation = result.get("explanation")

        if explanation:
            model = st.session_state["sessao"]["metadata"]["model"]
            st.space("medium")
            st.markdown("#### Porque é que o modelo previu isto?")
            st.space("small")
            display_explanation(explanation)

        st.space("medium")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Voltar ao início",use_container_width=True):
                st.switch_page("main_page.py")


        with col2:
            if st.button("Nova Previsão",type="primary",use_container_width=True):
                st.session_state.clear()
                st.switch_page("main_page.py")

        # Apos nova previsao permitir mudar diretamente o modelo para aqueles que nao foram usados
        model_options = get_model_options()

        current_model = (st.session_state["sessao"]["metadata"]["model"])

        available_models = {
            key: name
            for key, name in model_options.items()
            if key != current_model
        }

        st.space("small")

        with st.container(width=700,border=True):

            st.markdown("##### Obter previsão com outro modelo")

            selected_model = st.radio("Previsão à base de",
                options=list(
                    available_models.keys()
                ),
                format_func=lambda key:
                    available_models[key],
                label_visibility="collapsed",
            )

            if st.button("Obter previsão"):
                migrate_model_session(selected_model)

#st.session_state
