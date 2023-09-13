FROM python:3.7-buster

RUN apt-get update -y && \
    apt-get upgrade -y

COPY requirements.txt /src/
WORKDIR /src
RUN pip3 install -r requirements.txt

RUN python -m spacy download en_core_web_sm


COPY app /src/app
COPY run.py /src
COPY config/ /src/config

ENV FLASK_ENV=development
EXPOSE 5001

# enable waiting for db
ADD compose-wait/wait /wait
RUN chmod +x /wait

CMD python run.py

#COPY wsgi.py /src


# Finally, we run uWSGI with the ini file we
# created earlier
#CMD [ "uwsgi", "--ini", "app.ini" ]

#CMD ["gunicorn", '--bind', '0.0.0.0:5001', './app/wsgi:app']