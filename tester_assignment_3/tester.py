STUDENT_FOLDER = 'student_solution'
PATIENT = 'reference_patient'
REFERENCE_PICKLE = PATIENT + '.p'
REFERENCE_CSV = PATIENT + '.csv'
SENSOR_NAME = 'i'

COPY_FILES = [REFERENCE_PICKLE, REFERENCE_CSV]
EXPECTED_OUTPUT_FILE = PATIENT + '.pdf'

import subprocess
import os
from shutil import copy
from os.path import exists, join
import webbrowser

def check_pdf_file(filename):
    if exists(filename):
        print(' + PDF File vorhanden')
        return True
    else:
        print(' - PDF File nicht vorhanden')
        return False

def main():
    pdf_file = join(STUDENT_FOLDER, EXPECTED_OUTPUT_FILE)
    # remove old output file:
    try: os.remove(pdf_file)
    except: pass
    
    #copy files to student folder:
    for file in COPY_FILES:
        copy(file, STUDENT_FOLDER)
    
    # call student solution
    process = subprocess.Popen(['python', 'assignment_3.py', PATIENT, SENSOR_NAME],
        stdout=None, cwd=STUDENT_FOLDER)
    exit_code = process.wait()
    if exit_code != 0:
        print(' - Laufzeitfehler im Programm')
        exit()
    else:
        print(' + Programm laeuft')
        
    # check csv file
    if check_pdf_file(pdf_file):
        webbrowser.open(join(STUDENT_FOLDER, EXPECTED_OUTPUT_FILE))
    
main()