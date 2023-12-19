FROM python:3-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/main
COPY /usr/requirements.txt 
RUN pip install -r requirements.txt
COPY ./main.py /
ENTRYPOINT ["/main.py"]
