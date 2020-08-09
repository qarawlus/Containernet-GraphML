from mininet.log import debug, setLogLevel
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
from mininet.link import TCLink
from mininet.net import Controller
import networkx as nx
from geopy.distance import distance as dist
import numpy as np


class MnGML:
    """
    Create a simple Mininet/Containernet topology from GraphML files
    """
    def __init__(self, graphml_file: str, controller=Controller, image_name="ubuntu", per_node=1):
        self.__graphml_file_path = graphml_file
        self.__controller = controller
        self.__image_name = image_name
        self.__per_node = per_node
        self.__nx_net = self.read_graphml_file(self.__graphml_file_path)
        self.net, self.topology = self.create_topology()

    def create_topology(self):
        """
        Create a mininet topology
        """
        # storage for added nodes
        net = mn_cls(controller=self.__controller)
        net.addController('c0')
        topology = {}
        # add switches
        for n in self.__nx_net.nodes(data=True):
            topology[n[0]] = {}
            topology[n[0]]['switch'] = net.addSwitch(f's{n[0]}')
            topology[n[0]]['nodes'] = []
            # add nodes and connect to switches
            for i in range(self.__per_node):
                topology[n[0]]['nodes'].append(net.addDocker(f'd{n[0]}{i}', dimage=self.__image_name))
                net.addLink(topology[n[0]]['switch'], topology[n[0]]['nodes'][i])
        # add links between switches
        for e in self.__nx_net.edges(data=True):
            n1 = topology[e[0]]['switch']
            n2 = topology[e[1]]['switch']
            delay = f"{e[2]['delay']}ms"
            net.addLink(n1, n2, cls=TCLink, delay=delay)

        return net, topology

    @staticmethod
    def read_graphml_file(file_path):
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
