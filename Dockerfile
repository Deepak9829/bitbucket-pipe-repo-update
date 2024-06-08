FROM python:3.7-slim 
WORKDIR /app
COPY pipe.py /app
COPY requirements.txt /app
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt 

ENTRYPOINT ["python3", "/app/pipe.py"]
