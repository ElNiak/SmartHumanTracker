import numpy as np


def cusum_up(data):
    """
    :param data:
    :return: cusum value for all data
    """
    cus = [(0, 0)]
    data_without_time = [value[1] for value in data]
    mean = np.mean(data_without_time)
    std = np.std(data_without_time)
    for i in range(1, len(data)):
        cusum_time = data[i][0], (cusum_calculation_up(data[i][1], mean,
                                                       cus[i - 1][1], std))
        cus.append(cusum_time)
    cus.pop(0)
    # print(cus)
    return cus


def cusum_lo(data):
    """
    :param data:
    :return: cusum value for all data
    """
    cus = [(0, 0)]
    data_without_time = [value[1] for value in data]
    mean = np.mean(data_without_time)
    std = np.std(data_without_time)
    for i in range(1, len(data)):
        cusum_time = data[i][0], (cusum_calculation_lo(data[i][1], mean,
                                                       cus[i - 1][1], std))
        cus.append(cusum_time)
    cus.pop(0)
    # print(cus)
    return cus


def cusum_calculation_up(rate, mean, previous, variance):
    """
    :param rate: rate from one sequence
    :param mean: packet rate in mean to detect variation
    :param previous: value cusum from the previous calculation
    :param variance: to evaluate the k for the tolerance
    :return: cusum value for the rate interval
    """
    # mou 1 or 1/2 standard deviation
    k = 0.5 * variance
    return max(0, previous + rate - mean - k)


def cusum_calculation_lo(rate, mean, previous, variance):
    """
    :param rate: rate from one sequence
    :param mean: packet rate in mean to detect variation
    :param previous: value cusum from the previous calculation
    :param variance: to evalute the k for the tolerance
    :return: cusum value for the rate interval
    """
    # mou 1 or 1/2 standart deviantion
    k = 0.5 * variance
    return max(0, previous - rate + mean - k)


def smooth(data, coefficient):
    """
    :param data: axe values that we want smooth
    :param coefficient: if 3 then x 0 1 2
    :return: values smoothed
    """
    data_smooth = []
    for pkt in range(len(data) - 1 - coefficient):
        sum_smooth = 0
        for x in range(coefficient):
            sum_smooth = data[pkt + x] + sum_smooth
        mean = sum_smooth / coefficient
        data_smooth.append(mean)
    return data_smooth


def generate_interval(data, threshold):
    """
    :param data:
    :param threshold: find interval where all value are below this value
    :return:list of interval where all data are over a threshold
    """
    up = False
    left = 0
    right = 0
    list_interval = list()
    for i in range(0, len(data)):
        if up is False and data[i][1] >= threshold:
            up = True
            left = data[i][0]
        elif data[i][1] < threshold and up is True:
            right = data[i][0]
            interval = (left, right)
            list_interval.append(interval)
            up = False
    return list_interval
