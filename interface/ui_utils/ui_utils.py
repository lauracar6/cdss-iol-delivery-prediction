# O CHAT sugreiu fazer um file de utils para por uma função para os inputs de select box

from interface.ui_utils.explanations_displays import (
    technical_explanation,
    narrative_explanation,
    clinical_domain_explanation,
    tornado_explanation
) 

import streamlit as st
#from src.model_specs import MODEL_SPECS
from utils.paths import DATA_DIR, IMG_DIR
import pandas as pd
import os
from src.model_registry import get_model_specs, MODEL_REGISTRY
from src.features.feature_engineering import imc, aumento_ponderal, hadlock_formula
from src.session import migrate_model_session
from interface.ui_utils.ui_arquiteture import UI_ARCHITECTURE

def use_sample(sample):
    """
    For debug/testing samples fills in automatically the UI fields and the session state.
    """

    tabular_data = st.session_state["sessao"]["raw_input"]["tabular"]
    
    for key, value in sample.items():
        # 1. Atualiza o estado interno (raw_input)
        tabular_data[key] = value
        
        # 2. Atualiza a key do widget no Streamlit (se ele já existir no session_state)
        widget_key = f"widget_{key}"
        if widget_key in st.session_state:
            st.session_state[widget_key] = value

    # 3. Força o Streamlit a redesenhar a página imediatamente com os novos dados
    st.rerun()

