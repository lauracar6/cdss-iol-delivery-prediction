import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter
from sklearn.pipeline import Pipeline
import streamlit as st



CLINICAL_DOMAINS = {
    "Características maternas": [
        "Idade",
        "PesoInicial",
        "PesoFinal",
        "Altura",
        "PatologiasPrevias_19-obesidade",
    ],

    "Histórico obstétrico": [
        "Paridade",
        "PartoTermoAnterior",
        "CSAAnt",
    ],

    "Estado da gravidez": [
        "IG",
        "ComplicGravidez_2-DG",
    ],

    "Detalhes para a indução": [
        "Bishop",
        "MetodoInd_1-misoprostol",
        "MotivoInd_11-patologiafetal",
    ],
}

GROUPED_FEATURES_DOMAIN = {
    feature: group
    for group, features in CLINICAL_DOMAINS.items()
    for feature in features
}

CLEAN_FEATURE_LABELS = {
    "Paridade":"Paridade",
    "PartoTermoAnterior": "Nº de partos termo anteriores",
    "Idade":"Idade",
    "PesoInicial": "Peso inicial",
    "PesoFinal": "Peso final",
    "Altura": "Altura",
    "IG": "Idade gestacional",
    "Bishop": "índice de bishop",
    "MetodoInd_1-misoprostol": "Método de indução (misoprostol)", 
    "ComplicGravidez_2-DG": "Diabetes gestacional", 
    "PatologiasPrevias_19-obesidade": "IMC superior a 30", 
    "MotivoInd_11-patologiafetal": "Motivo de indução (patologia fetal)", 
    "CSAAnt": "Cesariana anterior"
}

def clinical_domains_contributions(ordered_feature_contributions):
    """
    Organizes feature contributions per clinical domain and computes the summed clinical
    domain contributions.

    :param list ordered_feature_contributions: List containing all the feature contributions 
    information (shap_value, feature_name, direction) ordered by contribution magnitude.
    """
    
    clinical_domains = {}

    for domain in CLINICAL_DOMAINS:
        clinical_domains[domain] = {
            "domain": domain,
            "total_shap": 0.0,
            "total_abs_shap": 0.0,
            "features": [],
        }
    
    for feature in ordered_feature_contributions:

        domain = GROUPED_FEATURES_DOMAIN.get(feature["feature"])

        if domain is None:
            continue

        clinical_domains[domain]["features"].append(feature)

        clinical_domains[domain]["total_shap"] += feature["shap_value"]
        clinical_domains[domain]["total_abs_shap"] += abs(feature["shap_value"])

    for domain in clinical_domains.values():
        domain["features"].sort(
            key=lambda x: x["shap_abs_value"],
            reverse=True,
        )

    # Order domains by most contributing to less
    clinical_domains = sorted(
        clinical_domains.values(),
        key=lambda x: x["total_abs_shap"],
        reverse=True,
    )

    return clinical_domains


def domain_contribution_bar(domain):
    """
    Plots a standalone horizontal bar starting from zero moving right.
    Direction and magnitude of contribution are represented by color and by size
    """
    domain_name = domain["domain"]
    num_factors = len(domain["features"])
    value = domain["total_shap"] * 100
    
    # Take the absolute value so the bar always grows from left to right
    bar_width = abs(value)

    # Determine coloring and clean string formatting based on original sign
    if value >= 0:
        color = "#7fdb71"  # Muted Green
        text_str = f"+{value:.1f}% ({num_factors} fatores)"
    else:
        color = "#f07a7a"  # Muted Red
        text_str = f"{value:.1f}% ({num_factors} fatores)"

    # Setup the figure canvas
    fig, ax = plt.subplots(figsize=(7, 0.7))

    # Draw the horizontal bar (always positive width, growing right)
    ax.barh(y=0, width=bar_width, left=0, height=0.5, color=color)
    
    # Left baseline reference line where all bars start
    ax.axvline(0, color="gray", linewidth=1, linestyle="-", alpha=0.7)

    # Add text label immediately in front of the bar on the right side
    # A small fixed padding prevents text colliding with the edge of the bar
    offset = max(bar_width * 0.05, 1.5)
    text_x = bar_width + offset

    ax.text(
        x=text_x,
        y=0,
        s=text_str,
        va="center",
        ha="left",  # Always align text to the right of its coordinate
        fontsize=10,
        color=color,
        fontweight="bold"
    )

    # Clean up the axis borders & ticks entirely for UI injection
    ax.set_yticks([])
    ax.set_xticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Set limits starting from 0 extending rightward to prevent cutoff text
    max_range = max(bar_width * 1.5, 30)  # Safe buffer zone for text length
    ax.set_xlim(0, max_range)

    plt.tight_layout(pad=1.5)
    
    return fig, domain_name

