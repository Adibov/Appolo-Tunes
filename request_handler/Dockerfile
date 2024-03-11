FROM python:3.10

WORKDIR /app
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD . .

CMD ["python", "-m", "flask", "/app/request_handler.py"]