def render_widget(key, width=300):
    """
    Renders Streamlit specific widget based on the UI input metadata:
    - Widget type (selectbox, multiselect, number input, radion button, file uploader)
    - Label 
    - Options
    - Formats

    :param str key: Field key according to the UI input metadata
    :param int width: (default=300) Widget width.
    
    """
    
    st.markdown("""
        <style>
        div[data-testid="stWidgetLabel"] p {
            font-size: 1rem !important;
            font-weight: 500 !important;
            color: #31333F !important;
        }
        </style>
    """, unsafe_allow_html=True)

    model = st.session_state["sessao"]["metadata"]["model"]
    model_specs = get_model_specs(model)
    ui_inputs = model_specs.ui_inputs

    # Get UI inputs metadata separate by modality
    if key in ui_inputs.get("tabular", {}):
        modality = "tabular"
    elif key in ui_inputs.get("images", {}):
        modality = "images"
    else:
        raise KeyError(f"Input '{key}' não encontrado em ui_inputs")

    # Metadata for a given input
    metadata = ui_inputs[modality][key]
    data = st.session_state["sessao"]["raw_input"][modality] # Get the current values in session for the guven modality
    widget_type = metadata["widget_type"]
    
    # Current saved value in session
    current = data.get(key)

    # Applies, if specified in metadata, the default value (only when the user hasn't introduced a vlue yet = None)
    if current is None and "default" in metadata:
        current = metadata.get("default")
        data[key] = current

    # Mandatory fields signaling
    label = metadata["label"]
    if metadata.get("user_required", False):
        label += " *"

    #---------------------
    # NUMERIC INPUT FIELDS
    #---------------------
    if widget_type == "numeric":
        range_values = metadata.get("range_values")
        min_value, max_value = (range_values[0], range_values[1]) if range_values else (None, None)
        step = metadata.get("step")
        fmt = "%.1f" if step == 0.1 else "%.2f" if step == 0.01 else "%d"

        value = None
        if current is not None:
            value = float(current) if step else int(current)

        value = st.number_input(
            label,
            value=value,
            min_value=min_value,
            max_value=max_value,
            step=step if step else 1,
            format=fmt,
            width=width,
            key=f"widget_{key}"
        )

    #---------------------
    # SELECTBOX FIELDS
    #---------------------
    elif widget_type == "selectbox":
        options = metadata["options"]
        index = options.index(current) if current in options else 0

        value = st.selectbox(
            label,
            options,
            index=index,
            width=width,
            key=f"widget_{key}"
        )

    #---------------------
    # RADION BUTTON FIELDS
    #---------------------
    elif widget_type == "radio":
        options = metadata["options"]
        index = options.index(current) if current in options else 0 #None

        value = st.radio(
            label,
            options,
            index=index,
            key=f"widget_{key}"
        )

    #---------------------
    # MULTISELECT FIELDS
    #---------------------
    elif widget_type == "multiselect":
        if isinstance(current, str):
            current = [current]
        current = current or []
        current = [v for v in current if v in metadata["options"]]

        value = st.multiselect(
            label,
            metadata["options"],
            default=current,
            width=width,
            key=f"widget_{key}"
        )

    #---------------------
    # FILE UPLOADERS
    #---------------------
    elif widget_type == "img":
        # Não se passa parâmetro 'value' para file_uploader
        uploaded_file = st.file_uploader(
            label,
            type=metadata.get("formats", ["png", "jpg", "jpeg"]),
            width=width,
            key=f"widget_{key}"
        )
        
        # Se o utilizador carregou um ficheiro, guarda os bytes. Caso contrário mantém o anterior.
        value = uploaded_file.getvalue() if uploaded_file is not None else current

    else:
        raise ValueError(f"Widget_type não suportado '{widget_type}' para '{key}'")

    # Se o valor mudou, invalida a previsão anterior
    if current != value:
        st.session_state["sessao"]["result"] = None
        st.session_state["sessao"]["metadata"]["request_id"] = None

    # Updates the values in session according t the collected value by the streamlit widgets
    data[key] = value

    # Display of internall calculations LOGIC
    if model == "multimodal_medvit":
        if key == "pesoInicial":
            altura = data.get("altura") or 0
            peso_i = data.get("pesoInicial") or 0
            if altura != 0 and peso_i != 0:
                st.markdown(f"<p style='font-size:14px; color:gray;'><b>IMC inicial:</b> {imc(altura, peso_i)}</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='font-size:14px; color:gray;'><b>IMC inicial: --</b></p>", unsafe_allow_html=True)
                
        elif key == "pesoFinal":
            altura = data.get("altura") or 0
            peso_i = data.get("pesoInicial") or 0
            peso_f = data.get("pesoFinal") or 0

            if altura > 0 and peso_f > 0:
                st.markdown(f"<p style='font-size:14px; color:gray;'><b>IMC final:</b> {imc(altura, peso_f)}</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='font-size:14px; color:gray;'><b>IMC final: --</b></p>", unsafe_allow_html=True)
            
            if peso_i > 0 and peso_f > 0:   
                st.markdown(f"<p style='font-size:14px; color:gray;'><b>Aumento ponderal:</b> {aumento_ponderal(peso_i, peso_f)} kg</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='font-size:14px; color:gray;'><b>Aumento ponderal: --</b></p>", unsafe_allow_html=True)

        elif key == "fl":
            st.space("medium")
            dpb, pc, pAB, fl = data.get("dpb") or 0, data.get("pc") or 0, data.get("pAB") or 0, data.get("fl") or 0
            if dpb != 0 and pc != 0 and pAB != 0 and fl != 0: 
                st.markdown(f"<p style='font-size:15px; color:gray;'><b>Peso fetal estimado (Hadlock):</b> {hadlock_formula(dpb, pAB, pc, fl)} g</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='font-size:15px; color:gray;'><b>Peso fetal estimado (Hadlock): --</b></p>", unsafe_allow_html=True)

    return value


def should_be_rendered(metadata: dict, input_data: dict) -> bool:
    """
    Conditionaly display of context-dependent variables: Returns TRUE if:
    - If the field is not context-dependent
    - If the field is context-dependent and the trigger condition is verified
    """
    if "depends_on" not in metadata or not metadata["depends_on"]:
        return True

    # Get all info about the dependency
    dependency = metadata["depends_on"]
    field = dependency.get("field")
    condition = dependency.get("condition")
    trigger_val = dependency.get("trigger_value")

    # Get current value of parent field
    current_val = input_data.get(field)

    # If the parent field still does not have a value the dependent field is not displayed
    if current_val is None:

        return False

    try:
        if isinstance(trigger_val, (int, float)) and isinstance(current_val, str) and current_val.isdigit():
            current_val = type(trigger_val)(current_val)
    except (ValueError, TypeError):
        pass

    # Triggerin conditions evaluation
    if condition in ("==", "eq"):
        return current_val == trigger_val
    elif condition in ("!=", "ne"):
        return current_val != trigger_val
    elif condition in (">", "gt"):
        try:
            return current_val > trigger_val
        except TypeError:
            return False
    elif condition in ("<", "lt"):
        try:
            return current_val < trigger_val
        except TypeError:
            return False
    elif condition == "in":
        if isinstance(trigger_val, (list, tuple, set)):
            return current_val in trigger_val
        return False
    
    return True



