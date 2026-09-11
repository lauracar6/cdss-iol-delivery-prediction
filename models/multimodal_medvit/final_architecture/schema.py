# MAPPINGS OF UI categorical inputs that need to be one hot encoded

MULTIMODAL_MEDVIT_CATEGORICAL_MAPPINGS = {

    "metodoInd":{
        "Misoprostol": "MetodoInd_1-misoprostol",
        "Dinoprostona": "MetodoInd_2-dinoprostona",
        "Ocitocina": "MetodoInd_3-ocitocina",
        "Sonda Foley": "MetodoInd_4-SF"
    },

    "tipoPartoAnt": {
        "Cesariana": "PartoAntTipo_1-csa",
        "Instrumentado": "PartoAntTipo_2-instrumentado",
        "Parto eutócico": "PartoAntTipo_3-PE",
        "Cesariana + parto eutócico": "PartoAntTipo_4-CSA+PE",
        "Cesariana + instrumentado": "PartoAntTipo_5-CSA+instrumentado", 
        "Parto eutócico + instrumentado": "PartoAntTipo_6-PE+instrumentado",
        "Sem parto anterior": "PartoAntTipo_SemPartoAnterior" 
    },

    "instrument": {
        "Ventosa": "TipoInstrument_1-ventosa",
        "Forceps": "TipoInstrument_2-forceps",
        "Ventosa e forceps": "TipoInstrument_3-ventosa+forceps",
        "Sem parto anterior": "TipoInstrument_SemPartoAnterior"
    },

    "motivoCSAnt": {
        "Estado fetal não tranquilizador":"MotivoCSAant_10-EFNTintraparto",
        "Outro motivo":"MotivoCSAant_11-outras",
        "Patologia própria da gravidez":"MotivoCSAant_3-patprópriadagravidez",
        "Apresentação fetal anómala":"MotivoCSAant_5-sit/apfetalanómala",
        "Gravidez múltipla":"MotivoCSAant_6-gravidezmúltipla",
        "Incompatibilidade Feto-Pélvica":"MotivoCSAant_7-suspdeIFP",
        "Indução falhada":"MotivoCSAant_8-Induçãofalhada",
        "Trabalho de parto estacionário":"MotivoCSAant_9-TPestacionário",
        "Sem cesariana anterior": "MotivoCSAant_SemPartoAnterior"

    }, 
    
    "complicGravidez": {
        "Sem complicações":"ComplicGravidez_0-semcomplicações",
        "Ruptura prematura de membranas (RPM)": "ComplicGravidez_1-RPM",
        "Colestase gravídica": "ComplicGravidez_10-colestasegravídica", # não entra
        "Diabetes gestacional": "ComplicGravidez_2-DG",
        "Hipertensão gestacional": "ComplicGravidez_3-HTA",
        "Pré eclâmpsia": "ComplicGravidez_4-pré-eclâmpsia",
        "Restrição de crescimento fetal (RCF)": "ComplicGravidez_5-RCF",
        "Oligoâmnios": "ComplicGravidez_6-oligoamnios",
        "Hidrâmnio": "ComplicGravidez_7-hidramnios", # NAO entra
        "Trombocitopenia": "ComplicGravidez_9-trombocitopeniagestacional"
    },


    "patolPrevias": {
        "Sem patologias prévias": "PatologiasPrevias_0-sempatologias",
        "Diabetes mellitus":"PatologiasPrevias_1-DM",
        "Nódulos tiroideus": "PatologiasPrevias_10-nódulostiroideus",
        "Síndrome do ovário poliquístico": "PatologiasPrevias_11-SOP",
        "Pneumológica": "PatologiasPrevias_12-Pneumológica",
        "Ginecológica":"PatologiasPrevias_13-ginecológica",
        "Cardíaca": "PatologiasPrevias_14-cardíaca",
        "Neurológica": "PatologiasPrevias_15-neurologica",
        "Hematologica": "PatologiasPrevias_17-hematologica",
        "Infeciosa": "PatologiasPrevias_18-infeciosa",
        #"Obesidade": "PatologiasPrevias_19-obesidade",
        "Hipotiroidismo": "PatologiasPrevias_2-hipotiroidismo",
        "Outras":"PatologiasPrevias_20-outras",
        "Hipertensão arterial": "PatologiasPrevias_3-HTAc",
        "Trombofilia": "PatologiasPrevias_4-trombofilia",
        "Patologia autoimune": "PatologiasPrevias_5-patologiaautoimune",
        "Patologia oncológica": "PatologiasPrevias_6-patologiaoncológica",
        "Doença renal poliquística": "PatologiasPrevias_8-doençarenalpoliquistica",
        "Cirurgia bariatrica": "PatologiasPrevias_9-cirurgiabariátrica"
    },


    "motivoInd": {
        "Restrição do crescimento fetal (RCF)": "MotivoInd_9-RCF",
        "IG superior a 41 semanas": "MotivoInd_1-IG41sem",
        "Patologia materna": "MotivoInd_10-patologiamaterna",
        "Patologia fetal": "MotivoInd_11-patologiafetal",
        "Ruptura prematura de mebranas (RPM)":"MotivoInd_12-RPM",
        "IG da Procriação Medicamente Assistida": "MotivoInd_13-IGPMA", #nao vai entrar supostamente 
        "Outro motivo": "MotivoInd_14-outro",
        "Cardiotocografia suspeito": "MotivoInd_15-CTGsuspeito",
        "Oligoâmnios": "MotivoInd_2-oligoamnios",
        "Colestase": "MotivoInd_3-colestase", # nao vai entrar supostamente 
        "Diabetes gestacional": "MotivoInd_4-DG",
        "Hipertensão gestacional": "MotivoInd_5-HTA",
        "Pré eclampsia": "MotivoInd_6-pré-eclâmpsia",
        "Trombofilia": "MotivoInd_7-trombofilia",
        "Doença autoimune": "MotivoInd_8-doençaautoimune", #nao vai entrar supostamente
        
    }
}


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

