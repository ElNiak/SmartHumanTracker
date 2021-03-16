import numpy as np


def find_nearest(array, value):
    """
    :param array: [a,b,c]
    :param value:
    :return: the index of an element of the table where whe have the closest element of value
    """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx


class Throughput:

    def __init__(self, timestamp, second):
        """
        :param int second: size in second of the interval where we count the number of packets
        :param collection.iterable timestamp: collection of all timestamp packets
        :return: list of tuple list(x,y) where x is time and y number packets per interval
        """
        start = timestamp[0]

        end = timestamp[len(timestamp) - 1]
        self.start = start
        self.end = end

        packet_per_second = [0] * int(((end - start) * (1 / second)) + 1)
        real_time = list(range(start, start + len(packet_per_second), 1))
        for x in timestamp:
            packet_per_second[int((x - start) * (1 / second))] += 1
        packet_per_second_tuple = list(zip(real_time, packet_per_second))
        # remove the first second because was already started before the launch
        # and the last second because she's not finish
        packet_per_second_tuple = packet_per_second_tuple[1:-1]

        self.packet_per_second_tuple = packet_per_second_tuple

    def get_interval(self, size, time, shift):
        """
        :param size: size of the (or the right) part of the subarray around the time value
        :param time: value that we want the most close in our array to have a right and left part
        :param shift: shift to the right from the array around the value
        :return: a subarray of data between arround the time value
        """
        a = find_nearest([x[0] for x in self.packet_per_second_tuple], time)
        subdata = self.packet_per_second_tuple[a - size + shift:a + size + 1 + shift]
        return subdata

    def check_threshold(self, threshold):
        """
        :param self: list of tuple (x,y) where x time and y packet/interval
        :param threshold: filter value equal or over upper this threshold
        :return: list filter with the threshold
        """
        return [x for x in self.packet_per_second_tuple if x[1] >= threshold]