def delivery_mode(predicted_class):

    PREDICTION_MAPPING = {
        0: "vaginal",
        1: "cesariana",
    } 

    return PREDICTION_MAPPING[predicted_class]

def feature_contributions_table(ordered_feature_contributions, predicted_class, base_value, n_top = 6):
    """
    Creates pandas dataframe of the individual contributions in magnitude's descending order.

    :param list ordered_feature_contributions: List containing all the feature contributions 
    information (shap_value, feature_name, direction) ordered by contribution magnitude.
    :param int predicted_class: Predicted class by the model.
    :param float base_value: Baseline predicted probability for the predicted class across the background dataset.
    """

    df = pd.DataFrame({
        "Fator": [d["feature_label"] for d in ordered_feature_contributions],
        "Valor da paciente": [d["input_value"] for d in ordered_feature_contributions],
        "Impacto": [f"{d['shap_value'] * 100:.2f} %" for d in ordered_feature_contributions],
            #"shap_abs": [d["shap_abs_value"] for d in top_features[:n_top]],
    }) 

    legenda = str(f"Impacto na probabilidade de parto por {delivery_mode(predicted_class)}, relativa à baseline de risco de {(base_value * 100):.2f} %")

    return df, legenda

def custom_shap_waterfall(
    explanation,
    predicted_class,
    max_display: int = 10, 
    feature_mapping = CLEAN_FEATURE_LABELS,
):
    """
    Plots a waterfall plot based on shap's feature contribution accumulation from the baseline
    to the predicted probability (for the predicted class!)

    :param dict explanation: SHAP Explanation object.
    :param int predicted_class: Predicted class by the model.
    :param int max_display: (default = 10) Sets the number of individual feature's bars plotted. If max_display < 
    number of model's input features, the remaining feature's contributions will be grouped in onw bar.
    :param dict feature_mapping: Mapping of model's feature labels to clean labels do be displayed on the plot.
    """

    if feature_mapping is None:
        feature_mapping = {}

    # Wrapping label text on the y-axis
    def wrap_label(text, max_chars=40):
        if len(text) <= max_chars:
            return text
        
        # For labels with more than 1 feature
        if text.startswith("[") and text.endswith("]"):
            inner = text[1:-1]
            parts = [p.strip() for p in inner.split(",")]
            lines = []
            current_line = []
            for p in parts:
                if len(", ".join(current_line + [p])) > max_chars and current_line:
                    lines.append(", ".join(current_line) + ",")
                    current_line = [p]
                else:
                    current_line.append(p)
            if current_line:
                lines.append(", ".join(current_line))
            return "[" + "\n  ".join(lines) + "]"
        
        # For labels of individual features
        words = text.split(" ")
        lines = []
        current_line = []
        for word in words:
            if len(" ".join(current_line + [word])) > max_chars and current_line:
                lines.append(" ".join(current_line))
                current_line = [word]
            else:
                current_line.append(word)
        if current_line:
            lines.append(" ".join(current_line))
        return "\n".join(lines)

    # Generate clean labels dynamically for every feature name
    clean_labels = [
        feature_mapping.get(name, name.replace("_", " ").title())
        for name in explanation.feature_names
    ]

    # Build the structured DataFrame cleanly
    df = pd.DataFrame({
        "feature": explanation.feature_names,
        "feature_label": clean_labels,  # Injected the mapped labels array
        "value": explanation.data,      # Raw user/input values
        "shap": explanation.values,
    })
    
    df["abs"] = df["shap"].abs()
  

    # Top features by impact, keeping the highest at the top (ascending=True for bottom-to-top rendering)
    df = df.sort_values("abs", ascending=False)
    top_df = df.head(max_display).copy()
    remaining_df = df.iloc[max_display:]

    if not remaining_df.empty:
        # Extrai os labels limpos dos fatores em falta para gerar o texto [Fator1, Fator2...]
        missing_features_list = remaining_df["feature_label"].tolist()
        others_label = f"[{', '.join(missing_features_list)}]"
        
        others_row = pd.DataFrame([{
            "feature": "others",
            "feature_label": others_label,
            "value": None,
            "shap": remaining_df["shap"].sum(),
            "abs": remaining_df["shap"].abs().sum()
        }])
        df = pd.concat([top_df, others_row], ignore_index=True)
    else:
        df = top_df

    df = df.iloc[::-1]

    base_value = float(explanation.base_values)
    current = base_value

    total_lines = sum(wrap_label(str(row.feature_label)).count('\n') + 1 for row in df.itertuples())
    fig_height = max(2.8, total_lines)
    fig, ax = plt.subplots(figsize=(8, fig_height))

    spacing = 0.5
    y_positions = np.arange(len(df)) * spacing

    # Fixed: uses row.feature_label and matches row.value (instead of input_value)
    y_labels = []
    for row in df.itertuples():
        wrapped = wrap_label(str(row.feature_label))
        if row.value is not None and str(row.value) != "None" and row.feature != "others":
            # Converte o valor para string ou int para validação
            val_str = str(row.value).strip()
            if val_str in ["0", "0.0"]:
                display_value = "Não"
            elif val_str in ["1", "1.0"]:
                display_value = "Sim"
            else:
                display_value = row.value

            y_labels.append(f"{wrapped}: {display_value}")
        else:
            y_labels.append(wrapped)

    for y, row in zip(y_positions, df.itertuples()):
        start = current
        end = current + row.shap
        width = end - start # se a width deu positivo signifca que essa feature contribui para o aumento da prob

        color = "#89e372" if width >= 0 else "#e16d6d"

        arrow_size = max(abs(width) * 0.08, 0.01) #

        body_width = width - arrow_size if width > 0 else width + arrow_size

        ax.barh(
            y=y,
            width=body_width,
            left=start,
            height=0.4,
            color=color,
            #edgecolor="black",
        )

        if width >= 0:
            triangle = Polygon(
                [
                    (end, y),
                    (end - arrow_size, y + 0.2),
                    (end - arrow_size, y - 0.2),
                ],
                closed=True,
                facecolor=color,
                #edgecolor="black",
                linewidth=1,
            )

        else:

            triangle = Polygon(
                [
                    (end, y),
                    (end + arrow_size, y + 0.2),
                    (end + arrow_size, y - 0.2),
                ],
                closed=True,
                facecolor=color,
                #edgecolor="black",
                linewidth=1,
            )

        ax.add_patch(triangle)

        # SHAP value
        offset = max(abs(width) * 0.02, 0.003)
        inside_tresh = 0.04

        if abs(width) > inside_tresh:

            ax.text(
                start + width/2,
                y,
                f"{((row.shap)*100):+.3f}",
                ha="center",
                va="center",
                fontsize=9,
                color="white",
                fontweight="bold",
            )
       
        else:

            if width >= 0:

                x = end + offset
                align = "left"

                ax.text(
                    x,
                    y,
                    f"{((row.shap)*100):+.3f}",
                    va="center",
                    ha=align,
                    fontsize=9,
                    color=color
                )

            else:

                x = end - offset
                align = "right"

                ax.text(
                    x,
                    y,
                    f"{((row.shap)*100):-.3f}",
                    va="center",
                    ha=align,
                    fontsize=9,
                    color=color
                )

       

        current = end

    ax.set_yticks(y_positions)
    ax.set_yticklabels(y_labels, fontsize=10)

    ax.tick_params(
        axis="y",
        pad=10,
    )
   
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


    ax.axvline(base_value, color="gray", linestyle="--",  linewidth=1.0, zorder=0)

    ax.axvline(current, color="gray", linewidth=1.0, zorder=0)

    y_top = y_positions[-1] + 0.45   # um pouco acima da última barra

    ax.text(
        base_value,
        y_top,
        f"Probabilidade\nmédia\n{(base_value * 100):.2f}%",
        ha="center",
        va="bottom",
        fontsize=9,
    )

    ax.text(
        current,
        y_top,
        f"Probabilidade\nprevista\n{(current *100):.2f}%",
        ha="center",
        va="bottom",
        fontsize=8.5,
        fontweight="bold",
    )
   
    last_rows = df.tail(2)
    legend_loc = "lower right"
    if (last_rows["shap"] > 0.15).any():
        legend_loc = "lower left"


    positive_patch = Patch(
        facecolor="#7fdb71",
        label="Aumenta probabilidade"
    )

    negative_patch = Patch(
        facecolor="#f07a7a",
        label="Diminui probabilidade"
    )

    ax.legend(
    handles=[
            positive_patch,
            negative_patch,
            #base_line,
            #pred_line,
        ],
        loc=legend_loc,
        frameon=True,
        fontsize=9,
    )

    #ax.set_xlabel(
     #   f"Contribuição para a probabilidade de parto {PREDICTION_MAPPING[predicted_class]}, relativo à baseline {(base_value * 100):.2f} %",
      #  fontsize=10,
       # fontstyle= "italic",
        #fontweight="bold",
    #)
   
    caption = str(f"Impacto na probabilidade de parto {delivery_mode(predicted_class)}, relativa à baseline de risco de {(base_value * 100):.2f} %")

    xmin, xmax = ax.get_xlim()
    padding = (xmax - xmin) * 0.15   # 15% de margem
    ax.set_xlim(
        xmin - padding,
        xmax + padding * 0.3
    )

    ax.xaxis.set_major_formatter(
        FuncFormatter(lambda x, pos: f"{x*100:.0f}%")
    )

    plt.tight_layout()

    return fig, caption 

