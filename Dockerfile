FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine
RUN apk --update add bash nano
ENV STATIC_URL /static
ENV STATIC_PATH /app/static
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt