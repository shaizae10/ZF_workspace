FROM ubuntu
RUN apt-get update && apt-get install \
  -y --no-install-recommends python3 python3-virtualenv

RUN python3 -m virtualenv --python=/usr/bin/python3 /opt/venv

WORKDIR ./.

RUN virtualenv env
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH
RUN which python

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .



CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

