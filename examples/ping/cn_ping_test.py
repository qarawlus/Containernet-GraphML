from mn_gml import MnGML
from mininet.net import CLI
import os

mn_gml = MnGML(os.path.join(os.getcwd(), "examples/ping/Abilene.graphml"), image_name="qarawlus/ping")

net = mn_gml.net
topology = mn_gml.topology
# net, topology = mn_cls(controller=Controller)

net.start()

# CLI(net)

net.stop()
print("Done")
