# our base image
FROM axiom/docker-luigi:latest

# update pip
RUN pip install --upgrade pip

# update packages
RUN conda update -y luigi


# keep the container portable
# bind volumes after creation
# open ports after creation

# if task scripts were pipable, you could manage them that way
# otherwise, copy the task script to the container after
# it has been instantiated


# tell the port number the container should expose
#EXPOSE 5000

# install Python modules needed by the Python app
#COPY requirements.txt /usr/src/app/
#RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

# copy files required for the app to run
#COPY app.py /usr/src/app/
#COPY templates/index.html /usr/src/app/templates/

# run the application
#CMD ["python", "/usr/src/app/app.py"]