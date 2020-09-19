FROM python:3.8

RUN pip install --upgrade pip
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./app /mygusto/app
ENV PYTHONPATH="${PYTHONPATH}:/mygusto/"
WORKDIR /mygusto/

CMD /mygusto/app/run_gunicorn
