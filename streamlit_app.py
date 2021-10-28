#!/usr/bin/env python3

# PIA - STREAMLIT WEBUI
# 2021 (c) Micha Johannes Birklbauer
# https://github.com/michabirklbauer/
# micha.birklbauer@gmail.com

"""
#####################################################
##                                                 ##
##            -- STREAMLIT MAIN APP --             ##
##                                                 ##
#####################################################
"""

import streamlit as st
from scripts import PIAWebBase, PIAWebScore, PIAWebPredict

#
def main():

    about_str = \
    """
    **PIA/PIAWeb 1.0.0**

    **PIA** - short for **Protein Interaction Analyzer** - is a tool for automatic identification of important interactions and interaction-frequency-based scoring in protein-ligand complexes.

    **Contact:** [Micha Birklbauer](mailto:micha.birklbauer@gmail.com)

    **License:** [MIT License](https://github.com/michabirklbauer/piaweb/blob/master/LICENSE.md)
    """

    st.set_page_config(page_title = "PIA - Protein Interaction Analyzer",
                       page_icon = ":test_tube:",
                       layout = "centered",
                       initial_sidebar_state = "expanded",
                       menu_items = {"Get Help": "https://github.com/michabirklbauer/PIA/discussions",
                                     "Report a bug": "https://github.com/michabirklbauer/PIA/issues",
                                     "About": about_str}
                       )

    pages = ("PIA: Extract Interactions", "PIAScore: Score Complexes", "PIAPredict: Predict Complexes")

    title = st.sidebar.title("PIA - Protein Interaction Analyzer")

    logo = st.sidebar.image("img/pmu_logo.jpg", caption = "PIA was developed in cooperation with the Institute of Pharmacy of the Paracelsus Medical Private University Salzburg.")

    page = st.sidebar.selectbox(label = "Select a Workflow:",
                                options = pages,
                                index = 0,
                                help = "Select a workflow that you want to run."
                                )

    doc_str = "**PIA** - short for **Protein Interaction Analyzer** - is a tool for automatic identification of important "
    doc_str += "interactions and interaction-frequency-based scoring in protein-ligand complexes. To get started make sure to read "
    doc_str += "the documentation in the [PIA Wiki](https://github.com/michabirklbauer/PIA/wiki). For general help, questions, suggestions or any other feedback please refer "
    doc_str += "to the [GitHub repository](https://github.com/michabirklbauer/PIA/discussions) or contact us directly!"
    doc = st.sidebar.markdown(doc_str)

    contact_str = "**Contact:** [Micha Birklbauer](mailto:micha.birklbauer@gmail.com)"
    contact = st.sidebar.markdown(contact_str)

    license_str = "**License:** [MIT License](https://github.com/michabirklbauer/piaweb/blob/master/LICENSE.md)"
    license = st.sidebar.markdown(license_str)

    if page == "PIA: Extract Interactions":
        PIAWebBase.main()
    elif page == "PIAScore: Score Complexes":
        PIAWebScore.main()
    elif page == "PIAPredict: Predict Complexes":
        PIAWebPredict.main()
    else:
        PIAWebBase.main()

if __name__ == "__main__":
    main()
