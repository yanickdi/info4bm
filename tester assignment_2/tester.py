STUDENT_FOLDER = 'student_solution'
REFERENCE_PICKLE = 'reference_pickle.p'
REFERENCE_CSV = 'reference_s0010_re.csv'
SENSOR_NAME = 'i'

COPY_FILES = [REFERENCE_PICKLE]
EXPECTED_OUTPUT_FILE = 'reference_pickle.csv'

import subprocess
import os
import filecmp
import re
from difflib import ndiff
from shutil import copy
from os.path import exists, join

def check_csv_file(filename):
    if exists(filename):
        print(' + CSV File vorhanden')
    else:
        print(' - CSV File nicht vorhanden')
        return False
    if filecmp.cmp(REFERENCE_CSV, filename):
        print(' + CSV Datei ist korrekt')
    else:
        print(' - CSV Datei unterschiedlich:')
        with open(REFERENCE_CSV) as right_csv, open(filename) as wrong_csv:
            try:
                right_vals = right_csv.read().split(',')
                wrong_vals = wrong_csv.read().split(',')
                if len(right_vals) != len(wrong_vals):
                    print('    {} anstatt {} Werte gefunden'.format(len(wrong_vals), len(right_vals)))
                else:
                    print('    Anzahl der Werte ist korrekt')
                    for i, vals in enumerate(zip(right_vals, wrong_vals)):
                        if vals[0] != vals[1]:
                            print("index {}: '{}' statt '{}'".format(i, vals[0], vals[1]))
            except:
                try:
                    print('   Kann CSV Datei nicht parsen, zeige diff:')
                    diff = ndiff(right_csv.readlines(),
                                 wrong_csv.readlines())
                    print(''.join(diff), end="")
                except:
                    print('    Geht auch nicht, vermutlich binär Datei!')
                    

def main():
    #copy files to student folder:
    for file in COPY_FILES:
        copy(file, STUDENT_FOLDER)
    
    # call student solution
    process = subprocess.Popen(['python', 'assignment_2.py', REFERENCE_PICKLE, SENSOR_NAME],
        stdout=None, cwd=STUDENT_FOLDER)
    exit_code = process.wait()
    if exit_code != 0:
        print(' - Laufzeitfehler im Programm')
    else:
        print(' + Programm laeuft')
        
    # check csv file
    check_csv_file(join(STUDENT_FOLDER, EXPECTED_OUTPUT_FILE))
    
main()