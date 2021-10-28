#!/usr/bin/env python3

# PIA - STREAMLIT WEBUI - SCORE
# 2021 (c) Micha Johannes Birklbauer
# https://github.com/michabirklbauer/
# micha.birklbauer@gmail.com

"""
#####################################################
##                                                 ##
##     -- STREAMLIT PIA SCORING FUNCTIONS --       ##
##                                                 ##
#####################################################
"""

import os
import json
import shutil
import random
import streamlit as st
from zipfile import ZipFile
from datetime import datetime
from scripts.redirect import *
from PIA.PIAScore import *
from PIA.PIAModel import PIAModel

#
def export_model(model, strat = "+"):

    s, c = model.change_strategy(strat)

    model_config = {"positives": model.positives,
                    "negatives": model.negatives,
                    "strategy": model.strategy,
                    "cutoff": model.cutoff,
                    "statistics": model.statistics}

    return json.dumps(model_config)

#
# don't cache! -> caching takes forever
#@st.cache
def score(pdb_file, sdf_file_1, sdf_file_2 = None, poses = "best", test_size = 0.3, val_size = 0.3, labels_by = "name", condition_operator = ">=", condition_value = 1000):

    # generated files
    filelist = []

    # output file prefix
    output_name_prefix = sdf_file_1.name.split(".sdf")[0] + datetime.now().strftime("%b-%d-%Y_%H-%M-%S") + "_" + str(random.randint(10000, 99999))

    # write uploaded files to tmp directory
    with open(output_name_prefix + "_pdb_file.pdb", "wb") as f1:
        f1.write(pdb_file.getbuffer())
    with open(output_name_prefix + "_sdf_file_1.sdf", "wb") as f2:
        f2.write(sdf_file_1.getbuffer())
    if sdf_file_2 != None:
        with open(output_name_prefix + "_sdf_file_2.sdf", "wb") as f2:
            f2.write(sdf_file_2.getbuffer())
        this_sdf_file_2 = output_name_prefix + "_sdf_file_2.sdf"
    else:
        this_sdf_file_2 = None

    # set condition value
    this_condition_value = float(condition_value)

    # train model
    model = PIAModel()
    train_results = model.train(output_name_prefix + "_pdb_file.pdb", output_name_prefix + "_sdf_file_1.sdf", this_sdf_file_2,
                                poses = poses, test_size = test_size, val_size = val_size,
                                labels_by = labels_by, condition_operator = condition_operator, condition_value = this_condition_value,
                                plot_prefix = output_name_prefix,  keep_files = False, tmp_dir_name = output_name_prefix + "_structures")

    # append comparison plots to filelist
    filelist.append(output_name_prefix + "_comparison_train.png")
    filelist.append(output_name_prefix + "_comparison_val.png")
    filelist.append(output_name_prefix + "_comparison_test.png")

    # print condition if molecules are labelled by ic50
    if labels_by == "ic50":
        print("Molecules with IC50 " + condition_operator + " " + str(condition_value) + " are labelled as decoys!")

    # save plots - ROC
    p_1 = plot_ROC_curve(train_results["TRAIN"]["+"]["ROC"]["fpr"], train_results["TRAIN"]["+"]["ROC"]["tpr"],
                         filename = output_name_prefix + "_roc_train_strat_p.png")
    filelist.append(output_name_prefix + "_roc_train_strat_p.png")
    p_2 = plot_ROC_curve(train_results["TRAIN"]["++"]["ROC"]["fpr"], train_results["TRAIN"]["++"]["ROC"]["tpr"],
                         filename = output_name_prefix + "_roc_train_strat_pp.png")
    filelist.append(output_name_prefix + "_roc_train_strat_pp.png")
    p_3 = plot_ROC_curve(train_results["TRAIN"]["+-"]["ROC"]["fpr"], train_results["TRAIN"]["+-"]["ROC"]["tpr"],
                         filename = output_name_prefix + "_roc_train_strat_pm.png")
    filelist.append(output_name_prefix + "_roc_train_strat_pm.png")
    p_4 = plot_ROC_curve(train_results["TRAIN"]["++--"]["ROC"]["fpr"], train_results["TRAIN"]["++--"]["ROC"]["tpr"],
                         filename = output_name_prefix + "_roc_train_strat_ppmm.png")
    filelist.append(output_name_prefix + "_roc_train_strat_ppmm.png")
    p_5 = plot_ROC_curve(train_results["VAL"]["+"]["ROC"]["fpr"], train_results["VAL"]["+"]["ROC"]["tpr"],
                         filename = output_name_prefix + "_roc_val_strat_p.png")
    filelist.append(output_name_prefix + "_roc_val_strat_p.png")
    p_6 = plot_ROC_curve(train_results["VAL"]["++"]["ROC"]["fpr"], train_results["VAL"]["++"]["ROC"]["tpr"],
                         filename = output_name_prefix + "_roc_val_strat_pp.png")
    filelist.append(output_name_prefix + "_roc_val_strat_pp.png")
    p_7 = plot_ROC_curve(train_results["VAL"]["+-"]["ROC"]["fpr"], train_results["VAL"]["+-"]["ROC"]["tpr"],
                         filename = output_name_prefix + "_roc_val_strat_pm.png")
    filelist.append(output_name_prefix + "_roc_val_strat_pm.png")
    p_8 = plot_ROC_curve(train_results["VAL"]["++--"]["ROC"]["fpr"], train_results["VAL"]["++--"]["ROC"]["tpr"],
                         filename = output_name_prefix + "_roc_val_strat_ppmm.png")
    filelist.append(output_name_prefix + "_roc_val_strat_ppmm.png")
    p_9 = plot_ROC_curve(train_results["TEST"]["+"]["ROC"]["fpr"], train_results["TEST"]["+"]["ROC"]["tpr"],
                         filename = output_name_prefix + "_roc_test_strat_p.png")
    filelist.append(output_name_prefix + "_roc_test_strat_p.png")
    p_10 = plot_ROC_curve(train_results["TEST"]["++"]["ROC"]["fpr"], train_results["TEST"]["++"]["ROC"]["tpr"],
                         filename = output_name_prefix + "_roc_test_strat_pp.png")
    filelist.append(output_name_prefix + "_roc_test_strat_pp.png")
    p_11 = plot_ROC_curve(train_results["TEST"]["+-"]["ROC"]["fpr"], train_results["TEST"]["+-"]["ROC"]["tpr"],
                         filename = output_name_prefix + "_roc_test_strat_pm.png")
    filelist.append(output_name_prefix + "_roc_test_strat_pm.png")
    p_12 = plot_ROC_curve(train_results["TEST"]["++--"]["ROC"]["fpr"], train_results["TEST"]["++--"]["ROC"]["tpr"],
                         filename = output_name_prefix + "_roc_test_strat_ppmm.png")
    filelist.append(output_name_prefix + "_roc_test_strat_ppmm.png")

    # save plots - CM
    cm_1 = plot_confusion_matrix(train_results["TRAIN"]["+"]["CM"], [0, 1], filename = output_name_prefix + "_cm_train_strat_p.png")
    filelist.append(output_name_prefix + "_cm_train_strat_p.png")
    cm_2 = plot_confusion_matrix(train_results["TRAIN"]["++"]["CM"], [0, 1], filename = output_name_prefix + "_cm_train_strat_pp.png")
    filelist.append(output_name_prefix + "_cm_train_strat_pp.png")
    cm_3 = plot_confusion_matrix(train_results["TRAIN"]["+-"]["CM"], [0, 1], filename = output_name_prefix + "_cm_train_strat_pm.png")
    filelist.append(output_name_prefix + "_cm_train_strat_pm.png")
    cm_4 = plot_confusion_matrix(train_results["TRAIN"]["++--"]["CM"], [0, 1], filename = output_name_prefix + "_cm_train_strat_ppmm.png")
    filelist.append(output_name_prefix + "_cm_train_strat_ppmm.png")
    cm_5 = plot_confusion_matrix(train_results["VAL"]["+"]["CM"], [0, 1], filename = output_name_prefix + "_cm_val_strat_p.png")
    filelist.append(output_name_prefix + "_cm_val_strat_p.png")
    cm_6 = plot_confusion_matrix(train_results["VAL"]["++"]["CM"], [0, 1], filename = output_name_prefix + "_cm_val_strat_pp.png")
    filelist.append(output_name_prefix + "_cm_val_strat_pp.png")
    cm_7 = plot_confusion_matrix(train_results["VAL"]["+-"]["CM"], [0, 1], filename = output_name_prefix + "_cm_val_strat_pm.png")
    filelist.append(output_name_prefix + "_cm_val_strat_pm.png")
    cm_8 = plot_confusion_matrix(train_results["VAL"]["++--"]["CM"], [0, 1], filename = output_name_prefix + "_cm_val_strat_ppmm.png")
    filelist.append(output_name_prefix + "_cm_val_strat_ppmm.png")
    cm_9 = plot_confusion_matrix(train_results["TEST"]["+"]["CM"], [0, 1], filename = output_name_prefix + "_cm_test_strat_p.png")
    filelist.append(output_name_prefix + "_cm_test_strat_p.png")
    cm_10 = plot_confusion_matrix(train_results["TEST"]["++"]["CM"], [0, 1], filename = output_name_prefix + "_cm_test_strat_pp.png")
    filelist.append(output_name_prefix + "_cm_test_strat_pp.png")
    cm_11 = plot_confusion_matrix(train_results["TEST"]["+-"]["CM"], [0, 1], filename = output_name_prefix + "_cm_test_strat_pm.png")
    filelist.append(output_name_prefix + "_cm_test_strat_pm.png")
    cm_12 = plot_confusion_matrix(train_results["TEST"]["++--"]["CM"], [0, 1], filename = output_name_prefix + "_cm_test_strat_ppmm.png")
    filelist.append(output_name_prefix + "_cm_test_strat_ppmm.png")

    # print and save summary statistics
    model.summary(filename = output_name_prefix + "_summary.txt")
    filelist.append(output_name_prefix + "_summary.txt")

    # save models
    model.save(output_name_prefix + "_best")
    filelist.append(output_name_prefix + "_best.piam")
    model.change_strategy("+")
    model.save(output_name_prefix + "_p")
    filelist.append(output_name_prefix + "_p.piam")
    model.change_strategy("++")
    model.save(output_name_prefix + "_pp")
    filelist.append(output_name_prefix + "_pp.piam")
    model.change_strategy("+-")
    model.save(output_name_prefix + "_pm")
    filelist.append(output_name_prefix + "_pm.piam")
    model.change_strategy("++--")
    model.save(output_name_prefix + "_ppmm")
    filelist.append(output_name_prefix + "_ppmm.piam")
    model.change_strategy("best")

    # generate zip archive
    with ZipFile(output_name_prefix + "_result.zip", "w") as zf:
        for f in filelist:
            zf.write(f)
        zf.close()

    # cleanup
    for f in filelist:
        os.remove(f)
    os.remove(output_name_prefix + "_pdb_file.pdb")
    os.remove(output_name_prefix + "_sdf_file_1.sdf")
    if sdf_file_2 != None:
        os.remove(output_name_prefix + "_sdf_file_2.sdf")

    # create return dict
    result = {"statistics": model.statistics,
              "model_p": export_model(model, strat = "+"),
              "model_pp": export_model(model, strat = "++"),
              "model_pm": export_model(model, strat = "+-"),
              "model_ppmm": export_model(model, strat = "++--"),
              "roc_plot_p": p_9,
              "roc_plot_pp": p_10,
              "roc_plot_pm": p_11,
              "roc_plot_ppmm": p_12,
              "zipfile": output_name_prefix + "_result.zip"}

    return result

