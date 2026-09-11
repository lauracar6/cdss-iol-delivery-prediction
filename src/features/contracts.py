"""
This script documents what comes from ui, what goes in and out of models. Serves as a truth source. 
Could later on be use for validation of api input and detect missing features.
"""

# pofia ter usado as listas de features que já tinha definido

# What comes from UI:
# -> Everything the system can receive before preprocessng 
RAW_INPUT_CONTRACT = {
    "multimodal_medvit": {
        "tabular": {
            "paridade": int,
            "gestacoes": int,
            "abortosEspont": int,
            "partoPreTermoAnt": int,
            "idade": int,
            "pesoInicial": int,
            "pesoFinal": int,
            "altura": int,
            "igpptAnt": int,
            "tempoPartoAnt": int,
            "idadeGest": int,
            "bishop": int,
            "eco3T": int,
            "dpb": int,
            "pc": int,
            "pAB": int,
            "fl": int,
            "metodoInd": str,
            "tipoPartoAnt": str,
            "instrument": str,
            "motivoCSAnt": str,
            "complicGravidez": list, # list of str
            "patolPrevias": list,
            "motivoInd": str       
            },

        "images": {
            "abdomen": bytes, 
            "head": bytes, 
            "femur": bytes  
        }
    },
    "rf_13_tabular": {
        "tabular": {
            "paridade": int,
            "idade": int,
            "pesoInicial": int,
            "pesoFinal": int,
            "altura": int,
            "idadeGest": int,
            "bishop": int,
            "metodoInd": str, 
            "complicGravidez": str, # 0 ou 1
            "patolPrevias": str, # 0 ou 1
            "motivoInd": str, # 0 ou 1
            "CSAAnt": str # 0 ou 1
        }
    }
}

# What goes in the model:
MODEL_INPUT_CONTRACT = {
    "multimodal_medvit": {
        "tabular": {
            "Paridade": float, "Gesta": float, "AE": float, "PartoTermoAnterior": float, "Idade": float,
            "PesoInicial": float, "PesoFinal": float, "Altura": float, "IMCInicial": float, "IMCfinal": float,
            "AumentoPonderal": float, "IGPPTAnterior": float, "PartoAntTempoMeses": float, "IG": float,
            "Bishop": float, "EPF(pesoemg)": float, "Eco3ºT(semanas)": float,"DPB(mm)": float, "PC(mm)": float,
            "pAB(mm)": float, "FL(mm)": float, "EPF(percentil)": float, "MetodoInd_1-misoprostol": float,
            "MetodoInd_2-dinoprostona": float, "MetodoInd_3-ocitocina": float, "MetodoInd_4-SF": float,
            "PartoAntTipo_1-csa": float, "PartoAntTipo_2-instrumentado": float, "PartoAntTipo_3-PE": float,
            "PartoAntTipo_4-CSA+PE": float,
            "PartoAntTipo_5-CSA+instrumentado": float,
            "PartoAntTipo_6-PE+instrumentado": float,
            "PartoAntTipo_SemPartoAnterior": float,
            "TipoInstrument_1-ventosa": float,
            "TipoInstrument_2-forceps": float,      
            "TipoInstrument_3-ventosa+forceps": float,
            "TipoInstrument_SemPartoAnterior": float,
            "MotivoCSAant_10-EFNTintraparto": float,
            "MotivoCSAant_11-outras": float,
            "MotivoCSAant_3-patprópriadagravidez": float,
            "MotivoCSAant_5-sit/apfetalanómala": float,
            "MotivoCSAant_6-gravidezmúltipla": float,
            "MotivoCSAant_7-suspdeIFP": float,
            "MotivoCSAant_8-Induçãofalhada": float,
            "MotivoCSAant_9-TPestacionário": float,
            "MotivoCSAant_SemPartoAnterior": float,
            "ComplicGravidez_0-semcomplicações": float,
            "ComplicGravidez_1-RPM": float,
            "ComplicGravidez_10-colestasegravídica": float,
            "ComplicGravidez_2-DG": float,
            "ComplicGravidez_3-HTA": float,
            "ComplicGravidez_4-pré-eclâmpsia": float,
            "ComplicGravidez_5-RCF": float,
            "ComplicGravidez_6-oligoamnios": float,
            "ComplicGravidez_7-hidramnios": float,
            "ComplicGravidez_9-trombocitopeniagestacional": float,
            "PatologiasPrevias_0-sempatologias": float,
            "PatologiasPrevias_1-DM": float,
            "PatologiasPrevias_10-nódulostiroideus": float,
            "PatologiasPrevias_11-SOP": float,
            "PatologiasPrevias_12-Pneumológica": float,
            "PatologiasPrevias_13-ginecológica": float,
            "PatologiasPrevias_14-cardíaca": float,
            "PatologiasPrevias_15-neurologica": float,
            "PatologiasPrevias_17-hematologica": float,
            "PatologiasPrevias_18-infeciosa": float,
            "PatologiasPrevias_19-obesidade": float,
            "PatologiasPrevias_2-hipotiroidismo": float,
            "PatologiasPrevias_20-outras": float,
            "PatologiasPrevias_3-HTAc": float,
            "PatologiasPrevias_4-trombofilia": float,
            "PatologiasPrevias_5-patologiaautoimune": float,
            "PatologiasPrevias_6-patologiaoncológica": float,
            "PatologiasPrevias_8-doençarenalpoliquistica": float,
            "PatologiasPrevias_9-cirurgiabariátrica": float,
            "MotivoInd_9-RCF": float,
            "MotivoInd_1-IG41sem": float,
            "MotivoInd_10-patologiamaterna": float,
            "MotivoInd_11-patologiafetal": float,
            "MotivoInd_12-RPM": float,
            "MotivoInd_13-IGPMA": float,
            "MotivoInd_14-outro": float,
            "MotivoInd_15-CTGsuspeito": float,
            "MotivoInd_2-oligoamnios": float,
            "MotivoInd_3-colestase": float,
            "MotivoInd_4-DG": float,
            "MotivoInd_5-HTA": float,
            "MotivoInd_6-pré-eclâmpsia": float,
            "MotivoInd_7-trombofilia": float,
            "MotivoInd_8-doençaautoimune": float,
            "CSAAnt": float,
            "PPTAnterior": float
        },  
        "images": {
            "abdomen_image": bytes, 
            "head_image": bytes, 
            "femur_image": bytes  
        }
    },

    "rf_13_tabular": {
        "tabular": {
            "Paridade": float,
            "PartoTermoAnterior": float,
            "Idade": float,
            "PesoInicial": float,
            "PesoFinal": float,
            "Altura": float,
            "IG": float,
            "Bishop": float,
            "MetodoInd_1-misoprostol": float, 
            "ComplicGravidez_2-DG": float, 
            "PatologiasPrevias_19-obesidade": float, 
            "MotivoInd_11-patologiafetal": float, 
            "CSAAnt": float, 
        },   
    }
}


# What comes out of the model:
MODEL_OUTPUT_CONTRACT = {
    "predicted_class": int,
    "class_0_proba": float,
    "class_1_proba": float
}

"""
This script documents the contracts for the functions in the project. 
It includes the expected input and output formats, as well as any assumptions or constraints 
that should be considered when using these functions. The contracts serve as a guide for developers 
to understand how to interact with the functions and what to expect from them, ensuring consistency 
and reliability in the codebase.
"""



