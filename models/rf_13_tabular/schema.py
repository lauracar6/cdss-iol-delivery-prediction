# UI INPUS METADATA ------------------------
#adicionar quando conseguir
"""        "id_paciente": {
                "type": "numeric",
                "group": "demograficas",
                "widget_type": "numeric",
                "label": "ID da paciente:",
                "options": None,
                "range_values": None,
                "default": None,
        },"""

RF_13_UI_INPUTS = {

    "tabular": {

        "paridade": {
                "type": "numeric",
                "required": True,
                "user_required": False,
                "group": "historico",
                "widget_type": "selectbox",
                "label": "Paridade",
                "options": [0,1,2,3,4,5,6],
                "range_values": None,
                "default": 0
        },

        "partoPreTermoAnt": {
                "type": "numeric",
                "required": True,
                "user_required": False,
                "group": "historico",
                "widget_type": "selectbox",
                "label": "Partos pré-termo anteriores",
                "options": [0,1,2,3,4,5,6],
                "range_values": None,
                "default": 0
            },

        "idade": {
                "type": "numeric",
                "required": True,
                "user_required": True,
                "group": "maternos",
                "widget_type": "numeric",
                "label": "Idade",
                "options": None,
                "range_values": [15,55],
                "default": 30
            },

        "altura": {
            "type": "numeric",
            "required": True,
            "user_required": True,
            "group": "maternos",
            "widget_type": "numeric",
            "label": "Altura (em cm)",
            "options": None,
            "range_values": [140,200],
            "default": None
        },

        "pesoInicial": {
            "type": "numeric",
            "required": True,
            "user_required": True,
            "group": "maternos",
            "widget_type": "numeric",
            "label": "Peso inicial (kg)",
            "options": None,
            "range_values": [30,200],
            "default": None
        },

        "pesoFinal": {
            "type": "numeric",
            "required": True,
            "user_required": True,
            "group": "maternos",
            "widget_type": "numeric",
            "label": "Peso final (kg)",
            "options": None,
            "range_values": [30,200],
            "default": None
        },


        "idadeGest": {
            "type": "numeric",
            "required": True,
            "user_required": True,
            "group":"gravidez",
            "widget_type": "numeric",
            "label": "Idade gestacional (semanas)",
            "options": None,
            "range_values": [28,42],
            "default": None
        },

        "bishop": {
            "type": "numeric",
            "required": True,
            "user_required": False,
            "group":"inducao",
            "widget_type": "selectbox",
            "label": "Índice Bishop",
            "options": [0,1,2,3,4,5,6,7],
            "range_values": None,
            "default": 0
        },
        
        "metodoInd": {
            "type": "categorical",
            "required": True,
            "user_required": False,
            "group": "inducao",
            "widget_type": "radio",
            "label": "Método de indução - misoprostol?",
            "options": ["Não", "Sim"],
            "range_values": None,
            "default": "Não"
        },

        "complicGravidez": {
            "type": "categorical",
            "required": True,
            "user_required": False,
            "group": "gravidez",
            "widget_type": "radio",
            "label":"Tem diabetes gestacional?",
            "options": ["Não", "Sim"],
            "range_values": None,
            "default": "Não"
        },

        "motivoInd": {
            "type": "categorical",
            "required": True,
            "user_required": False,
            "group": "inducao",
            "widget_type": "radio",
            "label": "Motivo da indução - patologia fetal?",
            "options": ["Não", "Sim"],
            "range_values": None,
            "default": "Não"
        },

        "CSAAnt": {
            "type": "categorical",
            "required": True,
            "user_required": False,
            "group": "historico",
            "widget_type": "radio",
            "label": "Parto anterior foi cesariana?",
            "options": ["Não", "Sim"],
            "range_values": None,
            "default": "Não"
        }
    },

    "images": {}
}

#"patolPrevias": {
    #   "type": "categorical",
    #  "group": "maternos",
    # "widget_type": "radio",
    # "label": "IMC é superior a 30?",
    # "options": ["Não", "Sim"],
    # "range_values": None,
    #  "default": None,
#},

# MODEL INPUT SCHEMA --------------------

RF_13_SCHEMA = {
    "tabular": [
        "Paridade",
        "PartoTermoAnterior",
        "Idade",
        "PesoInicial",
        "PesoFinal",
        "Altura",
        "IG",
        "Bishop",
        "MetodoInd_1-misoprostol", 
        "ComplicGravidez_2-DG", 
        "PatologiasPrevias_19-obesidade", 
        "MotivoInd_11-patologiafetal", 
        "CSAAnt"
    ]
}

# MAPPINGS OF UI received inputs that do not need preprocessing

RF_13_UI_INPUTS_TO_MODEL ={
    "tabular": {
        "paridade":"Paridade",
        "idade":"Idade",
        "pesoInicial":"PesoInicial",
        "pesoFinal":"PesoFinal",
        "altura":"Altura",
        "idadeGest":"IG",
        "bishop":"Bishop"
    }
}

# MAPPINGS OF UI categorical inputs that need to be one hot encoded

RF_13_CATEGORICAL_MAPPINGS = {
    "metodoInd":"MetodoInd_1-misoprostol",
    "complicGravidez":"ComplicGravidez_2-DG",
    #"patolPrevias":"PatologiasPrevias_19-obesidade",
    "motivoInd":"MotivoInd_11-patologiafetal",
    "CSAAnt":"CSAAnt"
}


YES_NO_MAPPING = {"Não": 0, "Sim": 1}


# SAMPLES FOR TESTING AND DEBUG -----------

RF_13_UI_SAMPLES = {
    "Caso 1 - Normal" :{
        "paridade": 0,
        "partoPreTermoAnt": 0,
        "idade": 27,
        "pesoInicial": 56,
        "pesoFinal": 62,
        "altura": 170,
        "idadeGest": 36,
        "bishop": 4,
        "metodoInd": "Sim",
        "complicGravidez": "Não",
        "motivoInd": "Não",
        "CSAAnt": "Não"
    },

    "Caso 2 - Risco": {
        "paridade": 2,
        "partoPreTermoAnt": 1,
        "idade": 40,
        "pesoInicial": 60,
        "pesoFinal": 78,
        "altura": 158,
        "idadeGest": 35,
        "bishop": 2,
        "metodoInd": "Sim",
        "complicGravidez": "Sim",
        "motivoInd": "Sim",
        "CSAAnt": "Sim"
    }

}
