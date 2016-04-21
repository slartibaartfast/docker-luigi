# -*- coding: utf-8 -*-

import docker
import pprint

pp = pprint.PrettyPrinter(indent=4)

#client = docker.from_env(assert_hostname=False)
#print (client.version())

tls_config = docker.tls.TLSConfig \
    (client_cert= \
        ('C:\\Users\\trota\\.docker\\machine\\certs\\cert.pem', \
        'C:\\Users\\trota\\.docker\\machine\\certs\\key.pem'), \
        verify='C:\\Users\\trota\\.docker\\machine\\certs\\ca.pem' \
        )
client = docker.Client(base_url='https://192.168.99.100:2376', tls=tls_config)

containerA = client.create_container ( \
    image='amikamsn/dokcer-luigid:latest', \
    #image='akursar/luigid:latest', \
    hostname="luigi-monitor", \
    ports=[8082, 2376], \
    host_config=client.create_host_config(port_bindings={8082: ('192.168.99.100', 8082)}) \
    )

client.start(containerA.get('Id'))

print("************Containers****************")
print(" ")
pp.pprint(client.containers())
print(" ")