#!/usr/bin/env python3

# PIA - STREAMLIT WEBUI - PREDICT
# 2021 (c) Micha Johannes Birklbauer
# https://github.com/michabirklbauer/
# micha.birklbauer@gmail.com

"""
#####################################################
##                                                 ##
##    -- STREAMLIT PIA PREDICTION FUNCTIONS --     ##
##                                                 ##
#####################################################
"""

import os
import math
import shutil
import random
import streamlit as st
from datetime import datetime
from scripts.redirect import *
from PIA.PIAModel import PIAModel

#
def color_code(value):
    if value == "inactive":
        color = "background-color: #b90e0a; color: white"
    elif value == "active":
        color = "background-color: #234f1e; color: white"
    else:
        color = "background-color: white; color: black"

    return color

#
def predict_pdb(model_info, pdb_file, cutoff = None, name = None):

    # check if model or interactions are given
    if isinstance(model_info, str):
        model = PIAModel(filename = model_info)
    else:
        if cutoff is not None:
            model = PIAModel(positives = model_info, strategy = "+", cutoff = cutoff)
        else:
            model = PIAModel(positives = model_info, strategy = "+", cutoff = math.ceil(len(model_info)/2))

    # return prediction
    return model.predict_pdb(pdb_file, name = name)

#
def predict_sdf(model_info, pdb_file, sdf_file, cutoff = None, tmp_dir_name = "piamodel_structures_tmp"):

    # check if model or interactions are given
    if isinstance(model_info, str):
        model = PIAModel(filename = model_info)
    else:
        if cutoff is not None:
            model = PIAModel(positives = model_info, strategy = "+", cutoff = cutoff)
        else:
            model = PIAModel(positives = model_info, strategy = "+", cutoff = math.ceil(len(model_info)/2))

    # return prediction
    return model.predict_sdf(pdb_file, sdf_file, save_csv = False, tmp_dir_name = tmp_dir_name)

