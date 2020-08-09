from mininet.log import info, debug, warn, setLogLevel
setLogLevel('info')
# Check to see if mininet or containernet is installed
try:
    from mininet.net import Containernet
    debug("*** Containernet found\n")
    mn_cls = Containernet
except NameError:
    debug("*** Containernet not found - Fallback to normal Mininet")
    from mininet.net import Mininet
    mn_cls = Mininet
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.net import Controller
import networkx as nx
from geopy.distance import distance as dist
import numpy as np

class MnGML:
    """
    Create a simple Mininet/Containernet topology from GraphML files
    """
    def __init__(self, graphml_file: str, controller=Controller):
        self.graphml_file_path = graphml_file
        self.controller = controller
        self.nx_net = self.read_graphml_file(self.graphml_file_path)

    def read_graphml_file(self, file_path):
        """
        Return a NX object from the GraphML file
        Based on:
        https://github.com/RealVNF/coord-sim/blob/master/src/coordsim/reader/reader.py
        """
        SPEED_OF_LIGHT = 299792458  # meter per second
        PROPAGATION_FACTOR = 0.77  # https://en.wikipedia.org/wiki/Propagation_delay

        if not file_path.endswith(".graphml"):
            raise ValueError("Path must end with graphml extension")
        graphml_nx = nx.read_graphml(file_path)

        for e in graphml_nx.edges(data=True):
            n1 = graphml_nx.nodes(data=True)[e[0]]
            n2 = graphml_nx.nodes(data=True)[e[1]]
            n1_lat, n1_long = n1.get("Latitude", None), n1.get("Longitude", None)
            n2_lat, n2_long = n2.get("Latitude", None), n2.get("Longitude", None)
            if n1_lat is None or n1_long is None or n2_lat is None or n2_long is None:
                raise ValueError("GraphML file does not have node coordinates")
            else:
                # Get the distance in meters
                distance = dist((n1_lat, n1_long), (n2_lat, n2_long)).meters
                # Round the delay to integers (in ms)
                delay = int(np.around((distance / SPEED_OF_LIGHT * 1000) * PROPAGATION_FACTOR))
            e[2]["delay"] = delay
        return graphml_nx


# from mininet.log import info, setLogLevel

mn_net = MnGML("/home/haydar/projects/cn-graphml/Abilene.graphml")

net = mn_cls(controller=Controller)
info('*** Adding controller\n')
net.addController('c0')
info('*** Adding docker containers\n')
d1 = net.addDocker('d1', ip='10.0.0.251', dimage="ubuntu:trusty")
d2 = net.addDocker('d2', ip='10.0.0.252', dimage="ubuntu:trusty")
info('*** Adding switches\n')
s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')
info('*** Creating links\n')
net.addLink(d1, s1)
net.addLink(s1, s2, cls=TCLink, delay='100ms', bw=1)
net.addLink(s2, d2)
info('*** Starting network\n')
net.start()
info('*** Testing connectivity\n')
net.ping([d1, d2])
# info('*** Running CLI\n')
# CLI(net)
info('*** Stopping network')
net.stop()
