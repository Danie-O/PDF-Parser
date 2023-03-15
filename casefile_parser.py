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

def generate_preview(x):
    """
    Generates a preview markdown file from the contents of the pdf file passed as input

    Args:
        x (_type_): _description_
    """
    pass

def generate_files(x):
    """
    Generates metadata, preview and technical files for a given pdf file

    Args:
        x (_type_): _description_
    """
    pass

def parse_files(file):
    """
    Parses all PDF files in the input directory by passing each file into the generate_function defined above

    Args:
        file (_type_): _description_
    """
    pass

# define main function to generate all required files(including log files), for all pdf files in a given directory path