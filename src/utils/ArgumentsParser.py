import argparse
import sys


class ArgumentParser:
    # TODO customize for other tools
    def __init__(self):
        pass

    def parse_arguments(self, allow_unk = False):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--capture",
            help="Capture network traffics TODO",
        )
        parser.add_argument(
            "--clients_ip",
            help="Client networks IP addresses (default :)",
            type=int,
        )
        parser.add_argument(
            "--verbose",
            help="Verbose output (default : False)",
            action="store_true",
        )
        #parser.add_argument("binary", help="Name of the binary to analyze")
        
        args = None
        if not allow_unk:
            args = parser.parse_args()
        else:
            args, unknown = parser.parse_known_args()

        return args
