FROM python:3.11-slim
# FROM python:3.11.9-bookworm
WORKDIR /app
COPY . /app

RUN apt update -y && apt-get install --assume-yes pkg-config awscli gcc g++ libhdf5-dev
# RUN  apt update -y && apt install awscli -y
# RUN apt update -y && apt install pkg-config && apt install awscli -y
# RUN apt update -y && apt-get install --assume-yes pkg-config awscli
# apt install pkg-config &&

RUN pip install -r requirements_old.txt
# RUN pip install -r requirements_test.txt
# RUN pip install -r requirements.txt

# Define the command to run when the container starts
CMD ["python", "app.py"]




