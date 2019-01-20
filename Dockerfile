FROM python:3.7
EXPOSE 5000
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY app.py /app
RUN adduser --disabled-password --gecos '' eidetic && chown eidetic:eidetic /app -R