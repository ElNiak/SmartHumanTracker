import matplotlib.pyplot as plt
import analysis_packet
import analysis_data


def throughput_graph(data, leg_x, leg_y):
    """
    :param list[(x,y)] data:  x timestamps that start the interval and y is number of packets for each interval
    :param str leg_x: legend axe x
    :param str leg_y: legend axe y
    :return: plot graph and show the graph (with the cusum graph)
    """

    x_val = [x[0] for x in data]
    y_val = [x[1] for x in data]
    create_graph(x_val, y_val, "Throughput", True)

    # cusum
    create_graph(x_val, analysis_data.cusum(y_val), "Cusum_Throughput", True)


def size_payload_graph(data, leg_x, leg_y, protocol):
    """
    :param protocol: TCP or UDP
    :param list[(x,y)] data:  x timestamps that start the interval and y is number of packets for each interval
    :param str leg_x: legend axe x
    :param str leg_y: legend axe y
    :return: set of coordinates where x time and y tcp payload size (no return) and show graph
    """
    x_val = [x[0] for x in data]
    y_val = [analysis_packet.get_tcp_payload_size(x[1], protocol) for x in data]

    create_graph(x_val, y_val, "Payload size for each packets", False)

    create_graph(analysis_data.smooth(x_val, 15),
                 analysis_data.smooth(y_val, 15), "Smooth value", False)


def create_graph(x_val, y_val, title, is_plot):
    """
    :param x_val: values x
    :param y_val: values y
    :param title: Title that will be show
    :param is_plot: True if plot graph false for scatter (point)
    :return: create and show the graph
    """
    print(x_val)
    # change quality
    plt.figure(figsize=(14, 14))
    plt.grid()
    # Major ticks every 20, minor ticks every 5
    if is_plot:
        plt.plot(x_val, y_val)
    else:
        plt.scatter(x_val, y_val)
    # plt.scatter(x_val, y_val, 'or')
    plt.title(title)
    plt.show()