def tornado_plot_per_domain(
    features,
    concept_name,
    predicted_class,
):
    df = pd.DataFrame(features)
    
    
    fig_height = max(2.8, len(df) * 0.5)
    fig, ax = plt.subplots(figsize=(8, fig_height))


    spacing = 0.5
    y_positions = np.arange(len(df)) * spacing

    # Generate labels matching the rows
    # Mapeamento de 0/1 para Não/Sim mantendo a flexibilidade
    y_labels = []
    for row in df.itertuples():
        val_str = str(row.input_value).strip()
        if val_str in ["0", "0.0"]:
            display_value = "Não"
        elif val_str in ["1", "1.0"]:
            display_value = "Sim"
        else:
            display_value = row.input_value
            
        y_labels.append(f"{row.feature_label}: {display_value}")

    # Draw bars
    for y, row in zip(y_positions, df.itertuples()):
        width = row.shap_value
        color = "#7fdb71" if width >= 0 else "#f07a7a"

        ax.barh(
            y=y,
            width=width,
            left=0,
            height=0.4,
            color=color,
        )
      
        # SHAP value label placement logic
        offset = max(abs(width) * 0.03, 0.005)
        inside_threshold = 0.03

        if abs(width) >= inside_threshold:
            ax.text(
                width / 2,
                y,
                f"{width*100:+.1f}%",
                ha="center",
                va="center",
                color="white",
                fontsize=9,
                fontweight="bold",
            )
        else:
            if width >= 0:
                ax.text(
                    width + offset,
                    y,
                    f"{width*100:+.1f}%",
                    ha="left",
                    va="center",
                    fontsize=9,
                    color=color,
                )
            else:
                ax.text(
                    width - offset,
                    y,
                    f"{width*100:+.1f}%",
                    ha="right",
                    va="center",
                    fontsize=9,
                    color=color,
                )

    ax.axvline(0, color="gray", linewidth=1)

    # Invert y-axis to plot greated bars on the top
    ax.invert_yaxis()  

    # Apply ticks AFTER inverting to maintain perfect alignment
    ax.set_yticks(y_positions)
    ax.set_yticklabels(y_labels, fontsize=10)

    ax.tick_params(axis="y", pad=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Legend setups
    legend_loc = "lower right"
    positive_patch = Patch(facecolor="#7fdb71", label="Aumenta probabilidade")
    negative_patch = Patch(facecolor="#f07a7a", label="Diminui probabilidade")

    ax.legend(
        handles=[positive_patch, negative_patch],
        loc=legend_loc,
        frameon=True,
        fontsize=9,
    )

    caption = (
        f"Impacto dos fatores de {concept_name} "
        f"na probabilidade de parto por "
        f"{delivery_mode(predicted_class)}"
    )

    # Add safe horizontal padding for text tags
    xmin, xmax = ax.get_xlim()
    padding = (xmax - xmin) * 0.15
    ax.set_xlim(xmin - padding, xmax + padding)

    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: f"{x*100:.0f}%"))
    plt.tight_layout()

    return fig, caption

