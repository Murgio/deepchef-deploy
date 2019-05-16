FROM python:3.7-slim-stretch

RUN apt-get update && apt-get install -y git python3-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN python app.py

EXPOSE 5042

CMD ["python", "app.py"]