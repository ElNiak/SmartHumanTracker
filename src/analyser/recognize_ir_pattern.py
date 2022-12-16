import main
from networks.throughput import Throughput
from analyser.graph import Graph
import analyser.frequent_sequence_miner

def IR_pattern_finder(conf1, file):
    packet_cam1 = main.execute_single_config(conf1, file)
    timestamp_rate_cam1 = Throughput([x[0] for x in packet_cam1], 1)
    graph_cam = Graph(timestamp_rate_cam1.packet_per_second_tuple, 'Timestamp (seconds)', 'Packets/Second',
                      "Traffic rate with the infrared transition detected",
                      True, 'Camera with infrared auto')


    calculate_diff_results(timestamp_rate_cam1)

    #-Uncoment if dataset to mining data
    #frequent_sequence_miner.main("data.dat", 16)

    # on
    pattern = [3, -2, 0, 3]
    # pattern = [-2, 0, 1]

    pattern_found = find_interval_time_pattern("data.dat", pattern)
    print(pattern_found)
    graph_cam.add_vertical_line(pattern_found, 'pattern match')

    graph_cam.create_graph()
    graph_cam.show_graph()



def find_interval_time_pattern(file, pattern):
    time_found_parttern = list()
    indices = 0
    file = open(file, "r")
    for line in file:
        split_line = line.split(" ")
        if split_line[0] == "\n":
            indices = 0
        else:
            print(line)
            print(split_line)
            print(split_line[0])
            if int(split_line[0]) == pattern[indices]:
                indices = indices + 1
                # all found
                if indices == len(pattern) - 1:
                    time_found_parttern.append(int(split_line[1]))
                    indices = 0
    return time_found_parttern

def classification_value(value):
    if value < -20:
        return -2
    if value < -10:
        return -1

    if value < -5:
        return 0
    if value < 5:
        return 0

    if value < 10:
        return 1
    if value < 20:
        return 2
    else:
        return 3


def filter_repeated(data):
    new_data = []
    is_present = 0
    threshold = 5
    size_max = 7
    size = 0
    for x in data:
        if -10 < x[1] <10:
            size = size +1
            is_present = is_present + 1
            if is_present > threshold :
                is_present = is_present + 1
            else:
                new_data.append(x)
        else:
            size = size + 1
            if is_present > threshold or size > size_max:
                new_data.append((0, 0))
                new_data.append(x)
                is_present = 0
                size = 0
            else:
                is_present = 0
                new_data.append(x)
    return new_data

def calculate_diff_results(timestamp_rate):
    timestamp_rate.diff_result()
    f = open("data.dat", "w+")
    data_filetered = filter_repeated(timestamp_rate.packet_per_second_tuple)

    f.write('\n'.join('{} {}'.format(classification_value(x[1]), x[0]) for x in data_filetered))
    f.close()

    # open file in read mode
    file = open("data.dat", "r")
    replaced_content = ""
    # looping through the file
    is_first = True
    for line in file:
        if line != "\n" and is_first:
            replaced_content = replaced_content + "\n"
        # stripping line break
        line = line.strip()
        # replacing the texts
        new_line = line.replace("0 0", "")
        # concatenate the new string and add an end-line break
        replaced_content = replaced_content + new_line + "\n"
        is_first = False

    # close the file
    file.close()
    # Open file in write mode
    write_file = open("data.dat", "w")
    # overwriting the old file contents with the new/replaced content
    write_file.write(replaced_content)
    # close the file
    write_file.close()