# Mapping of model's feature labels for the natural language text
FEATURE_LABEL_TEXT = {
    "Paridade": "paridade",
    "PartoTermoAnterior": "número de partos a termo anteriores",
    "Idade": "idade materna",
    "PesoInicial": "peso no início da gestação",
    "PesoFinal": "peso no fim da gestação",
    "Altura": "altura",
    "IG": "idade gestacional",
    "Bishop": "índice bishop",
    "MetodoInd_1-misoprostol": "método de indução", 
    "ComplicGravidez_2-DG": "complicações na gravidez", 
    "PatologiasPrevias_19-obesidade": "patologias prévias", 
    "MotivoInd_11-patologiafetal": "motivo de indução", 
    "CSAAnt": "cesariana anterior"
}

# Mapping of categorical feature values to text
FEATURE_VALUES = {

    "MetodoInd_1-misoprostol": {
        0: "sem indução com misoprostol",
        1: "indução com misoprostol",
    },

    "ComplicGravidez_2-DG": {
        0: "ausência de diabetes gestacional",
        1: "presença de diabetes gestacional",
    },

    "PatologiasPrevias_19-obesidade": {
        0: "imc é inferior a 30",
        1: "imc é superior a 30",
    },

    "MotivoInd_11-patologiafetal": {
        0: "indução não foi por motivo de patologia fetal",
        1: "indução por motivo de patologia fetal",
    },
    
    "CSAAnt": {
        0: "ausência de cesariana anterior",
        1: "existência de cesariana anterior",
    },

}

