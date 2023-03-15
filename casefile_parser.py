"""
    A script for parsing pdf files of court cases and extracting data required to generate the following for each case file;
    - a metadata.json file
    - a preview.md file
    - a technical.txt file
    - an error log file
    - an info log file
"""

import os
import re
import json
import PyPDF2
import datetime

# define helper functions to handle PDF parsing and output files generation
def extract_metadata(pdf):
    """
    Extracts metadata from a pdf file returns a dictionary which contains the required metadata fields and values

    Args:
        pdf (_type_): _description_
    """
    pass