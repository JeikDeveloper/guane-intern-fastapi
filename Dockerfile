FROM python:3.8

COPY . /usr/src/app

WORKDIR /usr/src/app

RUN pip install -r requirements.python

CMD ["uvicorn", "app.main:app","--host","0.0.0.0","--port","80"]