def render_widgets_for_group(group_name: str):
    """
    # Renders all widgets of the same page/screen (specified as group in the UI metadata)
    """
    model = st.session_state["sessao"]["metadata"]["model"]
    model_specs = get_model_specs(model)
    current_tabular_data = st.session_state["sessao"]["raw_input"]["tabular"]

    group = UI_ARCHITECTURE.get(group_name, {})
    sections = group.get("sections", {})

    rendered_sections = set()

    def _render_section_header(section_name: str):
        if section_name and section_name not in rendered_sections:
            st.space("small")
            st.markdown(f"#### {section_name}")
            rendered_sections.add(section_name)

            section = sections.get(section_name, {})
            caption = section.get("caption")
            if caption:
                st.write(caption)

    # Render tabular fields
    for key, metadata in model_specs.ui_inputs.get("tabular", {}).items():
        if metadata.get("group") != group_name:
           continue

          
        widget_key = f"widget_{key}" 

        if should_be_rendered(metadata, current_tabular_data):
            # if the widget
            # mas no dicionário tem o valor do fallback, limpamos para forçar a aplicação do default.
            if widget_key not in st.session_state:
                fallback_val = metadata.get("depends_on", {}).get("fallback")
                # Se o valor atual no dicionário é igual ao fallback, limpamos para None
                if fallback_val is not None and current_tabular_data.get(key) == fallback_val:
                    current_tabular_data[key] = None

            _render_section_header(metadata.get("section"))
            render_widget(key)
        
        else: # Se NÃO deve ser renderizado
            if "depends_on" in metadata and "fallback" in metadata["depends_on"]:
                current_tabular_data[key] = metadata["depends_on"]["fallback"]

            if widget_key in st.session_state:
                del st.session_state[widget_key]

    # 2. Render Image Inputs
    for key, metadata in model_specs.ui_inputs.get("images", {}).items():
        if metadata.get("group") == group_name:
            if should_be_rendered(metadata, current_tabular_data):
                _render_section_header(metadata.get("section"))
                render_widget(key)


def display_prediction(prediction):
    """
    Displays the prediction according to the predifined prediction outputs:
    - "prediction": predicted class
    - "y_proba_0": probability of class predicted being 0
    - "y_proba_1" probability of class predicted being 1

    """
    

    predicted_class = prediction.get("predicted_class")
    class_0_proba = prediction.get("class_0_proba")
    class_1_proba = prediction.get("class_1_proba")
    class_0_proba = round(class_0_proba * 100, 2)
    class_1_proba = round(class_1_proba * 100, 2)

    tipo_de_parto = ''
    outro = ''
    if predicted_class == 0:
        tipo_de_parto = "Vaginal"
        outro = "Cesariana"
    else:
        tipo_de_parto = "Cesariana"
        outro = "Vaginal"

    probabilidades = pd.DataFrame({
        tipo_de_parto: [f"{max(class_0_proba, class_1_proba)} %", tipo_de_parto],
        outro: [f"{min(class_0_proba, class_1_proba)} %", outro]
    })

    st.markdown(f"""
        <div style="background-color: #edf7ee; border: 2px solid #a8d5aa; padding: 20px; border-radius: 10px;">
            <h4 style="margin-bottom: 20px;">{tipo_de_parto}</h2>
            <p style="font-size: 18px"><strong>Probabilidade de cada tipo de parto:</strong></p>
            <table style="width: 100%; text-align: center; border-collapse: collapse;">
                <tr>
                    <th style="border: 1px solid #a8d5aa; padding: 8px;">{tipo_de_parto}</th>
                    <th style="border: 1px solid #a8d5aa; padding: 8px;">{outro}</th>
                </tr>
                <tr>
                    <td style="border: 1px solid #a8d5aa; padding: 8px;">{max(class_0_proba, class_1_proba)} %</td>
                    <td style="border: 1px solid #a8d5aa; padding: 8px;">{min(class_0_proba, class_1_proba)} %</td>
                </tr>
            </table>
        </div>
    """, unsafe_allow_html=True)

    return

