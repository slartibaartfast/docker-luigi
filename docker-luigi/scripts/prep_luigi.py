# -*- coding: utf-8 -*-

# setup a luigid scheduler container and luigi worker
# setup TLS support so they can talk to each other
# let the worker execute a task

import docker                   # to talk to docker
import pprint                   # for printing to the command line
import logging                  # log progress, or lack thereof
from threading import Thread    # to run selenium on its own thread
from selenium import webdriver  # launch a browser to watch luigid scheduler
import time                     # to control a loop

# TODO:
# bind logs directory with /var/log
# remove the worker container after the task is done
# let it tell you what it's doing on a slack channel
# make some more task classes
# set the luigi-worker working dir to scripts directory
# append a timestamp to task names so that tasks are unique
 
# minimal logging...
logging.basicConfig(
    filename="prep_luigi.log", 
    level=logging.DEBUG,
    format='%(asctime)s %(message)s', 
    datefmt='%m/%d/%Y %I:%M:%S %p',
    filemode='w'
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

#print(" ")
#print("*************Images****************")
#print(" ")
#pp.pprint(client.images())
#print(" ")

#print(" ")
#print("*************Volumes****************")
#print(" ")
#pp.pprint(client.volumes())
#print(" ")
#print(" ")

#create a luigid container
containerA = client.create_container (
    image='tedder42/docker-luigid:latest',
    hostname="luigi-monitor",
    name="luigi-monitor",
    ports=[8082, 2376],
    host_config=client.create_host_config(
        port_bindings={8082: ('192.168.99.100', 8082)},
        binds={'/c/Users/trota/Source/luigi/docker-luigi/luigid/state': {
            'bind': '/var/tmp',
            'mode': 'rw',
            }
        }
        )
    )

if containerA:
    # create a worker container
    containerB = client.create_container(
        image='trota/docker-luigi-worker:latest',
        ports=[8082, 2376],
        #command='/usr/local/app1/scripts/run.sh',
        stdin_open=True,
        tty=True,
        name='luigi-worker',
        host_config=client.create_host_config(binds={
            '/c/Users/trota/Source/luigi/docker-luigi/scripts': {
                'bind': '/usr/local/app1/scripts/test',
                'mode': 'rw',
                }
            })
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

print("")
print("1")
print("containerB")
pp.pprint(client.inspect_container(containerB))
print("")



# open a browser for luigid
def open_browser():
    # TODO: make this a class with tasks pending and running as object properties
    browser = webdriver.Chrome()
    browser.get('http://192.168.99.100:8082/static/visualiser/index.html#')

    tasks_pending = browser.find_element_by_css_selector(
        "#PENDING_info span.info-box-number"
        )
    tasks_running = browser.find_element_by_css_selector(
        "#RUNNING_info span.info-box-number"
        )

    num_tasks_pending = tasks_pending.text
    num_tasks_running = tasks_running.text

    num_tasks_pending.strip()
    num_tasks_running.strip()

    print("")
    print("pending: ", tasks_pending.text)
    print("")
    print("running: ", tasks_running.text)
    
	#time_end = time.time() + 60 * 5
    #while time.time() < time_end:
    while (int(num_tasks_pending) > 0) or (int(num_tasks_running) > 0):
        time.sleep(5)
        browser.refresh()

        tasks_pending = browser.find_element_by_css_selector(
            "#PENDING_info span.info-box-number"
            )
        tasks_running = browser.find_element_by_css_selector(
            "#RUNNING_info span.info-box-number"
            )

        num_tasks_pending = tasks_pending.text
        num_tasks_running = tasks_running.text

        num_tasks_pending.strip()
        num_tasks_running.strip()

        if (int(num_tasks_pending) == 0) and (int(num_tasks_running) == 0):
            time.sleep(5)  # give yourself 5 secs to see small tasks
            browser.quit()


browser_thread = Thread(target=open_browser)
browser_thread.start()




# TODO: call this from a luigi task class
#       let the py file name be a variable
# TODO: better to bind to host/scripts directory and pass in a filename
# exec_create to execute a command in a running container
# run.sh calls a specific python script

# run a python script from a shell script
#cmd_dict = client.exec_create(
#    container=containerB.get('Id'),
#    cmd='/usr/local/app1/scripts/run.sh', stdout=True, stderr=True
#    )

# run a python script directly
cmd_dict = client.exec_create(
    container=containerB.get('Id'),
    cmd='python /usr/local/app1/scripts/test/task_print_numbers.py', \
    stdout=True, stderr=True
    )



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
    logging.debug("Command:  %s", client.exec_inspect(v))
    print(" ")

# exec_start to run the command we just set up
# Just for running containers - you can set command in create_container.
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

# feeble thread management - this was the selenium browsers thread
browser_thread.join()

logging.debug("Done - debug")
#logging.info("Done - info")