def describe_feature(feature, value):

    if feature in FEATURE_VALUES:
        return FEATURE_VALUES[feature][value]

    return f"{FEATURE_LABEL_TEXT[feature]} ({value})"

def join_list(items):

    if len(items) == 0:
        return ""

    if len(items) == 1:
        return items[0]

    if len(items) == 2:
        return f"{items[0]} e {items[1]}"

    return ", ".join(items[:-1]) + f" e {items[-1]}"

def natural_language_text(top_features, predicted_class, n_top_simple = 3, n_top = 5):

    positive_contributors = []
    negative_contributors = []
    all_contributors = []

    for item in top_features[:n_top_simple]:

        description = describe_feature(
            item["feature"],
            item["input_value"],
        )

        all_contributors.append(f"**{description}**")

    for item in top_features[:n_top]:

        description = describe_feature(
            item["feature"],
            item["input_value"],
        )

        if item["shap_value"] > 0:
            positive_contributors.append(f"- **{description}**")
        else:
            negative_contributors.append(f"- **{description}**")

    simple_text = (
        f"O modelo atribuiu maior importância a {join_list(all_contributors)} "
        f"para prever um parto por {delivery_mode(predicted_class)}."
    )

    more_text = ""

    if positive_contributors:
        more_text += (
            "Entre os fatores que mais aumentaram a probabilidade destacam-se:\n\n"
            + "\n".join(positive_contributors)
        )

    if negative_contributors:
        more_text += (
            "\n\nPelo contrário, os seguintes fatores diminuíram essa probabilidade:\n\n"
            + "\n".join(negative_contributors)
        )

    return simple_text, more_text