MULTIMODAL_MEDVIT_UI_INPUTS = {

    "tabular":{

        "gestacoes": {
                "widget_type": "selectbox",            
                "label": "Gestações",
                "options": [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
                "default": 0,
                "type": "numeric",
                "required": True,
                "user_required": False,
                "range_values": None,
                "group": "historico",
        },

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

        "abortosEspont": {
            "type": "numeric",
            "required": True,
            "user_required": False,
            "group": "historico",
            "widget_type": "selectbox",
            "label": "Abortos espontâneos",
            "options": [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
            "range_values": None,
            "default": 0,
            #"dependes_on": None,
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
            "default": 0,
            "depends_on": {
                "field": "paridade",
                "condition": "!=",
                "trigger_value": 0,
                "fallback":0
            }
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

        
        "igpptAnt": {
            "type": "numeric",
            "required": True,
            "user_required": False,
            "group": "historico",
            "section": "Parto anterior",
            "widget_type": "selectbox",
            "label": "Idade gestacional do parto pré-termo anterior",
            "options": [24,25,26,27,28,29,30,31,32,33,34,35,36],
            "range_values": None,
            "default": 24,
            "depends_on": {
                "field": "partoPreTermoAnt",
                "condition": "!=",
                "trigger_value": 0,
                "fallback": 0
            }
        },

        "tempoPartoAnt": {
            "type": "numeric",
            "required": True,
            "user_required": True,
            "group": "historico",
            "section": "Parto anterior",
            "widget_type": "numeric",
            "label": "Tempo desde o último parto (meses)",
            "options": None,
            "range_values":None,
            "default": 9,
            "depends_on": {
                "field": "paridade",
                "condition": "!=",
                "trigger_value": 0,
                "fallback": 0
            }
        },

        "idadeGest": {
            "type": "numeric",
            "required": True,
            "user_required": True,
            "group": "gravidez",
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
            "group": "inducao",
            "widget_type": "selectbox",
            "label": "Índice Bishop",
            "options": [0,1,2,3,4,5,6,7],
            "range_values": None,
            "default": 0
        },
        
        "motivoInd": {
            "type": "categorical",
            "required": True,
            "user_required": False,
            "group": "inducao",
            "widget_type": "selectbox",
            "label":"Motivo da indução",
            "options":
                list(MULTIMODAL_MEDVIT_CATEGORICAL_MAPPINGS["motivoInd"].keys()),
            "range_values": None,
            "default": "Restrição do crescimento fetal (RCF)"
        },

        "metodoInd": {
            "type": "categorical",
            "required": True,
            "user_required": False,
            "group": "inducao",
            "widget_type": "selectbox",
            "label": "Método de indução",
            "options": list(MULTIMODAL_MEDVIT_CATEGORICAL_MAPPINGS["metodoInd"].keys()),
            "range_values": None,
            "default": "Misoprostol"
        },

        "eco3T": {
            "type": "numeric",
            "required": True,
            "user_required": False,
            "group": "gravidez",
            "widget_type": "selectbox",
            "label": "Semanas na ecografia do 3ºT",
            "options": [27,28,29,30,31,32,33,34,35,36,37,38,39],
            "range_values": None,
            "default": 30
        },

        "complicGravidez": {
            "type": "categorical",
            "required": True,
            "user_required": False,
            "group": "gravidez",
            "widget_type": "multiselect",
            "label": "Complicações na gravidez",
            "options":
                list(MULTIMODAL_MEDVIT_CATEGORICAL_MAPPINGS["complicGravidez"].keys()),
            "range_values": None,
            "default": ["Sem complicações"]
        },

        "dpb": {
            "type": "numeric",
            "required": True,
            "user_required": True,
            "group": "gravidez",
            "section": "Peso fetal estimado",
            "widget_type": "numeric",
            "step": 0.1,
            "label": "Diametro Biparietal (em mm)",
            "options": None,
            "range_values": [40.0, 120.0],
            "default": None
        },

        "pc": {
            "type": "numeric",
            "required": True,
            "user_required": True,
            "group": "gravidez",
            "section": "Peso fetal estimado",
            "widget_type": "numeric",
            "step": 0.1,
            "label": "Perimetro Cefálifo (em mm)",
            "options": None,
            "range_values": [150.0,370.0],
            "default": None
        },

        "pAB": {
            "type": "numeric",
            "required": True,
            "user_required": True,
            "group": "gravidez",
            "section": "Peso fetal estimado",
            "widget_type": "numeric",
            "step": 0.1,
            "label": "Perimetro Abdominal (em mm)",
            "options": None,
            "range_values": [120.0,370.0],
            "default": None
        },

        "fl": {
            "type": "numeric",
            "required": True,
            "user_required": True,
            "group": "gravidez",
            "section": "Peso fetal estimado",
            "widget_type": "numeric",
            "step": 0.1,
            "label": "Comprimento do Femur (em mm)",
            "options": None,
            "range_values": [30.0,100.0],
            "default": None
        },

        "epf_percentil": {
            "type": "numeric",
            "required": True,
            "user_required": True,
            "group": "gravidez",
            "section": "Peso fetal estimado",
            "widget_type": "numeric",
            "label": "Percentil (do peso fetal estimado)",
            "options": None,
            "range_values": [1,99],
            "default": None
        },

        
        "tipoPartoAnt": {
            "type": "categorical",
            "required": True,
            "user_required": False,
            "group": "historico",
            "section": "Parto anterior",
            "widget_type": "selectbox",
            "label": "Tipo de parto",
            "options": list(MULTIMODAL_MEDVIT_CATEGORICAL_MAPPINGS["tipoPartoAnt"].keys()),
            "range_values": None,
            "default": "Parto eutócico",
            "depends_on": {
                "field": "paridade",
                "condition": "!=",
                "trigger_value": 0,
                "fallback": "Sem parto anterior"
            }
        },

        "instrument": {
            "type": "categorical",
            "required": True,
            "user_required": False,
            "group": "historico",
            "section": "Parto anterior",
            "widget_type": "selectbox",
            "label": "Instrumentação",
            "options": list(MULTIMODAL_MEDVIT_CATEGORICAL_MAPPINGS["instrument"].keys()),
            "range_values": None,
            "default": "Ventosa",
            "depends_on": {
                "field": "tipoPartoAnt",
                "condition": "in",
                "trigger_value": ["Instrumentado","Cesariana e instrumentado", "Parto eutócico e instrumentado"],
                "fallback": "Sem parto anterior"
            }
        },

        "motivoCSAnt": {
            "type": "categorical",
            "required": True,
            "user_required": False,
            "group": "historico",
            "section": "Parto anterior",
            "widget_type": "selectbox",
            "label": "Motivo da cesariana anterior",
            "options": 
                list(MULTIMODAL_MEDVIT_CATEGORICAL_MAPPINGS["motivoCSAnt"].keys()),
            "range_values": None,
            "default": "Indução falhada",
            "depends_on": {
                "field": "tipoPartoAnt",
                "condition": "==",
                "trigger_value": "Cesariana",
                "fallback": "Sem cesariana anterior"
            }
        },


        "patolPrevias": {
            "type": "categorical",
            "required": True,
            "user_required": False,
            "group": "maternos",
            "widget_type": "multiselect",
            "label": "Patologias prévias",
            "options":
                list(MULTIMODAL_MEDVIT_CATEGORICAL_MAPPINGS["patolPrevias"].keys()),
            "range_values": None,
            "default": ["Sem patologias prévias"]
        },

    },

    "images": {

        "abdomen_image": {
            "type": "img",
            "required": True,
            "user_required": False,
            "group": "gravidez",
            "section": "Ecografias 3ºT",
            "widget_type": "img",
            "label": "Plano do Abdómen",
            "formats": ["jpg", "jpeg", "png"],
        },

        "head_image": {
            "type": "img",
            "required": True,
            "user_required": False,
            "group": "gravidez",
            "section": "Ecografias 3ºT",
            "widget_type": "img",
            "label": "Plano da Cabeça",
            "formats": ["jpg", "jpeg", "png"],
        },
        "femur_image": {
            "type": "img",
            "required": True,
            "user_required": False,
            "group": "gravidez",
            "section": "Ecografias 3ºT",
            "widget_type": "img",
            "label": "Plano do Femur",
            "formats": ["jpg", "jpeg", "png"],
        }

    }

}

# MODEL INPUT SCHEMA --------------------

MULTIMODAL_MEDVIT_SCHEMA = {
        "tabular": [
            "Paridade", 
            "Gesta", 
            "AE", 
            "PartoTermoAnterior", 
            "Idade", 
            "PesoInicial", 
            "PesoFinal", 
            "Altura", 
            "IMCInicial",
            "IMCfinal", 
            "AumentoPonderal", 
            "IGPPTAnterior", 
            "PartoAntTempoMeses", 
            "IG", 
            "Bishop",
            "EPF(pesoemg)", 
            "Eco3ºT(semanas)", 
            "DPB(mm)", 
            "PC(mm)", 
            "pAB(mm)", 
            "FL(mm)", 
            "EPF(percentil)",
            "MetodoInd_1-misoprostol", 
            "MetodoInd_2-dinoprostona", 
            "MetodoInd_3-ocitocina", 
            "MetodoInd_4-SF",
            "PartoAntTipo_1-csa", 
            "PartoAntTipo_2-instrumentado", 
            "PartoAntTipo_3-PE", 
            "PartoAntTipo_4-CSA+PE", 
            "PartoAntTipo_5-CSA+instrumentado",
            "PartoAntTipo_6-PE+instrumentado", 
            "PartoAntTipo_SemPartoAnterior", 
            "TipoInstrument_1-ventosa",
            "TipoInstrument_2-forceps", 
            "TipoInstrument_3-ventosa+forceps", 
            "TipoInstrument_SemPartoAnterior",
            "MotivoCSAant_10-EFNTintraparto", 
            "MotivoCSAant_11-outras", 
            "MotivoCSAant_3-patprópriadagravidez",
            "MotivoCSAant_5-sit/apfetalanómala", 
            "MotivoCSAant_6-gravidezmúltipla", 
            "MotivoCSAant_7-suspdeIFP",
            "MotivoCSAant_8-Induçãofalhada", 
            "MotivoCSAant_9-TPestacionário", 
            "MotivoCSAant_SemPartoAnterior",
            "ComplicGravidez_0-semcomplicações", 
            "ComplicGravidez_1-RPM", 
            "ComplicGravidez_10-colestasegravídica",
            "ComplicGravidez_2-DG", 
            "ComplicGravidez_3-HTA", 
            "ComplicGravidez_4-pré-eclâmpsia", 
            "ComplicGravidez_5-RCF",
            "ComplicGravidez_6-oligoamnios", 
            "ComplicGravidez_7-hidramnios", 
            "ComplicGravidez_9-trombocitopeniagestacional",
            "PatologiasPrevias_0-sempatologias", 
            "PatologiasPrevias_1-DM", 
            "PatologiasPrevias_10-nódulostiroideus",
            "PatologiasPrevias_11-SOP", 
            "PatologiasPrevias_12-Pneumológica", 
            "PatologiasPrevias_13-ginecológica",
            "PatologiasPrevias_14-cardíaca", 
            "PatologiasPrevias_15-neurologica", 
            "PatologiasPrevias_17-hematologica",
            "PatologiasPrevias_18-infeciosa", 
            "PatologiasPrevias_19-obesidade", 
            "PatologiasPrevias_2-hipotiroidismo",
            "PatologiasPrevias_20-outras", 
            "PatologiasPrevias_3-HTAc", 
            "PatologiasPrevias_4-trombofilia",
            "PatologiasPrevias_5-patologiaautoimune", 
            "PatologiasPrevias_6-patologiaoncológica",
            "PatologiasPrevias_8-doençarenalpoliquistica", 
            "PatologiasPrevias_9-cirurgiabariátrica", 
            "MotivoInd_9-RCF",
            "MotivoInd_1-IG41sem", 
            "MotivoInd_10-patologiamaterna", 
            "MotivoInd_11-patologiafetal", 
            "MotivoInd_12-RPM",
            "MotivoInd_13-IGPMA", 
            "MotivoInd_14-outro", 
            "MotivoInd_15-CTGsuspeito", 
            "MotivoInd_2-oligoamnios",
            "MotivoInd_3-colestase", 
            "MotivoInd_4-DG", 
            "MotivoInd_5-HTA", 
            "MotivoInd_6-pré-eclâmpsia",
            "MotivoInd_7-trombofilia", 
            "MotivoInd_8-doençaautoimune", 
            "CSAAnt", 
            "PPTAnterior"
        ],

        "images": [
            "abdomen_image", 
            "head_image", 
            "femur_image"
        ]
    }


# MAPPINGS OF UI received inputs that do not need preprocessing

MULTIMODAL_MEDVIT_UI_INPUTS_TO_MODEL= {
    "tabular":{
        "paridade": "Paridade",
        "gestacoes":"Gesta",
        "abortosEspont":"AE",
        "idade":"Idade",
        "pesoInicial":"PesoInicial",
        "pesoFinal":"PesoFinal",
        "altura":"Altura",
        "igpptAnt":"IGPPTAnterior",
        "tempoPartoAnt":"PartoAntTempoMeses",
        "idadeGest":"IG",
        "bishop":"Bishop",
        "eco3T":"Eco3ºT(semanas)",
        "dpb":"DPB(mm)",
        "pc":"PC(mm)",
        "pAB":"pAB(mm)",
        "fl":"FL(mm)",
        "epf_percentil":"EPF(percentil)",
        "partoPreTermoAnt": "PPTAnterior",
    },
    "images": {
        "abdomen_image":"abdomen_image", 
        "head_image":"head_image", 
        "femur_image":"femur_image"
    }
}


# SAMPLES FOR TESTING AND DEBUG -----------

MULTIMODAL_MEDVIT_UI_SAMPLES = {
    "Caso 1 - Normal" :{
        "paridade": 0,
        "gestacoes": 0,
        "abortosEspont": 0,
        "partoPreTermoAnt": 0,
        "idade": 27,
        "pesoInicial": 56,
        "pesoFinal": 62,
        "altura": 170,
        "igpptAnt": 0,
        "tempoPartoAnt": 0,
        "idadeGest": 37,
        "bishop": 5,
        "eco3T": 28,
        "dpb": 80,
        "pc": 270,
        "pAB": 250,
        "fl": 55,
        "epf_percentil": 50,
        "metodoInd": "Misoprostol",
        "tipoPartoAnt": "Sem parto anterior",
        "instrument": "Sem parto anterior",
        "motivoCSAnt": "Sem parto anterior",
        "complicGravidez": ["Sem complicações"],
        "patolPrevias": ["Sem patologias prévias"],
        "motivoInd": "Outro",

    },

        "Caso 2 - Risco" :{
        "paridade": 2,
        "gestacoes": 2,
        "abortosEspont": 0,
        "partoPreTermoAnt": 1,
        "idade": 45,
        "pesoInicial": 65,
        "pesoFinal": 78,
        "altura": 155,
        "igpptAnt": 35,
        "tempoPartoAnt": 20,
        "idadeGest": 38,
        "bishop": 1,
        "eco3T": 28,
        "dpb": 90,
        "pc": 310,
        "pAB": 300,
        "fl": 70,
        "epf_percentil": 70,
        "metodoInd": "Misoprostol",
        "tipoPartoAnt": "Cesariana",
        "instrument": "Ventosa",
        "motivoCSAnt": "Estado fetal não tranquilizador",
        "complicGravidez": [list(MULTIMODAL_MEDVIT_CATEGORICAL_MAPPINGS["complicGravidez"].keys())[i] for i in (1, 4)],
        "patolPrevias": list(MULTIMODAL_MEDVIT_CATEGORICAL_MAPPINGS["patolPrevias"].keys())[13],
        "motivoInd": "Rotura prematura de mebranas",

    }
}

