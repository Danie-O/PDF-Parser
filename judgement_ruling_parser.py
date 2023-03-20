import os
import re
import json
from PyPDF2 import PdfFileReader
from pathlib import Path
import textract
import logging
from datetime import datetime
import subprocess as sp
import ocrmypdf

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


# Function to log errors to file
def log_error(file_name, error_message):
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
    log_entry = f"{now}: Error processing file '{file_name}': {error_message}\n"
    with open(error_log, "a") as f:
        f.write(log_entry)

# Function to log info to file
def log_info(file_name, metadata_file_name, fields_with_error):
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
    error_fields_string = ", ".join(fields_with_error) if len(fields_with_error) > 0 else "None"
    log_entry = f"{now}: Metadata file '{metadata_file_name}' generated from '{file_name}' has the following errors: {error_fields_string}\n"
    with open(info_log, "a") as f:
        f.write(log_entry)

def ocr_scanned_file(file_path, new_file_path):
    # converts a scanned pdf to full text and saves it to a new filepath
    ocrmypdf.ocr(file_path, new_file_path, skip_text=True)

    # output = sp.getoutput("ocrmypdf input.pdf output.pdf")
    # if not re.search("PriorOcrFoundError: page already has text!",output):
    # print("Uploaded scanned pdf")
    # else:
    #     print("Uploaded digital pdf")

#Default function to parse pdf and write text to file
def write_to_file(file_path):
    file = file_path
    pdf = PdfFileReader(file)

    with open("output_path.extension", "w") as f:
        for page in range(pdf.numPages):
            page_obj = pdf.getPage(page)

            try:
                text = page_obj.extract_text()
            except Exception as e:
                log_error(file_path, e)
            else:
                f.write(text)
        f.close()             


# define helper functions to handle PDF parsing and output files generation
def generate_metadata(file_path: str):
    """
    Extracts metadata from a pdf file and returns a dictionary which contains the required metadata fields and values

    Args:
        file_path (str): _description_
    """
    with open(file_path, 'rb') as file:

        pdf = PdfFileReader(file)
        
        # Extract text from each page in PDF
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
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
    pdf = PdfFileReader(file_path)

    # Define regex patterns to match sections and paragraphs
    section_pattern = re.compile(r"__section__ (.+)")
    paragraph_pattern = re.compile(r"__paragraph__ (.+)")

    text = ''
    for page in pdf.pages:
        text += page.extract_text()

    # with Path(output_file).open(mode='w') as output:
    #     text = ''
    #     for page in pdf.pages:
    #         text += page.extract_text()
    #     output_file.write(text)
    

def generate_output_file_path(file_path):
    """_summary_

    Args:
        file_path (_type_): _description_
    """
    with open(file_path, 'rb') as file:

            pdf = PdfFileReader(file)
            
            # Extract text from first page in PDF
            first_page = pdf._get_page(0)
            first_page_text = first_page.extract_text()

            # Use textract to extract text from scanned PDFs
            # if not text:
            #     text = textract.process(pdf_path, method='tesseract', language='eng')
                
            """ Extract short title(plaintiff vs. defendant) to construct output filepath """
            # Define regular expressions for the plaintiff/appellant and defendant names
            plaintiff_regex = r'PLAINTIFF\/APPELLANT\s+(?P<plaintiff>[A-Z\s\.]+)'
            defendant_regex = r'VRS\s+(?P<defendant>[A-Z\s\.]+)'

            # Search for the plaintiff/appellant and defendant/respondent names in the text
            plaintiff_match = re.search(plaintiff_regex, first_page_text)
            defendant_match = re.search(defendant_regex, first_page_text)

            # Extract the names of the first plaintiff/appellant and defendant/respondent
            plaintiff_name = plaintiff_match.group('plaintiff').strip().split()[0]
            defendant_name = defendant_match.group('defendant').strip().split()[0]

            # Construct the short title using the first names of the plaintiff/appellant and defendant/respondent
            short_title = f"{plaintiff_name} vs {defendant_name}"

            # Extract case number to construct output filepath
            case_number_regex = re.compile(r'([JG]\d+/\d+/\d+)', re.IGNORECASE)
            case_number_match = case_number_regex.search(first_page_text)
            case_number = case_number_match.group(1).upper()

            # Get timestamp to construct output filepath
            timestamp = datetime.now()

            # Construct output filepath
            output_file_path = "{}_{}_{}".format(short_title, case_number, timestamp)

    return output_file_path


def generate_files(file_path: str):
    """
    Generates metadata, preview and technical files for a given pdf file

    Args:
        file_path (str): _description_
    """
    filename = generate_output_file_path(file_path=file_path)
    metadata = generate_metadata(file_path)
    preview = generate_preview(file_path)
    technical = generate_technical(file_path)
    

    with open(filename + '_metadata.txt', 'w') as f:
        for key, value in metadata.items():
            f.write(key + ': ' + str(value) + '\n')
    with open(filename + '_preview.md', 'w') as f:
        f.write(preview)
    with open(filename + '_technical.txt', 'w') as f:
        f.write(technical)
    pass

def parse_files(directory: str):
    """
    Parses all PDF files in the input directory by passing each file into the generate_function defined above

    Args:
        directory (str): _description_
    """
    pass

# define main function to generate all required files(including log files), for all pdf files in a given directory path



if __name__ == "__main__":
    print(generate_output_file_path("./input/2022-ghasc-1.pdf"))
    