def tornado_plot(
    top_features,
    predicted_class,
    base_value
):
    df = pd.DataFrame(top_features)

    fig_height = max(2.8, len(df) * 0.5)
    fig, ax = plt.subplots(figsize=(8, fig_height))


    spacing = 0.5
    y_positions = np.arange(len(df)) * spacing

    # Labels
    y_labels = []

    for row in df.itertuples():

        val_str = str(row.input_value).strip()

        if val_str in ["0", "0.0"]:
            display_value = "Não"
        elif val_str in ["1", "1.0"]:
            display_value = "Sim"
        else:
            display_value = row.input_value

        y_labels.append(
            f"{row.feature_label}: {display_value}"
        )

    # Draw bars
    for y, row in zip(y_positions, df.itertuples()):

        width = row.shap_value

        color = "#7fdb71" if width >= 0 else "#f07a7a"

        ax.barh(
            y=y,
            width=width,
            left=0,
            height=0.4,
            color=color,
        )

        # SHAP value
        offset = max(abs(width) * 0.03, 0.005)
        inside_threshold = 0.03

        if abs(width) >= inside_threshold:

            ax.text(
                width / 2,
                y,
                f"{width * 100:+.1f}%",
                ha="center",
                va="center",
                color="white",
                fontsize=9,
                fontweight="bold",
            )

        else:

            if width >= 0:

                ax.text(
                    width + offset,
                    y,
                    f"{width * 100:+.1f}%",
                    ha="left",
                    va="center",
                    fontsize=9,
                    color=color,
                )

            else:

                ax.text(
                    width - offset,
                    y,
                    f"{width * 100:+.1f}%",
                    ha="right",
                    va="center",
                    fontsize=9,
                    color=color,
                )

    # Set axis
    ax.axvline(0,color="gray",linewidth=1,)

    ax.set_yticks(y_positions)
    ax.set_yticklabels(y_labels,fontsize=10,)

    ax.tick_params(axis="y",pad=10,)

    ax.invert_yaxis()

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Set captions
    positive_patch = Patch(
        facecolor="#7fdb71",
        label="Aumenta probabilidade",
    )

    negative_patch = Patch(
        facecolor="#f07a7a",
        label="Diminui probabilidade",
    )

    ax.legend(
        handles=[
            positive_patch,
            negative_patch,
        ],
        loc="lower right",
        frameon=True,
        fontsize=9,
    )

    # Set labels
    ax.set_xlabel(
        f"Contribuição para a probabilidade de parto "
        f"{delivery_mode(predicted_class)}",
        fontsize=10,
    )

    caption = (
        f"Impacto dos fatores na probabilidade de parto "
        f"{delivery_mode(predicted_class)}"
        f", relativa à baseline de {(base_value * 100):.2f} %"
    )

    # Padding
    xmin, xmax = ax.get_xlim()

    padding = (xmax - xmin) * 0.15

    ax.set_xlim(
        xmin - padding,
        xmax + padding,
    )


    # Percentage axis
    ax.xaxis.set_major_formatter(
        FuncFormatter(lambda x, pos: f"{x * 100:.0f}%")
    )

    plt.tight_layout()

    return fig, caption


