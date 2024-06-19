FROM python:3.8-alpine

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip --no-cache-dir install -r requirements.txt

COPY . /app

EXPOSE 5000

ENTRYPOINT [ "python3" ]

CMD ["app.py"]