import main
from networks.throughput import Throughput
from analyser.graph import Graph
import analyser.test_statistics
import analyser.analysis_data as analysis_data
from analyser.distribution import Distribution
from environment.house import House
import logging


def light_camera(conf1, conf2, file):
    packet_camera, packet_light = main.execute_multiple_config("mapping_light/" + conf1, "mapping_light/" + conf2, file)

    timestamp_rate_camera = Throughput([x[0] for x in packet_camera], 1)
    timestamp_rate_light = Throughput([x[0] for x in packet_light], 1)
    list_threshold = timestamp_rate_light.check_threshold(1)

    # size (in second) for the interval after and before
    size = 15
    # before delay of 2
    is_light_and_camera = sub_array(timestamp_rate_camera, size, list_threshold, 0, 2)

    graph_representation = Graph(timestamp_rate_camera.packet_per_second_tuple, 'time', 'size',
                                 "Comparison light camera",
                                 True, 'camera')
    graph_representation.create_graph()
    graph_representation.add_vertical_line(is_light_and_camera, 'light_same_room')

    # for showing 2 same time
    graph_representation.add_data(timestamp_rate_light.packet_per_second_tuple, 'light')
    graph_representation.show_graph()
    return is_light_and_camera


def light_two_camera(conf1, conf2, conf3, file):
    """
    :param conf1 : configuration for the light
    :param conf2 : configuration first camera
    :param conf3 : configuration for the second camera
    """
    is_with_light_cam1 = light_camera(conf2, conf1, file)
    is_with_light_cam2 = light_camera(conf3, conf1, file)
    match_between_two_camera = (2*(len(set(is_with_light_cam1) & set(is_with_light_cam2))))/(len(is_with_light_cam1+is_with_light_cam2))
    print('***Percentage matching time between 2 camera *** :' + str(match_between_two_camera))
    return is_with_light_cam1, is_with_light_cam2, match_between_two_camera

def only_camera(conf1, file):

    packet_cam1 = main.execute_single_config("mapping_light/" + conf1, file)
    timestamp_rate_cam = Throughput([x[0] for x in packet_cam1], 1)
    timestamp_rate_cusum_cam = analysis_data.cusum_up(timestamp_rate_cam.packet_per_second_tuple)
    timestamp_rate_cusum_cam_lo = analysis_data.cusum_lo(timestamp_rate_cam.packet_per_second_tuple)

    graph = Graph(timestamp_rate_cusum_cam, 'time', 'size', "camera1 cusum",
                  True, 'camera')

    acceptable_interval_cam1 = analysis_data.generate_interval(timestamp_rate_cusum_cam, 1)
    acceptable_interval_cam1_cus_lo = analysis_data.generate_interval(timestamp_rate_cusum_cam_lo, 1)

    acceptable_interval_cam1 = acceptable_interval_cam1 + acceptable_interval_cam1_cus_lo
    # start_acceptable_interval = [x[0] for x in acceptable_interval_cam1]

    acceptable_interval_cam1 = sorted(acceptable_interval_cam1, key=lambda x: x[0])
    # size (in second) for the interval after and before
    size = 15
    # before delay of 2
    is_light_and_camera = sub_array(timestamp_rate_cam, size, acceptable_interval_cam1, 0, 2)

    graph_representation = Graph(timestamp_rate_cam.packet_per_second_tuple, 'time', 'size',
                                 "Comparison light camera",
                                 True, 'camera')
    graph_representation.create_graph()
    graph_representation.add_vertical_line(is_light_and_camera, 'light_same_room')

    graph.create_graph()
    graph.show_graph()


def sub_array(timestamp_rate, size, time_list, shift, delay):
    """
    :param timestamp_rate: list of tuple where (time, number of packets)
    :param size: size (in second) for the interval after and before
    :param time_list: list where light send data over a certain threshold
    :param shift: translate the interval
    :param delay: value that will no take in account after the potential cut
    :return: list with time where a cut is detected
    """
    time = [x[0] for x in time_list]
    last = 0
    list_is_present = []
    list_is_in_same_room = []

    my_house = House()

    for y in time:
        if last < y - delay - 4 and abs(
                timestamp_rate.start - y) > size:  # choose arbitrarily to avoid similar graph ( in future merge the intervals)
            logging.debug('time %s', y)

            subarray = timestamp_rate.get_interval(size, y, shift)
            statistics, pvalue, distribution_1, distribution_2 = test_statistics.difference_data(
                [x[1] for x in subarray]
                , size, delay)

            if pvalue is None:
                break
            last = y
            h0 = hypothesis_check_update_threshold(list_is_present, pvalue, y)

            if not h0:
                is_room = my_house.pattern_compare(distribution_1, distribution_2)
                if is_room:
                    list_is_in_same_room.append(y)
    print('***Threshold*** : '+str(my_house.in_same_room))
    print('***UP distribution*** : mean %s , std %s , number %s ' % (my_house.distribution_up.mean,
          my_house.distribution_up.std, my_house.distribution_up.number_data))
    print('***Down distribution*** : mean %s , std %s , number %s ' % (my_house.distribution_down.mean,
          my_house.distribution_down.std, my_house.distribution_down.number_data))
    # return list_is_present
    return list_is_in_same_room


def hypothesis_check_update_threshold(list_is_present, pvalue, y):
    alpha = 0.05
    if pvalue > alpha / 2:
        # print('H0 accepted -> mean_left=mean_right')
        return True
    else:
        # print('H0 rejected')
        list_is_present.append(y)
        return False
