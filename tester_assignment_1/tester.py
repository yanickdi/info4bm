STUDENT_FOLDER = 'student_solution'
REFERENCE_PICKLE = 'reference_pickle.p'
REFERENCE_PICKLE_NUM_FRAMES = 38400

COPY_FILES = ['s0010_re.dat']
EXPECTED_OUTPUT_FILE = 's0010_re.p'

import subprocess
import os
from shutil import copy
from os.path import exists, join
import pickle

def check_pickle_file(student_filename):
    with open(student_filename, 'rb') as student_file, open(REFERENCE_PICKLE, 'rb') as ref_file:
        ref_dict = pickle.load(ref_file)
        stud_dict = None
        try:
            stud_dict = pickle.load(student_file)
        except:
            print(' - Pickle File konnte nicht geladen werden')
            return False
            
    if type(stud_dict) is not type(ref_dict):
        print(' - Pickle File enthält kein Dictionary')
        return False
        
    #check all sensors:
    for sensor_num in ref_dict.keys():
        # first, compare the length of both
        if len(stud_dict[sensor_num]['data']) != len(ref_dict[sensor_num]['data']):
            print(' - Datenlänge des Sensors {} stimmt nicht überein ({} statt {})'.format(
                ref_dict[sensor_num]['name'], len(stud_dict[sensor_num]['data']),
                len(ref_dict[sensor_num]['data'])))
            return False
        # check all data
        for i, data in enumerate(ref_dict[sensor_num]['data']):
            pos_str = "dict[{}]['data'][{}]".format(sensor_num, i)
            stud_data = stud_dict[sensor_num]['data'][i]
            # check datatype
            if type(stud_data) is not type(data):
                print(' - Datentyp bei {} stimmt nicht ueberein ({} statt {})'.format(
                    pos_str, type(stud_data), type(data)))
                return False
            # check value
            if stud_data != data:
                print(' - Wert bei {} stimmt nicht ueberein ({} statt {})'.format(
                    pos_str, stud_data, data))
                return False
        
        return True

#copy files to studen folder:
for file in COPY_FILES:
    copy(file, STUDENT_FOLDER)

process = subprocess.Popen(['python', 'assignment_1.py', 's0010_re.dat', str(REFERENCE_PICKLE_NUM_FRAMES)],
    stdout=None, cwd=STUDENT_FOLDER)
process.wait()

if exists(join(STUDENT_FOLDER, EXPECTED_OUTPUT_FILE)):
    print(' + Pickle File vorhanden')
    success = False
    try:
        success = check_pickle_file(join(STUDENT_FOLDER, EXPECTED_OUTPUT_FILE))
    except:
        print(' - Pickle File invalid')
    if success:
        print(' + Alle Tests bestanden')
    os.remove(join(STUDENT_FOLDER, EXPECTED_OUTPUT_FILE))
else:
    print(' - Pickle File nicht vorhanden')