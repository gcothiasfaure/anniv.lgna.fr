FROM python:3.12
WORKDIR /app
COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
RUN mkdir /app/output
CMD ["python", "/app/main.py"]