from setuptools import setup, find_packages

setup(
    name="mn_gml",
    version="0.1",
    description='Create a mininet topology from GraphML files',
    author='Haydar Qarawlus',
    author_email='haydar.qarawlus@gmail.com',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    long_description="""
        Create a Minitnet topology based on GraphML topologies
        available from the TopologyZoo
        http://www.topology-zoo.org/dataset.html
        """,
    keywords='GraphML',
    license='MIT',
    install_requires=[
        'setuptools',
        'networkx',
        'mininet',
        'geopy',
        'numpy'
    ],
)
