from scipy import stats
from scipy import signal
import numpy as np
import logging
from src.distribution import Distribution
from graph import Graph


def difference_data(data, size, delay):
    """
    :param data:
    :param size: size of the right (or the left part of the array
    :param delay: time in the second that are not take in account in the right part (to avoid irrelevant threshold during the transition
    :return: print p-value, mean, std and return True if the hypothesis nul is accepted
    """
    x2 = np.array(data)
    if len(x2[size:2*size])-size < 0:
        logging.debug('not enough data to continue : %s but we must have at least %s ', x2[size:2*size], size)
        return None, None, None, None
    x2_left = x2[0:size]
    x2_right = x2[size+delay:2*size]
    x2_left_mean = np.mean(x2_left)
    x2_right_mean = np.mean(x2_right)
    x2_left_std = np.std(x2_left)
    x2_right_std = np.std(x2_right)
    # print(x2_left)
    # print(x2_left_mean)
    # print(x2_right)
    # print(x2_right_mean)

    # test T H0 same variance True for same variance
    statistics, pvalue = stats.ttest_ind_from_stats(x2_left_mean, x2_left_std, size, x2_right_mean,
                                                    x2_right_std, size-delay, False)
    size_right = size - delay
    distribution_1 = Distribution(x2_left_mean, x2_left_std, size)
    distribution_2 = Distribution(x2_right_mean, x2_right_std, size_right)
    logging.info('p_value between left and right part : %s', pvalue)
    return statistics, pvalue, distribution_1, distribution_2


def cross_product_between_2_interval(interval_a, interval_b, cus_a, cus_b):

    start_a = interval_a[0]
    end_a = interval_a[1]
    start_b = interval_b[0]
    end_b = interval_b[1]

    interval_cus_a = list()
    interval_cus_b = list()

    for elem in cus_a:
        if start_a <= elem[0] <= end_a:
            interval_cus_a.append(elem)
        else:
            elem_outside_interval = (elem[0], 0)
            interval_cus_a.append(elem_outside_interval)
            
    for elem in cus_b:
        if start_b <= elem[0] <= end_b:
            interval_cus_b.append(elem)
        else:
            elem_outside_interval = (elem[0], 0)
            interval_cus_b.append(elem_outside_interval)

    interval_a = [x[1] for x in interval_cus_a]
    interval_b = [x[1] for x in interval_cus_b]

    c =signal.correlate(interval_a,interval_b,mode='full',method='auto')
    print(c)
    maximum = max(c)
    c_list = c.tolist()
    indice_max = c_list.index(maximum)
    print(maximum)
    lag = indice_max - (max(len(interval_a),len(interval_b))-1)

    lags = signal.correlation_lags(len(interval_cus_a), len(interval_cus_b), mode="full")
    lagi = lags[np.argmax(c)]

    graph_cross = Graph(interval_cus_a, 'time', 'size', "lag representation",
          True, 'interval_a')
    graph_cross.add_data(interval_cus_b, 'interval b')

    lag_interval_1 = [x[1] for x in interval_cus_a]
    lag_interval_0 = [x[0] - lagi for x in interval_cus_a]
    lag_interval = list(zip(lag_interval_0, lag_interval_1))

    graph_cross.add_data(lag_interval, 'shift')

    graph_cross.create_graph()
    graph_cross.show_graph()

    print(indice_max)
    print(lag)


    print(lagi)

    return indice_max

