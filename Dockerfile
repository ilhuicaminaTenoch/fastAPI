FROM python:3.12.3
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
EXPOSE 8080
# CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8080"]
CMD ["fastapi", "run", "main.py", "--port", "80"]