def technical_explanation(explanation: dict | None):

    predicted_class = explanation["predicted_class"]
    raw_explanation = explanation["shap_raw_explanation"]
    
    fig, fig_caption = custom_shap_waterfall(raw_explanation,predicted_class)

    st.markdown(
        f"<p style='font-size:18px; font-weight:bold; text-align:center;'>Contribuição dos fatores</p>",
        unsafe_allow_html=True,
    )

    if fig is not None:
        fig.set_size_inches(8, 4)   # largura, altura
        st.pyplot(fig, clear_figure=False)
        st.markdown(
            f"<p style='font-size:16px; font-weight:bold; font-style:italic; text-align:center;'>{fig_caption}</p>",
            unsafe_allow_html=True,
        )

def narrative_explanation(explanation: dict | None):

    predicted_class = explanation["predicted_class"]
    base_value = explanation["base_value"]
    top_features = explanation["top_features"]

    table, table_caption = feature_contributions_table(top_features,predicted_class, base_value)
    simple_text, more_text = natural_language_text(top_features, predicted_class) 

    with st.container(border=True):
        st.markdown(simple_text)
        st.markdown(more_text)

        st.markdown(
            f"<p style='font-size:18px; font-weight:bold; text-align:center;'>Contribuição dos fatores</p>",
            unsafe_allow_html=True,
        )

        mostrar_tudo = st.toggle("Mostrar tabela completa")

        if mostrar_tudo:
            df = table
        else:
            df = table.head(5)
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown(
            f"<p style='font-size:16px; font-weight:bold; font-style:italic; text-align:center;'>{table_caption}</p>",
            unsafe_allow_html=True,
        )



def clinical_domain_explanation(explanation: dict | None):

    predicted_class = explanation["predicted_class"]
    top_features = explanation["top_features"]

    clinical_domains = clinical_domains_contributions(top_features)
    domain_explanations = {}

    for domain in clinical_domains:

        bar_fig, domain_name = domain_contribution_bar(domain)

        tornado_fig, tornado_caption = tornado_plot_per_domain(domain["features"],domain_name,predicted_class,)

        domain_explanations[domain_name] = {
            "total_shap": domain["total_shap"],
            "total_abs_shap": domain["total_abs_shap"],
            "bar": bar_fig,  # Storing just the matplotlib figure canvas now
            "tornado": tornado_fig,
            "tornado_caption": tornado_caption,
        }

    st.markdown(
            f"<p style='font-size:18px; font-weight:bold; text-align:center;'>Contribuição de fatores</p>",
            unsafe_allow_html=True,
        )

    for domain_name, data in domain_explanations.items():
        # Render the Concept Title
        with st.container(border=True):

            st.markdown(
                f"""
                <p style="
                    font-size:20px;
                    font-weight:bold;
                    margin-bottom:0px;
                ">
                    {domain_name}
                </p>
                """,
                unsafe_allow_html=True,
            )

            st.pyplot(data["bar"], clear_figure=False)

            with st.expander("Ver fatores"):
                st.pyplot(data["tornado"], clear_figure=False)
                tornado_caption = data["tornado_caption"]
                st.markdown(
                    f"<p style='font-size:16px; font-weight:bold; font-style:italic; text-align:center;'>{tornado_caption}</p>",
                    unsafe_allow_html=True,
                )
        

def tornado_explanation(explanation: dict | None):

        predicted_class = explanation["predicted_class"]
        top_features = explanation["top_features"]
        base_value = explanation["base_value"]

        tornado_fig, tornado_caption = tornado_plot(top_features,predicted_class,base_value)

        st.markdown(
            f"<p style='font-size:18px; font-weight:bold; text-align:center;'>Contribuição dos fatores</p>",
            unsafe_allow_html=True,
        )
    
        if tornado_fig is not None:
            tornado_fig.set_size_inches(8, 4)   # largura, altura
            st.pyplot(tornado_fig, clear_figure=False)
            st.markdown(
                f"<p style='font-size:16px; font-weight:bold; font-style:italic; text-align:center;'>{tornado_caption}</p>",
                unsafe_allow_html=True,
            )