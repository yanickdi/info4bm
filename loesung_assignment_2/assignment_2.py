import sys
import pickle
import numpy as np

def mean(data):
    mean_val = sum(data) / len(data)
    assert mean_val == np.mean(data) 
    return mean_val
    
def std(data, bessel=False):
    mean_val = mean(data)
    n = len(data)
    var = sum( (val - mean_val)**2 for val in data) * (1/n)
    std_val = None
    if bessel:
        mean_val = mean(data) *(n/(n-1))
        var = sum( (val - mean_val)**2 for val in data) * (1/n)
        var = var * (n/(n-1))
        std_val = var**(1/2)
        assert round(np.std(data, ddof=1), 5) == round(std_val, 5)
    else:
        std_val = var**(1/2)
        assert round(np.std(data), 5) == round(std_val, 5)
    return std_val

def hearbeat_detection(data, treshold):
    heartbeats = []
    forbidden = False
    for i, val in enumerate(data):
        if val > treshold and not forbidden:
            heartbeats.append(i)
            forbidden = True
        elif val < treshold and forbidden:
            forbidden = False
    return heartbeats

def main():
    filename, sensor_name = sys.argv[1], sys.argv[2]
    all_data = None
    sensor_data = None
    
    with open(filename, 'rb') as pickle_file:
        all_data = pickle.loads(pickle_file.read())
        
    # data is a dict, indexed from 0..len(sensors) - we have to find
    # the right dict by iterating all vals
    sensor_data = [val['data'] for val in all_data.values() if val['name'] == sensor_name][0]
    assert len(sensor_data) == 38400
    
    treshold = mean(sensor_data) + 2 * std(sensor_data)
    heartbeats = hearbeat_detection(sensor_data, treshold)
    
    assert len(heartbeats) == 60
    #store output
    with open(filename.replace('.p', '.csv'), 'wt', encoding='utf-8') as out_file:
        out_file.write(','.join([str(hb) for hb in heartbeats]))
    

if __name__ == '__main__':
    command_line = "s0010_re.p i"
    sys.argv += command_line.split(' ')
    main()
    