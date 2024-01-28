from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from traceback import print_exc



class SDN(Topo):

    def __init__(
        self
    ):
        Topo.__init__(self)

        A = self.addSwitch("s1")
        B = self.addSwitch("s2")
        C = self.addSwitch("s3")
        D = self.addSwitch("s4")
        E = self.addSwitch("s5")
        F = self.addSwitch("s6")

        self.addLink(A, B)
        self.addLink(A, C)
        self.addLink(A, D)
        self.addLink(A, E)
        self.addLink(A, F)
        self.addLink(B, C)
        self.addLink(B, D)
        self.addLink(B, E)
        self.addLink(B, F)
        self.addLink(C, D)
        self.addLink(C, E)
        self.addLink(C, F)
        self.addLink(D, E)
        self.addLink(D, F)
        self.addLink(E, F)




SDN_ = SDN()
Net = Mininet(topo = SDN_, link = TCLink)
Net.start()

# Do everything here
try:
    pass
except:
    Net.stop()
    print_exc()

Net.stop()