from __future__ import print_function

import sys

sys.path.append('..')

from src.sim import Sim
from src.packet import Packet

from networks.network import Network


class DelayHandler(object):
    @staticmethod
    def receive_packet(packet):
        print((Sim.scheduler.current_time(),
               packet.ident,
               packet.created,
               Sim.scheduler.current_time() - packet.created,
               packet.transmission_delay,
               packet.propagation_delay,
               packet.queueing_delay))


def main():
    #==================PART 1==============================
    # parameters
    Sim.scheduler.reset()

    # setup network
    net = Network('networks/two-fast-links.txt')

    # setup routes
    n1 = net.get_node('n1')
    n2 = net.get_node('n2')
    n3 = net.get_node('n3')
    n1.add_forwarding_entry(address=n2.get_address('n1'), link=n1.links[0])
    n2.add_forwarding_entry(address=n3.get_address('n2'), link=n2.links[1])

    # setup app
    d = DelayHandler()
    net.nodes['n2'].add_protocol(protocol="delay", handler=d)

    # send 1000 packets
    calculatedDelay = 0;
    p = Packet(destination_address=n2.get_address('n1'), ident=1, protocol='delay', length=1000)
    for i in range(0, 1):
        Sim.scheduler.add(delay=calculatedDelay, event=p, handler=n1.send_packet)
        calculatedDelay+=.008

    # run the simulation
    Sim.scheduler.run()

    #==================PART 2==============================
    # parameters
    Sim.scheduler.reset()

    # setup network
    net = Network('networks/one-fast-one-slow.txt')

    # setup routes
    n1 = net.get_node('n1')
    n2 = net.get_node('n2')
    n3 = net.get_node('n3')
    n1.add_forwarding_entry(address=n2.get_address('n1'), link=n1.links[0])
    n2.add_forwarding_entry(address=n3.get_address('n2'), link=n2.links[1])

    # setup app
    d = DelayHandler()
    net.nodes['n2'].add_protocol(protocol="delay", handler=d)

    # send 1000 packets
    calculatedDelay = 0;
    p = Packet(destination_address=n2.get_address('n1'), ident=1, protocol='delay', length=1000)
    for i in range(0, 1):
        Sim.scheduler.add(delay=calculatedDelay, event=p, handler=n1.send_packet)
        calculatedDelay+=.008

    # run the simulation
    Sim.scheduler.run()

if __name__ == '__main__':
    main()
