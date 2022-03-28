FROM ubuntu:latest
RUN apt-get -y update && apt-get update && apt install -y python3-pip
WORKDIR /app
ENV FLASK_APP=api
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
COPY api.py /app  
COPY requirements.txt /app
RUN pip3 install -U pip
RUN pip3 install -r requirements.txt  
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]