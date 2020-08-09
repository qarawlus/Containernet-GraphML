from mn_gml.mn_gml import MnGML
from mininet.net import CLI

mn_gml = MnGML("/home/haydar/projects/cn-graphml/Abilene.graphml", image_name="ping")

net = mn_gml.net
topology = mn_gml.topology
# net, topology = mn_cls(controller=Controller)

net.start()

# CLI(net)

net.stop()
print("Done")
