import csv
from util import isfloat
from os import path
from waveform import GuitarWaveform

def read(f, positions=['0', '1', '2', '3', '4', '5'], strings=['E', 'A'], 
        frets=['0', '3', '5', '7', '9', '12']):
    """Tries to read the data in f

    If f is a file the data will be read from the file, otherwise if f is a 
    folder the program will try to read all csv files

    Arguments:
        f - folder or file
        strings - The strings to analyze

    Returns:
        An array containing the data

    TODO:
        Implement the non-recursive behavior
    """
    data = []

    if path.isfile(f):
        with open(f, newline='') as csvfile:
            values = []
            
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                if not isfloat(row[0]):
                    if 'Sampling Period' in row[0]:
                        fs = 1 / float(row[1])
                    elif 'Vertical Scale' in row[0]:
                        v_scale = float(row[1])
                    elif 'Horizontal Scale' in row[0]:
                        h_scale = float(row[1])
                    else:
                        continue
                else:
                    values.append(int(row[0]))

            return GuitarWaveform(values, fs, v_scale, h_scale, f)

    elif path.isdir(f):
        for i in positions:
            for j in frets:
                for k in strings:
                    with open(path.join(f, i, j, k, 'DS0000.CSV'), 
                            newline='') as csvfile:
                        values = []

                        reader = csv.reader(csvfile, delimiter=',')
                        for row in reader:
                            if not isfloat(row[0]):
                                if 'Sampling Period' in row[0]:
                                    fs = 1 / float(row[1])
                                elif 'Vertical Scale' in row[0]:
                                    v_scale = float(row[1])
                                elif 'Horizontal Scale' in row[0]:
                                    h_scale = float(row[1])
                                else:
                                    continue
                            else:
                                values.append(int(row[0]))

                    data.append(GuitarWaveform(values, fs, v_scale, h_scale, 
                        f + i + '/' + j + '/' + k))

        return data

