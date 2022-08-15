FROM python:3.9.6-alpine
WORKDIR /project
COPY ./server.py /project
COPY ./requirements.txt /project
COPY static /project/static
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python" ]
CMD [ "server.py" ]