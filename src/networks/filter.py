from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP
import networks.cst as cst


class Filter:
    """
    Create a filter with boolean instance
    """

    def __init__(self, IPv4, TCP, UDP, SYN, client=None, server=None):
        self.IPv4 = IPv4
        self.TCP = TCP
        self.UDP = UDP
        self.SYN = SYN
        self.client = client
        self.server = server

    def address_src(self, pkt_data):
        """
        :param pkt_data:
        :return:
        :rtype: bool
        """
        ether_pkt = Ether(pkt_data)
        ip_pkt = ether_pkt[IP]
        return (ip_pkt.src == self.server) or (ip_pkt.src == self.client)

    def address_dst(self, pkt_data):
        """
        :param pkt_data:
        :return:
        :rtype: bool
        """
        ether_pkt = Ether(pkt_data)
        ip_pkt = ether_pkt[IP]
        return (ip_pkt.dst == self.server) and (ip_pkt.src == self.client)

    def port_src(self, pkt_data, client_port, server_port):
        """
        :param pkt_data:
        :param client_port:
        :param server_port:
        :return:
        :rtype: bool
        """
        ether_pkt = Ether(pkt_data)
        ip_pkt = ether_pkt[IP]
        tcp_pkt = ip_pkt[TCP]
        return (tcp_pkt.sport == int(server_port)) or (tcp_pkt.sport == int(client_port))

    def port_dst(self, pkt_data, client_port, server_port):
        """
        :param pkt_data:
        :param client_port:
        :param server_port:
        :return:
        :rtype: bool
        """
        ether_pkt = Ether(pkt_data)
        ip_pkt = ether_pkt[IP]
        tcp_pkt = ip_pkt[TCP]
        return (tcp_pkt.dport == int(server_port)) or (tcp_pkt.dport == int(client_port))

    def syn(self, pkt_data):
        """
        :param pkt_data:
        :return: true if we have a SYN packet
        :rtype: bool
        """
        ether_pkt = Ether(pkt_data)
        ip_pkt = ether_pkt[IP]
        tcp_pkt = ip_pkt[TCP]
        return tcp_pkt.flags == cst.SYN

    # disregard non-IPv4 packets
    def ipv4(self, pkt_data):
        """
        :param pkt_data:
        :return: true if we have IPv4
        :rtype: bool
        """
        ether_pkt = Ether(pkt_data)
        return ether_pkt.type == cst.IPV4

    def protocol(self, pkt_data, protocol_name):
        """
        :param protocol_name:
        :param pkt_data:
        :return: true if we have tcp
        :rtype: bool
        """
        ether_pkt = Ether(pkt_data)
        ip_pkt = ether_pkt[IP]
        return ip_pkt.proto == protocol_name
