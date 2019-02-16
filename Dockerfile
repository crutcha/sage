FROM python:3.7
EXPOSE 5000
WORKDIR /app
COPY ./* /app/
RUN pip install -r requirements.txt
RUN adduser --disabled-password --gecos '' eidetic && chown eidetic:eidetic /app -R
