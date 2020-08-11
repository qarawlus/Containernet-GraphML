FROM containernet/containernet

COPY . /containernet-graphml
WORKDIR /containernet-graphml
RUN pip3 install -e .
# RUN python3 examples/ping/cn_ping_test.py

