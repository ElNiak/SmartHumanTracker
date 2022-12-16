from scapy.layers.l2 import Ether
from scapy.layers.inet import IP
import analyser.analysis_data as analysis_data


def get_tcp_payload_size(pkt_data, protocol):
    """
    :param protocol: choose protocol (UDP or TCP)
    :param pkt_data: one packet from the file
    :return: packets payload size in byte
    :rtype: int
    """
    ether_pkt = Ether(pkt_data)
    ip_pkt = ether_pkt[IP]
    tcp_pkt = ip_pkt[protocol]
    return len(tcp_pkt.payload)


class PayloadSize:

    def __init__(self, data, protocol):
        x_val = [x[0] for x in data]
        y_val = [get_tcp_payload_size(x[1], protocol) for x in data]
        payload_tuple = list(zip(x_val, y_val))
        self.payload_tuple = payload_tuple

    def smooth_result(self, size):
        x_val = [x[0] for x in self.payload_tuple]
        y_val = [x[1] for x in self.payload_tuple]

        return list(zip(analysis_data.smooth(x_val, size), analysis_data.smooth(y_val, size)))
