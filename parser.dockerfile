FROM python:3.12.3
WORKDIR /app
COPY src/ .
RUN pip3 install -r requirements.txt
ENTRYPOINT [ "python3", "main.py" ]
