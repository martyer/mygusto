FROM python:3.8

RUN pip install --upgrade pip
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.5.0/wait /wait
RUN chmod +x /wait

COPY ./app /mygusto/app
ENV PYTHONPATH="${PYTHONPATH}:/mygusto/"
WORKDIR /mygusto/

CMD /mygusto/app/run_gunicorn
