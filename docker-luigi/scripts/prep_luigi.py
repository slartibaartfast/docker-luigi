# -*- coding: utf-8 -*-

# setup a luigid scheduler container and luigi worker
# setup TLS support so they can talk to each other
# let the worker execute a task

import docker                   # to talk to docker
import pprint                   # for printing to the command line
import logging                  #log progress, or lack thereof
from selenium import webdriver  # launch a browser to watch luigid

# TODO:
# let selenium launch http://192.168.99.100:8082/static/visualiser/index.html#
 
# minimal logging...
# add filemode="w" to overwrite
logging.basicConfig(
    filename="prep_luigi.log", 
    level=logging.DEBUG,
    format='%(asctime)s %(message)s', 
    datefmt='%m/%d/%Y %I:%M:%S %p'
    )
 
logging.debug("Start - debug")
#logging.info("Start - info")
#logging.error("Start - error")

#client = docker.from_env(assert_hostname=False)
#print (client.version())

# tls might not work, or at least not this way, with Docker Toolbox
# try putting the bridge network ip in the cfg file on the worker - no luck
# try changing RPC security settings?  - no
# run scripts from docker toolbox prompt
# or from within containers

tls_config = docker.tls.TLSConfig \
    (client_cert= \
        ('C:\\Users\\trota\\.docker\\machine\\certs\\cert.pem', \
        'C:\\Users\\trota\\.docker\\machine\\certs\\key.pem'), \
        verify='C:\\Users\\trota\\.docker\\machine\\certs\\ca.pem' \
        )
client = docker.Client(base_url='https://192.168.99.100:2376', tls=tls_config)

info = client.info()
pp = pprint.PrettyPrinter(indent=4)
print(" ")
print("****************Info********************")
print(" ")
pp.pprint(info)
print(" ")

print(" ")
print("*************Images****************")
print(" ")
pp.pprint(client.images())
print(" ")

#print(" ")
#print("*************Volumes****************")
#print(" ")
#pp.pprint(client.volumes())
#print(" ")
#print(" ")

# TODO:
# bind a scripts directory so luigid can run scripts
# bind logs directory with /var/log
# bind state file with /var/tmp/luigi-task-hist.db
# use -H, --hosts[] to connect luigid to the docker Daemon?


#create a luigid container
containerA = client.create_container (
    image='tedder42/docker-luigid:latest',
    hostname="luigi-monitor",
    name="luigi-monitor",
    ports=[8082, 2376],
    host_config=client.create_host_config(port_bindings={8082: ('192.168.99.100', 8082)})
    )

if containerA:
    # create a worker container
    containerB = client.create_container(
        image='trota/docker-luigi-worker:latest',
        ports=[8082, 2376],
        #command='/usr/local/app1/scripts/run.sh',
        stdin_open=True,
        tty=True,
        name='luigi-worker'
	    )
	
print(" ")
print("************Containers****************")
print(" ")
print('containerA', containerA)
print(" ")
print('containerB', containerB)
print(" ")


print("")
print("0")
print("")


#client.start(containerA.get('Id'))
#client.start(containerB.get('Id'))
client.start(containerA)
client.start(containerB)
print("")
print("containerA")
pp.pprint(client.inspect_container(containerA))
print("")

# open a browser for luigid
browser = webdriver.Chrome()
browser.get('http://192.168.99.100:8082/static/visualiser/index.html#')

print("")
print("1")
print("containerB")
pp.pprint(client.inspect_container(containerB))
print("")

# TODO: call this snippet from a luigi task class
# TODO: better to bind to host/scripts directory and pass in a filename
# exec_create to execute a command in a running container
cmd_dict = client.exec_create(container=containerB.get('Id'), cmd='/usr/local/app1/scripts/run.sh', stdout=True, stderr=True)

print("")
print("2")
print("")
print("")
pp.pprint(client.containers())
print("")
print("")
for k, v in cmd_dict.items():
    print(k, v)
    print(" ")
    pp.pprint(client.exec_inspect(v))
    logging.debug(client.exec_inspect(v))
    print(" ")

# exec_start to run the command we just set up
# Just for running containers?  You can set command in create_container.
print("executing argument...")
cmd_result = client.exec_start(v)
print("")
print("")
# see what execution returned
pp.pprint(cmd_result)
cmd_result = cmd_result.decode("utf-8")
print(cmd_result)

print("")
print("done")

logging.debug("Done - debug")
#logging.info("Done - info")