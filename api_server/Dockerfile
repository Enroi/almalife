FROM python:3.14-slim

WORKDIR /opt/almalife

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./etl ./etl
COPY ./fast_api_main.py .
COPY ./fast_api_empty.py .

EXPOSE 80

CMD ["fastapi", "run", "fast_api_main.py", "--port", "80", "--proxy-headers"]
# CMD ["fastapi", "run", "fast_api_empty.py", "--port", "80", "--proxy-headers"]