#
def main():

    title_1 = st.title("PIAPredict - Workflow III")

    text_1_1 = st.markdown("*Predict the activity of protein-ligand complexes using a PIAModel.*")
    text_1_2_txt = "Select one of two input modes for prediction: Either predict a single complex using a PDB file as input "
    text_1_2_txt += "*OR* predict multiple complexes by supplying a host protein structure in PDB format and docked ligand coordinates in SDF format."
    text_1_2 = st.markdown(text_1_2_txt)

    piamodel = st.file_uploader("Upload a model:",
                                type = ["piam"],
                                help = "The PIAModel that should be used for prediction."
                                )

    col_1_1, col_1_2 = st.columns(2)

    result_1 = None

    with col_1_1:
        text_1_3 = st.markdown("**Input Mode I - Single Structure:**")

        pdb_file_1_1 = st.file_uploader("Upload a PDB structure:",
                                      type = ["pdb"],
                                      help = "The protein-ligand complex in PDB file format that should be predicted by the model.",
                                      key = "pdb_file_1_1"
                                      )

        if st.button("Predict!", help = "Predict the activity of the given protein-ligand complex with the supplied model."):
            with st.expander("Show logging info:"):
                with st_stdout("info"):
                    if piamodel != None and pdb_file_1_1 != None:
                        try:
                            # create unique file prefix
                            output_name_prefix = datetime.now().strftime("%b-%d-%Y_%H-%M-%S") + "_" + str(random.randint(10000, 99999))
                            #write files
                            with open(output_name_prefix + pdb_file_1_1.name, "wb") as f1:
                                f1.write(pdb_file_1_1.getbuffer())
                            with open(output_name_prefix + piamodel.name, "wb") as f2:
                                f2.write(piamodel.getbuffer())
                            # get prediction
                            result_1 = predict_pdb(output_name_prefix + piamodel.name, output_name_prefix + pdb_file_1_1.name, name = pdb_file_1_1.name)
                            # cleanup
                            os.remove(output_name_prefix + pdb_file_1_1.name)
                            os.remove(output_name_prefix + piamodel.name)
                            # set status
                            status_1 = 0
                        except Exception as e:
                            this_e = st.exception(e)
                            status_1 = 1
                    else:
                        status_1 = 1
                        no_file = st.error("Error: Model and PDB structure have to be both provided for prediction!")
            if status_1 == 0:
                res_1_status = st.success("Prediction finished successfully!")
            else:
                res_1_status = st.error("Prediction failed! See log for more information!")

    with col_1_2:
        text_1_4 = st.markdown("**Input Mode II - Multiple Structures:**")

        pdb_file_1_2 = st.file_uploader("Upload the PDB host structure:",
                                        type = ["pdb"],
                                        help = "The target host structure that was used for docking of the ligands in PDB file format.",
                                        key = "pdb_file_1_2"
                                        )

        sdf_file_1_2 = st.file_uploader("Upload docked ligand coordinates in SDF format:",
                                        type = ["sdf"],
                                        help = "The coordinates of the docked ligands in SDF format. Not all SD files might be supported. Supported software: GOLD.",
                                        key = "sdf_file_1_2"
                                        )

        if st.button("Predict!", help = "Predict the activity of the given docked protein-ligand complexes with the supplied model."):
            with st.expander("Show logging info:"):
                with st_stdout("info"):
                    if piamodel != None and pdb_file_1_2 != None and sdf_file_1_2 != None:
                        try:
                            # create unique file prefix
                            output_name_prefix = datetime.now().strftime("%b-%d-%Y_%H-%M-%S") + "_" + str(random.randint(10000, 99999))
                            #write files
                            with open(output_name_prefix + pdb_file_1_2.name, "wb") as f1:
                                f1.write(pdb_file_1_2.getbuffer())
                            with open(output_name_prefix + sdf_file_1_2.name, "wb") as f1:
                                f1.write(sdf_file_1_2.getbuffer())
                            with open(output_name_prefix + piamodel.name, "wb") as f3:
                                f3.write(piamodel.getbuffer())
                            # get prediction
                            result_1 = predict_sdf(output_name_prefix + piamodel.name, output_name_prefix + pdb_file_1_2.name, output_name_prefix + sdf_file_1_2.name, tmp_dir_name = output_name_prefix + "_structures")
                            # cleanup
                            os.remove(output_name_prefix + pdb_file_1_2.name)
                            os.remove(output_name_prefix + sdf_file_1_2.name)
                            os.remove(output_name_prefix + piamodel.name)
                            # set status
                            status_1 = 0
                        except Exception as e:
                            this_e = st.exception(e)
                            status_1 = 1
                            try:
                                if os.path.isdir(output_name_prefix + "_structures"):
                                    shutil.rmtree(output_name_prefix + "_structures")
                            except Exception as e_2:
                                this_e_2 = st.exception(e_2)
                    else:
                        status_1 = 1
                        no_file = st.error("Error: Model, PDB host structure and ligands in SDF format have to be provided for prediction!")
            if status_1 == 0:
                res_1_status = st.success("Prediction finished successfully!")
            else:
                res_1_status = st.error("Prediction failed! See log for more information!")

    if result_1 != None:
        st.session_state["prediction_1"] = result_1["dataframe"]

    if "prediction_1" in st.session_state:
        sub_title_1 = st.subheader("Results")
        res_table_1 = st.dataframe(st.session_state["prediction_1"].style.applymap(color_code, subset = "PREDICTION"))

    title_2 = st.title("PIAPredict - Workflow IV")

    text_2_1 = st.markdown("*Predict the activity of protein-ligand complexes by manually specifying important interactions.*")
    text_2_2_txt = "Select one of two input modes for prediction: Either predict a single complex using a PDB file as input "
    text_2_2_txt += "*OR* predict multiple complexes by supplying a host protein structure in PDB format and docked ligand coordinates in SDF format."
    text_2_2 = st.markdown(text_2_2_txt)

    interactions_help_str = "Enter a list of interactions that are important for ligand binding, each interaction present in a protein-ligand complex will increase the score by one. "
    interactions_help_str += "Each interaction has to be in the format as given in the example and must be separated by a comma from the next interaction in the list."
    interactions = st.text_area(label = "Enter a list of interactions (an example is given):",
                                value = "Hydrogen_Bond:TYR383A, Hydrogen_Bond:ASP335A, Pi-Stacking:TRP336A, Hydrogen_Bond:TYR466A, Pi-Stacking:HIS524A",
                                height = 250,
                                help = interactions_help_str
                                )

    cutoff_help_str = "Enter a cutoff for prediction that determines if a protein-ligand complex is labelled as active or not. If the score is greater or equal to the cutoff "
    cutoff_help_str += "the complex is labelled as active, otherwise as inactive. Cutoff has to be a real number (will be cast to int internally). The default cutoff is "
    cutoff_help_str += "'None' which sets the cutoff to 'ceil(nr. of interactions/2)'."
    cutoff = st.text_input(label = "[Optional] Enter a cutoff for prediction:",
                           value = "None",
                           max_chars = 10,
                           help = cutoff_help_str
                           )

    col_2_1, col_2_2 = st.columns(2)

    result_2 = None

    with col_2_1:
        text_2_3 = st.markdown("**Input Mode I - Single Structure:**")

        pdb_file_2_1 = st.file_uploader("Upload a PDB structure:",
                                      type = ["pdb"],
                                      help = "The protein-ligand complex in PDB file format that should be predicted by the model.",
                                      key = "pdb_file_2_1"
                                      )

        if st.button("Predict!", help = "Predict the activity of the given protein-ligand complex with the supplied interactions."):
            with st.expander("Show logging info:"):
                with st_stdout("info"):
                    if pdb_file_2_1 != None:
                        try:
                            # create unique file prefix
                            output_name_prefix = datetime.now().strftime("%b-%d-%Y_%H-%M-%S") + "_" + str(random.randint(10000, 99999))
                            #write files
                            with open(output_name_prefix + pdb_file_2_1.name, "wb") as f1:
                                f1.write(pdb_file_2_1.getbuffer())
                            #process cutoff
                            try:
                                cutoff_2_1 = int(cutoff)
                            except:
                                cutoff_2_1 = None
                            # get prediction
                            result_2 = predict_pdb([i.strip() for i in interactions.split(",")], output_name_prefix + pdb_file_2_1.name, cutoff = cutoff_2_1, name = pdb_file_2_1.name)
                            # cleanup
                            os.remove(output_name_prefix + pdb_file_2_1.name)
                            # set status
                            status_2 = 0
                        except Exception as e:
                            this_e = st.exception(e)
                            status_2 = 1
                    else:
                        status_2 = 1
                        no_file = st.error("Error: PDB structure has to be both provided for prediction!")
            if status_2 == 0:
                res_2_status = st.success("Prediction finished successfully!")
            else:
                res_2_status = st.error("Prediction failed! See log for more information!")

    with col_2_2:
        text_2_4 = st.markdown("**Input Mode II - Multiple Structures:**")

        pdb_file_2_2 = st.file_uploader("Upload the PDB host structure:",
                                        type = ["pdb"],
                                        help = "The target host structure that was used for docking of the ligands in PDB file format.",
                                        key = "pdb_file_2_2"
                                        )

        sdf_file_2_2 = st.file_uploader("Upload docked ligand coordinates in SDF format:",
                                        type = ["sdf"],
                                        help = "The coordinates of the docked ligands in SDF format. Not all SD files might be supported. Supported software: GOLD.",
                                        key = "sdf_file_2_2"
                                        )

        if st.button("Predict!", help = "Predict the activity of the given docked protein-ligand complexes with the supplied interactions."):
            with st.expander("Show logging info:"):
                with st_stdout("info"):
                    if pdb_file_2_2 != None and sdf_file_2_2 != None:
                        try:
                            # create unique file prefix
                            output_name_prefix = datetime.now().strftime("%b-%d-%Y_%H-%M-%S") + "_" + str(random.randint(10000, 99999))
                            #write files
                            with open(output_name_prefix + pdb_file_2_2.name, "wb") as f1:
                                f1.write(pdb_file_2_2.getbuffer())
                            with open(output_name_prefix + sdf_file_2_2.name, "wb") as f1:
                                f1.write(sdf_file_2_2.getbuffer())
                            #process cutoff
                            try:
                                cutoff_2_2 = int(cutoff)
                            except:
                                cutoff_2_2 = None
                            # get prediction
                            result_2 = predict_sdf([i.strip() for i in interactions.split(",")], output_name_prefix + pdb_file_2_2.name, output_name_prefix + sdf_file_2_2.name, cutoff = cutoff_2_2, tmp_dir_name = output_name_prefix + "_structures")
                            # cleanup
                            os.remove(output_name_prefix + pdb_file_2_2.name)
                            os.remove(output_name_prefix + sdf_file_2_2.name)
                            # set status
                            status_2 = 0
                        except Exception as e:
                            this_e = st.exception(e)
                            status_2 = 1
                            try:
                                if os.path.isdir(output_name_prefix + "_structures"):
                                    shutil.rmtree(output_name_prefix + "_structures")
                            except Exception as e_2:
                                this_e_2 = st.exception(e_2)
                    else:
                        status_2 = 1
                        no_file = st.error("Error: PDB host structure and ligands in SDF format have to be provided for prediction!")
            if status_2 == 0:
                res_2_status = st.success("Prediction finished successfully!")
            else:
                res_2_status = st.error("Prediction failed! See log for more information!")

    if result_2 != None:
        st.session_state["prediction_2"] = result_2["dataframe"]

    if "prediction_2" in st.session_state:
        sub_title_2 = st.subheader("Results")
        res_table_2 = st.dataframe(st.session_state["prediction_2"].style.applymap(color_code, subset = "PREDICTION"))