#
def main():

    title = st.title("PIAScore - Workflow II")

    text_1 = st.markdown("*Train scoring models based on the frequencies of interactions present in active and inactive complexes.*")
    text_2 = st.markdown("Upload a protein host structure in PDB file format and active and inactive ligand coordinates in SDF format. Up to two SD files may supplied.")

    pdb_file = st.file_uploader("Upload the PDB host structure:",
                                type = ["pdb"],
                                help = "The target host structure that was used for docking of the ligands in PDB file format."
                                )

    sdf_file_1 = st.file_uploader("Upload docked ligand coordinates in SDF format:",
                                  type = ["sdf"],
                                  help = "The coordinates of the docked ligands in SDF format. Not all SD files might be supported. Supported software: GOLD."
                                  )

    sdf_file_2 = st.file_uploader("[Optional] Upload additional docked ligand coordinates in SDF format:",
                                  type = ["sdf"],
                                  help = "The coordinates of the docked ligands in SDF format. Not all SD files might be supported. Supported software: GOLD."
                                  )

    mode_help_str = "Select a labelling criterion e.g. if 'Ligand name' is selected ligands that contain the phrase 'inactive' or 'decoy' in their name will be labelled "
    mode_help_str += "inactive and all others will be treated as active. If option 'IC50 value' is supplied the labelling routine checks if the condition stated "
    mode_help_str += "in the expander below is fullfilled or not and labels ligands accordingly. For example if the condition is '>= 1000' any ligands with IC50 "
    mode_help_str += "greater or equal to 1000 will be treated as inactive (and the rest as active consequentially)."
    mode = st.radio(label = "Select a labelling criterion:",
                    options = [{"display": "Ligand name", "value": "name"}, {"display": "IC50 value", "value": "ic50"}],
                    index = 0,
                    format_func = lambda mode: mode["display"],
                    help = mode_help_str
                    )

    with st.expander("[Optional] IC50 labelling condition:"):
        condition_operator_help_str = "One of '==', '!=', '<=', '<', '>=', '>'. A molecule is labelled as inactive if the "
        condition_operator_help_str += "IC50 values is 'condition_operator' 'condition_value' e.g. if 'condition_operator' "
        condition_operator_help_str += "is '>=' and 'condition_value' is '1000' then all molecules where 'IC50 >= 1000' are labelled as inactive."
        condition_operator = st.text_input(label = "Enter the condition operator:",
                                           value = ">=",
                                           max_chars = 2,
                                           help = condition_operator_help_str
                                           )
        condition_value_help_str = "Reference value. Must be able to cast value to 'float' internally: Any real number (less than 10 characters) is allowed. Decimal sign - if used - has to be '.'. "
        condition_value_help_str += "A molecule is labelled as inactive if the IC50 values is 'condition_operator' 'condition_value' e.g. if 'condition_operator' "
        condition_value_help_str += "is '>=' and 'condition_value' is '1000' then all molecules where 'IC50 >= 1000' are labelled as inactive."
        condition_value = st.text_input(label = "Enter the condition value:",
                                        value = "1000",
                                        max_chars = 10,
                                        help = condition_value_help_str
                                        )

    result = None

    if st.button("Run!", help = "Train and evaluate model based on the given input."):
        with st.expander("Show logging info:"):
            with st_stdout("info"):
                if pdb_file != None and sdf_file_1 != None:
                    try:
                        result = score(pdb_file, sdf_file_1, sdf_file_2, labels_by = mode["value"], condition_operator = condition_operator, condition_value = condition_value)
                        status = 0
                    except Exception as e:
                        this_e = st.exception(e)
                        status = 1
                else:
                    status = 1
                    no_file = st.error("Error: PDB and SDF have to be both provided for scoring!")
        if status == 0:
            res_status = st.success("Scoring finished successfully!")
        else:
            res_status = st.error("Scoring stopped prematurely! See log for more information!")

    if result != None:
        st.session_state["model_statistics"] = result["statistics"]
        st.session_state["roc_plot_p"] = result["roc_plot_p"]
        st.session_state["roc_plot_pp"] = result["roc_plot_pp"]
        st.session_state["roc_plot_pm"] = result["roc_plot_pm"]
        st.session_state["roc_plot_ppmm"] = result["roc_plot_ppmm"]
        st.session_state["result_zip"] = result["zipfile"]
        st.session_state["model_p"] = result["model_p"]
        st.session_state["model_pp"] = result["model_pp"]
        st.session_state["model_pm"] = result["model_pm"]
        st.session_state["model_ppmm"] = result["model_ppmm"]

    col_1, col_2, col_3, col_4 = st.columns(4)

    with col_1:
        if "model_statistics" in st.session_state and "roc_plot_p" in st.session_state:
            sh_1 = st.subheader("Strategy +")
            if st.session_state["model_statistics"]["STRAT"]["best_strategy"] == "+":
                best_val_1 = st.caption("Best-On-Validation Model")
            else:
                best_val_1 = st.caption("Standard Model")
            desc_1 = st.markdown("**Metrics from the Test Partition:**")
            roc_plot_1 = st.pyplot(st.session_state["roc_plot_p"])
            mkdown_1 = "- **ACC:** " + str(round(st.session_state["model_statistics"]["TEST"]["+"]["ACC"], 5)) + "\n"
            mkdown_1 += "- **FPR:** " + str(round(st.session_state["model_statistics"]["TEST"]["+"]["FPR"], 5)) + "\n"
            mkdown_1 += "- **AUC:** " + str(round(st.session_state["model_statistics"]["TEST"]["+"]["AUC"], 5)) + "\n"
            mkdown_1 += "- **Ya:** " + str(round(st.session_state["model_statistics"]["TEST"]["+"]["Ya"], 5)) + "\n"
            mkdown_1 += "- **EF:** " + str(round(st.session_state["model_statistics"]["TEST"]["+"]["EF"], 5)) + "\n"
            mkdown_1 += "- **REF:** " + str(round(st.session_state["model_statistics"]["TEST"]["+"]["REF"], 5)) + "\n"
            metrics_1 = st.markdown(mkdown_1)
            if "model_p" in st.session_state:
                model_1 = st.download_button(label = "Download Model!",
                                             data = st.session_state["model_p"],
                                             file_name = "model_p.piam",
                                             mime = "text/json",
                                             help = "Download Model+ in PIAM format."
                                             )
    with col_2:
        if "model_statistics" in st.session_state and "roc_plot_pp" in st.session_state:
            sh_2 = st.subheader("Strategy ++")
            if st.session_state["model_statistics"]["STRAT"]["best_strategy"] == "++":
                best_val_1 = st.caption("Best-On-Validation Model")
            else:
                best_val_1 = st.caption("Standard Model")
            desc_2 = st.markdown("**Metrics from the Test Partition:**")
            roc_plot_2 = st.pyplot(st.session_state["roc_plot_pp"])
            mkdown_2 = "- **ACC:** " + str(round(st.session_state["model_statistics"]["TEST"]["++"]["ACC"], 5)) + "\n"
            mkdown_2 += "- **FPR:** " + str(round(st.session_state["model_statistics"]["TEST"]["++"]["FPR"], 5)) + "\n"
            mkdown_2 += "- **AUC:** " + str(round(st.session_state["model_statistics"]["TEST"]["++"]["AUC"], 5)) + "\n"
            mkdown_2 += "- **Ya:** " + str(round(st.session_state["model_statistics"]["TEST"]["++"]["Ya"], 5)) + "\n"
            mkdown_2 += "- **EF:** " + str(round(st.session_state["model_statistics"]["TEST"]["++"]["EF"], 5)) + "\n"
            mkdown_2 += "- **REF:** " + str(round(st.session_state["model_statistics"]["TEST"]["++"]["REF"], 5)) + "\n"
            metrics_2 = st.markdown(mkdown_2)
            if "model_pp" in st.session_state:
                model_2 = st.download_button(label = "Download Model!",
                                             data = st.session_state["model_pp"],
                                             file_name = "model_pp.piam",
                                             mime = "text/json",
                                             help = "Download Model++ in PIAM format."
                                             )

    with col_3:
        if "model_statistics" in st.session_state and "roc_plot_pm" in st.session_state:
            sh_3 = st.subheader("Strategy +-")
            if st.session_state["model_statistics"]["STRAT"]["best_strategy"] == "+-":
                best_val_1 = st.caption("Best-On-Validation Model")
            else:
                best_val_1 = st.caption("Standard Model")
            desc_3 = st.markdown("**Metrics from the Test Partition:**")
            roc_plot_3 = st.pyplot(st.session_state["roc_plot_pm"])
            mkdown_3 = "- **ACC:** " + str(round(st.session_state["model_statistics"]["TEST"]["+-"]["ACC"], 5)) + "\n"
            mkdown_3 += "- **FPR:** " + str(round(st.session_state["model_statistics"]["TEST"]["+-"]["FPR"], 5)) + "\n"
            mkdown_3 += "- **AUC:** " + str(round(st.session_state["model_statistics"]["TEST"]["+-"]["AUC"], 5)) + "\n"
            mkdown_3 += "- **Ya:** " + str(round(st.session_state["model_statistics"]["TEST"]["+-"]["Ya"], 5)) + "\n"
            mkdown_3 += "- **EF:** " + str(round(st.session_state["model_statistics"]["TEST"]["+-"]["EF"], 5)) + "\n"
            mkdown_3 += "- **REF:** " + str(round(st.session_state["model_statistics"]["TEST"]["+-"]["REF"], 5)) + "\n"
            metrics_3 = st.markdown(mkdown_3)
            if "model_pm" in st.session_state:
                model_3 = st.download_button(label = "Download Model!",
                                             data = st.session_state["model_pm"],
                                             file_name = "model_pm.piam",
                                             mime = "text/json",
                                             help = "Download Model+- in PIAM format."
                                             )

    with col_4:
        if "model_statistics" in st.session_state and "roc_plot_ppmm" in st.session_state:
            sh_4 = st.subheader("Strategy ++--")
            if st.session_state["model_statistics"]["STRAT"]["best_strategy"] == "++--":
                best_val_1 = st.caption("Best-On-Validation Model")
            else:
                best_val_1 = st.caption("Standard Model")
            desc_4 = st.markdown("**Metrics from the Test Partition:**")
            roc_plot_4 = st.pyplot(st.session_state["roc_plot_ppmm"])
            mkdown_4 = "- **ACC:** " + str(round(st.session_state["model_statistics"]["TEST"]["++--"]["ACC"], 5)) + "\n"
            mkdown_4 += "- **FPR:** " + str(round(st.session_state["model_statistics"]["TEST"]["++--"]["FPR"], 5)) + "\n"
            mkdown_4 += "- **AUC:** " + str(round(st.session_state["model_statistics"]["TEST"]["++--"]["AUC"], 5)) + "\n"
            mkdown_4 += "- **Ya:** " + str(round(st.session_state["model_statistics"]["TEST"]["++--"]["Ya"], 5)) + "\n"
            mkdown_4 += "- **EF:** " + str(round(st.session_state["model_statistics"]["TEST"]["++--"]["EF"], 5)) + "\n"
            mkdown_4 += "- **REF:** " + str(round(st.session_state["model_statistics"]["TEST"]["++--"]["REF"], 5)) + "\n"
            metrics_4 = st.markdown(mkdown_4)
            if "model_ppmm" in st.session_state:
                model_4 = st.download_button(label = "Download Model!",
                                             data = st.session_state["model_ppmm"],
                                             file_name = "model_ppmm.piam",
                                             mime = "text/json",
                                             help = "Download Model++-- in PIAM format."
                                             )

    if "result_zip" in st.session_state:
        with st.expander("Download all Results:"):
            with open(st.session_state["result_zip"], "rb") as f:
                all_zip = st.download_button(label = "Download ZIP of all results!",
                                             data = f,
                                             file_name = st.session_state["result_zip"],
                                             mime = "application/zip",
                                             help = "Download all generated result files compressed in ZIP file format!"
                                             )
