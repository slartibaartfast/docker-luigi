# docker-luigi
Scripts for running luigi tasks in containers

Just backing up some scripts for working with docker, luigi and docker-py.  Sorry I can't post the recent version.

This solves several problems:

1) Scale data processing - using docker and luigi we scale horizontally

2) Pipe output from one process to another - luigi makes it easy to chain tasks together

3) Automate processses and chains of processes - luigi lets you script tasks and task wrappers to do this

4) Let processes written in different languages or versions of Python be executed in the same chain, or execute them from the same control mechanism - docker containers makes this possible, as the luigi worker container can be configured to run Python 2.7 for tasks written in that version, and it's output can be consumed by another task written in Python 3.5 running in another container that is configured for Python 3.5, for example.  In the same way, a task written in PowerShell and running on 2012 r2 can share input and output with a task written in Python and running on Linux.

5) Platform independace - this doesn't have a dependancy on AWS or similar.  It can be run from anything that can host Docker.

Many images on https://hub.docker.com will work with this.  I posted some to https://hub.docker.com/r/trota/

See also:

[docker-py](https://github.com/docker/docker-py)

[axiom-data-science/docker-luigi](https://github.com/axiom-data-science/docker-luigi)

[asnir/docker-luigi](https://github.com/asnir/docker-luigi)
