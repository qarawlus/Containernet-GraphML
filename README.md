# Containernet-GraphML [![Build Status](https://travis-ci.com/qarawlus/Containernet-GraphML.svg?branch=master)](https://travis-ci.com/qarawlus/Containernet-GraphML)

A GraphML topology generation tool for Containernet (https://github.com/containernet/containernet)

The tool creates a Containernet topology based on GraphML topologies available from the [TopologyZoo](http://www.topology-zoo.org/dataset.html)


## Installation
In the same python environment as Containernet

```bash
git clone https://github.com/qarawlus/Containernet-GraphML.git

pip install . # add -e for development use
```

## Example use

Immport the MnGML class, and pass the absolute path to the GraphML file.

```python
from mn_gml import MnGML


mn_gml = MnGML("abs_path_to_graphml_file", image_name="qarawlus/ping", per_node=2)

net = mn_gml.net
topology = mn_gml.topology
```

This will create a Containernet topology with the following mapping:
- Each node is mapped as a switch, with TCLinks connecting them. The link delay is based on the distance between the nodes
- `per_node` docker containers based on the image provided in `image_name` will be created at the node and linked to the switch. 

Each node can be accessed the the topology object. 

