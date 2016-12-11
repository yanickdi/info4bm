import sys, struct, pickle

def parse_data_file(filename, num_frames):
    """Reads the file and returns a sensor_data dictionary"""
    sensor_data = {0: {"name": "i", "data": []},
                    1: {"name": "ii", "data": []},
                    2: {"name": "iii", "data": []},
                    3: {"name": "avr", "data": []},
                    4: {"name": "avl", "data": []},
                    5: {"name": "avf", "data": []},
                    6: {"name": "v1", "data": []},
                    7: {"name": "v2", "data": []},
                    8: {"name": "v3", "data": []},
                    9: {"name": "v4", "data": []},
                    10: {"name": "v5", "data": []},
                    11: {"name": "v6", "data": []}
                  }
    with open(filename, 'rb') as filep:
        for frame_index in range(num_frames):
            for lead in range(12):
                # read a signed short (2 bytes)
                shortVal = struct.unpack('h', filep.read(2))[0]
                sensor_data[lead]['data'].append(shortVal)
    return sensor_data
 
def dump_data(filename, sensor_data):
    assert filename.split('.')[-1] != 'dat'
    with open(filename, 'wb') as filep:
        pickle.dump(sensor_data, filep)
    
def main():
    if len(sys.argv) != 3:
        print('usage: python {} <data_file_name> <num_frames>'.format(sys.argv[0]))
        return -1;
    inp_filename = sys.argv[1]
    num_frames = sys.argv[2]
    out_filename = '.'.join(inp_filename.split('.')[0:-1]) + '.p'
    
    sensor_data = parse_data_file(sys.argv[1], int(sys.argv[2]))
    dump_data(out_filename, sensor_data)
    return 0
    
if __name__ == '__main__':
    sys.exit(main())