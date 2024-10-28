FROM python:3.9.9-slim


WORKDIR /test_docker

# ADD . /test_dockerd
COPY ./requirements.txt ./


EXPOSE 8080

RUN pip install -r requirements.txt

CMD [ "python", "check_data.py" ]

