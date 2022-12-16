from scapy.utils import RawPcapReader
import networks.cst as cst


def option_filter(pkt_data, filtering):
    """
    :param filtering:
    :param pkt_data:
    :return:
    """

    if filtering.IPv4:
        if not filtering.ipv4(pkt_data):
            return False
        if filtering.UDP:
            # filter manual
            if not filtering.address_dst(pkt_data):
                return False
            if filtering.protocol(pkt_data, cst.UDP):
                return True
            if not filtering.TCP:
                return False
        if filtering.TCP:
            # filter manual
            if not filtering.address_dst(pkt_data):
                return False
            if not filtering.protocol(pkt_data, cst.TCP):
                return False
            if filtering.SYN:
                if not filtering.syn(pkt_data):
                    return False
    return True


class Packets:

    def __init__(self, file):
        '''
        :param file:
        '''
        self.file_name = file
        self.data = None
        self.size = None

    def read_pcap(self):
        """
        The analysis will first select the relevant packets thanks to the option_filter
        :return:
        """
        count = 0
        tuple_pkt_data_time = []
        for (pkt_data, pkt_metadata,) in RawPcapReader(self.file_name):
            count += 1
            tuple_pkt_data_time.append((pkt_metadata.sec, pkt_data))

        self.data = tuple_pkt_data_time
        self.size = count

    def filter(self, filtering):
        return [x for x in self.data if option_filter(x[1], filtering)]
