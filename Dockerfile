FROM python:3.12.3
WORKDIR /app
COPY ./app/requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["uvicorn", "fastapi:app", "--host", "0.0.0.0", "--port", "8080"]