def display_explanation(explanation: dict | None) -> None:
    """
    Displays the explanation prediction according
    """

    if not explanation["success"]: # quando não existe explicação proque o modelo não tem explicabilidade associada ainda

        # a ui mostra so uma mensagem a dizer que o modelo nao tem explicabilidade ainda
        text = str(f"A **explicação** desta previsão ainda não está disponível nesta versão da ferramenta." 
                   f"\n\n A explicabilidade para este modelo de previsão encontra-se em desenvolvimento.")

        with st.container(border=True):
            st.markdown(text)


    else: 

        # caso se queira mostrar as 4 explicações fica aqui a visualização em tabs (é so descomentar o codigo)
        tab1, tab2, tab3, tab4 = st.tabs(["📈 Waterfall", "📊 Tabela", "📝 Conceitos", "📈 Tornado"])

        with tab1:
            technical_explanation(explanation)

        with tab2:
            narrative_explanation(explanation)

        with tab3:
            clinical_domain_explanation(explanation)

        with tab4:
            tornado_explanation(explanation)



    
def render_step_tracker(current_step):
    # Define your 4 steps here
    steps = ["1. Dados maternos", "2. Gravidez atual", "3. Histórico", "4. Indução"]
    
    # Custom CSS to mimic your image (pill shapes, connecting lines, colors)
    css_style = """ 
    <style>
    .tracker-container {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        font-family: sans-serif;
        margin-bottom: 20px;
    }
    .step-pill {
        padding: 8px 16px;
        border-radius: 24px;
        font-size: 11px;
        font-weight: 500;
        text-align: center;
        white-space: nowrap;
    }
    .active-pill {
        background-color: #333333; /* Bright Blue */
        color: white;
    }

    .inactive-pill {
        background-color: #f0f2f5; /* Soft light blue/grey */
        color: #8c8c8c;
    }
    .line-separator {
        flex-grow: 0;
        width: 40px;
        height: 2px;
        background-color: #d9d9d9;
        margin: 0 5px;
    }
    </style>
    """
    st.markdown(css_style, unsafe_allow_html=True)
    
    # Generate the HTML dynamically based on current_step_idx
    html_content = '<div class="tracker-container">'
    
    for i, name in enumerate(steps):
        # Determine if active or inactive
        pill_class = "active-pill" if i == current_step else "inactive-pill"
        html_content += f'<div class="step-pill {pill_class}">{name}</div>'
        
        # Add a connecting line between pills (but not after the last one)
        if i < len(steps) - 1:
            html_content += '<div class="line-separator"></div>'
            
    html_content += '</div>'
    
    st.markdown(html_content, unsafe_allow_html=True)

def get_model_options():
    model_options = {}

    for key, model_specs in MODEL_REGISTRY.items():
        model_options[key] = model_specs.ui_terminology

    return model_options


# PASSAR ISTO PARA AS MODEL SPECS OU ALTERAR AQUI (isto é so para adicionar na sidebar para os modelos):
model_name = {
    "rf_13_tabular": "Random Forest 13T",
    "multimodal_medvit": "Multimodal (MedViTV2)",
}

model_captions = {
    "rf_13_tabular": "⚡ Modelo de previsão default. Usar para uma previsão mais rápida.",
    "multimodal_medvit": "🩺 Modelo que combina mais dados clínicos com ultrasons do 3º trimestre. Usar para uma previsão mais completa."
}

