import os
import re
import json
from PyPDF2 import PdfFileReader
from pathlib import Path
# import textract
# import pdfminer
import logging
import datetime

"""
    A script for parsing pdf files of court cases and extracting data required to generate the following for each case file;
    - a metadata.json file, a preview.md file, a technical.txt file, an error log file, an info log file
"""
# define paths for the following; 
input_dir = "./input"
output_dir = "./output"
error_log = "./errors.log"
info_log = "./errors.log"

# set up loggers to handle errors and info about erroneous metadata files
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
error_logger = logging.getLogger('error')
error_logger.setLevel(logging.ERROR)
info_logger = logging.getLogger('info')
info_logger.setLevel(logging.INFO)

error_handler = logging.FileHandler('error.log')
error_handler.setLevel(logging.ERROR)
error_logger.addHandler(error_logger)

info_handler = logging.FileHandler('info.log')
info_handler.setLevel(logging.INFO)
info_logger.addHandler(info_handler)

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

def generate_technical(file_path: str):
    """
    Generates a technical text file from the contents of the pdf file passed as input

    Args:
        file_path (str): the path to the pdf file being parsed
    """
    output_file = f""
    pdf = PdfFileReader(file_path)
    pages = pdf._get_num_pages()
    
    with Path(output_file).open(mode='w') as output:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
        output_file.write(text)
    


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

