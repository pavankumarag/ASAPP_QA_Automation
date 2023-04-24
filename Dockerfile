FROM python:3.7.4-buster

# cp source code
COPY . /opt/store/qa

# install dependencies
WORKDIR /opt/store/qa
RUN pip install --upgrade pip; pip install -r requirements.txt