classifiers = {
    "rf_13_tabular": "Árvores de decisão",
    "multimodal_medvit": "Regressão logística + Transformer de Visão"
}

dados = {
            "rf_13_tabular": f"\n\n **13 variáveis clínicas** incluíndo: \n\n - Fatores maternos - idade, peso, altura \n\n - Estado da gravidez - idade gestacional, complicações na gravidez (diabetes gestacional) \n\n - Antecedentes obstétricos - paridade, cesariana anterior \n\n - Preparação para indução - índice de bishop, médodo de indução (Misoprostol) e motivo de indução (Patologia fetal)",
            "multimodal_medvit": f"\n\n **25 variáveis clínicas + 3 imagens de ultrasons** incluíndo: \n\n - Fatores maternos - idade, peso, altura e patologias prévias \n\n - Antecedentes obstétricos - gestações, paridade, partos pré termo, tipo de parto anterior \n\n - Estado da gravidez - idade gestacional, peso fetal estimado \n\n - Preparação para indução - índice de bishop, médodo e motivo de indução \n\n - Ecografias do 3ºT de três planos fetais (Abdómen, Cabeça, Femur)",
        }

def render_sidebar_model_menu(
        model_name=model_name, 
        captions=model_captions, 
        classifiers=classifiers,
        dados=dados
        ):
    """Renders a model switcher in the sidebar and handles data migration on change."""
    session = st.session_state.get("sessao")
    if not session:
        return

    with st.sidebar:
        st.markdown("## Modelo de previsão")
        
        current_model = session["metadata"]["model"]
        
        model_options = get_model_options()

        # Reverse mapping to get keys back
        inverse_options = {v: k for k, v in model_options.items()}
        
        with st.container(border=True):
            selected_label = st.radio(
                "Previsão à base de:",
                options=list(model_options.values()),
                index=list(model_options.keys()).index(current_model),
                #label_visibility="collapsed"
            )
        
        selected_model_key = inverse_options[selected_label]

        # para o caso de não existir caption definida para o modelo
        if captions[selected_model_key]:
            st.caption(captions[selected_model_key])

        if model_name[selected_model_key] or classifiers[selected_model_key] or dados[selected_model_key]:
            # como estas coisas nao estao nas specs do modelo este expander so aparece se definirem aqui estes detalhes
            st.space("small")
            with st.expander("Sobre este modelo", expanded=False):
        
                model_specs = get_model_specs(current_model)    
                st.markdown(f"**{model_name[selected_model_key]}**")  
                
                st.markdown(f"**Método de previsão:** {classifiers[selected_model_key]}")

                st.markdown(f"**Dados utilizados:** {dados[selected_model_key]}")
        
        # 1. Determine Modality (Your logic polished)
        ui_inputs = model_specs.ui_inputs
        has_tabular = len(ui_inputs.get("tabular", {})) > 0
        has_images = len(ui_inputs.get("images", {})) > 0
        
        if has_tabular and has_images:
            modality = ["Tabela de dados clínicos 📊" , "Imagens médicas 🖼️"]
        elif has_images:
            modality = ["Imagens médicas 🖼️"]
        else:
            modality = ["Tabela de dados clínicos 📊"]

        # 3. Collapsible sections for detailed clinical features
        # Clinicians want to know exactly what variables are driving the prediction

        #st.markdown(f"**Dados utilizados:**")
        #if has_tabular:
           # with st.expander("📊 Tabela de dados Clínicos", expanded=False):
               # for key, meta in ui_inputs.get("tabular", {}).items():
                    # Display the human-readable label instead of the dictionary key
                 #   label = meta.get("label", key)
                   # st.markdown(f"- {label}")
                    
        #if has_images:
            #with st.expander("🖼️ Imagens médicas", expanded=False):
                   # st.write("Ecografias dos seguintes planos anatómicos:")
                   # for key, meta in ui_inputs.get("images", {}).items():
                   #     label = meta.get("label", key)
                   #     st.markdown(f"- 📷 {label}")
        
        # If the user selects a different model, run migration
        if selected_model_key != current_model:
            migrate_model_session(selected_model_key)


