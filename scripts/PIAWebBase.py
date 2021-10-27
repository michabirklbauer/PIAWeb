#!/usr/bin/env python3

# PIA - STREAMLIT WEBUI - BASE
# 2021 (c) Micha Johannes Birklbauer
# https://github.com/michabirklbauer/
# micha.birklbauer@gmail.com

"""
#####################################################
##                                                 ##
##       -- STREAMLIT PIA BASE FUNCTIONS --        ##
##                                                 ##
#####################################################
"""

import os
import json
import shutil
import urllib.request as ur
from datetime import datetime
import streamlit as st
from scripts.redirect import *
from PIA.PIA import PIA
from PIA.PIA import Preparation

#
def return_csv(PIAResult):

    frequencies_csv = "Interaction,Frequency\n"
    for key in PIAResult.i_frequencies:
        frequencies_csv = frequencies_csv+ str(key) + "," + str(PIAResult.i_frequencies[key]) + "\n"

    return frequencies_csv

#
#@st.cache
def extract_codes(list_of_codes, normalize = True):

    # create list of PDB links
    filenames = [i + ".pdb" if i.split(".")[-1] != "pdb" else i for i in list_of_codes]
    download_links = ["https://files.rcsb.org/download/" + i for i in filenames]

    # download files
    for i, link in enumerate(download_links):
        ur.urlretrieve(link, filenames[i])
        print("Downloaded ", filenames[i])

    # extract interactions and frequencies
    result = PIA(filenames, normalize = normalize)

    # cleanup
    for f in filenames:
        os.remove(f)

    return result

#
#@st.cache
def extract_sdf(pdb_file, sdf_file, poses = "best", normalize = True):

    # create necessary directories
    structures_directory = "piascript_structures_tmp"
    structures_path = os.path.join(os.getcwd(), structures_directory)
    os.mkdir(structures_path)

    # write uploaded files to tmp directory
    with open("pdb_file.pdb", "wb") as f1:
        f1.write(pdb_file.getbuffer())
    with open("sdf_file.sdf", "wb") as f2:
        f2.write(sdf_file.getbuffer())

    # extract interactions and frequencies
    p = Preparation()
    pdb = p.remove_ligands("pdb_file.pdb", "pdb_file_cleaned.pdb")
    ligands = p.get_ligands("sdf_file.sdf")
    sdf_metainfo = p.get_sdf_metainfo("sdf_file.sdf")
    ligand_names = sdf_metainfo["names"]
    structures = p.add_ligands_multi("pdb_file_cleaned.pdb", "piascript_structures_tmp", ligands)
    result = PIA(structures, ligand_names = ligand_names, poses = poses, path = "current", normalize = normalize)

    # cleanup
    shutil.rmtree("piascript_structures_tmp")
    os.remove("pdb_file.pdb")
    os.remove("pdb_file_cleaned.pdb")
    os.remove("sdf_file.sdf")

    return result

#
def main():

    if os.path.isdir("piascript_structures_tmp"):
        shutil.rmtree("piascript_structures_tmp")

    title = st.title("PIA - Workflow I")

    text_1 = st.markdown("*Extract protein-ligand interactions and their corresponding frequencies.*")
    text_2 = st.markdown("Select one of two input modes: Either supply a list of PDB codes from the [Protein Data Bank](https://www.rcsb.org/) or upload a host PDB structure and ligand coordinates in SDF format.")

    col_1, col_2 = st.columns(2)

    with col_1:

        text_1_1 = st.markdown("**Input Mode I - PDB Codes:**")

        pdb_codes = st.text_area(label = "Enter a list of PDB codes (an example is given):",
                                 value = "5FP0,5MWA,6AUM,6FR2,6HGV",
                                 height = 250,
                                 help = "Enter a list of 4 character PDB identifier codes separated by commas to analyze them. For example: '5FP0,5MWA,6AUM,6FR2,6HGV'")

    with col_2:

        text_2_1 = st.markdown("**Input Mode II - PDB/SDF files:**")

        pdb_file = st.file_uploader("Upload the PDB host structure:",
                                    type = ["pdb"],
                                    help = "The target host structure that was used for docking of the ligands in PDB file format."
                                    )

        sdf_file = st.file_uploader("Upload docked ligand coordinates in SDF format:",
                                    type = ["sdf"],
                                    help = "The coordinates of the docked ligands in SDF format. Not all SD files might be supported. Supported software: GOLD."
                                    )

    col_1b, col_2b = st.columns(2)

    result = None

    with col_1b:
        if st.button("Run!", help = "Run analysis with PDB codes as input."):
            pdb_codes_processed = [i.strip() for i in pdb_codes.split(",")]
            with st.expander("Show logging info:"):
                with st_stdout("info"):
                    try:
                        result = extract_codes(pdb_codes_processed)
                        status_1 = 0
                    except Exception as e:
                        this_e = st.exception(e)
                        status_1 = 1
            if status_1 == 0:
                res_status_1 = st.success("Analysis finished successfully!")
            else:
                res_status_1 = st.error("Analysis stopped prematurely! See log for more information!")

    with col_2b:
        if st.button("Run!", help = "Run analysis with PDB/SDF as input."):
            with st.expander("Show logging info:"):
                with st_stdout("info"):
                    if pdb_file != None and sdf_file != None:
                        try:
                            result = extract_sdf(pdb_file, sdf_file)
                            status_2 = 0
                        except Exception as e:
                            this_e = st.exception(e)
                            status_2 = 1
                    else:
                        status_2 = 1
                        no_file = st.error("Error: PDB and SDF have to be both provided for this input mode!")
            if status_2 == 0:
                res_status_2 = st.success("Analysis finished successfully!")
            else:
                res_status_2 = st.error("Analysis stopped prematurely! See log for more information!")

    if result != None:
        st.session_state["csv_file"] = return_csv(result)
        st.session_state["json_file"] = json.dumps(result.result)
        st.session_state["plot"] = result.plot("Results of PIA - Workflow I")

    if "plot" in st.session_state:
        plot = st.pyplot(st.session_state["plot"])

    if "csv_file" in st.session_state or "json_file" in st.session_state:
        with st.expander("Download Results:"):
            if "csv_file" in st.session_state:
                csv = st.download_button(label = "Download CSV!",
                                         data = st.session_state["csv_file"],
                                         file_name = "result.csv",
                                         mime = "text/csv",
                                         help = "Download interactions and frequencies in CSV file format."
                                         )
            if "json_file" in st.session_state:
                jsf = st.download_button(label = "Download JSON!",
                                         data = st.session_state["json_file"],
                                         file_name = "result.json",
                                         mime = "text/json",
                                         help = "Download interactions, frequencies an structure information in JSON file format."
                                         )
