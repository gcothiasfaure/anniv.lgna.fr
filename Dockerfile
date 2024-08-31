FROM python:3.12
RUN apt-get update && apt-get -y install cron
WORKDIR /app
COPY crontab /etc/cron.d/crontab
COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
RUN touch /app/output.txt
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab
CMD ["cron", "-f"]