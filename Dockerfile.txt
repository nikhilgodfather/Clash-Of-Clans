FROM python:3-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/main
COPY requirements.txt /usr/
RUN pip install -U -r requirements.txt
COPY ./main.py /
ENTRYPOINT ["/main.py"]
